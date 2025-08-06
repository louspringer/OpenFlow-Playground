#!/bin/bash
# Test Google Cloud Secret Manager Integration

set -e

echo "🔐 Testing Google Cloud Secret Manager Integration"
echo "================================================"

# Check if gcloud CLI is available
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install Google Cloud SDK first."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with gcloud"
    echo "Please run: gcloud auth login"
    exit 1
fi

echo "✅ gcloud CLI available and authenticated"

# Configuration
PROJECT_ID=${GCP_PROJECT_ID:-"aardvark-linkedin-grepper"}

echo "📋 Configuration:"
echo "  Project ID: $PROJECT_ID"

echo ""
echo "📋 Available secrets:"
gcloud secrets list --project="$PROJECT_ID" --format="table(name,createTime)"

echo ""
echo "🔧 Testing secret access..."

# Test OpenAI API key
echo ""
echo "🔑 Testing OpenAI API key access..."
if gcloud secrets versions access latest --secret="openai-api-key" --project="$PROJECT_ID" &>/dev/null; then
    echo "✅ OpenAI API key is accessible"
    OPENAI_KEY_LENGTH=$(gcloud secrets versions access latest --secret="openai-api-key" --project="$PROJECT_ID" | wc -c)
    echo "   Key length: $OPENAI_KEY_LENGTH characters"
else
    echo "❌ OpenAI API key is not accessible or doesn't exist"
fi

# Test Anthropic API key
echo ""
echo "🔑 Testing Anthropic API key access..."
if gcloud secrets versions access latest --secret="anthropic-api-key" --project="$PROJECT_ID" &>/dev/null; then
    echo "✅ Anthropic API key is accessible"
    ANTHROPIC_KEY_LENGTH=$(gcloud secrets versions access latest --secret="anthropic-api-key" --project="$PROJECT_ID" | wc -c)
    echo "   Key length: $ANTHROPIC_KEY_LENGTH characters"
else
    echo "❌ Anthropic API key is not accessible or doesn't exist"
fi

echo ""
echo "💡 To add API keys:"
echo "  echo -n 'your-openai-key' | gcloud secrets versions add openai-api-key --data-file=-"
echo "  echo -n 'your-anthropic-key' | gcloud secrets versions add anthropic-api-key --data-file=-"

echo ""
echo "🚀 To deploy the updated Ghostbusters API with LLM support:"
echo "  ./scripts/deploy-ghostbusters-api.sh"

echo ""
echo "🧪 To test the LLM-enhanced agents:"
echo "  curl -X POST https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-analyze \\"
echo "    -H \"Content-Type: application/json\" \\"
echo "    -d '{\"project_path\": \".\", \"agents\": [\"security\", \"code_quality\"]}'" 