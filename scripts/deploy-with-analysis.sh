#!/bin/bash

# Intelligent Cloud Build Deployment with Ghostbusters Analysis
# This script triggers a Cloud Build that:
# 1. Clones the repository (with branch support)
# 2. Builds the container
# 3. Runs Ghostbusters analysis on the cloned code
# 4. Deploys to Cloud Run

set -e

# Configuration
PROJECT_ID="aardvark-linkedin-grepper"
REGION="us-central1"
BRANCH_NAME="${1:-main}"  # Default to main, or specify branch as first argument

echo "🚀 Starting Intelligent Cloud Build Deployment"
echo "📋 Project: $PROJECT_ID"
echo "🌿 Branch: $BRANCH_NAME"
echo "📍 Region: $REGION"

# Trigger Cloud Build with analysis
echo "🔍 Triggering Cloud Build with Ghostbusters analysis..."

gcloud builds submit \
  --config=src/ghostbusters_api/cloudbuild.yaml \
  --project=$PROJECT_ID \
  src/ghostbusters_api/

echo "✅ Cloud Build triggered successfully!"
echo ""
echo "📊 Build will:"
echo "   1. Clone repo from branch: $BRANCH_NAME"
echo "   2. Build container with analysis capabilities"
echo "   3. Run Ghostbusters analysis on the code"
echo "   4. Deploy to Cloud Run"
echo ""
echo "🔗 Monitor build: https://console.cloud.google.com/cloud-build/builds?project=$PROJECT_ID"
echo "🔗 View logs: gcloud builds log --project=$PROJECT_ID"

# Wait for build to complete and show results
echo ""
echo "⏳ Waiting for build to complete..."
BUILD_ID=$(gcloud builds list --limit=1 --format="value(id)" --project=$PROJECT_ID)

echo "📈 Build ID: $BUILD_ID"
echo "🔍 Check analysis results in the build logs above" 