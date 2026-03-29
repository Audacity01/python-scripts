import os
import shutil
import sys

CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.csv'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Code': ['.py', '.js', '.ts', '.cs', '.java', '.cpp', '.h', '.html', '.css'],
}

def get_category(ext):
    ext = ext.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return 'Other'

def organize(directory):
    if not os.path.isdir(directory):
        print(f"Not a valid directory: {directory}")
        return

    moved = 0
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1]
            if not ext:
                continue
            category = get_category(ext)
            dest_dir = os.path.join(directory, category)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(filepath, os.path.join(dest_dir, filename))
            moved += 1

    print(f"Organized {moved} files.")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    organize(target)
