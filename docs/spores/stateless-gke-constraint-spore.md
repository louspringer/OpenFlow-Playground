# 🍄 Stateless GKE Constraint Spore

**Date**: September 4, 2025  
**Purpose**: Define stateless constraints for GKE usage and common interface  
**Goal**: Enable dev/prod choice between GKE and Cloud Run

---

## 🎯 **Stateless GKE Usage Constraints**

### **Core Principle**
**GKE must be used in a stateless manner** to enable seamless migration between GKE and Cloud Run implementations.

### **Stateless Requirements**

#### **1. No Persistent Storage**
```yaml
# ❌ FORBIDDEN - Persistent volumes
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: kiro-data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi

# ✅ ALLOWED - ConfigMaps and Secrets only
apiVersion: v1
kind: ConfigMap
metadata:
  name: kiro-config
data:
  config.yaml: |
    api_endpoint: "https://api.example.com"
    timeout: 30
```

#### **2. No StatefulSets**
```yaml
# ❌ FORBIDDEN - StatefulSets
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: kiro-stateful-app
spec:
  serviceName: kiro-service
  replicas: 3
  selector:
    matchLabels:
      app: kiro-app

# ✅ ALLOWED - Deployments only
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kiro-stateless-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kiro-app
```

#### **3. No Node Affinity**
```yaml
# ❌ FORBIDDEN - Node affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/hostname
            operator: In
            values:
            - specific-node

# ✅ ALLOWED - Generic node selection
spec:
  nodeSelector:
    cloud.google.com/gke-preemptible: "true"
```

#### **4. No Host Path Volumes**
```yaml
# ❌ FORBIDDEN - Host path volumes
spec:
  containers:
  - name: kiro-container
    volumeMounts:
    - name: host-data
      mountPath: /data
  volumes:
  - name: host-data
    hostPath:
      path: /var/data

# ✅ ALLOWED - EmptyDir or ConfigMap volumes
spec:
  containers:
  - name: kiro-container
    volumeMounts:
    - name: config-volume
      mountPath: /config
  volumes:
  - name: config-volume
    configMap:
      name: kiro-config
```

---

## 🔧 **Common Interface Design**

### **1. Service Interface**
```python
# src/kiro_agents/common/interface.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class KiroRequest:
    """Common request structure"""
    data: Dict[str, Any]
    headers: Dict[str, str]
    method: str
    path: str

@dataclass
class KiroResponse:
    """Common response structure"""
    status_code: int
    data: Dict[str, Any]
    headers: Dict[str, str]

class KiroAgentInterface(ABC):
    """Common interface for Kiro agents"""
    
    @abstractmethod
    def process_request(self, request: KiroRequest) -> KiroResponse:
        """Process a Kiro agent request"""
        pass
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Health check endpoint"""
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent metrics"""
        pass
```

### **2. GKE Implementation**
```python
# src/kiro_agents/gke/agent.py
from flask import Flask, request, jsonify
from ..common.interface import KiroAgentInterface, KiroRequest, KiroResponse
import logging

class GKEKiroAgent(KiroAgentInterface):
    """GKE implementation of Kiro agent"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.logger = logging.getLogger(__name__)
    
    def setup_routes(self):
        """Setup Flask routes"""
        self.app.route('/analyze', methods=['POST'])(self.analyze_endpoint)
        self.app.route('/health', methods=['GET'])(self.health_endpoint)
        self.app.route('/metrics', methods=['GET'])(self.metrics_endpoint)
    
    def analyze_endpoint(self):
        """GKE analyze endpoint"""
        kiro_request = KiroRequest(
            data=request.get_json() or {},
            headers=dict(request.headers),
            method=request.method,
            path=request.path
        )
        
        response = self.process_request(kiro_request)
        return jsonify(response.data), response.status_code, response.headers
    
    def process_request(self, request: KiroRequest) -> KiroResponse:
        """Process Kiro agent request"""
        try:
            # Business logic here
            result = self._analyze_data(request.data)
            
            return KiroResponse(
                status_code=200,
                data={'status': 'success', 'result': result},
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return KiroResponse(
                status_code=500,
                data={'status': 'error', 'message': str(e)},
                headers={'Content-Type': 'application/json'}
            )
    
    def health_check(self) -> Dict[str, Any]:
        """Health check for GKE"""
        return {
            'status': 'healthy',
            'platform': 'gke',
            'timestamp': self._get_timestamp()
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get GKE-specific metrics"""
        return {
            'platform': 'gke',
            'pod_name': self._get_pod_name(),
            'node_name': self._get_node_name(),
            'timestamp': self._get_timestamp()
        }
    
    def _analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Core analysis logic"""
        # Implement your Kiro agent logic here
        return {'analysis': 'completed', 'data': data}
    
    def _get_pod_name(self) -> str:
        """Get pod name from environment"""
        import os
        return os.environ.get('HOSTNAME', 'unknown')
    
    def _get_node_name(self) -> str:
        """Get node name from environment"""
        import os
        return os.environ.get('NODE_NAME', 'unknown')
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()
    
    def run(self, host='0.0.0.0', port=8080):
        """Run the GKE agent"""
        self.app.run(host=host, port=port, debug=False)

# GKE-specific deployment
if __name__ == '__main__':
    agent = GKEKiroAgent()
    agent.run()
```

