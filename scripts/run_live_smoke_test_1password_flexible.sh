#!/bin/bash

# Live Smoke Test with Flexible 1Password Integration
# Tries multiple common item names and field names to find API credentials

echo "🔐 LIVE SMOKE TEST WITH FLEXIBLE 1PASSWORD"
echo "==========================================="

# Check if 1Password CLI is available
if ! command -v op &> /dev/null; then
    echo "❌ 1Password CLI not found. Please install it first:"
    echo "   https://1password.com/downloads/command-line/"
    exit 1
fi

# Check if user is signed in to 1Password
if ! op account list &> /dev/null; then
    echo "❌ Not signed in to 1Password CLI"
    echo "Please run: op signin"
    exit 1
fi

echo "✅ 1Password CLI available and signed in"

# Function to try multiple item names and field names
find_1password_credential() {
    local provider="$1"
    local possible_items=("$2")
    local possible_fields=("$3")
    
    echo "🔍 Looking for "provide"r API key in 1Password..."
    
    # Try different item names
    for item_name in "${possible_items[@]}"; do
        echo "  Trying item: '"item_name"'"
        
        # Try different field names
        for field_name in "${possible_fields[@]}"; do
            echo "    Trying field: '"field_name"'"
            
            # Try to get the credential
            if credential=$(op item get ""item_nam"e" --fields ""field_nam"e" --reveal 2>/dev/null)
[ -n ""credentia"l" ]; then
                echo "    ✅ Found "provide"r API key in '"item_name"' field '"field_name"'"
                echo ""credentia"l"
                return 0
            fi
        done
    done
    
    echo "  ❌ Could not find "provide"r API key"
    return 1
}

# Common OpenAI item names and field names
OPENAI_ITEMS=(
    "OpenAI API Key"
    "OpenAI"
    "OpenAI API"
    "GPT API Key"
    "GPT"
    "ChatGPT API"
    "ChatGPT"
)

OPENAI_FIELDS=(
    "credential"
    "password"
    "api_key"
    "key"
    "secret"
    "token"
)

# Common Anthropic item names and field names
ANTHROPIC_ITEMS=(
    "Anthropic Cursor AI"
    "Anthropic API Key"
    "Anthropic"
    "Anthropic API"
    "Claude API Key"
    "Claude"
    "Claude API"
)

ANTHROPIC_FIELDS=(
    "credential"
    "password"
    "api_key"
    "key"
    "secret"
    "token"
)

# Try to get OpenAI API key
echo ""
if OPENAI_API_KEY=$(find_1password_credential "OpenAI" "${OPENAI_ITEMS[*]}" "${OPENAI_FIELDS[*]}")
then
    echo "✅ Found OpenAI API key in 1Password"
    export OPENAI_API_KEY
else
    echo "⚠️ OpenAI API key not found in 1Password"
    OPENAI_API_KEY=""
fi

# Try to get Anthropic API key
echo ""
if ANTHROPIC_API_KEY=$(find_1password_credential "Anthropic" "${ANTHROPIC_ITEMS[*]}" "${ANTHROPIC_FIELDS[*]}")
then
    echo "✅ Found Anthropic API key in 1Password"
    export ANTHROPIC_API_KEY
else
    echo "⚠️ Anthropic API key not found in 1Password"
    ANTHROPIC_API_KEY=""
fi

# Check if we have any credentials
if [ -z ""OPENAI_API_KE"Y" ] && [ -z ""ANTHROPIC_API_KE"Y" ]; then
    echo ""
    echo "❌ No API credentials found in 1Password"
    echo ""
    echo "Tried these item names:"
    echo "  OpenAI: ${OPENAI_ITEMS[*]}"
    echo "  Anthropic: ${ANTHROPIC_ITEMS[*]}"
    echo ""
    echo "Tried these field names:"
    echo "  ${OPENAI_FIELDS[*]}"
    echo ""
    echo "To see all available items:"
    echo "  op item list"
    echo ""
    echo "To see item structure:"
    echo "  op item get 'Item Name'"
    echo ""
    echo "To add your API key to 1Password:"
    echo "  op item create --category=api-credential --title='OpenAI API Key'"
    exit 1
fi

echo ""
echo "🎯 Credentials Status:"
echo "   OpenAI API Key: ${OPENAI_API_KEY:+✅ SET}"
echo "   Anthropic API Key: ${ANTHROPIC_API_KEY:+✅ SET}"

echo ""
echo "🧪 Running live smoke test with 1Password credentials..."
echo ""

# Run the live smoke test
python live_smoke_test.py

echo ""
echo "📊 Test completed!"
echo ""
echo "💡 If credentials weren't found, you can:"
echo "  1. Add them to 1Password with one of the tried names"
echo "  2. Update this script with your specific item names"
echo "  3. Run 'op item list' to see your available items" 
