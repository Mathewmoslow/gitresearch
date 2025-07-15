#!/usr/bin/env python3
import subprocess
import sys
from typing import Optional
from datetime import datetime

def run(*args):
    return subprocess.run(["git"] + list(args), check=True)

def commit_and_push(branch: str, msg: Optional[str] = None) -> None:
    full_msg = msg or f"Auto-commit on {branch} at {datetime.now()}"
    
    # Ensure we're on the right branch
    run("checkout", branch)
    
    # Check if there are changes to commit
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not result.stdout.strip():
        print("No changes to commit")
        return
    
    # Stage and commit
    run("add", "-A")
    run("commit", "-m", full_msg)
    print(f"✅ Committed: {full_msg}")
    
    # Push to remote
    run("push", "-u", "origin", branch)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        branch = sys.argv[1]
        msg = sys.argv[2] if len(sys.argv) > 2 else None
        commit_and_push(branch, msg)
    else:
        print("Usage: python3 git_auto_commit.py <branch> [message]")
        sys.exit(1)