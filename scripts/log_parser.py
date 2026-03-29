import re
import sys
from collections import Counter
from datetime import datetime

LOG_PATTERN = re.compile(
    r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)'
)

def parse_log_file(filepath):
    entries = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            match = LOG_PATTERN.match(line)
            if match:
                timestamp_str, level, message = match.groups()
                entries.append({
                    'timestamp': timestamp_str,
                    'level': level.upper(),
                    'message': message
                })
    return entries


def summarize(entries):
    level_counts = Counter(e['level'] for e in entries)
    print(f"Total entries: {len(entries)}")
    print(f"Breakdown:")
    for level, count in level_counts.most_common():
        print(f"  {level}: {count}")

    errors = [e for e in entries if e['level'] == 'ERROR']
    if errors:
        print(f"\nLast 5 errors:")
        for e in errors[-5:]:
            print(f"  [{e['timestamp']}] {e['message']}")


def filter_by_level(entries, level):
    return [e for e in entries if e['level'] == level.upper()]


def filter_by_date(entries, date_str):
    return [e for e in entries if e['timestamp'].startswith(date_str)]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python log_parser.py <logfile> [--level ERROR] [--date 2024-01-15]")
        sys.exit(1)

    filepath = sys.argv[1]
    entries = parse_log_file(filepath)

    if '--level' in sys.argv:
        idx = sys.argv.index('--level')
        level = sys.argv[idx + 1]
        entries = filter_by_level(entries, level)

    if '--date' in sys.argv:
        idx = sys.argv.index('--date')
        date = sys.argv[idx + 1]
        entries = filter_by_date(entries, date)

    summarize(entries)
