#!/usr/bin/env python3
import yaml
import sys

# Files that need graphSchema wrapper and structure fixes
graphschema_files = [
    'src/grasch/examples/lex-2026.0.3.2-finbench-schema.yaml',
    'src/grasch/examples/lex-2026.0.3.2-snb-schema.yaml',
    'src/grasch/examples/lex-2026.0.3.2-snb-special-identification-example.yaml',
    'src/grasch/examples/lex-2026.0.3.2-type-definition-syntax-examples.yaml',
    'src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml',
    'src/grasch/examples/lex-2026.0.3.2-mixed-import-example.yaml',
]

for filepath in graphschema_files:
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        # Check if it needs wrapping
        if 'graphSchema' not in data:
            # It needs to be wrapped
            new_data = {'graphSchema': {}}
            
            # Move pathName
            if 'pathName' in data:
                new_data['graphSchema']['pathName'] = data['pathName']
            
            # Move valueTypeSystemName if present
            if 'valueTypeSystemName' in data:
                new_data['graphSchema']['valueTypeSystemName'] = data['valueTypeSystemName']
            
            # Handle graphType
            if 'graphType' in data:
                gt = data['graphType']
                new_gt = {}
                
                # Check if import is at graphType level (should be under defaults)
                if 'import' in gt and 'defaults' not in gt:
                    new_gt['defaults'] = {'import': gt['import']}
                elif 'defaults' in gt:
                    new_gt['defaults'] = gt['defaults']
                else:
                    # Need defaults
                    new_gt['defaults'] = {'import': 'lex-2026.0.3.2-graph-type-defaults.yaml'}
                
                # Copy nodeTypes and edgeTypes
                if 'nodeTypes' in gt:
                    new_gt['nodeTypes'] = gt['nodeTypes']
                if 'edgeTypes' in gt:
                    new_gt['edgeTypes'] = gt['edgeTypes']
                if 'allowSubtypesOf' in gt:
                    new_gt['allowSubtypesOf'] = gt['allowSubtypesOf']
                
                new_data['graphSchema']['graphType'] = new_gt
            
            # Move constraints
            if 'constraints' in data:
                new_data['graphSchema']['constraints'] = data['constraints']
            
            data = new_data
        
        # Write back
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"  ✓ Fixed {filepath}")
    except Exception as e:
        print(f"  ✗ Error: {e}", file=sys.stderr)

print("\nDone!")
