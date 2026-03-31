import sys
import re
from collections import Counter

def analyze_text(text):
    lines = text.split('\n')
    words = re.findall(r'\b\w+\b', text.lower())
    chars = len(text)
    chars_no_spaces = len(text.replace(' ', '').replace('\n', ''))
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    word_freq = Counter(words)
    avg_word_len = sum(len(w) for w in words) / len(words) if words else 0

    return {
        'lines': len(lines),
        'words': len(words),
        'characters': chars,
        'characters_no_spaces': chars_no_spaces,
        'sentences': len(sentences),
        'avg_word_length': round(avg_word_len, 1),
        'unique_words': len(set(words)),
        'most_common': word_freq.most_common(10),
    }


def reading_time(word_count, wpm=200):
    minutes = word_count / wpm
    if minutes < 1:
        return "less than a minute"
    elif minutes < 2:
        return "about 1 minute"
    else:
        return f"about {int(minutes)} minutes"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python text_stats.py <file>")
        sys.exit(1)

    with open(sys.argv[1], encoding='utf-8', errors='ignore') as f:
        text = f.read()

    stats = analyze_text(text)

    print(f"Lines:          {stats['lines']}")
    print(f"Words:          {stats['words']}")
    print(f"Characters:     {stats['characters']}")
    print(f"  (no spaces):  {stats['characters_no_spaces']}")
    print(f"Sentences:      {stats['sentences']}")
    print(f"Unique words:   {stats['unique_words']}")
    print(f"Avg word len:   {stats['avg_word_length']}")
    print(f"Reading time:   {reading_time(stats['words'])}")
    print(f"\nMost common words:")
    for word, count in stats['most_common']:
        print(f"  {word:15s} {count}")
