import asyncio
from auto_setup import AutoAgent
from message_models import BeastModeMessage, MessageType


class CustomAgent(AutoAgent):
    def __init__(self, agent_id: str, capabilities: list):
        super().__init__(agent_id, capabilities)
        # Add custom message handlers
        self.bus_client.register_message_handler(MessageType.PROMPT_REQUEST, self._handle_prompt)

    async def _handle_prompt(self, message: BeastModeMessage):
        prompt_type = message.payload.get("prompt_type", "general")
        print(f"🤖 Processing {prompt_type} prompt from {message.source}")

        # Process the prompt based on type
        if prompt_type == "cost_analysis":
            response = "Based on our analysis, GCP costs are optimized at $6.50/month"
        else:
            response = f"I received your {prompt_type} prompt and I'm processing it"

        # Send response
        await self.send_message(message.source, response)


async def main():
    agent = CustomAgent("cost_optimizer", ["gcp_optimization", "cost_analysis"])
    await agent.start()

    # Your custom agent is now ready!
    await asyncio.sleep(10)  # Keep running

    await agent.stop()


asyncio.run(main())
