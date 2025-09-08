# Cloud Vocabulary Mapping

## The Problem

Cloud providers use different terminology for the same concepts, causing confusion for developers and LLMs. This leads to:

- **Incorrect implementations** due to terminology confusion
- **Cost overruns** from misunderstanding pricing models
- **Architecture mistakes** from using wrong concepts
- **LLM hallucinations** when translating between providers

## Unified Cloud Vocabulary

### 1. Preemptible/Spot Instances

| Concept | GCP | AWS | Azure | Description |
|---------|-----|-----|-------|-------------|
| **Preemptible Instances** | ✅ Preemptible VMs | ❌ | ❌ | Can be terminated by provider |
| **Spot Instances** | ❌ | ✅ Spot Instances | ❌ | Can be terminated by provider |
| **Low Priority VMs** | ❌ | ❌ | ✅ Low Priority VMs | Can be terminated by provider |
| **Unified Term** | **"Interruptible Instances"** | **"Interruptible Instances"** | **"Interruptible Instances"** | Can be terminated by provider |

### 2. Auto-Scaling

| Concept | GCP | AWS | Azure | Description |
|---------|-----|-----|-------|-------------|
| **Auto Scaling** | ✅ Autoscaler | ✅ Auto Scaling Groups | ✅ Virtual Machine Scale Sets | Automatically adjust capacity |
| **Horizontal Scaling** | ✅ Horizontal Pod Autoscaler | ✅ Auto Scaling Groups | ✅ Virtual Machine Scale Sets | Add/remove instances |
| **Vertical Scaling** | ✅ Vertical Pod Autoscaler | ❌ | ❌ | Resize existing instances |
| **Unified Term** | **"Auto Scaling"** | **"Auto Scaling"** | **"Auto Scaling"** | Automatically adjust capacity |

### 3. Serverless Functions

| Concept | GCP | AWS | Azure | Description |
|---------|-----|-----|-------|-------------|
| **Cloud Functions** | ✅ Cloud Functions | ❌ | ❌ | Event-driven functions |
| **Lambda Functions** | ❌ | ✅ AWS Lambda | ❌ | Event-driven functions |
| **Azure Functions** | ❌ | ❌ | ✅ Azure Functions | Event-driven functions |
| **Unified Term** | **"Serverless Functions"** | **"Serverless Functions"** | **"Serverless Functions"** | Event-driven functions |

### 4. Container Services

| Concept | GCP | AWS | Azure | Description |
|---------|-----|-----|-------|-------------|
| **Cloud Run** | ✅ Cloud Run | ❌ | ❌ | Serverless containers |
| **Fargate** | ❌ | ✅ AWS Fargate | ❌ | Serverless containers |
| **Container Instances** | ❌ | ❌ | ✅ Azure Container Instances | Serverless containers |
| **Unified Term** | **"Serverless Containers"** | **"Serverless Containers"** | **"Serverless Containers"** | Serverless containers |

### 5. Managed Kubernetes

| Concept | GCP | AWS | Azure | Description |
|---------|-----|-----|-------|-------------|
| **GKE** | ✅ Google Kubernetes Engine | ❌ | ❌ | Managed Kubernetes |
| **EKS** | ❌ | ✅ Amazon EKS | ❌ | Managed Kubernetes |
| **AKS** | ❌ | ❌ | ✅ Azure Kubernetes Service | Managed Kubernetes |
| **Unified Term** | **"Managed Kubernetes"** | **"Managed Kubernetes"** | **"Managed Kubernetes"** | Managed Kubernetes |

### 6. Object Storage

| Concept | GCP | AWS | Azure | Description |
|---------|-----|-----|-------|-------------|
| **Cloud Storage** | ✅ Cloud Storage | ❌ | ❌ | Object storage |
| **S3** | ❌ | ✅ Amazon S3 | ❌ | Object storage |
| **Blob Storage** | ❌ | ❌ | ✅ Azure Blob Storage | Object storage |
| **Unified Term** | **"Object Storage"** | **"Object Storage"** | **"Object Storage"** | Object storage |

### 7. Database Services

| Concept | GCP | AWS | Azure | Description |
|---------|-----|-----|-------|-------------|
| **Cloud SQL** | ✅ Cloud SQL | ❌ | ❌ | Managed SQL database |
| **RDS** | ❌ | ✅ Amazon RDS | ❌ | Managed SQL database |
| **SQL Database** | ❌ | ❌ | ✅ Azure SQL Database | Managed SQL database |
| **Unified Term** | **"Managed SQL Database"** | **"Managed SQL Database"** | **"Managed SQL Database"** | Managed SQL database |

### 8. Load Balancing

| Concept | GCP | AWS | Azure | Description |
|---------|-----|-----|-------|-------------|
| **Cloud Load Balancing** | ✅ Cloud Load Balancing | ❌ | ❌ | Load balancing |
| **Application Load Balancer** | ❌ | ✅ ALB | ❌ | Application load balancing |
| **Application Gateway** | ❌ | ❌ | ✅ Application Gateway | Application load balancing |
| **Unified Term** | **"Load Balancer"** | **"Load Balancer"** | **"Load Balancer"** | Load balancing |

