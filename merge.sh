#!/bin/bash

# Variables
SOURCE_BRANCH="local/16.0"
AUTHOR_EMAIL="yibudak@gmail.com"

# Get the list of commit hashes authored by the specified email, reversed
COMMIT_HASHES=$(git log "$SOURCE_BRANCH" --author="$AUTHOR_EMAIL" --format="%H" | tac)

# Iterate through each commit hash and cherry-pick
for COMMIT in $COMMIT_HASHES; do
  echo "Cherry-picking commit: $COMMIT"
  
  # Attempt to cherry-pick the commit
  git cherry-pick "$COMMIT"
  
  # If there is a conflict, resolve it by accepting "theirs"
  if [ $? -ne 0 ]; then
    echo "Conflict detected. Resolving by accepting 'theirs'."
    git checkout --theirs .
    git add .
    git cherry-pick --continue
  fi
done

echo "Cherry-picking completed."
