import sys
import re

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c*2 for c in hex_color)
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx = max(r, g, b)
    mn = min(r, g, b)
    l = (mx + mn) / 2

    if mx == mn:
        h = s = 0
    else:
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6

    return round(h * 360), round(s * 100), round(l * 100)

def parse_color(color_str):
    color_str = color_str.strip()

    if color_str.startswith('#'):
        r, g, b = hex_to_rgb(color_str)
        return r, g, b

    rgb_match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color_str)
    if rgb_match:
        return int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3))

    parts = color_str.replace(',', ' ').split()
    if len(parts) == 3 and all(p.isdigit() for p in parts):
        return int(parts[0]), int(parts[1]), int(parts[2])

    return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python color_converter.py <color>")
        print("Examples:")
        print("  python color_converter.py '#ff5733'")
        print("  python color_converter.py 'rgb(255, 87, 51)'")
        print("  python color_converter.py '255 87 51'")
        sys.exit(1)

    color_input = ' '.join(sys.argv[1:])
    result = parse_color(color_input)

    if result is None:
        print(f"Could not parse color: {color_input}")
        sys.exit(1)

    r, g, b = result
    h, s, l = rgb_to_hsl(r, g, b)

    print(f"HEX: {rgb_to_hex(r, g, b)}")
    print(f"RGB: rgb({r}, {g}, {b})")
    print(f"HSL: hsl({h}, {s}%, {l}%)")
