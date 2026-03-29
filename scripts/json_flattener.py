import json
import sys

def flatten(obj, prefix='', sep='.'):
    items = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{prefix}{sep}{k}" if prefix else k
            items.update(flatten(v, new_key, sep))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            new_key = f"{prefix}{sep}{i}" if prefix else str(i)
            items.update(flatten(v, new_key, sep))
    else:
        items[prefix] = obj
    return items


def main():
    if len(sys.argv) < 2:
        print("Usage: python json_flattener.py <file.json>")
        return

    with open(sys.argv[1]) as f:
        data = json.load(f)

    flat = flatten(data)
    print(json.dumps(flat, indent=2))


if __name__ == '__main__':
    main()
