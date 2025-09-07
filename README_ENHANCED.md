# 🔥 Beast Mode Agent Collaboration Network - Enhanced Edition

**A batteries-included agent collaboration system with discovery, trust scoring, and health monitoring.**

## 🚀 10-Second Quick Start

1. **Install Redis** (any one):

   ```bash
   # macOS
   brew install redis && redis-server

   # Ubuntu
   sudo apt-get install redis-server && sudo systemctl start redis

   # Docker
   docker run -d -p 6379:6379 redis:alpine
   ```

1. **Install dependencies**:

   ```bash
   make install
   ```

1. **Start the system**:

   ```bash
   # Terminal 1: Start listener
   make start

   # Terminal 2: Run enhanced demo
   make run-demo
   ```

## ✨ What's New in Enhanced Edition

### 🎯 **Discovery Registry Wiring**

- **Automatic agent registration** - AGENT_DISCOVERY messages now properly register agents
- **Real-time capability tracking** - See what agents can do as they join
- **Smart agent discovery** - Find agents by capabilities with trust-based ranking

### 📊 **Trust Scoring System**

- **Collaboration tracking** - Agents learn from successful/failed interactions
- **Dynamic trust updates** - Trust scores adjust based on help quality
- **Smart recommendations** - Get the best agents for specific tasks

### 🏥 **Health Monitoring**

- **Agent status tracking** - Monitor which agents are healthy/available
- **Capability verification** - Verify agents can actually do what they claim
- **Response time monitoring** - Track performance metrics
- **Health reports** - Get system-wide health summaries

### 🛠️ **Enhanced Tooling**

- **Makefile commands** - `make run`, `make test`, `make redis`
- **Requirements.txt** - Explicit dependency management
- **Auto-setup script** - One-command deployment
- **Better documentation** - Clear setup and usage instructions

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Agent A       │    │   Message Bus    │    │   Agent B       │
│                 │◄──►│   (Redis)        │◄──►│                 │
│ - Discovery     │    │                  │    │ - Discovery     │
│ - Trust Scoring │    │ - Pub/Sub        │    │ - Trust Scoring │
│ - Health Check  │    │ - Message Types  │    │ - Health Check  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Health Monitor  │
                    │                 │
                    │ - Status Check  │
                    │ - Trust Updates │
                    │ - Health Reports│
                    └─────────────────┘
```

## 📋 Available Commands

### **Quick Commands**

```bash
make help          # Show all available commands
make install       # Install Python dependencies
make redis         # Start Redis server
make start         # Start message listener
make run-demo      # Run enhanced demo agent
```

### **Development Commands**

```bash
make test          # Run all tests
make lint          # Run linting checks
make format        # Format code with Black
make clean         # Clean up temporary files
```

### **Custom Agent**

```bash
make run-agent AGENT_ID=my_agent CAPABILITIES="python_coding,gcp_optimization"
```

## 🔧 Configuration

### **Environment Variables**

```bash
export REDIS_URL="redis://localhost:6379"
export AGENT_ID="my_agent"
export CAPABILITIES="python_coding,gcp_optimization,data_analysis"
```

### **Agent Capabilities**

Available capabilities include:

- `python_coding` - Python development and debugging
- `gcp_optimization` - Google Cloud Platform optimization
- `data_analysis` - Data analysis and visualization
- `system_administration` - System admin tasks
- `security_analysis` - Security assessment
- `documentation` - Technical writing
- `testing` - Test development and execution

## 📊 Trust Scoring

The system automatically tracks and updates trust scores based on:

- **Help Response Quality** - How well agents respond to help requests
- **Task Completion Success** - Whether completed tasks are successful
- **Response Time** - How quickly agents respond
- **Capability Verification** - Whether agents can actually do what they claim

**Trust Score Formula:**

```
Trust Score = (Success Rate × Time Factor × Capability Factor)
```

## 🏥 Health Monitoring

### **Health Status Levels**

- **🟢 Healthy** - Agent responding normally
- **🟡 Degraded** - Agent responding slowly
- **🔴 Unhealthy** - Agent not responding
- **⚪ Unknown** - No recent activity

### **Health Metrics**

- **Response Time** - Average response time in milliseconds
- **Uptime** - How long agent has been active
- **Success Rate** - Percentage of successful interactions
- **Capability Verification** - Which capabilities are verified

## 🤝 Collaboration Examples

### **Basic Agent Communication**

```python
from beast_mode.bus_client import BeastModeBusClient

