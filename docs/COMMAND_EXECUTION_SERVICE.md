# Command Execution Service

## 🚀 **Fire-and-Forget Command Execution with GCP Pub/Sub**

A scalable, secure command execution service built on Google Cloud Platform using Pub/Sub queues for asynchronous processing.

## 🎯 **Architecture Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTTP Client   │───▶│  Submit Command │───▶│  Input Queue    │
│                 │    │   (Cloud Func)  │    │   (Pub/Sub)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTTP Client   │◀───│  Get Status     │◀───│  Output Queue   │
│                 │    │   (Cloud Func)  │    │   (Pub/Sub)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       ▲
                                                       │
                                              ┌─────────────────┐
                                              │ Command Executor │
                                              │  (Cloud Func)   │
                                              └─────────────────┘
```

## 🔧 **Service Components**

### **1. Input Queue (Pub/Sub Topic)**
- **Topic**: `command-execution-input`
- **Purpose**: Receives commands for execution
- **Message Format**:
```json
{
  "job_id": "uuid",
  "command": "ls -la",
  "cwd": "/tmp",
  "user_id": "user-123"
}
```

### **2. Output Queue (Pub/Sub Topic)**
- **Topic**: `command-execution-output`
- **Purpose**: Publishes execution results
- **Message Format**:
```json
{
  "job_id": "uuid",
  "status": "completed|failed|executing",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "return_code": 0,
    "stdout": "output",
    "stderr": "errors",
    "success": true
  }
}
```

### **3. Cloud Functions**

#### **Submit Command Function**
- **Trigger**: HTTP
- **Purpose**: Submit commands for execution
- **Endpoint**: `POST /submit-command`

#### **Command Executor Function**
- **Trigger**: Pub/Sub (input queue)
- **Purpose**: Execute commands and publish results
- **Timeout**: 9 minutes (540s)

#### **Get Status Function**
- **Trigger**: HTTP
- **Purpose**: Check command execution status
- **Endpoint**: `GET /get-command-status?job_id=xxx`

#### **List Commands Function**
- **Trigger**: HTTP
- **Purpose**: List user's command history
- **Endpoint**: `GET /list-user-commands`

## 🚀 **Quick Start**

### **1. Deploy the Service**
```bash
# Make deployment script executable
chmod +x scripts/deploy-command-execution-service.sh

# Deploy to GCP
./scripts/deploy-command-execution-service.sh
```

### **2. Use the Python Client**
```python
from src.command_execution_service.client import CommandExecutionClient

# Initialize client
client = CommandExecutionClient(
    base_url="https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net"
)

# Fire and forget
result = client.submit_command("ls -la", "/tmp")
print(f"Job ID: {result['job_id']}")

# Wait for completion
final_result = client.execute_and_wait("echo 'Hello!'", timeout=60)
print(f"Output: {final_result['result']['stdout']}")
```

### **3. Direct HTTP API Usage**
```bash
# Submit a command
curl -X POST https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/submit-command \
  -H 'Content-Type: application/json' \
  -d '{"command": "ls -la", "cwd": "/tmp"}'

# Check status
curl "https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/get-command-status?job_id=YOUR_JOB_ID"

# List commands
curl https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/list-user-commands
```

## 📋 **API Reference**

### **Submit Command**
```http
POST /submit-command
Content-Type: application/json

{
  "command": "ls -la",
  "cwd": "/tmp"
}
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "submitted",
  "message": "Command submitted for execution"
}
```

### **Get Command Status**
```http
GET /get-command-status?job_id=550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "command": "ls -la",
  "created_at": "2024-01-01T00:00:00Z",
  "completed_at": "2024-01-01T00:00:05Z",
  "result": {
    "return_code": 0,
    "stdout": "total 8\ndrwxrwxrwt 2 root root 4096 Jan 1 00:00 .\n",
    "stderr": "",
    "success": true,
    "command": "ls -la",
    "cwd": "/tmp"
  }
}
```

### **List User Commands**
```http
GET /list-user-commands
```

**Response:**
```json
{
  "commands": [
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "command": "ls -la",
      "created_at": "2024-01-01T00:00:00Z",
      "completed_at": "2024-01-01T00:00:05Z"
    }
  ],
  "count": 1
}
```

## 🔒 **Security Features**

### **Command Execution Safety**
- **Timeout**: 5-minute maximum execution time
- **Working Directory**: Configurable working directory
- **Error Handling**: Comprehensive error capture
- **Resource Limits**: Memory and CPU limits enforced

### **Authentication**
- **Bearer Token**: Optional API key authentication
- **User Isolation**: Commands isolated by user ID
- **Access Control**: Users can only see their own commands

### **Data Security**
- **No Credential Storage**: Commands executed in isolated environment
- **Audit Logging**: All executions logged in Firestore
- **Secure Communication**: HTTPS-only endpoints

## 📊 **Monitoring & Logging**

### **Firestore Collections**
- **`command_executions`**: Job metadata and results
- **Fields**: job_id, user_id, command, cwd, status, created_at, completed_at, result

### **Pub/Sub Topics**
- **`command-execution-input`**: Command submission queue
- **`command-execution-output`**: Result publication queue

### **Cloud Function Logs**
- **Submit Command**: HTTP request/response logging
- **Command Executor**: Execution progress and error logging
- **Get Status**: Query logging
- **List Commands**: User command history logging

## 🧪 **Testing**

### **Run Tests**
```bash
# Run unit tests
python -m pytest tests/test_command_execution_service.py -v

