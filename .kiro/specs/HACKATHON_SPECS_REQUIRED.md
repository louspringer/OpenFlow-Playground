# Required Specs for Dual Hackathon Sprint

**Based on**: Master Planner PR #30 + program/requirements/mapping.yaml  
**Timeline**: Oct 30 - Nov 9, 2025  
**Deadline 1**: AWS×NVIDIA (Nov 4)  
**Deadline 2**: Cloud Run (Nov 9)

---

## 📋 Hackathon Submission Specs (2)

### 1. AWS×NVIDIA Generative AI Hackathon
**Path**: `.kiro/specs/aws-nvidia-hackathon/`
- **Requirements**: FR-050, NFR-004, OBS-001/002, RED-001, SEC-010/011, DATA-011
- **Deliverables**: 
  - Demo video (3 min max)
  - GitHub repo (public, AWS deployment instructions)
  - Devpost narrative (~800 words)
  - Architecture diagram
  - Cost estimate
  - Compliance statement
- **Components**: kiro-ai-development-hackathon, beast-adapter-aws, beast-redaction-client, beast-observability
- **Status**: ⏳ CREATE

### 2. Google Cloud Run Hackathon
**Path**: `.kiro/specs/gcp-cloud-run-hackathon/`
- **Requirements**: FR-051, NFR-004, OBS-001/002, RED-001, SEC-010/011, DATA-011
- **Deliverables**:
  - Demo video (2-3 min)
  - GitHub repo (public, Cloud Run deployment)
  - Devpost narrative (500-800 words)
  - Live Cloud Run URL
  - Architecture diagram
  - Deployment instructions
- **Components**: cloud-run-app, beast-adapter-gcp, beast-redaction-client, beast-observability
- **Status**: ⏳ CREATE

---

## 🧩 Shared Component Specs (4)

### 3. beast-redaction-client
**Path**: `.kiro/specs/beast-redaction-client/`
- **Requirements**: RED-001 (primary), RED-002/003/004, SEC-011
- **Purpose**: HMAC-protected classify() + apply_redactions API
- **Integration**: Both AWS×NVIDIA and Cloud Run apps
- **Dependency**: Classifier microservice endpoint
- **Status**: ⏳ CREATE

### 4. beast-observability
**Path**: `.kiro/specs/beast-observability/` (exists but needs review)
- **Requirements**: NFR-004, OBS-001/002/005, DATA-011
- **Purpose**: Unified telemetry (logs/metrics/traces) across clouds
- **Integration**: Observatory-Portal, AWS adapters, GCP adapters
- **Deployment**: vonnegut.local (Prometheus + Grafana)
- **Status**: ✅ EXISTS - needs update for hackathon requirements

### 5. beast-adapter-aws
**Path**: `.kiro/specs/beast-adapter-aws/`
- **Requirements**: FR-050 (supporting)
- **Purpose**: EKS job runner, SageMaker invoke, ECR helpers
- **Integration**: AWS×NVIDIA hackathon app
- **Dependencies**: AWS credentials, EKS cluster
- **Status**: ⏳ CREATE

### 6. beast-adapter-gcp
**Path**: `.kiro/specs/beast-adapter-gcp/`
- **Requirements**: FR-051 (supporting)
- **Purpose**: Cloud Run deploy/run helpers, worker pool orchestration
- **Integration**: Cloud Run hackathon app
- **Dependencies**: GCP project credentials
- **Status**: ⏳ CREATE

---

## 🚀 Platform-Specific Application Specs (2)

### 7. kiro-ai-development-hackathon (AWS App)
**Path**: `.kiro/specs/kiro-ai-development-hackathon/`
- **Requirements**: FR-050 (primary)
- **Purpose**: Agentic retrieval app on EKS/SageMaker with NIM endpoints
- **Platform**: AWS (EKS or SageMaker)
- **Features**:
  - NIM LLM integration
  - NIM Retrieval integration
  - Classifier workload
  - GPU-accelerated inference (NVIDIA)
- **Status**: ⏳ CREATE

### 8. cloud-run-app (GCP App)
**Path**: `.kiro/specs/cloud-run-app/`
- **Requirements**: FR-051 (primary)
- **Purpose**: Agentic app on Cloud Run (service/job/worker pool)
- **Platform**: GCP Cloud Run
- **Features**:
  - AI Studio workflow integration
  - Worker pool orchestration
  - Service + Job + Worker Pool deployment
  - Portability demo (from AWS)
