#!/bin/bash

# Get version from user input.
while true; do
    read -p "Enter new version (format X.Y.Z): " user_input
    if [[ "$user_input" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        break
    else
        echo "Invalid version format. Please enter a version in the format X.Y.Z."
    fi
done

# Check if user wants to push to origin.
while true; do
    read -p "Do you want to push to origin? (y/N, default is N): " push_to_origin
    push_to_origin=${push_to_origin:-N}
    if [[ "$push_to_origin" =~ ^[yYnN]$ ]]; then
        break
    else
        echo "Invalid input. Please enter 'y' or 'n'."
    fi
done

# Update version.txt and create a commit with.
echo "$user_input" >"$WORKSPACE_PATH/version.txt"
if ! git diff --quiet "$WORKSPACE_PATH/version.txt" ||
    ! git ls-files --error-unmatch "$WORKSPACE_PATH/version.txt" &>/dev/null; then

    git add "$WORKSPACE_PATH/version.txt"
    git commit -m "chore: update number version to $user_input"
else
    echo "No changes in version.txt, skipping commit."
fi

# Create a tag with the new version. Delete the tag if it already exists.
if git tag -l | grep -q "release-v$user_input"; then
    git tag -d "release-v$user_input"
fi
git tag "release-v$user_input"
echo "Created tag 'release-v$user_input'"

# Push to origin if user wants to.
if [[ "$push_to_origin" =~ ^[Yy]$ ]]; then
    git push origin

    if git ls-remote --tags origin | grep -q "refs/tags/release-v$user_input"; then
        git push origin --delete "release-v$user_input"
    fi
    git push origin "release-v$user_input"
fi
