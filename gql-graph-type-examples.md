# GQL Graph Type Internal Structure and DDL Examples

## Overview

Based on examination of the ISO GQL standard BNF grammar, this document demonstrates the internal structure of GQL:graph and GQL:graph type objects, showing both pattern-based (Cypher-style) and verbose SQL-like DDL syntax.

## Hierarchical Structure

### GQL:graph type (Primary Catalog Object - PCO)
Contains Secondary Catalog Objects (SCOs):
- **Node types** - define permitted node structures and properties
- **Edge types** - define permitted edge structures, properties, and connectivity constraints

### GQL:graph (Primary Catalog Object - PCO)  
Contains Secondary Catalog Objects (SCOs):
- **Nodes** - actual node instances conforming to node types
- **Edges** - actual edge instances conforming to edge types

## DDL Syntax Examples

The following examples demonstrate identical semantic content expressed in both syntactic forms:

### Example 1: Pattern-Based Syntax (Cypher-style)

```gql
CREATE GRAPH TYPE PersonCompanyGraph {
  // Node type definitions using pattern syntax with key label sets and multiple labels
  (person :Person => :Person & Audit & DataQuality {
    name STRING,
    lastModified TIMESTAMP,
    principal STRING,
    governanceStatus STRING
  }),
  (company :Company => :Company & Audit & DataQuality {
    name STRING,
    lastModified TIMESTAMP,
    principal STRING,
    governanceStatus STRING
  }),
  
  // Edge type definition using pattern syntax with multiple labels and properties
  (person)-[:WORKS_FOR & Audit & DataQuality {
    since DATE,
    lastModified TIMESTAMP,
    principal STRING,
    governanceStatus STRING
  }]->(company)
}
```

### Example 2: Verbose SQL-like Syntax (GSQL-inherited)

```gql
CREATE GRAPH TYPE PersonCompanyGraph {
  -- Node type definitions using phrase syntax with multiple labels and properties
  NODE TYPE Person :Person & Audit & DataQuality {
    name STRING,
    lastModified TIMESTAMP,
    principal STRING,
    governanceStatus STRING
  },
  NODE TYPE Company :Company & Audit & DataQuality {
    name STRING,
    lastModified TIMESTAMP,
    principal STRING,
    governanceStatus STRING
  },
  
  /* Edge type definition using phrase syntax with FROM...TO */
  DIRECTED EDGE TYPE WorksFor :WORKS_FOR & Audit & DataQuality {
    since DATE,
    lastModified TIMESTAMP,
    principal STRING,
    governanceStatus STRING
  } CONNECTING (person TO company)
}
```

### Example 3: LEX Extension - Direct Key Label Reference

In LEX (as opposed to GQL), single-member key label sets can be used directly as node type references in edge patterns. This leverages the mathematical notation where `{A}` and `A` are synonymous for singleton sets.

```lex
CREATE GRAPH TYPE PersonCompanyGraph {
  // Node type definitions with key label sets (same as GQL)
  (person :Person => :Person & Audit & DataQuality {
    name STRING,
    lastModified TIMESTAMP,
    principal STRING,
    governanceStatus STRING
  }),
  (company :Company => :Company & Audit & DataQuality {
    name STRING,
    lastModified TIMESTAMP,
    principal STRING,
    governanceStatus STRING
  }),
  
  // LEX extension: Direct key label reference in edge pattern
  // Since {Person} has only one member, Person can represent the set
  (Person)-[:WORKS_FOR & Audit & DataQuality {
    since DATE,
    lastModified TIMESTAMP,
    principal STRING,
    governanceStatus STRING
  }]->(Company)
}
```

**LEX Innovation Notes:**
- `Person` directly references the node type with key label set `{Person}`
- `Company` directly references the node type with key label set `{Company}`
- This notation abuse treats singleton sets `{A}` as equivalent to their single member `A`
- This is illegal in standard GQL but legal in LEX for improved readability
- The mathematical convenience allows direct semantic reference without intermediate aliases

## Graph Instance Creation and Data Examples

### Creating the Graph Instance

```gql
-- Create the actual graph instance using the graph type
CREATE GRAPH CompanyEmployeeData OF TYPE PersonCompanyGraph
```

### Inserting Graph Elements

