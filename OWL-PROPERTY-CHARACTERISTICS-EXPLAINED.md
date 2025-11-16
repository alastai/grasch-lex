# OWL Property Characteristics Explained
## What Gets Lost in OWL → LEX Translation

## Overview

When translating from OWL/RDFS to LEX-2026, one of the most significant **potential** losses is **property characteristics**. These are special semantic behaviors that OWL allows you to declare for properties, which reasoning engines can then use to automatically infer new facts.

LEX-2026 has **no equivalent mechanism** for these characteristics. They must be implemented in application logic or query patterns.

## Important Note: Jaguar Ontology Analysis

**The jaguar conservation ontology analyzed in this project uses ZERO property characteristics.** It is a straightforward structural ontology using only:
- Basic class hierarchies (`rdfs:subClassOf`)
- Simple properties (`owl:ObjectProperty`, `owl:DatatypeProperty`)
- Domain and range constraints (`rdfs:domain`, `rdfs:range`)
- Documentation annotations (`rdfs:comment`)

Therefore, **nothing was actually lost** in the jaguar ontology translation regarding property characteristics. This document explains what *could* be lost if an ontology *did* use these advanced OWL features, which is important for understanding the general limitations of OWL → LEX translation.

## The 8 OWL Property Characteristics

### 1. Transitive Property

**Definition**: If A relates to B, and B relates to C, then A relates to C.

**OWL Declaration:**
```turtle
ont:hasAncestor a owl:ObjectProperty ;
    rdf:type owl:TransitiveProperty .
```

**Example:**
```turtle
:Jaguar1 ont:hasAncestor :Jaguar2 .
:Jaguar2 ont:hasAncestor :Jaguar3 .
# Reasoner automatically infers:
:Jaguar1 ont:hasAncestor :Jaguar3 .
```

**Conservation Use Case:**
```turtle
ont:hasOffspring a owl:ObjectProperty ;
    rdf:type owl:TransitiveProperty .

# Data:
:ElJefe ont:hasOffspring :Cub1 .
:Cub1 ont:hasOffspring :Cub2 .

# Automatic inference:
:ElJefe ont:hasOffspring :Cub2 .  # El Jefe is ancestor of Cub2
```

**LEX-2026 Equivalent:**
```yaml
# No way to declare transitivity
- edgeType:
    typeLabel: HAS_OFFSPRING
    direction: DIRECTED
    firstEndpointNodeType: {typeLabel: Jaguar}
    secondEndpointNodeType: {typeLabel: Jaguar}
```

**Application Must Handle:**
```cypher
// GQL query must explicitly traverse multiple hops
MATCH (ancestor:Jaguar)-[:HAS_OFFSPRING*]->(descendant:Jaguar)
WHERE ancestor.name = 'El Jefe'
RETURN descendant
```

---

### 2. Symmetric Property

**Definition**: If A relates to B, then B relates to A.

**OWL Declaration:**
```turtle
ont:isSiblingOf a owl:ObjectProperty ;
    rdf:type owl:SymmetricProperty .
```

**Example:**
```turtle
:Jaguar1 ont:isSiblingOf :Jaguar2 .
# Reasoner automatically infers:
:Jaguar2 ont:isSiblingOf :Jaguar1 .
```

**Conservation Use Case:**
```turtle
ont:sharesHabitat a owl:ObjectProperty ;
    rdf:type owl:SymmetricProperty .

# Data:
:Population1 ont:sharesHabitat :Population2 .

# Automatic inference:
:Population2 ont:sharesHabitat :Population1 .
```

**LEX-2026 Equivalent:**
```yaml
# Could use UNDIRECTED, but loses semantic meaning
- edgeType:
    typeLabel: SHARES_HABITAT
    direction: UNDIRECTED  # Closest approximation
    firstEndpointNodeType: {typeLabel: JaguarPopulation}
    secondEndpointNodeType: {typeLabel: JaguarPopulation}
```

