import struct
import sys
import os

def get_image_info(filepath):
    with open(filepath, 'rb') as f:
        header = f.read(30)

    info = {
        'path': filepath,
        'size_bytes': os.path.getsize(filepath),
        'format': 'unknown',
        'width': 0,
        'height': 0,
    }

    if header[:8] == b'\x89PNG\r\n\x1a\n':
        info['format'] = 'PNG'
        w, h = struct.unpack('>II', header[16:24])
        info['width'] = w
        info['height'] = h
    elif header[:2] == b'\xff\xd8':
        info['format'] = 'JPEG'
        f_handle = open(filepath, 'rb')
        f_handle.read(2)
        while True:
            marker, size = struct.unpack('>HH', f_handle.read(4))
            if marker == 0xFFC0 or marker == 0xFFC2:
                f_handle.read(1)
                h, w = struct.unpack('>HH', f_handle.read(4))
                info['width'] = w
                info['height'] = h
                break
            else:
                f_handle.read(size - 2)
        f_handle.close()
    elif header[:4] == b'GIF8':
        info['format'] = 'GIF'
        w, h = struct.unpack('<HH', header[6:10])
        info['width'] = w
        info['height'] = h
    elif header[:2] == b'BM':
        info['format'] = 'BMP'
        w, h = struct.unpack('<II', header[18:26])
        info['width'] = w
        info['height'] = h

    return info


def format_size(b):
    for unit in ['B', 'KB', 'MB']:
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} GB"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python image_resizer.py <image_path> [image_path2 ...]")
        print("Shows image dimensions and metadata (no external deps)")
        sys.exit(1)

    for path in sys.argv[1:]:
        if not os.path.exists(path):
            print(f"Not found: {path}")
            continue
        info = get_image_info(path)
        print(f"{os.path.basename(path)}")
        print(f"  Format: {info['format']}")
        print(f"  Size: {format_size(info['size_bytes'])}")
        if info['width'] and info['height']:
            print(f"  Dimensions: {info['width']}x{info['height']}")
        print()
