import os
import sys
import shutil
import platform
import subprocess

def check_command(cmd):
    path = shutil.which(cmd)
    if path:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=5)
            version = result.stdout.strip().split('\n')[0] or result.stderr.strip().split('\n')[0]
            return True, version
        except Exception:
            return True, "(version unknown)"
    return False, None


TOOLS = [
    'python', 'python3', 'pip', 'node', 'npm', 'git',
    'dotnet', 'java', 'docker', 'kubectl', 'terraform',
    'aws', 'az', 'gcloud', 'code', 'vim', 'curl', 'wget'
]


if __name__ == '__main__':
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print(f"Python: {platform.python_version()}")
    print(f"User: {os.getenv('USER') or os.getenv('USERNAME')}")
    print()

    custom_tools = sys.argv[1:] if len(sys.argv) > 1 else TOOLS

    print("Tool Check:")
    for tool in custom_tools:
        found, version = check_command(tool)
        if found:
            print(f"  ✓ {tool:12s} — {version}")
        else:
            print(f"  ✗ {tool:12s} — not found")

    print()
    env_vars = ['PATH', 'HOME', 'JAVA_HOME', 'DOTNET_ROOT', 'GOPATH', 'NODE_ENV']
    print("Key env vars:")
    for var in env_vars:
        val = os.environ.get(var)
        if val:
            if len(val) > 60:
                val = val[:57] + "..."
            print(f"  {var}: {val}")