### 9. Monitoring and Logging

| Concept | GCP | AWS | Azure | Description |
|---------|-----|-----|-------|-------------|
| **Cloud Monitoring** | ✅ Cloud Monitoring | ❌ | ❌ | Monitoring and alerting |
| **CloudWatch** | ❌ | ✅ Amazon CloudWatch | ❌ | Monitoring and alerting |
| **Monitor** | ❌ | ❌ | ✅ Azure Monitor | Monitoring and alerting |
| **Unified Term** | **"Cloud Monitoring"** | **"Cloud Monitoring"** | **"Cloud Monitoring"** | Monitoring and alerting |

### 10. Cost Management

| Concept | GCP | AWS | Azure | Description |
|---------|-----|-----|-------|-------------|
| **Cloud Billing** | ✅ Cloud Billing | ❌ | ❌ | Cost management |
| **Cost Explorer** | ❌ | ✅ AWS Cost Explorer | ❌ | Cost analysis |
| **Cost Management** | ❌ | ❌ | ✅ Azure Cost Management | Cost management |
| **Unified Term** | **"Cost Management"** | **"Cost Management"** | **"Cost Management"** | Cost management |

## Common Confusion Points

### 1. Preemptible vs Spot vs Low Priority

- **All are interruptible instances** that can be terminated by the provider
- **Cost savings**: 60-90% compared to regular instances
- **Use case**: Batch processing, development, testing
- **Risk**: Can be terminated with short notice

### 2. Serverless vs Container Services

- **Serverless Functions**: Event-driven, single-purpose functions
- **Serverless Containers**: Full applications in containers, auto-scaling
- **Both**: Pay-per-use, scale to zero, managed infrastructure

### 3. Auto-Scaling vs Manual Scaling

- **Auto-Scaling**: Automatic based on metrics (CPU, memory, requests)
- **Manual Scaling**: Fixed instance count, no automatic adjustment
- **Cost impact**: Auto-scaling saves 70-90% costs

### 4. Regional vs Zonal Resources

- **Regional**: Available across multiple zones, higher availability
- **Zonal**: Available in single zone, lower cost
- **Cost impact**: Regional resources cost 20-50% more

## LLM-Friendly Vocabulary

### For Code Generation

```python
# Use unified terms in code
def create_interruptible_instance(provider, region):
    if provider == "gcp":
        return create_preemptible_vm(region)
    elif provider == "aws":
        return create_spot_instance(region)
    elif provider == "azure":
        return create_low_priority_vm(region)

def setup_auto_scaling(provider, service):
    if provider == "gcp":
        return setup_gke_autoscaler(service)
    elif provider == "aws":
        return setup_ec2_autoscaling(service)
    elif provider == "azure":
        return setup_vmss_autoscaling(service)
```

### For Documentation

- **Always use unified terms** in documentation
- **Provide provider-specific examples** when needed
- **Include cost implications** for each option
- **Show migration paths** between providers

### For Requirements

- **Use unified vocabulary** in requirements
- **Specify provider-specific details** in acceptance criteria
- **Include cost optimization** for each provider
- **Provide fallback options** for different providers

## Implementation Guidelines

### 1. Code Comments

```python
# Use unified terms in comments
def create_serverless_function(provider, function_name):
    """
    Create a serverless function (Cloud Functions/Lambda/Azure Functions)
    with auto-scaling and pay-per-use pricing.
    """
    pass
```

### 2. Configuration Files

```yaml
# Use unified terms in config
services:
  api:
    type: serverless_containers  # Cloud Run/Fargate/Container Instances
    scaling:
      min_instances: 0
      max_instances: 10
    pricing: pay_per_use
```

### 3. Documentation

- **Use unified terms** in all documentation
- **Provide provider-specific examples** in appendices
- **Include cost comparisons** for each provider
- **Show migration guides** between providers

## Cost Optimization Vocabulary

### Unified Cost Terms

- **Pay-per-use**: Only pay when resources are active
- **Auto-scaling**: Automatically adjust capacity based on demand
- **Interruptible**: Can be terminated by provider (60-90% cost savings)
- **Regional**: Multi-zone availability (20-50% cost premium)
- **Zonal**: Single-zone availability (lower cost)

### Cost Optimization Strategies

1. **Use interruptible instances** for batch processing
1. **Enable auto-scaling** for all services
1. **Set minInstances=0** for serverless services
1. **Use zonal resources** when high availability isn't needed
1. **Implement cost monitoring** and alerts

## Conclusion

**Unified cloud vocabulary eliminates confusion and reduces errors.** By using consistent terminology across all providers, we can:

- **Reduce implementation errors** from terminology confusion
- **Improve cost optimization** through better understanding
- **Enable better LLM assistance** with consistent terms
- **Simplify multi-cloud architectures** with unified concepts

**Always use unified terms in requirements, code, and documentation!**
