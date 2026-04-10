import platform
import os
import sys
import socket
import datetime

def get_disk_usage(path='/'):
    try:
        if sys.platform == 'win32':
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            total_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(path), None, ctypes.pointer(total_bytes), ctypes.pointer(free_bytes))
            total = total_bytes.value
            free = free_bytes.value
        else:
            st = os.statvfs(path)
            total = st.f_blocks * st.f_frsize
            free = st.f_bavail * st.f_frsize
        used = total - free
        return total, used, free
    except:
        return 0, 0, 0

def format_bytes(b):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "unknown"


if __name__ == '__main__':
    print("=== System Information ===")
    print(f"Hostname:  {socket.gethostname()}")
    print(f"OS:        {platform.system()} {platform.release()}")
    print(f"Version:   {platform.version()}")
    print(f"Machine:   {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Python:    {platform.python_version()}")
    print(f"User:      {os.getenv('USER') or os.getenv('USERNAME')}")
    print(f"Local IP:  {get_ip()}")
    print(f"Time:      {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\n=== Disk Usage ===")
    drive = 'C:\\' if sys.platform == 'win32' else '/'
    total, used, free = get_disk_usage(drive)
    if total > 0:
        pct = round(used / total * 100, 1)
        print(f"Drive {drive}")
        print(f"  Total: {format_bytes(total)}")
        print(f"  Used:  {format_bytes(used)} ({pct}%)")
        print(f"  Free:  {format_bytes(free)}")

    print(f"\n=== Environment ===")
    print(f"PATH entries: {len(os.environ.get('PATH', '').split(os.pathsep))}")
    print(f"Env vars: {len(os.environ)}")
