import subprocess

def cleanup(path):
    try:
        subprocess.run(["rm", "-rf", path], check=True)
    except Exception as e:
        print(f"Failed to remove {path}: {e}")