#!/usr/bin/env bash

# Start College Management System Web Server
cd "$(dirname "$0")"
echo "Starting server on http://localhost:5001..."
python3 application/server.py
