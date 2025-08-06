#!/bin/bash
# Deploy Ghostbusters API Service to GCP Cloud Functions

set -e

echo "🚀 Deploying Ghostbusters API Service to GCP Cloud Functions..."

# Check if gcloud CLI is available
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install Google Cloud SDK first."
    exit 1
fi

# Configuration
PROJECT_ID=${GCP_PROJECT_ID:-"aardvark-linkedin-grepper"}
REGION=${GCP_REGION:-"us-central1"}
SERVICE_NAME="ghostbusters-api"

echo "📋 Configuration:"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo "  Service: $SERVICE_NAME"
echo "  Source: src/ghostbusters_api"

# Create Pub/Sub topics if they don't exist
echo "📡 Creating Pub/Sub topics..."
gcloud pubsub topics create ghostbusters-analysis --project=$PROJECT_ID || echo "Topic already exists"
gcloud pubsub topics create ghostbusters-recovery --project=$PROJECT_ID || echo "Topic already exists"

# Deploy the analysis worker function (triggered by Pub/Sub)
echo "🔧 Deploying Ghostbusters analysis worker..."
gcloud functions deploy ghostbusters-analysis-worker \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=src/ghostbusters_api \
    --entry-point=ghostbusters_analysis_worker \
    --trigger-topic=ghostbusters-analysis \
    --memory=512MB \
    --timeout=540s \
    --project=$PROJECT_ID

# Deploy the recovery worker function (triggered by Pub/Sub)
echo "🔧 Deploying Ghostbusters recovery worker..."
gcloud functions deploy ghostbusters-recovery-worker \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=src/ghostbusters_api \
    --entry-point=ghostbusters_recovery_worker \
    --trigger-topic=ghostbusters-recovery \
    --memory=512MB \
    --timeout=540s \
    --project=$PROJECT_ID

# Deploy the analyze endpoint (HTTP trigger)
echo "🔧 Deploying Ghostbusters analyze endpoint..."
gcloud functions deploy ghostbusters-analyze \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=src/ghostbusters_api \
    --entry-point=ghostbusters_analyze \
    --trigger-http \
    --allow-unauthenticated \
    --memory=256MB \
    --timeout=60s \
    --project=$PROJECT_ID

# Deploy the recover endpoint (HTTP trigger)
echo "🔧 Deploying Ghostbusters recover endpoint..."
gcloud functions deploy ghostbusters-recover \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=src/ghostbusters_api \
    --entry-point=ghostbusters_recover \
    --trigger-http \
    --allow-unauthenticated \
    --memory=256MB \
    --timeout=60s \
    --project=$PROJECT_ID

# Deploy the status endpoint (HTTP trigger)
echo "🔧 Deploying Ghostbusters status endpoint..."
gcloud functions deploy ghostbusters-status \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=src/ghostbusters_api \
    --entry-point=ghostbusters_status \
    --trigger-http \
    --allow-unauthenticated \
    --memory=256MB \
    --timeout=60s \
    --project=$PROJECT_ID

# Deploy the jobs endpoint (HTTP trigger)
echo "🔧 Deploying Ghostbusters jobs endpoint..."
gcloud functions deploy ghostbusters-jobs \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=src/ghostbusters_api \
    --entry-point=ghostbusters_jobs \
    --trigger-http \
    --allow-unauthenticated \
    --memory=256MB \
    --timeout=60s \
    --project=$PROJECT_ID

echo "✅ Ghostbusters API Service deployed successfully!"
echo ""
echo "📋 Service URLs:"
echo "  Analyze: https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-analyze"
echo "  Recover: https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-recover"
echo "  Status: https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-status"
echo "  Jobs: https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-jobs"
echo ""
echo "🔧 Usage Examples:"
echo "  # Queue analysis"
echo "  curl -X POST https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-analyze \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"project_path\": \".\", \"agents\": [\"security\", \"code_quality\"]}'"
echo ""
echo "  # Queue recovery"
echo "  curl -X POST https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-recover \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"recovery_type\": \"syntax\", \"target_files\": [\"src/main.py\"]}'"
echo ""
echo "  # Check status"
echo "  curl \"https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-status?job_id=YOUR_JOB_ID\""
echo ""
echo "  # List jobs"
echo "  curl https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-jobs" 