### **3. Cloud Run Implementation**
```python
# src/kiro_agents/cloudrun/agent.py
from flask import Flask, request, jsonify
from ..common.interface import KiroAgentInterface, KiroRequest, KiroResponse
import logging

class CloudRunKiroAgent(KiroAgentInterface):
    """Cloud Run implementation of Kiro agent"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.logger = logging.getLogger(__name__)
    
    def setup_routes(self):
        """Setup Flask routes"""
        self.app.route('/analyze', methods=['POST'])(self.analyze_endpoint)
        self.app.route('/health', methods=['GET'])(self.health_endpoint)
        self.app.route('/metrics', methods=['GET'])(self.metrics_endpoint)
    
    def analyze_endpoint(self):
        """Cloud Run analyze endpoint"""
        kiro_request = KiroRequest(
            data=request.get_json() or {},
            headers=dict(request.headers),
            method=request.method,
            path=request.path
        )
        
        response = self.process_request(kiro_request)
        return jsonify(response.data), response.status_code, response.headers
    
    def process_request(self, request: KiroRequest) -> KiroResponse:
        """Process Kiro agent request"""
        try:
            # Same business logic as GKE
            result = self._analyze_data(request.data)
            
            return KiroResponse(
                status_code=200,
                data={'status': 'success', 'result': result},
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return KiroResponse(
                status_code=500,
                data={'status': 'error', 'message': str(e)},
                headers={'Content-Type': 'application/json'}
            )
    
    def health_check(self) -> Dict[str, Any]:
        """Health check for Cloud Run"""
        return {
            'status': 'healthy',
            'platform': 'cloudrun',
            'timestamp': self._get_timestamp()
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get Cloud Run-specific metrics"""
        return {
            'platform': 'cloudrun',
            'instance_id': self._get_instance_id(),
            'timestamp': self._get_timestamp()
        }
    
    def _analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Core analysis logic (same as GKE)"""
        # Implement your Kiro agent logic here
        return {'analysis': 'completed', 'data': data}
    
    def _get_instance_id(self) -> str:
        """Get Cloud Run instance ID"""
        import os
        return os.environ.get('K_SERVICE', 'unknown')
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()
    
    def run(self, host='0.0.0.0', port=8080):
        """Run the Cloud Run agent"""
        self.app.run(host=host, port=port, debug=False)

# Cloud Run-specific deployment
if __name__ == '__main__':
    agent = CloudRunKiroAgent()
    agent.run()
```

---

## 🚀 **Deployment Configurations**

### **1. GKE Deployment (Stateless)**
```yaml
# k8s/kiro-agents-gke.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kiro-agent
  namespace: kiro-agents
  labels:
    app: kiro-agent
    platform: gke
spec:
  replicas: 2
  selector:
    matchLabels:
      app: kiro-agent
  template:
    metadata:
      labels:
        app: kiro-agent
        platform: gke
    spec:
      nodeSelector:
        cloud.google.com/gke-preemptible: "true"
      containers:
      - name: kiro-agent
        image: gcr.io/aardvark-linkedin-grepper/kiro-agent:gke
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
        - name: PLATFORM
          value: "gke"
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        # No persistent volumes - stateless only
        volumeMounts:
        - name: config-volume
          mountPath: /config
      volumes:
      - name: config-volume
        configMap:
          name: kiro-config
      # No persistent volumes allowed
      restartPolicy: Always

---
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

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: kiro-config
  namespace: kiro-agents
data:
  config.yaml: |
    platform: gke
    timeout: 30
    max_requests: 1000
```

### **2. Cloud Run Deployment**
```yaml
# cloudrun/kiro-agents-cloudrun.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: kiro-agent
  namespace: default
  labels:
    app: kiro-agent
    platform: cloudrun
spec:
  template:
    metadata:
      labels:
        app: kiro-agent
        platform: cloudrun
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        autoscaling.knative.dev/minScale: "0"
        run.googleapis.com/cpu-throttling: "true"
    spec:
      containerConcurrency: 100
      timeoutSeconds: 300
      containers:
      - image: gcr.io/aardvark-linkedin-grepper/kiro-agent:cloudrun
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: "512Mi"
            cpu: "1"
        env:
        - name: PLATFORM
          value: "cloudrun"
        - name: K_SERVICE
          value: "kiro-agent"
        # No persistent volumes - stateless only
        volumeMounts:
        - name: config-volume
          mountPath: /config
      volumes:
      - name: config-volume
        configMap:
          name: kiro-config
```

---

## 🔄 **Dev/Prod Decision Framework**

### **Development Environment**
```bash
# Use Cloud Run for development (cheaper)
gcloud run deploy kiro-agent-dev \
  --image gcr.io/aardvark-linkedin-grepper/kiro-agent:dev \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=development
```

