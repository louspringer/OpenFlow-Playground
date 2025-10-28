# Helm Charts for Beast + Openflow + Hackathon

Production-credible Helm charts for deploying the integrated stack on AWS EKS.

## Charts

### 1. nim-llm
NVIDIA NIM LLM Service (Llama 3.1 8B Instruct)
- GPU-accelerated inference
- Model caching with persistent storage
- IRSA for AWS access
- OpenTelemetry instrumentation

### 2. nim-embeddings
NVIDIA NIM Retrieval Embedding Service
- GPU-accelerated embedding generation
- Horizontal autoscaling (2-5 replicas)
- Batch processing optimization
- Pod disruption budget for HA

### 3. beast
Beast Agentic Orchestrator + Agent Fleet
- Orchestrator: Single replica with state management
- Agents: Auto-scaling fleet (3-10 replicas)
- Snowflake integration for data access
- Service mesh ready

### 4. observability
OpenTelemetry Collector + Grafana Stack
- OTel Collector for traces/metrics/logs
- Prometheus for metrics storage
- Loki for log aggregation
- Tempo for distributed tracing
- Grafana for visualization
- External export to observatory.nkllon.com

## Quick Start

### Prerequisites
```bash
# EKS cluster with GPU nodes
kubectl get nodes -l node.kubernetes.io/instance-type=g5.xlarge

# NVIDIA device plugin
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.0/nvidia-device-plugin.yml

# Secrets
kubectl create secret docker-registry ngc-secret \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password=<NGC_API_KEY>

kubectl create secret generic snowflake-credentials \
  --from-literal=account=<ACCOUNT> \
  --from-literal=user=<USER> \
  --from-literal=password=<PASSWORD> \
  --from-literal=warehouse=<WAREHOUSE> \
  --from-literal=database=<DATABASE>

kubectl create secret generic observatory-credentials \
  --from-literal=api-key=<OBSERVATORY_API_KEY>
```

### Deploy Stack
```bash
# 1. Observability first (provides collector endpoint)
helm install observability ./observability \
  --namespace observability \
  --create-namespace

# 2. NIM Services
helm install nim-llm ./nim-llm \
  --namespace default

helm install nim-embeddings ./nim-embeddings \
  --namespace default

# 3. Beast Orchestrator
helm install beast ./beast \
  --namespace default \
  --set config.snowflakeAccount=<ACCOUNT>

# 4. Verify
kubectl get pods --all-namespaces
kubectl logs -n default -l app.kubernetes.io/name=nim-llm
```

## Configuration

### GPU Node Selector
All GPU workloads target `g5.xlarge` nodes:
```yaml
nodeSelector:
  node.kubernetes.io/instance-type: g5.xlarge
```

### IRSA (IAM Roles for Service Accounts)
Set IRSA role ARNs in values:
```yaml
serviceAccount:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/beast-irsa-role
```

### OpenTelemetry
All services export to OTel Collector:
```yaml
opentelemetry:
  enabled: true
  endpoint: http://otel-collector.observability.svc.cluster.local:4317
```

## Monitoring

Access Grafana:
```bash
kubectl port-forward -n observability svc/observability-grafana 3000:3000
# Open http://localhost:3000
```

Golden dashboards included:
- NIM LLM Performance
- NIM Embeddings Throughput
- Beast Orchestrator Metrics
- End-to-End Trace View

## Production Readiness

### Security
- ✅ Non-root containers
- ✅ Read-only root filesystem
- ✅ Capabilities dropped
- ✅ IRSA for AWS credentials
- ✅ Secret management via Kubernetes secrets

### Reliability
- ✅ Health checks (liveness/readiness)
- ✅ Resource limits
- ✅ Pod disruption budgets
- ✅ Horizontal autoscaling
- ✅ Anti-affinity rules

### Observability
- ✅ OpenTelemetry instrumentation
- ✅ Structured logging
- ✅ Distributed tracing
- ✅ Metrics export
- ✅ External observatory integration

## Cost Optimization

Approximate costs (us-east-1):
- 3x g5.xlarge nodes: ~$3.06/hr (~$73/day)
- EBS gp3 storage (180GB): ~$18/month
- Data transfer: ~$5/month

**Hackathon profile:** ~$100 for 24-48 hours

## Troubleshooting

### GPU Not Available
```bash
kubectl describe node <node-name> | grep nvidia.com/gpu
kubectl logs -n kube-system -l name=nvidia-device-plugin-ds
```

### OOM Errors
```bash
# Check memory usage
kubectl top pods
# Adjust resources in values.yaml
```

### ImagePullBackOff
```bash
# Verify NGC credentials
kubectl get secret ngc-secret -o yaml
```

## Architecture

```
┌─────────────────┐
│   Grafana UI    │
└────────┬────────┘
         │
┌────────▼────────┐       ┌──────────────┐
│ OTel Collector  │◄──────┤ NIM LLM      │
│                 │       └──────────────┘
│  ├─ Prometheus  │       ┌──────────────┐
│  ├─ Loki        │◄──────┤ NIM Embed    │
│  ├─ Tempo       │       └──────────────┘
│  └─ Observatory │       ┌──────────────┐
└─────────────────┘◄──────┤ Beast Orch   │
                          └──────────────┘
                          ┌──────────────┐
                          │ Beast Agents │
                          └──────────────┘
```

## References
- [NVIDIA NIM Docs](https://docs.nvidia.com/nim/)
- [OpenTelemetry](https://opentelemetry.io/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)

