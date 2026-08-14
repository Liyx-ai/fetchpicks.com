#!/bin/bash
# GitHub push with auto-retry (5 min intervals, up to 12 retries = 1 hour)
# Usage: bash git-push-retry.sh
# Credentials: reads GITHUB_TOKEN env var (set via `setx GITHUB_TOKEN "..."`)
#              Falls back to manual URL if env var unset.

SITE_DIR="/d/fetchpicks-site"
MAX_RETRIES=12
RETRY_DELAY=300  # 5 minutes in seconds
GITHUB_USER="Liyx-ai"
GITHUB_REPO="fetchpicks.com"
PLAIN_URL="https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

cd "$SITE_DIR" || exit 1

# Check if there's anything to push
UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null)
if [ -z "$UNPUSHED" ]; then
    echo "No unpushed commits. Nothing to do."
    exit 0
fi

echo "Found unpushed commits:"
echo "$UNPUSHED"

# Build auth URL from env var, or fall back to plain URL
if [ -n "$GITHUB_TOKEN" ]; then
    AUTH_URL="https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"
    # Temporarily set remote with credentials
    git remote set-url origin "$AUTH_URL"
    TRAP_RESTORE=1
else
    echo "WARNING: GITHUB_TOKEN not set. Trying plain URL (may fail if credentials not cached)."
fi

cleanup() {
    if [ -n "$TRAP_RESTORE" ]; then
        git remote set-url origin "$PLAIN_URL"
        echo "Remote URL restored to plain (no token)."
    fi
}
trap cleanup EXIT

for i in $(seq 1 $MAX_RETRIES); do
    echo "Push attempt $i/$MAX_RETRIES..."

    git push origin main 2>&1

    if [ $? -eq 0 ]; then
        echo "Push successful!"
        exit 0
    fi

    if [ $i -lt $MAX_RETRIES ]; then
        echo "Push failed. Retrying in $RETRY_DELAY seconds..."
        sleep $RETRY_DELAY
    fi
done

echo "All $MAX_RETRIES attempts failed. Will retry on next automation cycle."
exit 1
