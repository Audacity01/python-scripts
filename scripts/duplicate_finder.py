import os
import hashlib
import sys
from collections import defaultdict

def hash_file(path, chunk_size=8192):
    h = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                h.update(chunk)
    except (PermissionError, OSError):
        return None
    return h.hexdigest()

def find_duplicates(directory):
    hashes = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            file_hash = hash_file(path)
            if file_hash:
                hashes[file_hash].append(path)

    dupes = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return dupes

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    duplicates = find_duplicates(target)

    if not duplicates:
        print("No duplicates found.")
    else:
        for h, paths in duplicates.items():
            print(f"\nDuplicate group ({h[:8]}):")
            for p in paths:
                print(f"  {p}")