**Limitation**: UNDIRECTED edges are bidirectional but don't capture the semantic meaning of symmetry. You can't query "which properties are symmetric?"

---

### 3. Functional Property

**Definition**: Each subject can have at most one value for this property.

**OWL Declaration:**
```turtle
ont:hasMother a owl:ObjectProperty ;
    rdf:type owl:FunctionalProperty .
```

**Example:**
```turtle
:Jaguar1 ont:hasMother :MotherJaguar .
:Jaguar1 ont:hasMother :AnotherJaguar .
# Reasoner infers: :MotherJaguar owl:sameAs :AnotherJaguar
# OR reports inconsistency
```

**Conservation Use Case:**
```turtle
ont:hasGender a owl:DatatypeProperty ;
    rdf:type owl:FunctionalProperty .

# Each jaguar has exactly one gender
:ElJefe ont:hasGender "Male" .
# Cannot have: :ElJefe ont:hasGender "Female" (inconsistent)
```

**LEX-2026 Equivalent:**
```yaml
# No cardinality constraints beyond notNull
- nodeType:
    typeLabel: Jaguar
    adding:
      propertyTypes:
        - name: hasGender
          valueType: STRING
          notNull: true  # Can enforce presence, not uniqueness
```

**Application Must Handle:**
- Validation logic to ensure only one value
- No automatic consistency checking
- No inference of identity

---

### 4. Inverse Functional Property

**Definition**: If two subjects have the same value, they must be the same subject.

**OWL Declaration:**
```turtle
ont:hasTrackingID a owl:DatatypeProperty ;
    rdf:type owl:InverseFunctionalProperty .
```

**Example:**
```turtle
:Jaguar1 ont:hasTrackingID "TAG-001" .
:Jaguar2 ont:hasTrackingID "TAG-001" .
# Reasoner infers: :Jaguar1 owl:sameAs :Jaguar2
```

**Conservation Use Case:**
```turtle
ont:hasIdentificationMark a owl:DatatypeProperty ;
    rdf:type owl:InverseFunctionalProperty .

# Unique spot patterns identify individuals
:UnknownJaguar ont:hasIdentificationMark "SPOT-PATTERN-XYZ" .
:ElJefe ont:hasIdentificationMark "SPOT-PATTERN-XYZ" .
# Reasoner infers: :UnknownJaguar owl:sameAs :ElJefe
```

**LEX-2026 Equivalent:**
```yaml
# No mechanism for inverse functional properties
- nodeType:
    typeLabel: Jaguar
    adding:
      propertyTypes:
        - name: hasIdentificationMark
          valueType: STRING
# Could add UNIQUE constraint, but no identity inference
```

**Application Must Handle:**
- Uniqueness constraints in database
- Manual entity resolution
- No automatic identity inference

---

### 5. Inverse Property

**Definition**: Two properties are inverses of each other.

**OWL Declaration:**
```turtle
ont:hasParent a owl:ObjectProperty ;
    owl:inverseOf ont:hasChild .
```

**Example:**
```turtle
:Cub1 ont:hasParent :ElJefe .
# Reasoner automatically infers:
:ElJefe ont:hasChild :Cub1 .
```

**Conservation Use Case:**
```turtle
ont:rescuedBy a owl:ObjectProperty ;
    owl:inverseOf ont:rescued .

# Data:
:OrphanedCub ont:rescuedBy :ConservationOrg .

# Automatic inference:
:ConservationOrg ont:rescued :OrphanedCub .
```

**LEX-2026 Equivalent:**
```yaml
# Must create both edge types manually
- edgeType:
    typeLabel: RESCUED_BY
    direction: DIRECTED
    firstEndpointNodeType: {typeLabel: Jaguar}
    secondEndpointNodeType: {typeLabel: ConservationOrganization}

- edgeType:
    typeLabel: RESCUED
    direction: DIRECTED
    firstEndpointNodeType: {typeLabel: ConservationOrganization}
    secondEndpointNodeType: {typeLabel: Jaguar}
```

