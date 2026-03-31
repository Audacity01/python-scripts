import re
import sys

def test_pattern(pattern, text, flags=0):
    results = {
        'pattern': pattern,
        'matches': [],
        'groups': [],
        'total': 0,
    }

    try:
        compiled = re.compile(pattern, flags)
    except re.error as e:
        results['error'] = str(e)
        return results

    for match in compiled.finditer(text):
        results['matches'].append({
            'text': match.group(),
            'start': match.start(),
            'end': match.end(),
            'groups': match.groups(),
        })
    results['total'] = len(results['matches'])
    return results


def interactive_mode():
    print("Regex Tester (type 'quit' to exit)")
    print("-" * 40)

    while True:
        pattern = input("\nPattern: ").strip()
        if pattern.lower() == 'quit':
            break

        text = input("Text: ").strip()
        case_insensitive = input("Case insensitive? (y/n): ").strip().lower() == 'y'

        flags = re.IGNORECASE if case_insensitive else 0
        results = test_pattern(pattern, text, flags)

        if 'error' in results:
            print(f"Invalid regex: {results['error']}")
            continue

        if results['total'] == 0:
            print("No matches found.")
        else:
            print(f"\n{results['total']} match(es) found:")
            for i, m in enumerate(results['matches']):
                print(f"  [{i+1}] '{m['text']}' at position {m['start']}-{m['end']}")
                if m['groups']:
                    for j, g in enumerate(m['groups']):
                        print(f"       Group {j+1}: '{g}'")


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        pattern = sys.argv[1]
        text = sys.argv[2]
        flags = re.IGNORECASE if '--ignore-case' in sys.argv else 0
        results = test_pattern(pattern, text, flags)

        if 'error' in results:
            print(f"Error: {results['error']}")
        elif results['total'] == 0:
            print("No matches.")
        else:
            for m in results['matches']:
                print(f"Match: '{m['text']}' [{m['start']}:{m['end']}]")
                for j, g in enumerate(m['groups']):
                    print(f"  Group {j+1}: '{g}'")
    else:
        interactive_mode()
