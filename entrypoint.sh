#!/bin/sh

mkdir -p /app/data
chown app:app /app/data
exec "$@"
