import asyncio
import logging
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime

from redis_foundation import RedisConnectionManager
from message_models import BeastModeMessage, MessageType, AgentCapabilities, MessageSerializer

logger = logging.getLogger(__name__)


class BeastModeBusClient:
    def __init__(self, redis_url: str = "redis://localhost:6379", capabilities: List[str] = None, agent_id: str = None):
        self.redis_url = redis_url
        self.agent_id = agent_id or "unknown_agent"
        self.capabilities = capabilities or []
        self.connection_manager = RedisConnectionManager(redis_url)
        self.is_connected = False
        self.is_listening = False
        self.message_handlers: Dict[MessageType, Callable] = {}

    async def connect(self) -> bool:
        if await self.connection_manager.connect():
            self.is_connected = True
            logger.info(f"✅ Agent {self.agent_id} connected successfully")
            return True
        return False

    async def disconnect(self) -> None:
        self.is_listening = False
        await self.connection_manager.disconnect()
        self.is_connected = False
        logger.info(f"Agent {self.agent_id} disconnected")

    async def announce_presence(self) -> None:
        if not self.is_connected:
            logger.warning("Cannot announce presence: not connected")
            return

        discovery_message = BeastModeMessage(
            type=MessageType.AGENT_DISCOVERY, source=self.agent_id, payload={"capabilities": {"agent_id": self.agent_id, "capabilities": self.capabilities, "availability": "ready_for_business"}}
        )

        await self.send_message(discovery_message)
        logger.info(f"Announced presence: {self.capabilities}")

    async def send_message(self, message: BeastModeMessage) -> bool:
        if not self.is_connected:
            logger.warning("Cannot send message: not connected")
            return False

        try:
            serialized_message = MessageSerializer.serialize(message)
            await self.connection_manager.publish("beast_mode_network", serialized_message)
            logger.debug(f"📤 Sent message: {message.type.value}")
            return True
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    async def send_simple_message(self, message_text: str, target_agent: str = None) -> bool:
        message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source=self.agent_id, target=target_agent, payload={"message": message_text})
        return await self.send_message(message)

    def register_message_handler(self, message_type: MessageType, handler: Callable) -> None:
        self.message_handlers[message_type] = handler
        logger.info(f"Registered handler for {message_type}")

    async def listen_for_messages(self) -> None:
        if not self.is_connected:
            logger.warning("Cannot start listening: not connected")
            return

        self.is_listening = True
        logger.info("🎧 Started listening for messages...")

        try:
            pubsub = await self.connection_manager.get_pubsub()
            await pubsub.subscribe("beast_mode_network")

            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        parsed_message = MessageSerializer.deserialize(message["data"])
                        if parsed_message.source != self.agent_id:
                            handler = self.message_handlers.get(parsed_message.type)
                            if handler:
                                await handler(parsed_message)
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
        except Exception as e:
            logger.error(f"Error in message listener: {e}")
        finally:
            self.is_listening = False

    def stop_listening(self) -> None:
        self.is_listening = False
        logger.info("Stopped listening for messages")
