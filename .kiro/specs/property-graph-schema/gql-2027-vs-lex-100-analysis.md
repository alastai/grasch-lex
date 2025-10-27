# Analysis: GQL:2027 CD1SP1 vs LEX-100 Constraint Organization

## Analysis: GQL:2027 CD1SP1 vs LEX-100 Constraint Organization

### **Key Organizational Difference: Constraint Location**

**GQL:2027 CD1SP1 Organization:**
- Constraints are **inside** the graph type descriptor
- Graph type descriptor includes: "The constraint set dictionary that maps the name of each constraint in the constraint set of this graph type descriptor to that constraint"
- Constraints are part of the graph type definition

**LEX-100 Organization:**
- Constraints are **outside** the graph type, directly in the graph schema
- LEX graph schema structure: `identifier + principal + value_type_system + graph_type + constraints`
- Graph type is "structural" (without constraints), constraints are separate

### **LEX-100's Rationale for Reorganization:**

LEX-100 explicitly states:
> "This seems more logical because a constraint applies to a graph and not to a graph type. It depends on the actual values in a specific graph."

> "The information content of a LEX:2026.0 graph schema is therefore intended to be a strict superset of the information content of a GQL:2027 graph type, even if organized differently."

### **Constraint Descriptor Content Comparison:**

**GQL:2027 CD1SP1 Constraint Descriptors:**
- Constraint name
- Constraint subject set (registered subjects)
- Constraint scope (constrained elements)
- Key value component specifications (for KEY/UNIQUE)
- Detailed enforcement semantics with exception handling

**LEX-100 Constraint Descriptors (Current Draft):**
```
– constraint
    – name <string>
    – rule
        – subject KEY | UNIQUE     
        – constraint pattern
        – unique key component property names <set>
```

### **Analysis: Gaps in LEX-100 Design**

**1. Incomplete Constraint Descriptor Definition:**
LEX-100 acknowledges: "COMMENT ONLY The GQL specification is unclear to me with respect to descriptors in this area."

The LEX-100 constraint descriptor is significantly simplified compared to GQL:2027 CD1SP1:
- Missing: constraint subject set management
- Missing: constraint scope definition  
- Missing: detailed enforcement semantics
- Missing: constraint graph pattern details
- Simplified: "constraint pattern" vs detailed graph pattern syntax

**2. Missing GQL:2027 CD1SP1 Features:**
- No mention of constraint enforcement (validation, checking, enforcement)
- No exception handling (class 23, class G2)
- No deferred enforcement capabilities
- No constraint parent graph specification
- No CREATE/DROP CONSTRAINT statement syntax

**3. Conceptual Inconsistency:**
LEX-100 argues constraints "apply to a graph and not to a graph type" but GQL:2027 CD1SP1 clearly shows constraints can apply to graph types and be inherited by conforming graphs.

### **Conclusion: LEX-100 is Currently Incomplete**

LEX-100 appears to be a **partial reorganization** rather than a complete alternative. It:

1. **Reorganizes** constraint location (outside graph type vs inside)
2. **Simplifies** constraint descriptors (possibly too much)
3. **Omits** significant GQL:2027 CD1SP1 constraint framework features
4. **Acknowledges** its own incompleteness regarding constraint descriptors

**Recommendation:** LEX:2026.0 should:
1. Implement the **complete** GQL:2027 CD1SP1 constraint framework first
2. Then provide the LEX organizational alternative (constraints outside graph type)
3. Ensure both organizations have identical information content
4. Add LEX extensions (cardinality, participation constraints) in future versions

The LEX-100 reorganization has conceptual merit, but the current specification is incomplete compared to the rich GQL:2027 CD1SP1 constraint framework.