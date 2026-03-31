import re
import sys

def convert(md):
    lines = md.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False

    for line in lines:
        if line.startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                lang = line[3:].strip()
                cls = f' class="{lang}"' if lang else ''
                html_lines.append(f'<pre><code{cls}>')
                in_code_block = True
            continue

        if in_code_block:
            html_lines.append(line)
            continue

        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{process_inline(line[2:])}</li>')
        elif line.startswith('> '):
            html_lines.append(f'<blockquote>{process_inline(line[2:])}</blockquote>')
        elif line.strip() == '---':
            html_lines.append('<hr />')
        elif line.strip() == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<p>{process_inline(line)}</p>')

    if in_list:
        html_lines.append('</ul>')

    return '\n'.join(html_lines)


def process_inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1" />', text)
    return text


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_html.py <file.md> [output.html]")
        sys.exit(1)

    with open(sys.argv[1], encoding='utf-8') as f:
        md = f.read()

    result = convert(md)

    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Written to {sys.argv[2]}")
    else:
        print(result)
