# Graph RAG Analysis - Niklas Emegård's Implementation

## Executive Summary

This is a **Semantic Graph RAG** system that demonstrates true ontology-driven knowledge graph integration with LLMs. The project showcases two key capabilities:

1. **Query Interface**: Natural language → SPARQL → GraphDB → Natural language responses
2. **Knowledge Extraction**: Unstructured text → Ontology-guided extraction → RDF/Turtle → GraphDB

**Key Innovation**: Uses formal RDFS/OWL ontologies (not just LPG) to provide semantic structure that LLMs can understand and leverage for intelligent entity disambiguation and relationship inference.

## Architecture Overview

### Technology Stack
- **Agent Framework**: Microsoft Agent Framework (Preview) with DevUI
- **LLM**: OpenAI GPT-4/GPT-5 with function calling
- **Knowledge Graph**: Ontotext GraphDB (RDF triple store)
- **Query Language**: SPARQL
- **Ontology Format**: RDF/Turtle with RDFS/OWL semantics
- **Interface**: Built-in DevUI (auto-opening browser at localhost:8000)

### Core Components

```
User Query (DevUI)
    ↓
JaguarQueryAgent (Microsoft Agent Framework)
    ↓
GPT-4 (SPARQL Generation)
    ↓
query_jaguar_database Tool
    ↓
GraphDB (SPARQL Execution)
    ↓
GPT-4 (Result Interpretation)
    ↓
Natural Language Response (DevUI)
```

## Domain Model: Jaguar Conservation

### Ontology Structure

**Class Hierarchy:**
```
ont:Animal
  ├─ ont:Mammal
  │   └─ ont:BigCat
  │       └─ ont:Jaguar (Panthera onca)
  └─ ont:Prey
      ├─ ont:Livestock
      ├─ ont:Herbivore
      ├─ ont:Mesopredator
      ├─ ont:Fish
      └─ ont:Reptile

ont:Habitat
  ├─ ont:Forest
  │   └─ ont:Rainforest
  ├─ ont:Wetland
  ├─ ont:Grassland
  ├─ ont:Shrubland
  └─ ont:WaterBody

ont:Location
  ├─ ont:Country
  ├─ ont:State
  ├─ ont:Region
  ├─ ont:MountainRange
  └─ ont:HabitatArea

ont:Threat
  ├─ ont:AnthropogenicThreat
  │   ├─ ont:HabitatLoss
  │   ├─ ont:HabitatFragmentation
  │   ├─ ont:Poaching
  │   ├─ ont:IllegalWildlifeTrade
  │   ├─ ont:HumanWildlifeConflict
  │   └─ ont:BorderBarrier
  └─ ont:EnvironmentalThreat
      ├─ ont:ClimateChange
      └─ ont:Wildfire

ont:ConservationOrganization
  ├─ ont:GovernmentAgency
  ├─ ont:NGO
  └─ ont:AcademicInstitution

ont:ConservationEffort
  ├─ ont:RecoveryPlan
  ├─ ont:WildlifeCorridor
  ├─ ont:RewildingProgram
  ├─ ont:CommunityEngagement
  └─ ont:InternationalCooperation
```

**Key Properties:**
- **Individual Tracking**: hasGender, hasIdentificationMark, hasMonitoringStartDate, hasLastSightingDate
- **Life Events**: wasKilled, causeOfDeath, isOrphaned, isRehabilitated, isReleased
- **Relationships**: rescuedBy, reintroducedBy, monitoredByOrg, facesThreat
- **Locations**: occursIn, originatesFrom, locatedIn
- **Observations**: hasObservation, observedDate, observedBy

## Ontology-Driven Knowledge Extraction

### The "Jaguar Problem"

**Challenge**: Extract jaguar conservation data from a corpus containing:
- 🐆 Wildlife jaguars (Panthera onca)
- 🚗 Jaguar cars (E-Type, XK-E)
- 🎸 Fender Jaguar guitars

**Solution**: The system uses the formal ontology to provide semantic context to GPT-5:

1. **Ontology Loading**: Loads `jaguar_ontology.ttl` with formal class definitions
2. **Corpus Processing**: Reads mixed-content text from `jaguar_corpus.txt`
3. **Semantic Analysis**: GPT-5 uses ontology structure to understand domain
4. **Entity Disambiguation**: Automatically filters out cars and guitars
5. **RDF Generation**: Creates valid Turtle syntax aligned with ontology
6. **GraphDB Import**: Imports generated RDF via "Text snippet" interface

