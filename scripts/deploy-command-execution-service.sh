#!/bin/bash
# Deploy Command Execution Service to GCP Cloud Functions

set -e

echo "🚀 Deploying Command Execution Service to GCP Cloud Functions..."

# Check if gcloud CLI is available
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install Google Cloud SDK first."
    exit 1
fi

# Configuration
PROJECT_ID=${GCP_PROJECT_ID:-"aardvark-linkedin-grepper"}
REGION=${GCP_REGION:-"us-central1"}
SERVICE_NAME="command-execution-service"

echo "📋 Configuration:"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo "  Service: $SERVICE_NAME"
echo "  Source: src/command_execution_service"

# Create Pub/Sub topics if they don't exist
echo "📡 Creating Pub/Sub topics..."
gcloud pubsub topics create command-execution-input --project=$PROJECT_ID || echo "Topic already exists"
gcloud pubsub topics create command-execution-output --project=$PROJECT_ID || echo "Topic already exists"

# Deploy the command executor function (triggered by Pub/Sub)
echo "🔧 Deploying command executor function..."
gcloud functions deploy command-executor \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=src/command_execution_service \
    --entry-point=command_executor \
    --trigger-topic=command-execution-input \
    --memory=512MB \
    --timeout=540s \
    --project=$PROJECT_ID

# Deploy the submit command function (HTTP trigger)
echo "🔧 Deploying submit command function..."
gcloud functions deploy submit-command \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=src/command_execution_service \
    --entry-point=submit_command \
    --trigger-http \
    --allow-unauthenticated \
    --memory=256MB \
    --timeout=60s \
    --project=$PROJECT_ID

# Deploy the get status function (HTTP trigger)
echo "🔧 Deploying get status function..."
gcloud functions deploy get-command-status \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=src/command_execution_service \
    --entry-point=get_command_status \
    --trigger-http \
    --allow-unauthenticated \
    --memory=256MB \
    --timeout=60s \
    --project=$PROJECT_ID

# Deploy the list commands function (HTTP trigger)
echo "🔧 Deploying list commands function..."
gcloud functions deploy list-user-commands \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=src/command_execution_service \
    --entry-point=list_user_commands \
    --trigger-http \
    --allow-unauthenticated \
    --memory=256MB \
    --timeout=60s \
    --project=$PROJECT_ID

echo "✅ Command Execution Service deployed successfully!"
echo ""
echo "📋 Service URLs:"
echo "  Submit Command: https://$REGION-$PROJECT_ID.cloudfunctions.net/submit-command"
echo "  Get Status: https://$REGION-$PROJECT_ID.cloudfunctions.net/get-command-status"
echo "  List Commands: https://$REGION-$PROJECT_ID.cloudfunctions.net/list-user-commands"
echo ""
echo "🔧 Usage Examples:"
echo "  # Submit a command"
echo "  curl -X POST https://$REGION-$PROJECT_ID.cloudfunctions.net/submit-command \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"command\": \"ls -la\", \"cwd\": \"/tmp\"}'"
echo ""
echo "  # Check status"
echo "  curl \"https://$REGION-$PROJECT_ID.cloudfunctions.net/get-command-status?job_id=YOUR_JOB_ID\""
echo ""
echo "  # List user commands"
echo "  curl https://$REGION-$PROJECT_ID.cloudfunctions.net/list-user-commands" 