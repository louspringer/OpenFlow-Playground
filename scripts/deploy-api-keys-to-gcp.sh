#!/bin/bash
# Deploy API Keys to Google Cloud Secret Manager

set -e

echo "🔐 Deploying API Keys to Google Cloud Secret Manager"
echo "=================================================="

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

# Function to create secret and store value
create_secret() {
    local secret_name="$1"
    local secret_value="$2"
    
    echo "🔑 Creating secret: $secret_name"
    
    # Create the secret if it doesn't exist
    if ! gcloud secrets describe "$secret_name" --project="$PROJECT_ID" &>/dev/null; then
        echo "  Creating secret..."
        gcloud secrets create "$secret_name" --replication-policy="automatic" --project="$PROJECT_ID"
    else
        echo "  Secret already exists"
    fi
    
    # Store the secret value
    echo "  Storing secret value..."
    echo -n "$secret_value" | gcloud secrets versions add "$secret_name" --data-file=- --project="$PROJECT_ID"
    
    echo "  ✅ Secret '$secret_name' created and stored"
}

# Function to get credential from 1Password
get_1password_credential() {
    local item_name="$1"
    local field_name="$2"
    
    echo "🔍 Looking for '$item_name' in 1Password..."
    
    # Try to get the item
    if op item get "$item_name" --fields "$field_name" --reveal 2>/dev/null; then
        return 0
    else
        echo "❌ Could not find '$item_name' with field '$field_name'"
        return 1
    fi
}

# Try to get OpenAI API key from 1Password
echo ""
echo "🔑 Attempting to get OpenAI API key from 1Password..."
OPENAI_API_KEY=""
if command -v op &> /dev/null && op account list &>/dev/null; then
    OPENAI_API_KEY=$(get_1password_credential "OpenAI API Key" "credential")
    if [ $? -eq 0 ]; then
        echo "✅ Found OpenAI API key in 1Password"
    else
        echo "⚠️ OpenAI API key not found in 1Password"
    fi
else
    echo "⚠️ 1Password CLI not available"
fi

# Try to get Anthropic API key from 1Password
echo ""
echo "🔑 Attempting to get Anthropic API key from 1Password..."
ANTHROPIC_API_KEY=""
if command -v op &> /dev/null && op account list &>/dev/null; then
    ANTHROPIC_API_KEY=$(get_1password_credential "Anthropic API Key" "credential")
    if [ $? -eq 0 ]; then
        echo "✅ Found Anthropic API key in 1Password"
    else
        echo "⚠️ Anthropic API key not found in 1Password"
    fi
else
    echo "⚠️ 1Password CLI not available"
fi

# Check environment variables as fallback
if [ -z "$OPENAI_API_KEY" ] && [ -n "$OPENAI_API_KEY_ENV" ]; then
    echo "📝 Using OpenAI API key from environment variable"
    OPENAI_API_KEY="$OPENAI_API_KEY_ENV"
fi

if [ -z "$ANTHROPIC_API_KEY" ] && [ -n "$ANTHROPIC_API_KEY_ENV" ]; then
    echo "📝 Using Anthropic API key from environment variable"
    ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY_ENV"
fi

# Deploy secrets to GCP
echo ""
echo "🚀 Deploying secrets to Google Cloud Secret Manager..."

if [ -n "$OPENAI_API_KEY" ]; then
    create_secret "openai-api-key" "$OPENAI_API_KEY"
else
    echo "⚠️ No OpenAI API key found - skipping"
fi

if [ -n "$ANTHROPIC_API_KEY" ]; then
    create_secret "anthropic-api-key" "$ANTHROPIC_API_KEY"
else
    echo "⚠️ No Anthropic API key found - skipping"
fi

echo ""
echo "✅ API Keys deployed to Google Cloud Secret Manager!"
echo ""
echo "📋 Available secrets:"
gcloud secrets list --project="$PROJECT_ID" --format="table(name,createTime)"

echo ""
echo "🔧 To use these secrets in Cloud Functions:"
echo "  1. Grant access to the Cloud Function service account:"
echo "     gcloud secrets add-iam-policy-binding openai-api-key \\"
echo "       --member=\"serviceAccount:1077539189076-compute@developer.gserviceaccount.com\" \\"
echo "       --role=\"roles/secretmanager.secretAccessor\""
echo ""
echo "  2. Access in code:"
echo "     from google.cloud import secretmanager"
echo "     client = secretmanager.SecretManagerServiceClient()"
echo "     name = f\"projects/{PROJECT_ID}/secrets/openai-api-key/versions/latest\""
echo "     response = client.access_secret_version(request={\"name\": name})"
echo "     api_key = response.payload.data.decode(\"UTF-8\")"

echo ""
echo "💡 To manually add secrets later:"
echo "  echo -n 'your-api-key' | gcloud secrets versions add openai-api-key --data-file=-"
echo "  echo -n 'your-api-key' | gcloud secrets versions add anthropic-api-key --data-file=-" 