# Create agent
agent = BeastModeBusClient(
    agent_id="my_agent",
    capabilities=["python_coding", "gcp_optimization"]
)

# Send message
await agent.send_message(
    target="other_agent",
    message_type="HELP_WANTED",
    payload={"description": "Need help with GCP cost optimization"}
)
```

### **Request Help with Trust-Based Selection**

```python
from beast_mode.help_system import HelpSystemManager

# Request help (automatically selects best agent based on trust)
help_agents = await help_manager.request_help(
    required_capabilities=["gcp_optimization"],
    description="Optimize GCP costs"
)

# Get trust scores
trust_scores = await help_manager.get_trust_scores()
print(f"Agent trust scores: {trust_scores}")
```

### **Health Monitoring**

```python
from beast_mode.health_monitor import HealthMonitor

# Start health monitoring
health_monitor = HealthMonitor(redis_manager, agent_registry)
await health_monitor.start_monitoring(interval_seconds=30)

# Get health summary
summary = await health_monitor.get_health_summary()
print(f"System health: {summary['health_percentage']:.1f}%")
```

## 🔄 Message Types

### **Discovery Messages**

- `AGENT_DISCOVERY` - Announce agent presence and capabilities
- `AGENT_RESPONSE` - Respond to discovery announcements

### **Help Messages**

- `HELP_WANTED` - Request assistance with specific capabilities
- `HELP_RESPONSE` - Offer to help with capabilities
- `HELP_COMPLETED` - Mark help task as completed

### **Health Messages**

- `HEALTH_CHECK` - Ping agent for health status
- `HEALTH_RESPONSE` - Respond to health check
- `HEALTH_REPORT` - Send health status report

### **System Messages**

- `SIMPLE_MESSAGE` - Basic text communication
- `TECHNICAL_EXCHANGE` - Technical setup information
- `SPORE_DELIVERY` - Share implementation packages

## 🧪 Testing

### **Run All Tests**

```bash
make test
```

### **Run Specific Tests**

```bash
# Test discovery system
uv run python -m pytest tests/test_agent_discovery_communication.py -v

# Test trust scoring
uv run python -m pytest tests/test_trust_scoring.py -v

# Test health monitoring
uv run python -m pytest tests/test_health_monitoring.py -v
```

## 🚀 Deployment

### **Docker Deployment**

```bash
# Build and run with Docker Compose
docker-compose up -d
```

### **Production Setup**

```bash
# Install system dependencies
make install

# Start Redis as service
make redis

# Start agent as service
make start
```

## 🔧 Troubleshooting

### **Common Issues**

**Redis Connection Failed**

```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# Start Redis if not running
make redis
```

**Agent Not Discovering Others**

```bash
# Check if agents are on same channel
# All agents should use: beast_mode_network

# Verify message format
# Messages should be valid JSON with required fields
```

**Trust Scores Not Updating**

```bash
# Check if help completion is being called
# Call: await help_manager.mark_help_completed(request_id, success=True)
```

## 📈 Performance

### **Benchmarks**

- **Message Latency**: < 10ms (local Redis)
- **Agent Discovery**: < 1 second
- **Trust Score Updates**: < 100ms
- **Health Checks**: < 50ms

### **Scaling**

- **Concurrent Agents**: 100+ (tested)
- **Message Throughput**: 1000+ messages/second
- **Memory Usage**: < 50MB per agent

## 🤝 Contributing

1. **Fork the repository**
1. **Create feature branch**: `git checkout -b feature/amazing-feature`
1. **Make changes** and add tests
1. **Run tests**: `make test`
1. **Commit changes**: `git commit -m 'Add amazing feature'`
1. **Push to branch**: `git push origin feature/amazing-feature`
1. **Open Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Redis** - For the reliable message bus
- **asyncio** - For async Python support
- **The diversity hypothesis** - For proving that multiple approaches make systems better

______________________________________________________________________

**🔥 Beast Mode Activated! 🔥**

*The future of agent collaboration starts here!*