```gql
-- Insert person nodes with realistic property values
INSERT (p1 :Person & Audit & DataQuality {
  name: 'Alice Johnson',
  lastModified: TIMESTAMP '2024-08-22 10:30:00',
  principal: 'system.etl.process',
  governanceStatus: 'VERIFIED'
}),
(p2 :Person & Audit & DataQuality {
  name: 'Bob Smith',
  lastModified: TIMESTAMP '2024-08-22 09:15:00',
  principal: 'hr.data.import',
  governanceStatus: 'PENDING_REVIEW'
}),
(p3 :Person & Audit & DataQuality {
  name: 'Carol Davis',
  lastModified: TIMESTAMP '2024-08-21 16:45:00',
  principal: 'manual.data.entry',
  governanceStatus: 'VERIFIED'
})

-- Insert company nodes with realistic property values
INSERT (c1 :Company & Audit & DataQuality {
  name: 'TechCorp Solutions',
  lastModified: TIMESTAMP '2024-08-20 14:20:00',
  principal: 'corporate.registry.sync',
  governanceStatus: 'VERIFIED'
}),
(c2 :Company & Audit & DataQuality {
  name: 'DataFlow Industries',
  lastModified: TIMESTAMP '2024-08-19 11:30:00',
  principal: 'external.api.feed',
  governanceStatus: 'VERIFIED'
})

-- Insert employment relationships with multiple instances
INSERT (p1)-[:WORKS_FOR & Audit & DataQuality {
  since: DATE '2022-03-15',
  lastModified: TIMESTAMP '2024-08-22 10:35:00',
  principal: 'hr.system.update',
  governanceStatus: 'VERIFIED'
}]->(c1),

(p2)-[:WORKS_FOR & Audit & DataQuality {
  since: DATE '2023-07-01',
  lastModified: TIMESTAMP '2024-08-22 09:20:00',
  principal: 'hr.data.import',
  governanceStatus: 'PENDING_REVIEW'
}]->(c1),

(p3)-[:WORKS_FOR & Audit & DataQuality {
  since: DATE '2021-11-08',
  lastModified: TIMESTAMP '2024-08-21 16:50:00',
  principal: 'manual.data.entry',
  governanceStatus: 'VERIFIED'
}]->(c2)

-- Commit the transaction to persist all changes
COMMIT
```

## Detailed Syntax Breakdown

### Pattern-Based Node Type Syntax
```bnf
node_type_pattern ::= 
  [node_synonym [TYPE] node_type_name] 
  '(' [local_node_type_alias] [node_type_filler] ')'

node_type_filler ::= 
  [node_type_key_label_set] [node_type_implied_content]
  | node_type_implied_content

node_type_implied_content ::=
  node_type_label_set [node_type_property_types]
  | node_type_property_types
  | node_type_label_set node_type_property_types
```

### Pattern-Based Edge Type Syntax
```bnf
edge_type_pattern ::=
  [edge_kind edge_synonym [TYPE] edge_type_name]
  ( edge_type_pattern_directed | edge_type_pattern_undirected )

edge_type_pattern_directed ::=
  source_node_type_reference arc_type_pointing_right destination_node_type_reference
  | destination_node_type_reference arc_type_pointing_left source_node_type_reference

arc_type_pointing_right ::= '-[' edge_type_filler ']->'
arc_type_pointing_left ::= '<-[' edge_type_filler ']-'
arc_type_undirected ::= '~[' edge_type_filler ']~'
```

### Verbose SQL-like Edge Type Syntax
```bnf
edge_type_phrase ::=
  edge_kind edge_synonym [TYPE] edge_type_phrase_filler endpoint_pair_phrase

endpoint_pair_phrase ::= 'CONNECTING' endpoint_pair

endpoint_pair_directed ::=
  endpoint_pair_pointing_right | endpoint_pair_pointing_left

endpoint_pair_pointing_right ::=
  '(' source_node_type_alias connector_pointing_right destination_node_type_alias ')'

connector_pointing_right ::= 'TO' | '->'
```

### Property Types Specification
```bnf
property_types_specification ::= '{' [property_type_list] '}'

property_type_list ::= property_type (',' property_type)*

property_type ::= property_name [typed] property_value_type

property_value_type ::= value_type
```

## Key Observations

1. **Semantic Equivalence**: Both syntactic forms express identical graph type constraints
2. **Pattern Syntax**: More concise, familiar to Cypher users, uses visual ASCII art
3. **Phrase Syntax**: More verbose, SQL-like, explicit FROM...TO directionality
4. **Node Type References**: In patterns, nodes are referenced by position; in phrases, by explicit aliases
5. **Property Syntax**: Identical `{property_name TYPE}` syntax in both forms
6. **Edge Directionality**: Patterns use `->` arrows; phrases use `TO` keywords or arrows

## Implementation Notes

- No DDL exists for creating individual nodes/edges (SCOs within GQL:graph)
- Node types and edge types are the primary SCOs within GQL:graph type
- Both syntactic forms can be mixed within the same graph type definition
- The BNF grammar supports both forms as alternatives in the same production rules