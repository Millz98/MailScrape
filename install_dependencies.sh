#!/bin/bash

echo "🚀 Installing Email Scraper Dependencies"
echo "========================================"

# Check if pip3 is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install Python 3 and pip first."
    exit 1
fi

echo "📦 Installing required packages..."

# Try to install for the current user first
echo "Attempting user installation..."
if pip3 install --user -r requirements.txt; then
    echo "✅ Dependencies installed successfully for current user!"
    echo ""
    echo "💡 If you still get 'ModuleNotFoundError', try running:"
    echo "   python3 -m pip install --user -r requirements.txt"
    echo ""
    echo "   Or for system-wide installation (requires sudo):"
    echo "   sudo pip3 install -r requirements.txt"
else
    echo "⚠️  User installation failed. Trying system-wide installation..."
    echo "This requires sudo privileges..."
    
    if sudo pip3 install -r requirements.txt; then
        echo "✅ Dependencies installed successfully system-wide!"
    else
        echo "❌ Installation failed. Please check your Python/pip setup."
        exit 1
    fi
fi

echo ""
echo "🎉 Installation complete! You can now run:"
echo "   python3 es.py --help"
echo ""
echo "📚 For more information, see README.md"
