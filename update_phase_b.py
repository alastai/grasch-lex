import re

with open('src/grasch/examples/test-phase-b-edgetype-ti.yaml', 'r') as f:
    content = f.read()

# Pattern: via: LABEL followed by implies: on edgeType level
# Replace with via: { typeLabel: LABEL, implies: ... }

# This is complex, so let me just show what needs updating
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'via:' in line and not 'typeLabel:' in line:
        print(f"Line {i+1}: {line.strip()}")
