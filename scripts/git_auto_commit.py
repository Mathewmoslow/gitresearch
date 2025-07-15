import subprocess
import sys
from datetime import datetime

def run(*args):
    return subprocess.run(["git"] + list(args), check=True)

def commit_and_push(branch, msg=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    full_msg = msg or f"Auto-update: {timestamp}"
    
    run("checkout", branch)
    run("add", "-A")
    run("commit", "-m", full_msg)
    run("push", "-u", "origin", branch)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python git_auto_commit.py <branch-name> [commit-message]")
        sys.exit(1)

    branch = sys.argv[1]
    msg = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
    commit_and_push(branch, msg)

