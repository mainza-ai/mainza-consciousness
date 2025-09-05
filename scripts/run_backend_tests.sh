#!/bin/bash

# Backend Test Runner Script
# Ensures proper Python import paths for testing

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
TEST_DIR="$BACKEND_DIR/tests"

echo "🐍 Backend Test Runner"
echo "====================="
echo "📁 Project Root: $PROJECT_ROOT"
echo "📁 Backend Dir:  $BACKEND_DIR"
echo "📁 Test Dir:     $TEST_DIR"
echo ""

# Set PYTHONPATH to project root
export PYTHONPATH="$PROJECT_ROOT"

# Change to backend directory for relative imports
cd "$BACKEND_DIR" || exit 1

echo "🚀 Running backend tests..."
echo "📊 Command: cd $BACKEND_DIR && PYTHONPATH=$PROJECT_ROOT pytest tests/ -v"
echo ""

# Run pytest with proper PYTHONPATH
PYTHONPATH="$PROJECT_ROOT" pytest tests/ -v

echo ""
echo "✅ Test run complete"