**Application Must Handle:**
- Maintain both edges manually
- Keep them synchronized
- No automatic bidirectional inference

---

### 6. Reflexive Property

**Definition**: Every individual has this property with itself.

**OWL Declaration:**
```turtle
ont:isRelatedTo a owl:ObjectProperty ;
    rdf:type owl:ReflexiveProperty .
```

**Example:**
```turtle
# For any jaguar X:
:AnyJaguar ont:isRelatedTo :AnyJaguar .
# Automatically true for all individuals
```

**Conservation Use Case:**
```turtle
ont:sharesGeneticMaterial a owl:ObjectProperty ;
    rdf:type owl:ReflexiveProperty .

# Every jaguar shares genetic material with itself
# Reasoner automatically infers this for all jaguars
```

**LEX-2026 Equivalent:**
```yaml
# No mechanism for reflexive properties
- edgeType:
    typeLabel: SHARES_GENETIC_MATERIAL
    direction: DIRECTED
    firstEndpointNodeType: {typeLabel: Jaguar}
    secondEndpointNodeType: {typeLabel: Jaguar}
```

**Application Must Handle:**
- Explicitly create self-loops if needed
- Query logic must account for reflexivity
- No automatic inference

---

### 7. Irreflexive Property

**Definition**: No individual can have this property with itself.

**OWL Declaration:**
```turtle
ont:isParentOf a owl:ObjectProperty ;
    rdf:type owl:IrreflexiveProperty .
```

**Example:**
```turtle
:Jaguar1 ont:isParentOf :Jaguar1 .
# Reasoner reports: INCONSISTENCY
```

**Conservation Use Case:**
```turtle
ont:hasOffspring a owl:ObjectProperty ;
    rdf:type owl:IrreflexiveProperty .

# A jaguar cannot be its own offspring
:ElJefe ont:hasOffspring :ElJefe .
# Reasoner detects inconsistency
```

**LEX-2026 Equivalent:**
```yaml
# No mechanism for irreflexive constraints
- edgeType:
    typeLabel: HAS_OFFSPRING
    direction: DIRECTED
    firstEndpointNodeType: {typeLabel: Jaguar}
    secondEndpointNodeType: {typeLabel: Jaguar}
```

**Application Must Handle:**
- Validation logic to prevent self-loops
- No automatic consistency checking
- Must implement constraint in application

---

### 8. Asymmetric Property

**Definition**: If A relates to B, then B cannot relate to A.

**OWL Declaration:**
```turtle
ont:isChildOf a owl:ObjectProperty ;
    rdf:type owl:AsymmetricProperty .
```

**Example:**
```turtle
:Cub1 ont:isChildOf :ElJefe .
:ElJefe ont:isChildOf :Cub1 .
# Reasoner reports: INCONSISTENCY
```

**Conservation Use Case:**
```turtle
ont:preys a owl:ObjectProperty ;
    rdf:type owl:AsymmetricProperty .

# If Jaguar preys on Deer, Deer cannot prey on Jaguar
:Jaguar ont:preysOn :Deer .
:Deer ont:preysOn :Jaguar .
# Reasoner detects inconsistency
```

**LEX-2026 Equivalent:**
```yaml
# No mechanism for asymmetric constraints
- edgeType:
    typeLabel: PREYS_ON
    direction: DIRECTED
    firstEndpointNodeType: {typeLabel: Animal}
    secondEndpointNodeType: {typeLabel: Prey}
```

**Application Must Handle:**
- Validation logic to prevent reverse edges
- No automatic consistency checking
- Must implement constraint in application

---

## Summary Table

