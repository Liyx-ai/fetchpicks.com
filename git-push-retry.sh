#!/bin/bash
# GitHub push with auto-retry (5 min intervals, up to 12 retries = 1 hour)
# Usage: bash git-push-retry.sh
# Note: The git remote URL should already be configured with credentials.

SITE_DIR="/d/fetchpicks-site"
MAX_RETRIES=12
RETRY_DELAY=300  # 5 minutes in seconds

cd "$SITE_DIR" || exit 1

# Check if there's anything to push
UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null)
if [ -z "$UNPUSHED" ]; then
    echo "No unpushed commits. Nothing to do."
    exit 0
fi

echo "Found unpushed commits:"
echo "$UNPUSHED"

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
