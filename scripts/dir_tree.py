import os
import sys

def print_tree(path, prefix='', max_depth=None, depth=0):
    if max_depth is not None and depth >= max_depth:
        return

    entries = sorted(os.listdir(path))
    dirs = [e for e in entries if os.path.isdir(os.path.join(path, e)) and not e.startswith('.')]
    files = [e for e in entries if os.path.isfile(os.path.join(path, e)) and not e.startswith('.')]

    all_items = dirs + files
    for i, name in enumerate(all_items):
        is_last = i == len(all_items) - 1
        connector = '└── ' if is_last else '├── '
        full_path = os.path.join(path, name)

        if os.path.isdir(full_path):
            print(f"{prefix}{connector}{name}/")
            extension = '    ' if is_last else '│   '
            print_tree(full_path, prefix + extension, max_depth, depth + 1)
        else:
            size = os.path.getsize(full_path)
            size_str = format_size(size)
            print(f"{prefix}{connector}{name} ({size_str})")


def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.0f}{unit}" if unit == 'B' else f"{bytes:.1f}{unit}"
        bytes /= 1024
    return f"{bytes:.1f}TB"


def count_stats(path):
    total_files = 0
    total_dirs = 0
    total_size = 0
    ext_count = {}

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        total_dirs += len(dirs)
        for f in files:
            if f.startswith('.'):
                continue
            total_files += 1
            fp = os.path.join(root, f)
            try:
                total_size += os.path.getsize(fp)
            except OSError:
                pass
            ext = os.path.splitext(f)[1].lower() or '(none)'
            ext_count[ext] = ext_count.get(ext, 0) + 1

    return total_files, total_dirs, total_size, ext_count


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    max_d = int(sys.argv[2]) if len(sys.argv) > 2 else None

    print(f"{os.path.basename(os.path.abspath(target))}/")
    print_tree(target, max_depth=max_d)

    files, dirs, size, exts = count_stats(target)
    print(f"\n{dirs} directories, {files} files, {format_size(size)} total")
    if exts:
        top = sorted(exts.items(), key=lambda x: -x[1])[:5]
        print("Top extensions: " + ", ".join(f"{e}({c})" for e, c in top))
