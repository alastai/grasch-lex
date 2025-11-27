# JSON Schema Import Pattern Analysis

## Overview

This analysis checks for consistency in import patterns throughout the schema.

**Total issues found:** 13

## High Severity Issues

### graphSchema

- **Path:** `root.oneOf[1].properties.graphSchema`
- **Issue:** Missing oneOf for importable property

### directories

- **Path:** `root.$defs.Directory.properties.directories`
- **Issue:** Missing oneOf for importable property

### graphType

- **Path:** `root.$defs.GraphSchemaContent.properties.graphType`
- **Issue:** Missing oneOf for importable property

### graphType

- **Path:** `root.$defs.GraphContent.properties.graphSchema.oneOf[0].properties.graphType`
- **Issue:** Missing oneOf for importable property

### graphType

- **Path:** `root.$defs.GraphContent.properties.graphSchema.oneOf[2].properties.graphType`
- **Issue:** Missing oneOf for importable property

### nodeTypes

- **Path:** `root.$defs.GraphType.properties.nodeTypes`
- **Issue:** Missing oneOf for importable property

### nodeTypes

- **Path:** `root.$defs.GraphType.properties.subtypesOf.properties.abstract.properties.nodeTypes`
- **Issue:** Missing oneOf for importable property

### edgeTypes

- **Path:** `root.$defs.GraphType.properties.subtypesOf.properties.abstract.properties.edgeTypes`
- **Issue:** Missing oneOf for importable property

### nodeTypes

- **Path:** `root.$defs.GraphType.properties.subtypesOf.properties.nodeTypes`
- **Issue:** Missing oneOf for importable property

### edgeTypes

- **Path:** `root.$defs.GraphType.properties.subtypesOf.properties.edgeTypes`
- **Issue:** Missing oneOf for importable property

### edgeTypes

- **Path:** `root.$defs.GraphType.properties.edgeTypes`
- **Issue:** Missing oneOf for importable property

### nodeTypes

- **Path:** `root.$defs.NodeTypeItem.oneOf[7].properties.sealed.properties.nodeTypes`
- **Issue:** Missing oneOf for importable property

### edgeTypes

- **Path:** `root.$defs.EdgeTypeItem.oneOf[7].properties.sealed.properties.edgeTypes`
- **Issue:** Missing oneOf for importable property

## Recommendations

1. Every importable property should have a oneOf pattern
2. The oneOf should include both the actual content and an import option
3. Import options should be consistent across all definitions
