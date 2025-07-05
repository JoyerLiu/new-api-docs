#!/bin/sh

# Development server script after switching to mkdocs-static-i18n

echo "🚀 Starting development server with i18n (hot-reload)..."

echo "📱 Chinese version: http://127.0.0.1:8000"
echo "📱 English version: http://127.0.0.1:8000/en/"
echo "🛑 Press Ctrl+C to stop the server"

# Start mkdocs with hot reload on single port
mkdocs serve --dev-addr 127.0.0.1:8000 