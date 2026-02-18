#!/bin/bash
# Setup OpenClaw Gateway for local development

echo "🔧 Setting up OpenClaw Gateway for Voice Vision development"
echo "=========================================================="

# Check if openclaw is installed
if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw CLI not found"
    echo "Please install OpenClaw first: https://docs.openclaw.ai"
    exit 1
fi

echo "✅ OpenClaw CLI found"

# Check gateway status
echo ""
echo "📡 Checking OpenClaw Gateway status..."
openclaw gateway status

# Start gateway if not running
if [ $? -ne 0 ]; then
    echo ""
    echo "🚀 Starting OpenClaw Gateway..."
    openclaw gateway start
    sleep 3
fi

# Verify gateway is running
echo ""
echo "✅ Verifying gateway..."
curl -s http://localhost:3000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Gateway is running on http://localhost:3000"
else
    echo "⚠️  Gateway may not be responding"
fi

# Install the manufacturing skill
echo ""
echo "🔌 Installing OpenClaw skill..."
cd openclaw-skill
pip3 install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure .env with your credentials"
echo "2. Test: python3 test_connection.py"
echo "3. Start iOS app in Xcode"
