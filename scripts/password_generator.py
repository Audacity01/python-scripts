import random
import string
import sys

def generate_password(length=16, use_special=True):
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += "!@#$%^&*"

    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
    ]
    if use_special:
        password.append(random.choice("!@#$%^&*"))

    password += [random.choice(chars) for _ in range(length - len(password))]
    random.shuffle(password)
    return ''.join(password)


if __name__ == '__main__':
    length = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    for _ in range(count):
        print(generate_password(length))