# Run with coverage
python -m pytest tests/test_command_execution_service.py --cov=src.command_execution_service
```

### **Test Client**
```bash
# Test the Python client
python src/command_execution_service/client.py
```

## 🔧 **Configuration**

### **Environment Variables**
```bash
# GCP Configuration
GCP_PROJECT_ID=aardvark-linkedin-grepper
GCP_REGION=us-central1

# Service Configuration
COMMAND_TIMEOUT=300  # 5 minutes
MAX_MEMORY=512MB
```

### **Pub/Sub Topics**
```bash
# Create topics manually (if needed)
gcloud pubsub topics create command-execution-input --project=aardvark-linkedin-grepper
gcloud pubsub topics create command-execution-output --project=aardvark-linkedin-grepper
```

## 🚀 **Usage Patterns**

### **1. Fire and Forget**
```python
# Submit command and don't wait
result = client.submit_command("long-running-process", "/tmp")
print(f"Job submitted: {result['job_id']}")
# Continue with other work...
```

### **2. Wait for Completion**
```python
# Submit and wait for result
result = client.execute_and_wait("echo 'Hello World'", timeout=60)
if result['result']['success']:
    print(f"Output: {result['result']['stdout']}")
else:
    print(f"Error: {result['result']['stderr']}")
```

### **3. Batch Processing**
```python
# Submit multiple commands
commands = ["ls -la", "pwd", "whoami"]
job_ids = []

for cmd in commands:
    result = client.submit_command(cmd)
    job_ids.append(result['job_id'])

# Check all results later
for job_id in job_ids:
    status = client.get_status(job_id)
    print(f"{job_id}: {status['status']}")
```

### **4. Real-time Monitoring**
```python
# Monitor command progress
job_id = client.submit_command("sleep 30")['job_id']

while True:
    status = client.get_status(job_id)
    print(f"Status: {status['status']}")
    
    if status['status'] in ['completed', 'failed']:
        break
    
    time.sleep(5)
```

## 🔍 **Troubleshooting**

### **Common Issues**

#### **Command Timeout**
```bash
# Check if command is too long
# Default timeout is 5 minutes
# Increase timeout in client.execute_and_wait(timeout=600)
```

#### **Permission Denied**
```bash
# Commands run in isolated environment
# Use absolute paths for files
# Check working directory with 'pwd'
```

#### **Pub/Sub Connection Issues**
```bash
# Verify GCP credentials
gcloud auth application-default login

# Check topic permissions
gcloud pubsub topics list --project=aardvark-linkedin-grepper
```

### **Debug Commands**
```bash
# Test basic command
curl -X POST https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/submit-command \
  -H 'Content-Type: application/json' \
  -d '{"command": "echo \"Hello World\""}'

# Check service health
curl https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/list-user-commands
```

## 📈 **Performance & Scaling**

### **Concurrent Execution**
- **Pub/Sub**: Handles thousands of concurrent commands
- **Cloud Functions**: Auto-scales based on queue depth
- **Firestore**: Handles high read/write loads

### **Resource Limits**
- **Memory**: 512MB per execution
- **Timeout**: 9 minutes maximum
- **Concurrent**: Limited by Cloud Function quotas

### **Cost Optimization**
- **Cold Starts**: Minimized with keep-warm patterns
- **Storage**: Firestore costs for job history
- **Network**: Pub/Sub message costs

## 🔮 **Future Enhancements**

### **Planned Features**
- **Command Templates**: Predefined command patterns
- **Scheduled Execution**: Time-based command scheduling
- **Command Chaining**: Sequential command execution
- **File Upload/Download**: Support for file operations
- **WebSocket Streaming**: Real-time output streaming

### **Advanced Security**
- **Command Whitelisting**: Allow only specific commands
- **Resource Quotas**: Per-user execution limits
- **Network Isolation**: VPC integration
- **Audit Trail**: Enhanced logging and monitoring

---

**🎉 The Command Execution Service provides a robust, scalable solution for fire-and-forget command execution using GCP's powerful Pub/Sub infrastructure!** 