import urllib.request
import re
import sys
from html.parser import HTMLParser

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_text = ''
        self.in_a = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.in_a = True
            for attr, value in attrs:
                if attr == 'href':
                    self.links.append({'href': value, 'text': ''})

    def handle_endtag(self, tag):
        if tag == 'a' and self.in_a:
            self.in_a = False
            if self.links:
                self.links[-1]['text'] = self.current_text.strip()
            self.current_text = ''

    def handle_data(self, data):
        if self.in_a:
            self.current_text += data


def scrape_links(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')

    parser = LinkExtractor()
    parser.feed(html)
    return parser.links


def extract_title(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')

    match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else 'No title found'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python web_scraper.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"Title: {extract_title(url)}\n")
    print("Links found:")
    for link in scrape_links(url):
        text = link['text'] or '(no text)'
        print(f"  [{text}] -> {link['href']}")
