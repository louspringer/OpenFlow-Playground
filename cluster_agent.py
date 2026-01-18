#!/usr/bin/env python3
"""
OpenFlow Playground Agent - Connecting to Beast Mode Cluster
"""
import asyncio
from beast_agent import BaseAgent
from beast_agent.decorators import capability


class OpenFlowAgent(BaseAgent):
    """Agent for OpenFlow Playground - testing multi-agent coordination"""
    
    def __init__(self):
        # Auto-configures from REDIS_HOST, REDIS_PORT, REDIS_PASSWORD env vars
        super().__init__(
            agent_id="openflow-playground-agent",
            capabilities=["hackathon-coordination", "spec-validation", "code-generation"],
            mailbox_url=None  # Auto-configures from env vars
        )
        
        self._logger.info("OpenFlow Agent initialized (auto-configured from env vars)")
    
    async def on_startup(self) -> None:
        """Called after mailbox connection is established"""
        self._logger.info("🚀 OpenFlow Agent connected to cluster!")
        self._logger.info(f"Agent ID: {self.agent_id}")
        self._logger.info(f"Capabilities: {self.capabilities}")
        
        # Register message handlers
        self.register_handler("HELP_REQUEST", self.handle_help_request)
        self.register_handler("AGENT_DISCOVERY", self.handle_discovery)
        self.register_handler("TASK_ASSIGNMENT", self.handle_task)
        
        self._logger.info("✅ Handlers registered, agent ready!")
    
    @capability("hackathon-coordination")
    async def handle_help_request(self, content: dict) -> None:
        """Handle help requests from other agents"""
        sender = content.get("sender", "unknown")
        request = content.get("request", "")
        
        self._logger.info(f"📨 Help request from {sender}: {request}")
        
        # Send response
        await self.send_message(
            target=sender,
            message_type="HELP_RESPONSE",
            content={
                "agent_id": self.agent_id,
                "response": f"OpenFlow agent here! I can help with: {', '.join(self.capabilities)}",
                "available": True
            }
        )
    
    async def handle_discovery(self, content: dict) -> None:
        """Handle discovery messages from other agents"""
        agent_id = content.get("agent_id", "unknown")
        capabilities = content.get("capabilities", [])
        
        self._logger.info(f"👋 Discovered agent: {agent_id}")
        self._logger.info(f"   Capabilities: {capabilities}")
    
    async def handle_task(self, content: dict) -> None:
        """Handle task assignments"""
        task = content.get("task", "")
        sender = content.get("sender", "unknown")
        
        self._logger.info(f"📋 Task from {sender}: {task}")
        
        # Acknowledge task
        await self.send_message(
            target=sender,
            message_type="TASK_RESPONSE",
            content={
                "agent_id": self.agent_id,
                "status": "acknowledged",
                "task": task
            }
        )
    
    async def on_shutdown(self) -> None:
        """Called before mailbox disconnection"""
        self._logger.info("👋 OpenFlow Agent shutting down...")


async def main():
    """Run the agent"""
    agent = OpenFlowAgent()
    
    # Start agent
    await agent.startup()
    
    print("\n" + "="*60)
    print("🎯 OpenFlow Agent ONLINE")
    print("="*60)
    print(f"Agent ID: {agent.agent_id}")
    print(f"Capabilities: {', '.join(agent.capabilities)}")
    print("="*60)
    print("\nListening for messages... (Ctrl+C to stop)")
    print("="*60 + "\n")
    
    try:
        # Keep agent running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
    finally:
        await agent.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

