import urllib.request
import sys
import time
from concurrent.futures import ThreadPoolExecutor

def check_url(url):
    if not url.startswith('http'):
        url = 'https://' + url

    start = time.time()
    try:
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            elapsed = round((time.time() - start) * 1000)
            return {
                'url': url,
                'status': resp.status,
                'ok': True,
                'time_ms': elapsed,
                'redirect': resp.url if resp.url != url else None,
            }
    except urllib.error.HTTPError as e:
        elapsed = round((time.time() - start) * 1000)
        return {'url': url, 'status': e.code, 'ok': False, 'time_ms': elapsed}
    except Exception as e:
        return {'url': url, 'status': 0, 'ok': False, 'error': str(e)}


def check_urls_from_file(filepath):
    with open(filepath) as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return urls


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python url_checker.py <url1> [url2] ...")
        print("       python url_checker.py --file urls.txt")
        sys.exit(1)

    if sys.argv[1] == '--file':
        urls = check_urls_from_file(sys.argv[2])
    else:
        urls = sys.argv[1:]

    print(f"Checking {len(urls)} URL(s)...\n")

    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(check_url, urls))

    for r in results:
        status = r.get('status', '???')
        icon = '✓' if r.get('ok') else '✗'
        time_str = f"{r.get('time_ms', '?')}ms" if 'time_ms' in r else ''
        print(f"  {icon} [{status}] {r['url']}  {time_str}")
        if r.get('redirect'):
            print(f"    -> redirected to {r['redirect']}")
        if r.get('error'):
            print(f"    error: {r['error']}")

    ok = sum(1 for r in results if r.get('ok'))
    print(f"\n{ok}/{len(results)} URLs are reachable")
