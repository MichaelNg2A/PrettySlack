#!/bin/sh
set -eu

TARGET="/workspaces/Operator_Context"
REPO="https://github.com/MichaelNg2A/Operator_Context.git"

if git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Operator_Context already cloned at $TARGET."
    exit 0
fi

if [ -e "$TARGET" ]; then
    echo "$TARGET exists but is not a Git work tree; skipping Operator_Context clone."
    exit 0
fi

if git ls-remote "$REPO" >/dev/null 2>&1; then
    git clone "$REPO" "$TARGET"
else
    echo "Operator_Context is not accessible; skipping clone."
fi
