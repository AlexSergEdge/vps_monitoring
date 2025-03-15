#!/bin/sh
set -e

# Environment variables are set in Dockerfile
USER_NAME="$APPUSER"
GROUP_NAME="$APPGROUP"
USER_HOME="$APPUSER_HOME"

# If we defined $UID and $GID as env variables - we will change id
# for non-root container user
if [ -n "$UID" ] && [ -n "$GID" ]; then
    echo "Updating container user UID:GID to: $UID:$GID"
    groupmod -g "$GID" "$GROUP_NAME"
    usermod -u "$UID" -g "$GID" "$USER_NAME"
    chown -R "$UID:$GID" "$USER_HOME"
fi

# gosu was insttalled during build and is used to run CMD as non-root user
exec gosu "$USER_NAME" "$@"
