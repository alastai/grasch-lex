from rdflib import Graph, Namespace, RDF, RDFS, OWL
import json

def shacl_to_json_schema(shacl_turtle):
    g = Graph()
    g.parse(data=shacl_turtle, format="turtle")
    
    SH = Namespace("http://www.w3.org/ns/shacl#")
    RDFS_NS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
    
    def get_local_name(uri):
        """Extract the local name from a URI."""
        return uri.split("#")[-1] if "#" in uri else uri.split("/")[-1]

    def parse_constraints(prop_node):
        """Parse SHACL constraints and translate them to JSON Schema."""
        constraints = {}

        # Handling datatype
        datatype = g.value(prop_node, SH.datatype)
        if datatype:
            xsd_map = {
                XSD.string: "string",
                XSD.integer: "integer",
                XSD.decimal: "number",
                XSD.boolean: "boolean",
                XSD.date: "string",
                XSD.dateTime: "string"
            }
            constraints["type"] = xsd_map.get(datatype, "string")

        # Handling minCount and maxCount
        min_count = g.value(prop_node, SH.minCount)
        if min_count:
            constraints["minItems"] = int(min_count)
        max_count = g.value(prop_node, SH.maxCount)
        if max_count:
            constraints["maxItems"] = int(max_count)

        # Handling value ranges
        min_inclusive = g.value(prop_node, SH.minInclusive)
        if min_inclusive:
            constraints["minimum"] = float(min_inclusive)
        max_inclusive = g.value(prop_node, SH.maxInclusive)
        if max_inclusive:
            constraints["maximum"] = float(max_inclusive)

        # Handling string length constraints
        min_length = g.value(prop_node, SH.minLength)
        if min_length:
            constraints["minLength"] = int(min_length)
        max_length = g.value(prop_node, SH.maxLength)
        if max_length:
            constraints["maxLength"] = int(max_length)

        # Handling regex pattern
        pattern = g.value(prop_node, SH.pattern)
        if pattern:
            constraints["pattern"] = str(pattern)

        # Handling sh:in (value range check)
        in_values = g.value(prop_node, SH.in_)
        if in_values:
            constraints["enum"] = [str(value) for value in g.objects(in_values, None)]

        return constraints

    def parse_logical_constraints(prop_node):
        """Handle logical components: sh:not, sh:and, sh:or, sh:xone."""
        logical_constraints = {}

        # sh:not
        not_constraint = g.value(prop_node, SH.not_)
        if not_constraint:
            logical_constraints["not"] = parse_node_shape(not_constraint)

        # sh:and
        and_constraints = list(g.objects(prop_node, SH.and_))
        if and_constraints:
            logical_constraints["allOf"] = [parse_node_shape(c) for c in and_constraints]

        # sh:or
        or_constraints = list(g.objects(prop_node, SH.or_))
        if or_constraints:
            logical_constraints["oneOf"] = [parse_node_shape(c) for c in or_constraints]

        # sh:xone (exclusive or)
        xone_constraints = list(g.objects(prop_node, SH.xone))
        if xone_constraints:
            logical_constraints["oneOf"] = [parse_node_shape(c) for c in xone_constraints]
            logical_constraints["exclusiveMaximum"] = True  # This is a conceptual map for exclusive OR.

        return logical_constraints

    def parse_node_shape(node):
        """Parse a SHACL NodeShape into a JSON Schema object."""
        schema = {
            "type": "object",
            "properties": {}
        }
        label = g.value(node, RDFS_NS.label)
        if label:
            schema["title"] = str(label)

        # Parse each property
        for _, _, prop_node in g.triples((node, SH.property, None)):
            path = g.value(prop_node, SH.path)
            if path:
                prop_name = get_local_name(str(path))
                print(f"Parsing property: {prop_name}")  # Debugging line
                constraints = parse_constraints(prop_node)
                
                # Parse any logical constraints for this property
                logical_constraints = parse_logical_constraints(prop_node)
                if logical_constraints:
                    constraints.update(logical_constraints)
                
                if constraints:  # Only add to properties if constraints are present
                    schema["properties"][prop_name] = constraints

        return schema

    json_schema = {}
    for node in g.subjects(RDF.type, SH.NodeShape):
        node_schema = parse_node_shape(node)
        class_name = g.value(node, RDFS_NS.label)
        if class_name:
            print(f"Parsing node shape: {class_name}")  # Debugging line
            # Only add non-empty schemas
            if node_schema.get("properties"):
                json_schema[str(class_name)] = node_schema

    # Debugging line to show the generated JSON schema before returning
    print("Generated JSON Schema:")
    print(json.dumps(json_schema, indent=4))

    return json.dumps(json_schema, indent=4)

# Example Usage
shacl_data = """
@prefix dash: <http://datashapes.org/dash#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

schema:PersonShape
    a sh:NodeShape ;
    sh:targetClass schema:Person ;
    sh:property [
        sh:path schema:givenName ;
        sh:datatype xsd:string ;
        sh:name "given name" ;
    ] ;
    sh:property [
        sh:path schema:birthDate ;
        sh:lessThan schema:deathDate ;
        sh:maxCount 1 ;
    ] ;
    sh:property [
        sh:path schema:gender ;
        sh:in ( "female" "male" ) ;
    ] ;
    sh:property [
        sh:path schema:address ;
        sh:node schema:AddressShape ;
    ] .

schema:AddressShape
    a sh:NodeShape ;
    sh:closed true ;
    sh:property [
        sh:path schema:streetAddress ;
        sh:datatype xsd:string ;
    ] ;
    sh:property [
        sh:path schema:postalCode ;
        sh:or ( [ sh:datatype xsd:string ] [ sh:datatype xsd:integer ] ) ;
        sh:minInclusive 10000 ;
        sh:maxInclusive 99999 ;
    ] .
"""

print(shacl_to_json_schema(shacl_data))



# Example Usage
shacl_data = """
@prefix g: <http://example.org#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

g:GeoConcept
    a owl:Class ;
    a sh:NodeShape ;
    rdfs:label "Geo concept"@en ;
    sh:property [
        sh:path g:GeoConcept-image ;
        sh:datatype xsd:string ;
    ] ;
    sh:property [
        sh:path g:GeoConcept-webLink ;
        sh:datatype xsd:string ;
        sh:pattern "https?://.*" ;
    ] .

g:Country
    a owl:Class ;
    a sh:NodeShape ;
    rdfs:label "Country"@en ;
    sh:property [
        sh:path g:Country-capital ;
        sh:datatype xsd:string ;
        sh:minLength 2 ;
    ] ;
    sh:property [
        sh:path g:Country-isoCountryCode2 ;
        sh:datatype xsd:string ;
        sh:minLength 2 ;
        sh:maxLength 2 ;
    ] ;
    sh:property [
        sh:path g:Country-population ;
        sh:datatype xsd:integer ;
        sh:minInclusive 0 ;
    ] .
"""

print(shacl_to_json_schema(shacl_data))

