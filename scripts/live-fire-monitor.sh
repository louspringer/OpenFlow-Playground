#!/bin/bash
# 🎯 LIVE FIRE MONITOR - Real-time Kiro Agent Activity Dashboard

set -e

echo "🎯 LIVE FIRE EXERCISE - Kiro Agent Real-Time Monitor"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to get current timestamp
timestamp() {
    date '+%H:%M:%S'
}

# Function to display status
show_status() {
    echo -e "${CYAN}[$(timestamp)]${NC} Fetching live status..."
    
    # Get status
    STATUS=$(curl -s http://localhost:8080/status 2>/dev/null || echo '{"status":"error"}')
    
    if [[ "$STATUS" == *"error"* ]]; then
        echo -e "${RED}❌ Agent not responding${NC}"
        return 1
    fi
    
    # Parse status
    REGISTERED_AGENTS=$(echo "$STATUS" | jq -r '.coordinator.registered_agents // 0')
    ACTIVE_TASKS=$(echo "$STATUS" | jq -r '.coordinator.active_tasks // 0')
    COORDINATION_CYCLES=$(echo "$STATUS" | jq -r '.coordinator.stats.coordination_cycles // 0')
    TASKS_COMPLETED=$(echo "$STATUS" | jq -r '.coordinator.stats.tasks_completed // 0')
    TASKS_FAILED=$(echo "$STATUS" | jq -r '.coordinator.stats.tasks_failed // 0')
    VALIDATION_REQUESTS=$(echo "$STATUS" | jq -r '.coordinator.stats.validation_requests // 0')
    
    echo -e "${GREEN}✅ Agent Status: RUNNING${NC}"
    echo -e "${BLUE}📊 Live Metrics:${NC}"
    echo -e "   🤖 Registered Agents: ${YELLOW}$REGISTERED_AGENTS${NC}"
    echo -e "   📋 Active Tasks: ${YELLOW}$ACTIVE_TASKS${NC}"
    echo -e "   🔄 Coordination Cycles: ${YELLOW}$COORDINATION_CYCLES${NC}"
    echo -e "   ✅ Tasks Completed: ${GREEN}$TASKS_COMPLETED${NC}"
    echo -e "   ❌ Tasks Failed: ${RED}$TASKS_FAILED${NC}"
    echo -e "   🔍 Validation Requests: ${PURPLE}$VALIDATION_REQUESTS${NC}"
    echo ""
}

# Function to show active tasks
show_tasks() {
    echo -e "${CYAN}[$(timestamp)]${NC} Active Tasks:"
    
    TASKS=$(curl -s http://localhost:8080/tasks 2>/dev/null || echo '{"tasks":[]}')
    
    if [[ "$TASKS" == *"error"* ]]; then
        echo -e "${RED}❌ Could not fetch tasks${NC}"
        return 1
    fi
    
    TASK_COUNT=$(echo "$TASKS" | jq -r '.tasks | length')
    
    if [ "$TASK_COUNT" -eq 0 ]; then
        echo -e "${YELLOW}📭 No active tasks${NC}"
    else
        echo "$TASKS" | jq -r '.tasks[] | "   🎯 \(.task_id): \(.type) - \(.description)"' | head -5
        if [ "$TASK_COUNT" -gt 5 ]; then
            echo -e "   ... and $((TASK_COUNT - 5)) more tasks"
        fi
    fi
    echo ""
}

# Function to show metrics
show_metrics() {
    echo -e "${CYAN}[$(timestamp)]${NC} Prometheus Metrics:"
    
    METRICS=$(curl -s http://localhost:8080/metrics 2>/dev/null || echo "")
    
    if [[ -z "$METRICS" ]]; then
        echo -e "${RED}❌ Could not fetch metrics${NC}"
        return 1
    fi
    
    echo "$METRICS" | grep -E "(kiro_agent_|# HELP)" | while read line; do
        if [[ "$line" == "# HELP"* ]]; then
            echo -e "   ${BLUE}$line${NC}"
        else
            echo -e "   ${GREEN}$line${NC}"
        fi
    done
    echo ""
}

# Function to show cluster info
show_cluster() {
    echo -e "${CYAN}[$(timestamp)]${NC} GKE Cluster Status:"
    
    # Get pod status
    PODS=$(kubectl get pods -n kiro-agents --no-headers 2>/dev/null | wc -l || echo "0")
    RUNNING_PODS=$(kubectl get pods -n kiro-agents --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l || echo "0")
    
    echo -e "   🖥️  Total Pods: ${YELLOW}$PODS${NC}"
    echo -e "   ✅ Running Pods: ${GREEN}$RUNNING_PODS${NC}"
    
    # Get node info
    NODES=$(kubectl get nodes --no-headers 2>/dev/null | wc -l || echo "0")
    echo -e "   🏗️  Cluster Nodes: ${YELLOW}$NODES${NC}"
    echo ""
}

# Main monitoring loop
echo -e "${GREEN}🚀 Starting Live Fire Monitor...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

while true; do
    clear
    echo -e "${PURPLE}🎯 LIVE FIRE EXERCISE - Kiro Agent Real-Time Monitor${NC}"
    echo -e "${PURPLE}==================================================${NC}"
    echo ""
    
    show_status
    show_tasks
    show_metrics
    show_cluster
    
    echo -e "${CYAN}⏰ Next update in 5 seconds...${NC}"
    sleep 5
done
