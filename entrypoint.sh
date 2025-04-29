#!/bin/sh

# docker should always create it or we will have permission errors
mkdir -p /app/data
exec "$@"