### **Production Environment**
```bash
# Use GKE for production (more control)
kubectl apply -f k8s/kiro-agents-gke.yaml
```

### **Environment Selection Script**
```python
# scripts/deploy_kiro_agent.py
import os
import subprocess
import sys

def deploy_kiro_agent(environment: str, platform: str):
    """Deploy Kiro agent to specified environment and platform"""
    
    if environment == "development":
        if platform == "cloudrun":
            deploy_cloudrun_dev()
        elif platform == "gke":
            deploy_gke_dev()
        else:
            raise ValueError(f"Unknown platform: {platform}")
    
    elif environment == "production":
        if platform == "cloudrun":
            deploy_cloudrun_prod()
        elif platform == "gke":
            deploy_gke_prod()
        else:
            raise ValueError(f"Unknown platform: {platform}")
    
    else:
        raise ValueError(f"Unknown environment: {environment}")

def deploy_cloudrun_dev():
    """Deploy to Cloud Run development"""
    print("🚀 Deploying to Cloud Run (Development)")
    subprocess.run([
        "gcloud", "run", "deploy", "kiro-agent-dev",
        "--image", "gcr.io/aardvark-linkedin-grepper/kiro-agent:dev",
        "--platform", "managed",
        "--region", "us-central1",
        "--allow-unauthenticated",
        "--set-env-vars", "ENVIRONMENT=development,PLATFORM=cloudrun"
    ])

def deploy_gke_dev():
    """Deploy to GKE development"""
    print("🚀 Deploying to GKE (Development)")
    subprocess.run([
        "kubectl", "apply", "-f", "k8s/kiro-agents-gke-dev.yaml"
    ])

def deploy_cloudrun_prod():
    """Deploy to Cloud Run production"""
    print("🚀 Deploying to Cloud Run (Production)")
    subprocess.run([
        "gcloud", "run", "deploy", "kiro-agent-prod",
        "--image", "gcr.io/aardvark-linkedin-grepper/kiro-agent:prod",
        "--platform", "managed",
        "--region", "us-central1",
        "--allow-unauthenticated",
        "--set-env-vars", "ENVIRONMENT=production,PLATFORM=cloudrun"
    ])

def deploy_gke_prod():
    """Deploy to GKE production"""
    print("🚀 Deploying to GKE (Production)")
    subprocess.run([
        "kubectl", "apply", "-f", "k8s/kiro-agents-gke-prod.yaml"
    ])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python deploy_kiro_agent.py <environment> <platform>")
        print("Environments: development, production")
        print("Platforms: cloudrun, gke")
        sys.exit(1)
    
    environment = sys.argv[1]
    platform = sys.argv[2]
    
    deploy_kiro_agent(environment, platform)
```

---

## 📋 **Usage Examples**

### **Deploy to Cloud Run (Development)**
```bash
python scripts/deploy_kiro_agent.py development cloudrun
```

### **Deploy to GKE (Production)**
```bash
python scripts/deploy_kiro_agent.py production gke
```

### **Switch Between Platforms**
```bash
# Switch from GKE to Cloud Run
kubectl delete -f k8s/kiro-agents-gke.yaml
python scripts/deploy_kiro_agent.py production cloudrun

# Switch from Cloud Run to GKE
gcloud run services delete kiro-agent-prod --region=us-central1
python scripts/deploy_kiro_agent.py production gke
```

---

## 🎯 **Benefits of This Approach**

### **1. Flexibility**
- ✅ **Dev/Prod choice** between platforms
- ✅ **Cost optimization** (Cloud Run for dev, GKE for prod)
- ✅ **Easy migration** between platforms

### **2. Consistency**
- ✅ **Common interface** ensures compatibility
- ✅ **Same business logic** across platforms
- ✅ **Unified testing** and monitoring

### **3. Stateless Design**
- ✅ **No persistent storage** dependencies
- ✅ **Horizontal scaling** capability
- ✅ **Platform agnostic** deployment

---

## 🚨 **Enforcement Rules**

### **GKE Stateless Constraints**
1. **No PersistentVolumeClaims**
2. **No StatefulSets**
3. **No Node Affinity**
4. **No Host Path Volumes**
5. **Deployments only**
6. **ConfigMaps and Secrets only**

### **Validation Script**
```bash
# scripts/validate_stateless_gke.sh
#!/bin/bash

echo "🔍 Validating GKE stateless constraints..."

# Check for forbidden resources
forbidden_resources=("PersistentVolumeClaim" "StatefulSet" "DaemonSet")

for resource in "${forbidden_resources[@]}"; do
    if kubectl get "$resource" -n kiro-agents 2>/dev/null; then
        echo "❌ FORBIDDEN: $resource found in kiro-agents namespace"
        exit 1
    fi
done

echo "✅ GKE stateless constraints validated"
```

---

**Status**: Stateless constraints defined  
**Priority**: High (Architecture compliance)  
**Owner**: Kiro Agents Team  
**Review Date**: September 5, 2025
