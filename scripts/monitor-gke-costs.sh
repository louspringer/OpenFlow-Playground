#!/bin/bash
# 💰 GKE Cost Monitor
# Monitor and alert on GKE cluster costs

set -e

PROJECT_ID="aardvark-linkedin-grepper"
CLUSTER_NAME="kiro-agents-cluster"
REGION="us-central1"
BUDGET_THRESHOLD=20  # Alert when approaching $20

echo "💰 GKE Cost Monitor"
echo "==================="
echo "Project: $PROJECT_ID"
echo "Cluster: $CLUSTER_NAME"
echo "Region: $REGION"
echo ""

# Get current month's usage
echo "📊 Current Month Usage:"
gcloud billing budgets list --billing-account=01F112-E73FD5-795507 --format="table(displayName,amount.specifiedAmount.units,thresholdRules[].thresholdPercent)"

# Get cluster node information
echo ""
echo "🖥️  Cluster Nodes:"
kubectl get nodes -o wide

# Get pod resource usage
echo ""
echo "📈 Pod Resource Usage:"
kubectl top pods --all-namespaces

# Check if we should scale down
echo ""
echo "💡 Cost Optimization Suggestions:"
echo "- Consider scaling down to 1 node during non-peak hours"
echo "- Use preemptible instances for development workloads"
echo "- Monitor with: kubectl top nodes"

# Quick cost estimate
NODES=$(kubectl get nodes --no-headers | wc -l)
ESTIMATED_COST=$((NODES * 15))  # ~$15/month per e2-small node
echo ""
echo "📊 Estimated Monthly Cost: ~$${ESTIMATED_COST} (${NODES} nodes)"

if [ $ESTIMATED_COST -gt $BUDGET_THRESHOLD ]; then
    echo "⚠️  WARNING: Estimated cost ($${ESTIMATED_COST}) exceeds threshold ($${BUDGET_THRESHOLD})"
    echo "💡 Consider scaling down the cluster"
fi
