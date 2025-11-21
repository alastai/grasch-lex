#!/usr/bin/env python3
"""Fix implies/propertyTypes indentation in YAML files"""

import re

files_to_fix = [
    'src/grasch/examples/lex-2026.0.3.2-finbench-schema.yaml',
    'src/grasch/examples/lex-2026.0.3.2-snb-schema.yaml',
    'src/grasch/examples/lex-2026.0.3.2-snb-special-identification-example.yaml',
    'src/grasch/examples/lex-2026.0.3.2-type-definition-syntax-examples.yaml',
]

for filepath in files_to_fix:
    print(f"Processing {filepath}...")
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)
        
        # Check if this is an "implies:" line with wrong indentation
        if re.match(r'^(\s+)implies:\s*$', line):
            indent = re.match(r'^(\s+)', line).group(1)
            # Check if next line is propertyTypes at same level
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if re.match(r'^' + indent + r'propertyTypes:', next_line):
                    # Need to indent propertyTypes
                    print(f"  Found implies/propertyTypes at line {i+1}")
                    # Skip the current implies line (already added)
                    i += 1
                    # Add propertyTypes with extra indentation
                    while i < len(lines):
                        curr_line = lines[i]
                        # If line starts with same indent as implies, add 2 spaces
                        if curr_line.startswith(indent) and not curr_line.startswith(indent + '  '):
                            if curr_line.strip() and not curr_line.strip().startswith('#'):
                                # Check if this is a new top-level key (like edgeTypes, constraints, etc)
                                if re.match(r'^' + indent + r'[a-zA-Z]', curr_line) and ':' in curr_line:
                                    # This is a new section, stop indenting
                                    break
                                fixed_lines.append('  ' + curr_line)
                                i += 1
                            else:
                                fixed_lines.append(curr_line)
                                i += 1
                        else:
                            fixed_lines.append(curr_line)
                            i += 1
                            if curr_line.strip() and not curr_line.startswith(indent):
                                # Different indentation level, might be done
                                if i < len(lines) and not lines[i].startswith(indent + '  '):
                                    break
                    continue
        
        i += 1
    
    with open(filepath, 'w') as f:
        f.writelines(fixed_lines)
    print(f"  Fixed {filepath}")

print("Done!")