- **Status**: ⏳ CREATE

---

## 🔧 Platform Integration Specs (2)

### 9. NIM Integration (NVIDIA)
**Path**: `.kiro/specs/nim-integration/`
- **Requirements**: FR-050 (technical detail)
- **Purpose**: NVIDIA NIM endpoint integration for LLM + Retrieval
- **Components**: NIM LLM, NIM Retrieval, GPU optimization
- **Platform**: AWS (EKS g-series or SageMaker GPU endpoints)
- **Status**: ⏳ CREATE

### 10. AI Studio Workflow (Google)
**Path**: `.kiro/specs/ai-studio-workflow/`
- **Requirements**: FR-051 (technical detail)
- **Purpose**: Google AI Studio integration for agentic workflows
- **Components**: AI Studio APIs, workflow orchestration
- **Platform**: GCP Cloud Run
- **Status**: ⏳ CREATE

---

## 🔒 Compliance & Security Specs (3)

### 11. Threat Model (SEC-010)
**Path**: `.kiro/specs/threat-model-hackathon/`
- **Requirements**: SEC-010
- **Purpose**: Security threat analysis for both hackathon submissions
- **Deliverables**:
  - AWS attack surface analysis
  - GCP attack surface analysis
  - Mitigation strategies
  - Security controls mapping
- **Status**: ⏳ CREATE

### 12. Redaction Policy (RED-004)
**Path**: `.kiro/specs/redaction-policy-hackathon/`
- **Requirements**: RED-004, RED-001/002/003
- **Purpose**: Policy mapping and governance for data redaction
- **Deliverables**:
  - Policy matrix
  - Governance summary
  - GCP-specific notes
  - AWS-specific notes
- **Status**: ⏳ CREATE

### 13. Data Lineage (DATA-011)
**Path**: `.kiro/specs/data-lineage-hackathon/`
- **Requirements**: DATA-011
- **Purpose**: Lineage and provenance tracking across clouds
- **Deliverables**:
  - Lineage report (agent + classifier flow)
  - Cross-cloud movement tracking
  - Trace ID correlation
- **Status**: ⏳ CREATE

---

## 📦 Submission Artifacts Specs (1)

### 14. Devpost Submission Package
**Path**: `.kiro/specs/devpost-submission-package/`
- **Requirements**: FR-052
- **Purpose**: Submission templates, narratives, disclosures
- **Deliverables**:
  - AWS×NVIDIA Devpost narrative + disclosure
  - Cloud Run Devpost narrative + reuse statement
  - Distinctness documentation
  - New-work disclosures
- **Status**: ⏳ CREATE

---

## 📊 Summary

**Total Specs Required**: 14  
**Existing Specs**: 1 (beast-observatory - needs update)  
**Specs to Create**: 13  

**Priority Order** (based on dependencies):

### Phase 1: Foundation (Days 1-2)
1. beast-redaction-client
2. beast-observability (update)
3. beast-adapter-aws
4. beast-adapter-gcp

### Phase 2: AWS×NVIDIA (Days 3-5)
5. NIM Integration
6. kiro-ai-development-hackathon
7. Threat Model
8. AWS×NVIDIA Hackathon submission spec

### Phase 3: Cloud Run (Days 6-9)
9. AI Studio Workflow
10. cloud-run-app
11. Cloud Run Hackathon submission spec
12. Devpost Submission Package

### Phase 4: Compliance (Parallel with Phases 2-3)
13. Redaction Policy
14. Data Lineage

---

## 🚀 Next Action

Create these specs using `/kiro:spec-init` workflow:

```bash
# Foundation
/kiro:spec-init beast-redaction-client
/kiro:spec-init beast-adapter-aws
/kiro:spec-init beast-adapter-gcp

# AWS×NVIDIA
/kiro:spec-init nim-integration
/kiro:spec-init kiro-ai-development-hackathon
/kiro:spec-init aws-nvidia-hackathon

# Cloud Run
/kiro:spec-init ai-studio-workflow
/kiro:spec-init cloud-run-app
/kiro:spec-init gcp-cloud-run-hackathon

# Compliance
/kiro:spec-init threat-model-hackathon
/kiro:spec-init redaction-policy-hackathon
/kiro:spec-init data-lineage-hackathon

# Submission
/kiro:spec-init devpost-submission-package
```

**Time Estimate**: ~2-3 hours to create all specs with proper requirements/design/tasks

