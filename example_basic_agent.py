import asyncio
from auto_setup import AutoAgent


async def main():
    # Create agent with specific capabilities
    agent = AutoAgent("my_agent", ["python_coding", "gcp_optimization"])

    # Start the agent
    await agent.start()

    # Send a message
    await agent.send_message("broadcast", "Hello everyone!")

    # Request help
    await agent.request_help(["python_coding"], "I need help with Python")

    # Discover other agents
    await agent.discover_agents()

    # Stop the agent
    await agent.stop()


asyncio.run(main())
