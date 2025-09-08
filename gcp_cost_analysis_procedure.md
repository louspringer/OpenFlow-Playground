# GCP Cost Analysis Procedure

## Lesson Learned: Default Cloud Provider Settings

**Critical Finding**: Cloud providers (GCP, AWS, Azure) default to **maximum availability** settings that maximize costs, not cost efficiency.

### The Problem

- **Default behavior**: Services run 24/7 with minimum instances > 0
- **Cost impact**: 90-95% higher costs than necessary
- **Frequency**: Happens on every new deployment
- **Detection**: Only caught through cost analysis, not obvious

### The Solution

- **Always set minInstances=0** for auto-scaling services
- **Use pay-per-use pricing** models
- **Implement cost monitoring** from day one
- **Add cost checks** to deployment procedures

## GCP Cost Analysis Procedure

### When User Says "Run GCP Cost Analysis"

#### 1. Immediate Cost Check

```bash
# Check current project
gcloud config get-value project

# List all running services
gcloud run services list --format="table(metadata.name,status.conditions[0].status,spec.template.spec.containers[0].resources.limits)"

# Check scaling configuration
gcloud run services describe [SERVICE_NAME] --region=us-central1 --format="yaml" | grep -A 2 -B 2 "minScale\|maxScale"
```

#### 2. Identify Cost Issues

- **Services running 24/7**: No minInstances=0
- **Over-provisioned resources**: CPU/memory too high
- **No auto-scaling**: Fixed instance counts
- **Unused services**: Running but not needed

#### 3. Apply Immediate Fixes

```bash
# Fix Cloud Run services
gcloud run services update [SERVICE_NAME] --region=us-central1 --min-instances=0 --max-instances=5

# Right-size resources
gcloud run services update [SERVICE_NAME] --region=us-central1 --cpu=0.5 --memory=256Mi

# Stop unused services
gcloud run services delete [SERVICE_NAME] --region=us-central1
```

#### 4. Verify Cost Optimization

- **Check scaling**: minInstances=0, maxInstances=5
- **Verify resources**: Right-sized CPU/memory
- **Test scaling**: Ensure services scale to zero
- **Monitor costs**: Set up billing alerts

## AWS Cost Analysis Procedure

### When User Says "Run AWS Cost Analysis"

#### 1. Check EC2 Instances

```bash
# List running instances
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType]' --output table

# Check for over-provisioned instances
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name]' --filters "Name=instance-state-name,Values=running" --output table
```

#### 2. Check Lambda Functions

```bash
# List Lambda functions
aws lambda list-functions --query 'Functions[*].[FunctionName,Runtime,MemorySize,Timeout]' --output table

# Check for over-provisioned memory
aws lambda list-functions --query 'Functions[?MemorySize>`512`].[FunctionName,MemorySize,Runtime]' --output table
```

#### 3. Check RDS Instances

```bash
# List RDS instances
aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceClass,Engine,DBInstanceStatus]' --output table

# Check for over-provisioned instances
aws rds describe-db-instances --query 'DBInstances[?DBInstanceClass>`db.t3.micro`].[DBInstanceIdentifier,DBInstanceClass,Engine]' --output table
```

#### 4. Apply AWS Cost Fixes

```bash
# Stop unused EC2 instances
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Right-size Lambda functions
aws lambda update-function-configuration --function-name my-function --memory-size 256

# Right-size RDS instances
aws rds modify-db-instance --db-instance-identifier my-db --db-instance-class db.t3.micro
```

## Azure Cost Analysis Procedure

### When User Says "Run Azure Cost Analysis"

#### 1. Check App Services

```bash
# List App Services
az webapp list --query '[].{Name:name,State:state,ResourceGroup:resourceGroup}' --output table

# Check scaling configuration
az webapp show --name [APP_NAME] --resource-group [RG_NAME] --query 'siteConfig.minimumElasticInstanceCount'
```

#### 2. Check Virtual Machines

```bash
# List VMs
az vm list --query '[].{Name:name,ResourceGroup:resourceGroup,Size:hardwareProfile.vmSize,State:provisioningState}' --output table

# Check for over-provisioned VMs
az vm list --query '[?hardwareProfile.vmSize>`Standard_B1s`].[name,hardwareProfile.vmSize,resourceGroup]' --output table
```

#### 3. Apply Azure Cost Fixes

```bash
# Stop unused VMs
az vm deallocate --name [VM_NAME] --resource-group [RG_NAME]

# Right-size App Services
az webapp update --name [APP_NAME] --resource-group [RG_NAME] --min-elastic-instance-count 0
```

