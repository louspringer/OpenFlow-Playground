#!/bin/bash

# Setup Cloud Build Trigger for Develop Branch
# This creates a trigger that automatically builds and deploys on pushes to develop

set -e

PROJECT_ID="aardvark-linkedin-grepper"
TRIGGER_NAME="ghostbusters-api-develop-trigger"
REPO_NAME="OpenFlow-Playground"
REPO_OWNER="louspringer"
BRANCH_PATTERN="^develop$"

echo "🚀 Setting up Cloud Build Trigger for develop branch"
echo "📋 Project: "PROJECT_I"D"
echo "🔗 Trigger: "TRIGGER_NAM"E"
echo "🌿 Branch: "BRANCH_PATTER"N"
echo "👤 Owner: "REPO_OWNE"R"

# Create Cloud Build trigger
echo "🔧 Creating Cloud Build trigger..."

gcloud builds triggers create github \
  --name=""TRIGGER_NAM"E" \
  --repo-name=""REPO_NAM"E" \
  --repo-owner=""REPO_OWNE"R" \
  --branch-pattern=""BRANCH_PATTER"N" \
  --build-config="cloudbuild.yaml" \
  --project=""PROJECT_I"D" \
  --description="Automatic build and deploy Ghostbusters API on push to develop branch"

echo "✅ Cloud Build trigger created successfully!"
echo ""
echo "📊 Trigger Details:"
echo "   Name: "TRIGGER_NAM"E"
echo "   Repository: "REPO_NAM"E"
echo "   Owner: "REPO_OWNE"R"
echo "   Branch: "BRANCH_PATTER"N"
echo "   Config: cloudbuild.yaml"
echo ""
echo "🔗 View triggers:
https://console.cloud.google.com/cloud-build/triggers?project="PROJECT_I"D"
echo "🔗 View builds:
https://console.cloud.google.com/cloud-build/builds?project="PROJECT_I"D"

# Test the trigger
echo ""
echo "🧪 Testing the trigger..."
echo "   Push a commit to trigger the build:"
echo "   git add . \
   
git commit -m 'test: trigger cloud build' \
   
git push" 
