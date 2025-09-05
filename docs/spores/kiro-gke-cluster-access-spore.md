# 🍄 Kiro GKE Cluster Access Instructions Spore

**Date**: September 3, 2025  
**Purpose**: Instructions for Kiro to access and manage the optimized GKE cluster  
**Cluster**: `kiro-agents-cluster` (3 preemptible nodes, cost-optimized)

---

## 🎯 **Cluster Overview**

### **Current Configuration**
- **Cluster Name**: `kiro-agents-cluster`
- **Location**: `us-central1`
- **Project**: `aardvark-linkedin-grepper`
- **Nodes**: 3 preemptible e2-small nodes
- **Cost**: ~$25/month (optimized from $197/month)

### **Node Pool Structure**
- **default-pool**: 0 nodes (disabled for cost optimization)
- **preemptible-pool**: 3 nodes (active, cost-optimized)

---

## 🔧 **Access Instructions for Kiro**

### **1. Get Cluster Credentials**
```bash
# Authenticate with GCP
gcloud auth login

# Set the project
gcloud config set project aardvark-linkedin-grepper

# Get cluster credentials
gcloud container clusters get-credentials kiro-agents-cluster \
  --location=us-central1 \
  --project=aardvark-linkedin-grepper
```

### **2. Verify Access**
```bash
# Check cluster connection
kubectl cluster-info

# List nodes
kubectl get nodes

# List pods in kiro-agents namespace
kubectl get pods -n kiro-agents
```

### **3. Deploy Kiro Agents**
```bash
# Apply kiro agents deployment
kubectl apply -f k8s/kiro-agents-deployment.yaml

# Check deployment status
kubectl get deployments -n kiro-agents

# Check pod status
kubectl get pods -n kiro-agents -o wide
```

---

## 📋 **Kiro Agent Deployment Template**

### **Namespace Creation**
```yaml
# k8s/kiro-agents-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: kiro-agents
```

### **Deployment Configuration**
```yaml
# k8s/kiro-agents-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kiro-agent
  namespace: kiro-agents
  labels:
    app: kiro-agent
spec:
  replicas: 2  # Scale based on workload
  selector:
    matchLabels:
      app: kiro-agent
  template:
    metadata:
      labels:
        app: kiro-agent
    spec:
      nodeSelector:
        cloud.google.com/gke-preemptible: "true"  # Use preemptible nodes
      containers:
      - name: kiro-agent
        image: gcr.io/aardvark-linkedin-grepper/kiro-agent:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: NODE_ENV
          value: "production"
        - name: LOG_LEVEL
          value: "info"
```

### **Service Configuration**
```yaml
# k8s/kiro-agents-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: kiro-agent-service
  namespace: kiro-agents
spec:
  selector:
    app: kiro-agent
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

---

## 🚀 **Scaling Instructions**

### **Scale Up (When Needed)**
```bash
# Scale deployment
kubectl scale deployment kiro-agent --replicas=3 -n kiro-agents

# Check scaling status
kubectl get pods -n kiro-agents
```

### **Scale Down (Cost Optimization)**
```bash
# Scale to minimum
kubectl scale deployment kiro-agent --replicas=1 -n kiro-agents

# Check resource usage
kubectl top pods -n kiro-agents
```

---

## 💰 **Cost Management Guidelines**

### **Current Cost Structure**
- **3 Preemptible Nodes**: ~$25/month
- **Management Fee**: ~$7/month
- **Total**: ~$32/month

### **Cost Optimization Rules**
1. **Never scale above 3 nodes** (would exceed budget)
2. **Use preemptible nodes only** (70% cost savings)
3. **Scale down when idle** (reduce to 1 replica)
4. **Monitor daily costs** (target < $1.50/day)

### **Budget Alerts**
- **Warning**: > $1.00/day
- **Critical**: > $1.50/day
- **Emergency**: > $2.00/day

---

## 🔍 **Monitoring Commands**

### **Health Checks**
```bash
# Check cluster health
kubectl get nodes
kubectl get pods --all-namespaces

# Check kiro agents specifically
kubectl get pods -n kiro-agents
kubectl describe pods -n kiro-agents

# Check logs
kubectl logs -f deployment/kiro-agent -n kiro-agents
```

### **Resource Usage**
```bash
# Check node resources
kubectl top nodes

# Check pod resources
kubectl top pods -n kiro-agents

# Check resource quotas
kubectl describe quota -n kiro-agents
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Pod ImagePullBackOff**
```bash
# Check image availability
kubectl describe pod <pod-name> -n kiro-agents

# Pull image manually
docker pull gcr.io/aardvark-linkedin-grepper/kiro-agent:latest
```

#### **Preemptible Node Termination**
```bash
# Check node status
kubectl get nodes

# Check pod eviction events
kubectl get events -n kiro-agents --sort-by='.lastTimestamp'
```

#### **Resource Constraints**
```bash
# Check resource limits
kubectl describe nodes

# Adjust resource requests/limits in deployment
kubectl edit deployment kiro-agent -n kiro-agents
```

---

## 📊 **Performance Optimization**

### **Resource Recommendations**
- **CPU Request**: 100m (0.1 cores)
- **Memory Request**: 256Mi
- **CPU Limit**: 500m (0.5 cores)
- **Memory Limit**: 512Mi

### **Scaling Strategy**
- **Min Replicas**: 1 (cost optimization)
- **Max Replicas**: 3 (budget constraint)
- **Scale Up**: When CPU > 70% for 5 minutes
- **Scale Down**: When CPU < 30% for 10 minutes

---

## 🎯 **Best Practices**

### **Deployment**
1. **Always use preemptible nodes** (nodeSelector)
2. **Set resource requests and limits**
3. **Use health checks and readiness probes**
4. **Implement graceful shutdown**

### **Cost Management**
1. **Monitor daily costs**
2. **Scale down during low usage**
3. **Use horizontal pod autoscaling**
4. **Regular cost reviews**

### **Security**
1. **Use service accounts with minimal permissions**
2. **Enable network policies**
3. **Regular security updates**
4. **Monitor for vulnerabilities**

---

## 📞 **Support Contacts**

### **GCP Support**
- **Project**: aardvark-linkedin-grepper
- **Billing Account**: 01F112-E73FD5-795507
- **Budget Alert**: $25/month

### **Cluster Information**
- **Console**: https://console.cloud.google.com/kubernetes/clusters/details/us-central1/kiro-agents-cluster
- **Logs**: https://console.cloud.google.com/logs/query
- **Monitoring**: https://console.cloud.google.com/monitoring

---

## 🎯 **Quick Reference**

### **Essential Commands**
```bash
# Connect to cluster
gcloud container clusters get-credentials kiro-agents-cluster --location=us-central1

# Deploy kiro agents
kubectl apply -f k8s/kiro-agents-deployment.yaml

# Check status
kubectl get pods -n kiro-agents

# Scale deployment
kubectl scale deployment kiro-agent --replicas=2 -n kiro-agents

# View logs
kubectl logs -f deployment/kiro-agent -n kiro-agents
```

### **Cost Monitoring**
```bash
# Check current costs
gcloud billing budgets list --billing-account=01F112-E73FD5-795507

# Monitor cluster costs
gcloud container clusters describe kiro-agents-cluster --location=us-central1
```

---

**Status**: Ready for Kiro deployment  
**Priority**: High (Cost-optimized cluster access)  
**Owner**: Kiro Agents Team  
**Review Date**: September 10, 2025