### Why This Requires Formal Ontologies

**Cannot be done with LPG databases:**

❌ **No Formal Semantics**
- LPG labels are just strings
- No machine-readable domain definitions
- LLM has no semantic guidance

❌ **No Class Hierarchies**
- No RDFS/OWL inheritance
- No taxonomic structure
- No reasoning capabilities

❌ **No Property Constraints**
- No domain/range definitions
- No cardinality rules
- No validation mechanisms

✅ **RDF/Ontologies Provide:**
- Formal class definitions (`ont:Jaguar rdfs:subClassOf ont:BigCat`)
- Property semantics (`ont:hasGender rdfs:domain ont:Jaguar`)
- Hierarchical structure for LLM understanding
- Validation and reasoning capabilities
- W3C standards for interoperability

## Graph RAG Query Patterns

### Example SPARQL Queries

**Count Total Jaguars:**
```sparql
@prefix ont: <http://example.org/ontology#>.
@prefix : <http://example.org/resource#>.
SELECT (COUNT(?jaguar) as ?count) WHERE { 
  ?jaguar a ont:Jaguar . 
}
```

**Find by Gender:**
```sparql
@prefix ont: <http://example.org/ontology#>.
@prefix : <http://example.org/resource#>.
SELECT ?jaguar ?label ?gender WHERE { 
  ?jaguar a ont:Jaguar . 
  OPTIONAL { ?jaguar rdfs:label ?label . } 
  OPTIONAL { ?jaguar ont:hasGender ?gender . } 
}
```

**Find Killed Jaguars:**
```sparql
@prefix ont: <http://example.org/ontology#>.
@prefix : <http://example.org/resource#>.
SELECT ?jaguar ?label ?causeOfDeath WHERE { 
  ?jaguar a ont:Jaguar . 
  ?jaguar ont:wasKilled true . 
  OPTIONAL { ?jaguar rdfs:label ?label . } 
  OPTIONAL { ?jaguar ont:causeOfDeath ?causeOfDeath . } 
}
```

**Find Rescue Operations:**
```sparql
@prefix ont: <http://example.org/ontology#>.
@prefix : <http://example.org/resource#>.
SELECT ?jaguar ?label ?org ?rescueDate WHERE {
  ?jaguar a ont:Jaguar .
  ?jaguar ont:rescuedBy ?org .
  OPTIONAL { ?jaguar rdfs:label ?label . }
  OPTIONAL { ?jaguar ont:hasRescueDate ?rescueDate . }
}
```

## Agent Design

### System Prompt Strategy

The agent uses a carefully crafted system prompt that:

1. **Establishes Graph RAG Context**: "You have access to a comprehensive jaguar database stored in GraphDB"
2. **Provides Ontology Reference**: Full ontology embedded in tool description
3. **Guides SPARQL Generation**: "Make simple queries first, add complexity if needed"
4. **Enforces Data Attribution**: "Always mention information comes from jaguar database"
5. **Formats Responses**: Use markdown, code blocks, bullet points

### Tool Integration

**Function**: `query_jaguar_database(sparql_query: str) -> str`

**Tool Description Includes:**
- Complete ontology (classes and properties)
- Example SPARQL queries
- Best practices for query construction
- Prefix requirements

**Return Format**: JSON string with SPARQL results

### Response Flow

1. User asks natural language question
2. Agent analyzes question and decides to use GraphDB tool
3. GPT-4 generates SPARQL query based on ontology
4. Tool executes query against GraphDB
5. Raw JSON results returned to agent
6. GPT-4 interprets results and generates natural language response
7. Response formatted with markdown (bold, bullets, code blocks)

## Relevance to Grasch/LEX-2026

### Alignment with Grasch Goals

**1. Schema-Driven Development**
- Both use formal schemas (LEX-2026 vs. RDFS/OWL)
- Both emphasize type systems and validation
- Both support hierarchical type structures

**2. Knowledge Graph Integration**
- Grasch targets Kuzu (embedded graph DB)
- graph_RAG uses GraphDB (RDF triple store)
- Both need schema representation and query generation

**3. LLM Integration Opportunities**
- graph_RAG demonstrates LLM-driven query generation
- Grasch could benefit from similar natural language → GQL translation
- LEX-2026 schemas could guide LLM understanding like ontologies do

### Potential Integration Points