| Characteristic | OWL Support | LEX-2026 Support | Workaround |
|----------------|-------------|------------------|------------|
| **Transitive** | ✅ Automatic inference | ❌ None | Use path expressions `*` in queries |
| **Symmetric** | ✅ Automatic inference | ⚠️ UNDIRECTED edges | Use UNDIRECTED (loses semantics) |
| **Functional** | ✅ Cardinality + inference | ⚠️ notNull only | Application validation |
| **Inverse Functional** | ✅ Identity inference | ❌ None | UNIQUE constraint + app logic |
| **Inverse** | ✅ Bidirectional inference | ❌ None | Create both edge types manually |
| **Reflexive** | ✅ Automatic inference | ❌ None | Create self-loops explicitly |
| **Irreflexive** | ✅ Consistency checking | ❌ None | Application validation |
| **Asymmetric** | ✅ Consistency checking | ❌ None | Application validation |

## Practical Impact

### With OWL + Reasoner

```sparql
# Find all descendants of El Jefe (transitive)
SELECT ?descendant WHERE {
    :ElJefe ont:hasOffspring+ ?descendant .
}
# Reasoner handles transitivity automatically

# Find all jaguars related to El Jefe (symmetric)
SELECT ?related WHERE {
    { :ElJefe ont:isRelatedTo ?related }
    UNION
    { ?related ont:isRelatedTo :ElJefe }
}
# Reasoner infers symmetric relationships

# Check for inconsistencies
# Reasoner automatically detects:
# - Functional property violations
# - Irreflexive property violations
# - Asymmetric property violations
```

### With LEX-2026 + GQL

```cypher
// Find all descendants (must specify path length)
MATCH (ancestor:Jaguar {name: 'El Jefe'})-[:HAS_OFFSPRING*]->(descendant:Jaguar)
RETURN descendant
// Application must handle transitivity

// Find related jaguars (undirected helps but loses semantics)
MATCH (jaguar:Jaguar {name: 'El Jefe'})-[:IS_RELATED_TO]-(related:Jaguar)
RETURN related
// No automatic symmetric inference

// Check for inconsistencies
// Must implement validation in application:
// - Check for duplicate functional properties
// - Prevent self-loops for irreflexive properties
// - Prevent reverse edges for asymmetric properties
```

## Recommendations

### For Schema Design

1. **Document Lost Semantics**: Add comments explaining which properties should be transitive, symmetric, etc.

```yaml
# This edge type represents a transitive relationship
# Application must handle transitivity in queries
- edgeType:
    typeLabel: HAS_OFFSPRING
    direction: DIRECTED
```

2. **Use Naming Conventions**: Indicate semantic properties in names

```yaml
- edgeType:
    typeLabel: HAS_ANCESTOR_TRANSITIVE  # Indicates transitivity
- edgeType:
    typeLabel: SHARES_HABITAT_SYMMETRIC  # Indicates symmetry
```

3. **Implement Validation**: Add application-level constraints

```python
def validate_functional_property(node, property_name):
    """Ensure functional property has at most one value"""
    values = node.get_property_values(property_name)
    if len(values) > 1:
        raise ValidationError(f"Functional property {property_name} has multiple values")
```

### For Query Patterns

1. **Transitive Queries**: Use path expressions

```cypher
// Instead of relying on transitive inference
MATCH (a)-[:RELATIONSHIP*1..]->(b)
```

2. **Symmetric Queries**: Query both directions

```cypher
// Instead of relying on symmetric inference
MATCH (a)-[:RELATIONSHIP]-(b)  // Undirected match
```

3. **Consistency Checks**: Implement in application

```python
def check_asymmetric_constraint(graph, edge_type):
    """Ensure no reverse edges exist for asymmetric relationships"""
    for edge in graph.edges(edge_type):
        reverse = graph.find_edge(edge.target, edge.source, edge_type)
        if reverse:
            raise ConsistencyError(f"Asymmetric violation: {edge}")
```

## Conclusion

Property characteristics are a powerful feature of OWL that enable:
- **Automatic inference** of new facts
- **Consistency checking** of data
- **Semantic richness** in schema definition

When translating to LEX-2026, these capabilities are lost and must be:
- **Documented** in schema comments
- **Implemented** in application logic
- **Enforced** through validation code
- **Handled** in query patterns

This is one of the key trade-offs when moving from semantic web technologies (OWL/RDFS) to property graph databases (LEX-2026/GQL).
