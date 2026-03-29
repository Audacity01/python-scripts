import csv
import json
import sys

def convert(csv_path, output_path=None):
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    result = json.dumps(rows, indent=2)

    if output_path:
        with open(output_path, 'w') as f:
            f.write(result)
        print(f"Written to {output_path}")
    else:
        print(result)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python csv_to_json.py input.csv [output.json]")
        sys.exit(1)

    out = sys.argv[2] if len(sys.argv) > 2 else None
    convert(sys.argv[1], out)