**1. LEX-2026 as Ontology Replacement**
- LEX-2026 provides formal type definitions
- Content types, node types, edge types with constraints
- Could serve similar role to RDFS/OWL for LLM guidance

**2. GQL Query Generation**
- Adapt SPARQL generation approach to GQL
- Use LEX-2026 schema to guide query construction
- Validate generated queries against schema

**3. Schema-Driven Knowledge Extraction**
- Use LEX-2026 schemas to guide entity extraction
- Generate graph data conforming to schema
- Import into Kuzu with validation

**4. Natural Language Interface**
- Build similar agent framework for Grasch
- Natural language → GQL queries
- Schema-aware response generation

### Key Differences

| Aspect | graph_RAG | Grasch/LEX-2026 |
|--------|-----------|-----------------|
| **Graph Model** | RDF (triples) | Property Graph |
| **Schema Language** | RDFS/OWL | LEX-2026 (GQL-based) |
| **Query Language** | SPARQL | GQL |
| **Database** | GraphDB | Kuzu |
| **Standards** | W3C (RDF, SPARQL) | ISO GQL, LDBC LEX |
| **Type System** | Class hierarchies | Content types + Element types |
| **Reasoning** | Built-in (RDFS/OWL) | Application-level |

### Lessons Learned

**1. Ontology/Schema in Tool Description**
- Embedding full schema in tool description works well
- LLM can reference schema when generating queries
- Reduces hallucination of non-existent properties

**2. Example-Driven Guidance**
- Providing example queries helps LLM understand patterns
- Simple examples first, complex examples for edge cases
- Prefix handling is critical

**3. Response Formatting**
- Showing generated query builds trust
- Markdown formatting improves readability
- Data attribution is important for credibility

**4. Error Handling**
- Return errors as JSON with original query
- LLM can interpret errors and retry
- Connection errors need clear messaging

**5. Semantic Disambiguation**
- Formal semantics enable intelligent entity extraction
- LLMs need structured guidance, not just labels
- Ontologies/schemas are essential for quality extraction

## Implementation Insights

### Microsoft Agent Framework

**Pros:**
- Built-in DevUI for rapid prototyping
- Automatic state management
- Thread-based conversation context
- Function calling integration
- Zero frontend code required

**Cons:**
- Preview/beta status
- Limited customization of DevUI
- Tied to Microsoft ecosystem
- Documentation still evolving

### GraphDB Integration

**Approach:**
- Direct HTTP requests to SPARQL endpoint
- URL-encoded query parameters
- JSON response format
- 30-second timeout

**Alternative Approaches:**
- SPARQLWrapper library (more Pythonic)
- RDFLib for local RDF processing
- GraphDB Python client (if available)

### SPARQL Generation Quality

**Observations:**
- GPT-4 generates valid SPARQL most of the time
- Prefix handling is the most common error
- Complex queries sometimes need refinement
- Example queries in prompt significantly help

## Potential Enhancements

### For graph_RAG

1. **Query Caching**: Cache frequent SPARQL patterns
2. **Query Optimization**: Analyze and optimize generated queries
3. **Multi-Graph Support**: Query multiple repositories
4. **Streaming Responses**: Real-time result streaming
5. **Visualization**: Graph visualization of results

### For Grasch Integration

1. **LEX-2026 Tool Description**: Embed schema in tool description
2. **GQL Query Generation**: Adapt SPARQL generation to GQL
3. **Schema Validation**: Validate queries against LEX-2026 schema
4. **Natural Language Interface**: Build similar agent for Grasch
5. **Knowledge Extraction**: Schema-guided data extraction

## Conclusion

This graph_RAG implementation demonstrates a mature approach to semantic Graph RAG using formal ontologies. The key insights are:

1. **Formal semantics matter**: RDFS/OWL provides structure LLMs can leverage
2. **Schema-in-prompt works**: Embedding schema in tool description is effective
3. **Examples are critical**: Query examples significantly improve generation quality
4. **Disambiguation requires structure**: Entity extraction needs formal semantics
5. **Agent frameworks simplify**: Built-in state management reduces complexity

For Grasch, the most valuable takeaway is the **schema-driven approach**: using LEX-2026 schemas to guide LLM understanding and query generation, similar to how this system uses RDFS/OWL ontologies.

The main adaptation challenge is translating from RDF/SPARQL to Property Graph/GQL, but the core pattern of "schema → LLM → query → results → natural language" remains the same.
