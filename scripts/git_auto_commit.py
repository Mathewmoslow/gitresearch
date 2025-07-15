import subprocess
import sys
from datetime import datetime

def run(*args):
    return subprocess.run(["git"] + list(args), check=True)

def commit_and_push(branch, msg=None):
    """Stage, commit (if needed), and push to <branch>."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    full_msg = msg or f"Auto‑update: {timestamp}"

    # Ensure branch
    run("checkout", branch)

    # Stage all changes
    run("add", "-A")

    # Only commit if there are staged changes
    status = subprocess.check_output(["git", "status", "--porcelain"]).strip()
    if status:
        run("commit", "-m", full_msg)
        print(f"✅ Committed: {full_msg}")
    else:
        print("✅ No changes to commit.")

    # Always push (keeps branch in sync)
    run("push", "-u", "origin", branch)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python git_auto_commit.py <branch-name> [commit-message]")
        sys.exit(1)

    branch = sys.argv[1]
    message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
    commit_and_push(branch, message)
