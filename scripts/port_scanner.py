import socket
import sys
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = {
    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
    53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
    443: 'HTTPS', 993: 'IMAPS', 995: 'POP3S',
    3306: 'MySQL', 5432: 'PostgreSQL', 6379: 'Redis',
    8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 27017: 'MongoDB'
}

def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            service = COMMON_PORTS.get(port, 'unknown')
            return port, service
    except (socket.error, OSError):
        pass
    return None


def scan(host, ports=None):
    if ports is None:
        ports = sorted(COMMON_PORTS.keys())

    print(f"Scanning {host}...")
    open_ports = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_port, host, p): p for p in ports}
        for future in futures:
            result = future.result()
            if result:
                open_ports.append(result)

    open_ports.sort(key=lambda x: x[0])
    return open_ports


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python port_scanner.py <host> [port_range]")
        print("Example: python port_scanner.py localhost")
        print("Example: python port_scanner.py 192.168.1.1 1-1024")
        sys.exit(1)

    host = sys.argv[1]

    ports = None
    if len(sys.argv) > 2:
        start, end = sys.argv[2].split('-')
        ports = range(int(start), int(end) + 1)

    results = scan(host, ports)

    if results:
        print(f"\nOpen ports on {host}:")
        for port, service in results:
            print(f"  {port:>5} - {service}")
    else:
        print("No open ports found.")
