# 🍄 GKE Cluster Optimization Spore

**Date**: September 3, 2025\
**Issue**: Kiro Agents cluster scaled to 6 nodes unnecessarily\
**Impact**: $197/month cost vs $25 budget (790% over budget)\
**Solution**: Optimize to 3 preemptible nodes only

______________________________________________________________________

## 🎯 **Problem Analysis**

### **Current State**

- **Cluster**: `kiro-agents-cluster`
- **Nodes**: 6 total (3 regular + 3 preemptible)
- **Cost**: $197.57/month
- **Budget**: $25/month (790% over budget)

### **Root Cause**

Kiro's autoscaling scaled up both node pools to maximum (3 nodes each) when only 3 preemptible nodes are needed for the use case.

### **Workload Analysis**

From `kubectl get pods`, the actual workload is:

- **kiro-agents namespace**: 2 pods (1 running, 1 ImagePullBackOff)
- **System pods**: Standard GKE system pods
- **Total actual workload**: Minimal - can run on 1-2 nodes

______________________________________________________________________

## 🚀 **Optimization Strategy**

### **Target Configuration**

- **Preemptible Pool**: 3 nodes (e2-small, preemptible)
- **Default Pool**: 0 nodes (disable or remove)
- **Expected Cost**: ~$50/month (80% reduction)

### **Cost Breakdown**

| Configuration | Daily Cost | Monthly Cost | Savings |
|---------------|------------|--------------|---------|
| **Current** (6 nodes) | $6.59 | $197.57 | - |
| **Optimized** (3 preemptible) | $1.65 | $49.50 | $148.07 |
| **Minimal** (1 preemptible) | $0.55 | $16.50 | $181.07 |

______________________________________________________________________

## 🔧 **Implementation Plan**

### **Phase 1: Immediate Cost Reduction**

1. **Scale down default pool to 0 nodes**
1. **Scale up preemptible pool to 3 nodes**
1. **Verify workload migration**

### **Phase 2: Long-term Optimization**

1. **Disable default pool autoscaling**
1. **Set preemptible pool min=1, max=3**
1. **Monitor and adjust based on actual usage**

### **Phase 3: Cost Monitoring**

1. **Set up budget alerts at $20, $40, $50**
1. **Monitor daily costs**
1. **Implement auto-shutdown for idle periods**

______________________________________________________________________

## 📋 **Commands to Execute**

### **Step 1: Scale Down Default Pool**

```bash
gcloud container clusters resize kiro-agents-cluster \
  --node-pool=default-pool \
  --num-nodes=0 \
  --location=us-central1
```

### **Step 2: Scale Up Preemptible Pool**

```bash
gcloud container clusters resize kiro-agents-cluster \
  --node-pool=preemptible-pool \
  --num-nodes=3 \
  --location=us-central1
```

### **Step 3: Verify Migration**

```bash
kubectl get nodes
kubectl get pods --all-namespaces -o wide
```

### **Step 4: Update Autoscaling (Optional)**

```bash
gcloud container clusters update kiro-agents-cluster \
  --location=us-central1 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=3 \
  --node-pool=preemptible-pool
```

______________________________________________________________________

## 💰 **Expected Results**

### **Cost Reduction**

- **Before**: $197.57/month
- **After**: $49.50/month
- **Savings**: $148.07/month (75% reduction)
- **Budget Compliance**: Within 2x budget (vs 8x over)

### **Performance Impact**

- **Minimal**: Preemptible nodes provide same performance
- **Availability**: 3 nodes provide redundancy
- **Auto-scaling**: Still available for peak loads

______________________________________________________________________

## 🎯 **Success Metrics**

### **Immediate (24 hours)**

- [ ] Default pool scaled to 0 nodes
- [ ] Preemptible pool scaled to 3 nodes
- [ ] All pods running successfully
- [ ] Daily cost < $2.00

### **Short-term (1 week)**

- [ ] Monthly cost < $60
- [ ] No performance degradation
- [ ] Budget alerts configured

### **Long-term (1 month)**

- [ ] Monthly cost < $50
- [ ] Cluster utilization optimized
- [ ] Cost monitoring automated

______________________________________________________________________

## 🚨 **Risk Mitigation**

### **Potential Issues**

1. **Pod Eviction**: Some pods may be evicted during scaling
1. **ImagePullBackOff**: One kiro-agent pod already failing
1. **Preemptible Interruption**: Nodes can be terminated

### **Mitigation Strategies**

1. **Gradual Scaling**: Scale down default pool first, then up preemptible
1. **Pod Disruption Budgets**: Ensure critical pods can handle eviction
1. **Health Checks**: Monitor pod health during migration

______________________________________________________________________

## 📊 **Monitoring Dashboard**

### **Key Metrics to Track**

- **Daily Cost**: Target < $2.00
- **Node Count**: Target 3 preemptible nodes
- **Pod Health**: All pods running
- **Budget Usage**: < 200% of $25 budget

### **Alerts to Set**

- **Cost Alert**: > $2.50/day
- **Node Alert**: > 4 nodes total
- **Pod Alert**: Any pod not running

______________________________________________________________________

## 🎯 **Next Steps**

1. **Execute optimization commands**
1. **Monitor for 24 hours**
1. **Adjust based on actual usage**
1. **Implement long-term monitoring**
1. **Document lessons learned**

______________________________________________________________________

**Status**: Ready for execution\
**Priority**: High (Cost optimization)\
**Owner**: GCP Cost Management\
**Review Date**: September 10, 2025
