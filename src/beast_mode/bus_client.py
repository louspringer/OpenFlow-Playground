"""
Basic Bus Client Functionality for Beast Mode Agent Collaboration Network

Task 3: Build basic bus client functionality
- Implement BeastModeBusClient class with connection management
- Add message sending capabilities with proper formatting
- Create message receiving and parsing logic
- Implement graceful error handling for connection failures
- Write integration tests for basic send/receive operations
- Requirements: 1.1, 1.3
"""

import asyncio
import logging
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime

from .redis_foundation import RedisConnectionManager
from .message_models_dataclass import BeastModeMessage, MessageType, AgentCapabilities, MessageSerializer


class BeastModeBusClient:
    """
    Core bus client for Beast Mode Agent Collaboration Network.

    Handles connection management, message sending/receiving, and provides
    the primary interface for agent communication.
    """

    def __init__(self, redis_url: str = "redis://localhost:6379", capabilities: List[str] = None, agent_id: str = None):
        """
        Initialize Beast Mode bus client.

        Args:
            redis_url: Redis server URL
            capabilities: List of agent capabilities
            agent_id: Unique agent identifier
        """
        self.agent_id = agent_id or f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.capabilities = capabilities or []
        self.specializations = []

        self.connection_manager = RedisConnectionManager(redis_url)
        self.logger = logging.getLogger(__name__)

        # Message handlers by type
        self.message_handlers: Dict[MessageType, Callable[[BeastModeMessage], None]] = {}

        # Connection state
        self.is_connected = False
        self.is_listening = False

        # Setup connection callbacks
        self.connection_manager.on_connect = self._on_connect
        self.connection_manager.on_disconnect = self._on_disconnect
        self.connection_manager.on_error = self._on_error

    async def connect(self) -> bool:
        """
        Connect to the Beast Mode network.

        Returns:
            True if connection successful, False otherwise
        """
        self.logger.info(f"Connecting agent {self.agent_id} to Beast Mode network...")

        success = await self.connection_manager.connect()
        if success:
            self.is_connected = True
            self.logger.info(f"✅ Agent {self.agent_id} connected successfully")
        else:
            self.logger.error(f"❌ Failed to connect agent {self.agent_id}")

        return success

    async def disconnect(self) -> None:
        """Disconnect from the Beast Mode network."""
        self.logger.info(f"Disconnecting agent {self.agent_id}...")

        self.is_listening = False
        await self.connection_manager.disconnect()
        self.is_connected = False

        self.logger.info(f"Agent {self.agent_id} disconnected")

    async def announce_presence(self) -> None:
        """
        Announce agent presence and capabilities to the network.
        """
        if not self.is_connected:
            self.logger.warning("Cannot announce presence: not connected")
            return

        discovery_message = MessageSerializer.create_agent_discovery(source=self.agent_id, capabilities=self.capabilities, specializations=self.specializations)

        await self.send_message(discovery_message)
        self.logger.info(f"Announced presence: {self.capabilities}")

    async def send_message(self, message: BeastModeMessage) -> bool:
        """
        Send message to the Beast Mode network.

        Args:
            message: Message to send

        Returns:
            True if message sent successfully, False otherwise
        """
        if not self.is_connected:
            self.logger.warning("Cannot send message: not connected")
            return False

        try:
            # Validate message before sending
            if not MessageSerializer.validate_message(message):
                self.logger.error("Invalid message, not sending")
                return False

            # Ensure message has source set
            if not message.source:
                message.source = self.agent_id

            # Serialize and send
            json_str = MessageSerializer.serialize(message)
            success = await self.connection_manager.publish("beast_mode_network", json_str)

            if success:
                self.logger.info(f"📤 Sent {message.type} message: {message.id}")
            else:
                self.logger.error(f"❌ Failed to send message: {message.id}")

            return success

        except MessageValidationError as e:
            self.logger.error(f"Message validation error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False

    async def send_simple_message(self, message_text: str, target: Optional[str] = None, priority: int = 5) -> bool:
        """
        Send a simple text message.

        Args:
            message_text: Text content of the message
            target: Target agent (None for broadcast)
            priority: Message priority (1-10)

        Returns:
            True if message sent successfully, False otherwise
        """
        message = MessageSerializer.create_simple_message(source=self.agent_id, message_text=message_text, target=target, priority=priority)

        return await self.send_message(message)

    async def send_prompt_request(self, prompt: str, target: Optional[str] = None, context: Optional[str] = None, priority: int = 9) -> bool:
        """
        Send a prompt request message.

        Args:
            prompt: The prompt/request text
            target: Target agent (None for broadcast)
            context: Additional context
            priority: Message priority (1-10)

        Returns:
            True if message sent successfully, False otherwise
        """
        message = MessageSerializer.create_prompt_request(source=self.agent_id, prompt=prompt, target=target, context=context, priority=priority)

        return await self.send_message(message)

    def register_message_handler(self, message_type: MessageType, handler: Callable[[BeastModeMessage], None]) -> None:
        """
        Register a handler for specific message types.

        Args:
            message_type: Type of message to handle
            handler: Function to call when message received
        """
        self.message_handlers[message_type] = handler
        self.logger.info(f"Registered handler for {message_type}")

    async def listen_for_messages(self) -> None:
        """
        Start listening for messages on the Beast Mode network.
        """
        if not self.is_connected:
            self.logger.warning("Cannot start listening: not connected")
            return

        self.is_listening = True
        self.logger.info("🎧 Started listening for messages...")

        def message_handler(json_str: str) -> None:
            """Handle incoming messages."""
            try:
                message = MessageSerializer.deserialize(json_str)

                # Don't process our own messages
                if message.source == self.agent_id:
                    return

                self.logger.info(f"📨 Received {message.type} from {message.source}")

                # Call registered handler if available
                if message.type in self.message_handlers:
                    try:
                        self.message_handlers[message.type](message)
                    except Exception as e:
                        self.logger.error(f"Error in message handler: {e}")

                # Default handling for unhandled message types
                else:
                    self.logger.info(f"No handler for {message.type}, ignoring")

            except MessageValidationError as e:
                self.logger.error(f"Invalid message received: {e}")
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")

        # Start listening
        await self.connection_manager.subscribe("beast_mode_network", message_handler)

    def stop_listening(self) -> None:
        """Stop listening for messages."""
        self.is_listening = False
        self.logger.info("Stopped listening for messages")

    def add_capability(self, capability: str) -> None:
        """Add capability to agent."""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
            self.logger.info(f"Added capability: {capability}")

    def add_specialization(self, specialization: str) -> None:
        """Add specialization to agent."""
        if specialization not in self.specializations:
            self.specializations.append(specialization)
            self.logger.info(f"Added specialization: {specialization}")

    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {"agent_id": self.agent_id, "capabilities": self.capabilities, "specializations": self.specializations, "is_connected": self.is_connected, "is_listening": self.is_listening}

    async def _on_connect(self) -> None:
        """Handle connection event."""
        self.logger.info("Connection established")

    async def _on_disconnect(self) -> None:
        """Handle disconnection event."""
        self.logger.info("Connection lost")
        self.is_connected = False
        self.is_listening = False

    async def _on_error(self, error: Exception) -> None:
        """Handle connection error."""
        self.logger.error(f"Connection error: {error}")


# Example usage and testing
async def test_bus_client():
    """Test bus client functionality."""
    print("Testing BeastModeBusClient...")

    # Create client
    client = BeastModeBusClient(capabilities=["python_coding", "gcp_optimization"], agent_id="test_agent")

    # Test connection
    if await client.connect():
        print("✅ Client connected successfully")

        # Test sending simple message
        if await client.send_simple_message("Hello, Beast Mode!"):
            print("✅ Simple message sent successfully")

        # Test sending prompt request
        if await client.send_prompt_request("Can you help with GCP optimization?"):
            print("✅ Prompt request sent successfully")

        # Test agent info
        info = client.get_agent_info()
        print(f"✅ Agent info: {info}")

        await client.disconnect()
        print("✅ Client disconnected successfully")
    else:
        print("❌ Client connection failed")


if __name__ == "__main__":
    # Run client test
    asyncio.run(test_bus_client())
