import urllib.request
import json
import sys
import time

def make_request(url, method='GET', data=None, headers=None):
    if headers is None:
        headers = {'User-Agent': 'PythonApiTester/1.0'}

    if data:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    start = time.time()

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            elapsed = time.time() - start
            body = resp.read().decode('utf-8', errors='ignore')
            return {
                'status': resp.status,
                'headers': dict(resp.headers),
                'body': body,
                'time_ms': round(elapsed * 1000),
                'size': len(body),
            }
    except urllib.error.HTTPError as e:
        elapsed = time.time() - start
        return {
            'status': e.code,
            'error': str(e.reason),
            'time_ms': round(elapsed * 1000),
        }
    except Exception as e:
        return {'error': str(e)}


def print_response(result):
    if 'error' in result and 'status' not in result:
        print(f"ERROR: {result['error']}")
        return

    status = result.get('status', '?')
    time_ms = result.get('time_ms', '?')
    print(f"Status: {status}  |  Time: {time_ms}ms")

    if 'size' in result:
        print(f"Size: {result['size']} bytes")

    if 'body' in result:
        try:
            parsed = json.loads(result['body'])
            print(json.dumps(parsed, indent=2)[:2000])
        except json.JSONDecodeError:
            print(result['body'][:500])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python api_tester.py <url> [method] [json_data]")
        print("Examples:")
        print("  python api_tester.py https://httpbin.org/get")
        print('  python api_tester.py https://httpbin.org/post POST \'{"key": "value"}\'')
        sys.exit(1)

    url = sys.argv[1]
    method = sys.argv[2].upper() if len(sys.argv) > 2 else 'GET'
    data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None

    print(f"{method} {url}")
    print("-" * 50)
    result = make_request(url, method, data)
    print_response(result)
