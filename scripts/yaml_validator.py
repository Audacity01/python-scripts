import sys
import re

def tokenize_yaml(text):
    lines = text.split('\n')
    errors = []
    indent_stack = [0]
    in_multiline = False

    for i, line in enumerate(lines, 1):
        if not line.strip() or line.strip().startswith('#'):
            continue

        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if line.rstrip().endswith('|') or line.rstrip().endswith('>'):
            in_multiline = True
            continue

        if in_multiline:
            if indent <= indent_stack[-1]:
                in_multiline = False
            else:
                continue

        if '\t' in line:
            errors.append((i, "Tab character found — YAML requires spaces"))

        if indent % 2 != 0:
            errors.append((i, f"Odd indentation ({indent} spaces) — use multiples of 2"))

        if stripped.startswith('- '):
            continue

        if ':' in stripped and not stripped.startswith('-'):
            key_part = stripped.split(':')[0]
            if ' ' in key_part and not key_part.startswith('"') and not key_part.startswith("'"):
                errors.append((i, f"Key '{key_part}' contains spaces — consider quoting"))

        if indent > indent_stack[-1] + 2:
            errors.append((i, f"Indentation jump too large ({indent_stack[-1]} -> {indent})"))

        if indent > indent_stack[-1]:
            indent_stack.append(indent)
        elif indent < indent_stack[-1]:
            while indent_stack and indent_stack[-1] > indent:
                indent_stack.pop()

    return errors


def check_duplicates(text):
    lines = text.split('\n')
    keys_at_indent = {}
    errors = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith('-'):
            continue
        indent = len(line) - len(line.lstrip())
        if ':' in stripped:
            key = stripped.split(':')[0].strip()
            level_key = (indent, key)
            if level_key in keys_at_indent:
                errors.append((i, f"Duplicate key '{key}' at same level (first at line {keys_at_indent[level_key]})"))
            else:
                keys_at_indent[level_key] = i

    return errors


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python yaml_validator.py <file.yaml>")
        sys.exit(1)

    with open(sys.argv[1], encoding='utf-8') as f:
        content = f.read()

    errors = tokenize_yaml(content) + check_duplicates(content)
    errors.sort(key=lambda x: x[0])

    if not errors:
        print(f"✓ {sys.argv[1]} looks valid")
    else:
        print(f"Found {len(errors)} issue(s) in {sys.argv[1]}:")
        for line_num, msg in errors:
            print(f"  Line {line_num}: {msg}")
