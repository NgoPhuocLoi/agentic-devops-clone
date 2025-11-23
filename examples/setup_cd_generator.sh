#!/bin/bash

# Setup script for CD Manifest Generator

echo "🚀 Setting up CD Manifest Generator"
echo "===================================="
echo ""

# Check if we're in the right directory
if [ ! -f "cd_manifest_generator.py" ]; then
    echo "❌ Error: This script must be run from the examples directory"
    exit 1
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "⚠️  Warning: OPENAI_API_KEY environment variable is not set"
    echo "   Please set it before running the generator:"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
    echo ""
else
    echo "✅ OPENAI_API_KEY is set"
fi

# Check for GitHub token (optional)
if [ -z "$GITHUB_TOKEN" ]; then
    echo ""
    echo "ℹ️  Info: GITHUB_TOKEN is not set (optional for public repos)"
    echo "   For private repos or higher rate limits, set:"
    echo "   export GITHUB_TOKEN='your-github-token'"
    echo ""
else
    echo "✅ GITHUB_TOKEN is set"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
cd ../agentic_devops

if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

# Go back to examples directory
cd ../examples

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the generator:"
echo "  1. Make sure you're in the virtual environment:"
echo "     source ../agentic_devops/.venv/bin/activate"
echo ""
echo "  2. Set your OpenAI API key:"
echo "     export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "  3. Run the generator:"
echo "     python cd_manifest_generator.py"
echo ""
echo "  Or run the simple demo:"
echo "     python cd_manifest_demo.py"
echo ""