## Universal Cost Analysis Requirements

### Requirement 34: Automated Cost Analysis and Optimization

**User Story:** As a system operator, I want automated cost analysis and optimization for all cloud platforms, so that I never accidentally run expensive services 24/7.

#### Acceptance Criteria

1. **WHEN deploying to any cloud platform** THEN the system SHALL automatically:

   - Set minInstances=0 for auto-scaling services
   - Right-size resource allocations
   - Enable pay-per-use pricing models
   - Set up cost monitoring and alerts

1. **WHEN running cost analysis** THEN the system SHALL:

   - Check all running services and their configurations
   - Identify over-provisioned resources
   - Detect services running 24/7 unnecessarily
   - Provide specific optimization recommendations

1. **WHEN detecting cost issues** THEN the system SHALL:

   - Apply immediate fixes automatically
   - Verify optimization worked
   - Set up ongoing cost monitoring
   - Document lessons learned

1. **WHEN monitoring costs** THEN the system SHALL:

   - Track daily spending by service
   - Alert when costs exceed thresholds
   - Provide cost breakdown and trends
   - Suggest further optimizations

1. **WHEN documenting cost issues** THEN the system SHALL:

   - Create incident reports with root causes
   - Update deployment procedures
   - Add cost checks to CI/CD pipelines
   - Share lessons learned across teams

### Requirement 35: Cloud Provider Cost Optimization

**User Story:** As a developer, I want cost optimization to be the default for all cloud deployments, so that I never accidentally create expensive resources.

#### Acceptance Criteria

1. **WHEN deploying to GCP** THEN the system SHALL:

   - Set Cloud Run minInstances=0
   - Use preemptible instances where possible
   - Enable auto-scaling for all services
   - Set up cost alerts and monitoring

1. **WHEN deploying to AWS** THEN the system SHALL:

   - Use Spot instances for non-critical workloads
   - Right-size Lambda function memory
   - Enable auto-scaling for EC2 instances
   - Use S3 Intelligent Tiering

1. **WHEN deploying to Azure** THEN the system SHALL:

   - Use App Service auto-scaling
   - Enable VM auto-shutdown
   - Use consumption-based pricing
   - Set up cost management alerts

1. **WHEN deploying to any platform** THEN the system SHALL:

   - Validate cost optimization settings
   - Test auto-scaling behavior
   - Set up cost monitoring
   - Document cost implications

## Cost Analysis Checklist

### Pre-Deployment

- [ ] **Set minInstances=0** for auto-scaling services
- [ ] **Right-size resources** based on actual needs
- [ ] **Enable pay-per-use** pricing models
- [ ] **Set up cost alerts** and monitoring
- [ ] **Test auto-scaling** behavior

### Post-Deployment

- [ ] **Verify cost optimization** settings
- [ ] **Monitor daily spending** for first week
- [ ] **Check auto-scaling** is working
- [ ] **Validate cost alerts** are firing
- [ ] **Document cost baseline** for future reference

### Ongoing Monitoring

- [ ] **Daily cost checks** for first month
- [ ] **Weekly cost reviews** after that
- [ ] **Monthly optimization** reviews
- [ ] **Quarterly cost audits** for all services
- [ ] **Annual cost strategy** updates

## Common Cost Issues and Fixes

### GCP Issues

- **Cloud Run running 24/7**: Set minInstances=0
- **Over-provisioned CPU**: Right-size based on usage
- **Unused services**: Delete or stop
- **No auto-scaling**: Enable with proper limits

### AWS Issues

- **EC2 instances running 24/7**: Use Spot instances or auto-scaling
- **Lambda over-provisioned**: Right-size memory allocation
- **RDS over-provisioned**: Right-size instance class
- **S3 expensive storage**: Use Intelligent Tiering

### Azure Issues

- **App Services running 24/7**: Set minElasticInstanceCount=0
- **VMs running 24/7**: Enable auto-shutdown
- **Over-provisioned resources**: Right-size based on usage
- **No cost monitoring**: Set up Cost Management

## Remember

**When user says "Run GCP Cost Analysis":**

1. **Check current costs** and identify issues
1. **Apply immediate fixes** for cost optimization
1. **Verify optimization** worked correctly
1. **Set up monitoring** to prevent future issues
1. **Document lessons learned** for future deployments

**This will happen again** - cloud providers default to maximum availability, not cost efficiency. Always check and fix cost settings on every deployment!
