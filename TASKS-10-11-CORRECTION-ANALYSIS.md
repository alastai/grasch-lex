# Tasks 10-11 Correction Analysis

## Problem Statement

Tasks 10 and 11 were marked as complete, but there are two critical issues that need to be addressed:

1. **Vestigial definitions**: `NodeTypesProperty` and `EdgeTypesProperty` exist in the schema but are not referenced anywhere
2. **Missing Level-1 TI support**: The GraphType definition is missing 1-level TI wrappers (`abstract:` and `concrete:`)

## Current State Analysis

### Issue 1: Unused Definitions

**Location in schema**: Lines 2470-2700 (NodeTypesProperty) and 3181-3400 (EdgeTypesProperty)

These definitions are from an earlier design and are **not referenced anywhere** in the schema:
- No `$ref` to `#/$defs/NodeTypesProperty`
- No `$ref` to `#/$defs/EdgeTypesProperty`

**Action required**: Remove these definitions entirely.

### Issue 2: Missing Level-1 TI Wrappers

**Location in schema**: GraphType definition starting at line 743

**Current GraphType structure** (simplified):
```json
"GraphType": {
  "properties": {
    "nodeTypes": { ... },              // ✅ 0-level (bare)
    "edgeTypes": { ... },              // ✅ 0-level (bare)
    "exactlyOf": {                     // ✅ 2-level
      "properties": {
        "concrete": {
          "properties": {
            "nodeTypes": { ... },
            "edgeTypes": { ... }
          }
        },
        "abstract": {
          "properties": {
            "nodeTypes": { ... },
            "edgeTypes": { ... }
          }
        }
      }
    },
    "subtypesOf": {                    // ✅ 2-level
      "properties": {
        "concrete": {
          "properties": {
            "nodeTypes": { ... },
            "edgeTypes": { ... }
          }
        },
        "abstract": {
          "properties": {
            "nodeTypes": { ... },
            "edgeTypes": { ... }
          }
        }
      }
    },
    "propertyGraphDataModel": { ... }
  }
}
```

**Missing 1-level TI wrappers**:
```json
"concrete": {                          // ❌ MISSING 1-level
  "properties": {
    "nodeTypes": { ... },
    "edgeTypes": { ... }
  }
},
"abstract": {                          // ❌ MISSING 1-level
  "properties": {
    "nodeTypes": { ... },
    "edgeTypes": { ... }
  }
}
```

## Required Changes

### Change 1: Remove Vestigial Definitions

**File**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`

**Action**: Delete the following definitions:
1. `NodeTypesProperty` (lines ~2470-2700)
2. `EdgeTypesProperty` (lines ~3181-3400)

### Change 2: Add Level-1 TI Wrappers to GraphType

**File**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`

**Action**: Add two new properties to GraphType (after the bare `nodeTypes` and `edgeTypes` properties):

```json
"concrete": {
  "type": "object",
  "description": "1-level TI: concrete types (shorthand for exactlyOf:concrete:)",
  "properties": {
    "nodeTypes": {
      "oneOf": [
        {
          "type": "array",
          "items": {
            "$ref": "#/$defs/NodeType"
          }
        },
        {
          "type": "object",
          "description": "Import content from file",
          "required": ["import"],
          "properties": {
            "import": {
              "type": "string",
              "description": "Import content from file"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "edgeTypes": {
      "oneOf": [
        {
          "type": "array",
          "items": {
            "$ref": "#/$defs/EdgeType"
          }
        },
        {
          "type": "object",
          "description": "Import content from file",
          "required": ["import"],
          "properties": {
            "import": {
              "type": "string",
              "description": "Import content from file"
            }
          },
          "additionalProperties": false
        }
      ]
    }
  },
  "additionalProperties": false
},
"abstract": {
  "type": "object",
  "description": "1-level TI: abstract types (shorthand for properSubtypesOf:abstract:)",
  "properties": {
    "nodeTypes": {
      "oneOf": [
        {
          "type": "array",
          "items": {
            "$ref": "#/$defs/NodeType"
          }
        },
        {
          "type": "object",
          "description": "Import content from file",
          "required": ["import"],
          "properties": {
            "import": {
              "type": "string",
              "description": "Import content from file"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "edgeTypes": {
      "oneOf": [
        {
          "type": "array",
          "items": {
            "$ref": "#/$defs/EdgeType"
          }
        },
        {
          "type": "object",
          "description": "Import content from file",
          "required": ["import"],
          "properties": {
            "import": {
              "type": "string",
              "description": "Import content from file"
            }
          },
          "additionalProperties": false
        }
      ]
    }
  },
  "additionalProperties": false
}
```

## Validation

After making these changes:

1. **Verify schema is valid JSON**: Run JSON validator
2. **Test 1-level TI syntax**: Create test files using `concrete: { nodeTypes: [...] }` and `abstract: { nodeTypes: [...] }`
3. **Run existing tests**: Ensure no regressions in Phases A-D
4. **Run Phase E tests**: Verify Locations 2-3 tests pass

## Requirements Validation

These changes address:
- **Requirement 1.3**: Support 0-level (bare), 1-level (shorthand), and 2-level (explicit) TI syntax
- **Requirement 2.2**: Location 2 (NodeTypesInterpretation) - TI wrappers wrap nodeTypes array
- **Requirement 2.3**: Location 3 (EdgeTypesInterpretation) - TI wrappers wrap edgeTypes array
- **Requirement 8.3**: Same nesting structure at all locations

## Next Steps

1. Present this analysis to the user for confirmation
2. Upon approval, implement the schema changes
3. Create test files to validate 1-level TI syntax
4. Run comprehensive validation
5. Update task status in tasks.md
