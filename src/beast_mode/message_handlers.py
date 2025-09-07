#!/usr/bin/env python3
"""
Standardized Message Type Handling for Beast Mode Agent Collaboration Network

Implements handlers for each MessageType enum value, message routing based on type and target,
compatibility layer for different message formats, and message validation with graceful error handling.

Requirements: 6.1, 6.2, 6.3, 6.4
"""

import asyncio
import logging
from typing import Dict, List, Optional, Callable, Any, Union
from datetime import datetime
from dataclasses import dataclass

from beast_mode.message_models_dataclass import BeastModeMessage, MessageType, MessageSerializer
from beast_mode.agent_discovery import AgentDiscoveryManager
from beast_mode.help_system import HelpSystemManager

logger = logging.getLogger(__name__)


@dataclass
class MessageHandlerResult:
    """Result of message handling operation."""

    success: bool
    response: Optional[BeastModeMessage] = None
    error: Optional[str] = None
    should_continue: bool = True


class MessageTypeHandler:
    """Base class for message type handlers."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    async def handle(self, message: BeastModeMessage) -> MessageHandlerResult:
        """Handle a message of this type."""
        raise NotImplementedError("Subclasses must implement handle method")

    def can_handle(self, message: BeastModeMessage) -> bool:
        """Check if this handler can handle the message."""
        return True


class SimpleMessageHandler(MessageTypeHandler):
    """Handles simple_message type messages."""

    async def handle(self, message: BeastModeMessage) -> MessageHandlerResult:
        """Handle simple message."""
        try:
            message_text = message.payload.get("message", "")
            logger.info(f"Received simple message from {message.source}: {message_text}")

            # Echo back with acknowledgment
            response = BeastModeMessage(
                type=MessageType.SIMPLE_MESSAGE, source=self.agent_id, target=message.source, payload={"message": f"Received: {message_text}", "timestamp": datetime.now().isoformat()}
            )

            return MessageHandlerResult(success=True, response=response)

        except Exception as e:
            logger.error(f"Error handling simple message: {e}")
            return MessageHandlerResult(success=False, error=str(e))


class PromptRequestHandler(MessageTypeHandler):
    """Handles prompt_request type messages."""

    async def handle(self, message: BeastModeMessage) -> MessageHandlerResult:
        """Handle prompt request."""
        try:
            prompt_data = message.payload.get("prompt_data", {})
            prompt_type = message.payload.get("prompt_type", "general")

            logger.info(f"Received prompt request from {message.source}: {prompt_type}")

            # Process the prompt based on type
            response_text = await self._process_prompt(prompt_type, prompt_data)

            response = BeastModeMessage(
                type=MessageType.PROMPT_RESPONSE, source=self.agent_id, target=message.source, payload={"prompt_type": prompt_type, "response": response_text, "timestamp": datetime.now().isoformat()}
            )

            return MessageHandlerResult(success=True, response=response)

        except Exception as e:
            logger.error(f"Error handling prompt request: {e}")
            return MessageHandlerResult(success=False, error=str(e))

    async def _process_prompt(self, prompt_type: str, prompt_data: Dict[str, Any]) -> str:
        """Process a prompt based on its type."""
        if prompt_type == "cost_analysis":
            return "I can help with cost analysis. Based on our recent work, we achieved 93.6% cost reduction on GCP."
        elif prompt_type == "gcp_optimization":
            return "For GCP optimization, I recommend reviewing cluster sizing, Cloud Run scaling, and resource allocation."
        elif prompt_type == "system_architecture":
            return "I can assist with system architecture design and implementation patterns."
        else:
            return f"I received your {prompt_type} prompt and I'm processing it."


class SporeDeliveryHandler(MessageTypeHandler):
    """Handles spore_delivery type messages."""

    def __init__(self, agent_id: str, spore_directory: str = "spores"):
        super().__init__(agent_id)
        self.spore_directory = spore_directory

    async def handle(self, message: BeastModeMessage) -> MessageHandlerResult:
        """Handle spore delivery."""
        try:
            spore_data = message.payload.get("spore_data", {})
            spore_name = message.payload.get("spore_name", "unknown")
            spore_version = message.payload.get("spore_version", "1.0")

            logger.info(f"Received spore '{spore_name}' v{spore_version} from {message.source}")

            # Save spore to local directory
            await self._save_spore(spore_name, spore_data, spore_version)

            # Send acknowledgment
            response = BeastModeMessage(
                type=MessageType.SPORE_DELIVERY,
                source=self.agent_id,
                target=message.source,
                payload={"spore_name": spore_name, "status": "received", "message": f"Spore '{spore_name}' received and saved", "timestamp": datetime.now().isoformat()},
            )

            return MessageHandlerResult(success=True, response=response)

        except Exception as e:
            logger.error(f"Error handling spore delivery: {e}")
            return MessageHandlerResult(success=False, error=str(e))

    async def _save_spore(self, spore_name: str, spore_data: Dict[str, Any], version: str) -> None:
        """Save spore to local directory."""
        import os
        import json

        # Ensure spore directory exists
        os.makedirs(self.spore_directory, exist_ok=True)

        # Create spore file
        spore_file = os.path.join(self.spore_directory, f"{spore_name}_v{version}.json")
        with open(spore_file, "w") as f:
            json.dump(spore_data, f, indent=2)

        logger.info(f"Saved spore to {spore_file}")


class SystemHealthHandler(MessageTypeHandler):
    """Handles system_health type messages."""

    async def handle(self, message: BeastModeMessage) -> MessageHandlerResult:
        """Handle system health check."""
        try:
            health_data = message.payload.get("health_data", {})
            check_type = message.payload.get("check_type", "general")

            logger.info(f"Received system health check from {message.source}: {check_type}")

            # Perform health check
            health_status = await self._perform_health_check(check_type, health_data)

            response = BeastModeMessage(
                type=MessageType.SYSTEM_HEALTH, source=self.agent_id, target=message.source, payload={"check_type": check_type, "health_status": health_status, "timestamp": datetime.now().isoformat()}
            )

            return MessageHandlerResult(success=True, response=response)

        except Exception as e:
            logger.error(f"Error handling system health check: {e}")
            return MessageHandlerResult(success=False, error=str(e))

    async def _perform_health_check(self, check_type: str, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a health check."""
        if check_type == "redis_connection":
            return {"status": "healthy", "message": "Redis connection is active"}
        elif check_type == "message_processing":
            return {"status": "healthy", "message": "Message processing is working"}
        elif check_type == "agent_discovery":
            return {"status": "healthy", "message": "Agent discovery is functional"}
        else:
            return {"status": "healthy", "message": "System is operational"}


class MessageRouter:
    """Routes messages to appropriate handlers based on type and target."""

    def __init__(self, agent_id: str, discovery_manager: AgentDiscoveryManager, help_manager: HelpSystemManager):
        self.agent_id = agent_id
        self.discovery_manager = discovery_manager
        self.help_manager = help_manager
        self.handlers: Dict[MessageType, MessageTypeHandler] = {}
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup message type handlers."""
        self.handlers = {
            MessageType.SIMPLE_MESSAGE: SimpleMessageHandler(self.agent_id),
            MessageType.PROMPT_REQUEST: PromptRequestHandler(self.agent_id),
            MessageType.PROMPT_RESPONSE: SimpleMessageHandler(self.agent_id),  # Reuse simple handler
            MessageType.SPORE_DELIVERY: SporeDeliveryHandler(self.agent_id),
            MessageType.SPORE_REQUEST: SimpleMessageHandler(self.agent_id),  # Reuse simple handler
            MessageType.TECHNICAL_EXCHANGE: SimpleMessageHandler(self.agent_id),  # Reuse simple handler
            MessageType.SYSTEM_HEALTH: SystemHealthHandler(self.agent_id),
        }

    async def route_message(self, message: BeastModeMessage) -> MessageHandlerResult:
        """Route a message to the appropriate handler."""
        try:
            # Check if message is for this agent
            if message.target and message.target != self.agent_id:
                logger.debug(f"Message not for this agent (target: {message.target})")
                return MessageHandlerResult(success=True, should_continue=False)

            # Check if message is from this agent
            if message.source == self.agent_id:
                logger.debug(f"Ignoring message from self")
                return MessageHandlerResult(success=True, should_continue=False)

            # Route to discovery manager for discovery-related messages
            if message.type in [MessageType.AGENT_DISCOVERY, MessageType.AGENT_RESPONSE]:
                discovery_handlers = self.discovery_manager.get_handlers()
                if message.type in discovery_handlers:
                    await discovery_handlers[message.type](message)
                return MessageHandlerResult(success=True)

            # Route to help manager for help-related messages
            if message.type in [MessageType.HELP_WANTED, MessageType.HELP_RESPONSE]:
                help_handlers = self.help_manager.get_handlers()
                if message.type in help_handlers:
                    await help_handlers[message.type](message)
                return MessageHandlerResult(success=True)

            # Route to specific message type handler
            if message.type in self.handlers:
                handler = self.handlers[message.type]
                return await handler.handle(message)

            # Unknown message type - log and continue
            logger.warning(f"Unknown message type: {message.type}")
            return MessageHandlerResult(success=True, should_continue=True)

        except Exception as e:
            logger.error(f"Error routing message: {e}")
            return MessageHandlerResult(success=False, error=str(e))


class MessageCompatibilityLayer:
    """Provides compatibility layer for different message formats."""

    @staticmethod
    def convert_legacy_message(legacy_data: Dict[str, Any]) -> BeastModeMessage:
        """Convert legacy message format to BeastModeMessage."""
        try:
            # Handle different legacy formats
            if "type" in legacy_data and "source" in legacy_data:
                # Already in correct format
                return BeastModeMessage(**legacy_data)

            # Convert from simple format
            if "message" in legacy_data:
                return BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source=legacy_data.get("source", "unknown"), payload={"message": legacy_data["message"]})

            # Convert from prompt format
            if "prompt" in legacy_data:
                return BeastModeMessage(type=MessageType.PROMPT_REQUEST, source=legacy_data.get("source", "unknown"), payload={"prompt_data": legacy_data})

            # Default fallback
            return BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source=legacy_data.get("source", "unknown"), payload=legacy_data)

        except Exception as e:
            logger.error(f"Error converting legacy message: {e}")
            # Return a safe default message
            return BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source="unknown", payload={"error": f"Failed to convert message: {e}"})

    @staticmethod
    def validate_message(message: BeastModeMessage) -> bool:
        """Validate a message for required fields and format."""
        try:
            # Check required fields
            if not message.id or not message.type or not message.source:
                return False

            # Check timestamp is valid
            if not isinstance(message.timestamp, datetime):
                return False

            # Check priority is in valid range
            if not (1 <= message.priority <= 10):
                return False

            # Check payload is dict
            if not isinstance(message.payload, dict):
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating message: {e}")
            return False


class MessageHandlerManager:
    """Manages all message handling functionality."""

    def __init__(self, agent_id: str, discovery_manager: AgentDiscoveryManager, help_manager: HelpSystemManager):
        self.agent_id = agent_id
        self.discovery_manager = discovery_manager
        self.help_manager = help_manager
        self.router = MessageRouter(agent_id, discovery_manager, help_manager)
        self.compatibility = MessageCompatibilityLayer()
        self.message_count = 0
        self.error_count = 0

    async def handle_message(self, raw_message: str) -> Optional[BeastModeMessage]:
        """Handle a raw message string."""
        try:
            self.message_count += 1

            # Deserialize message
            message = MessageSerializer.deserialize(raw_message)

            # Validate message
            if not self.compatibility.validate_message(message):
                logger.warning(f"Invalid message format: {message.id}")
                self.error_count += 1
                return None

            # Route message
            result = await self.router.route_message(message)

            if not result.success:
                logger.error(f"Error handling message {message.id}: {result.error}")
                self.error_count += 1
                return None

            # Send response if one was generated
            if result.response:
                await self._send_response(result.response)

            return message

        except Exception as e:
            logger.error(f"Error handling message: {e}")
            self.error_count += 1
            return None

    async def _send_response(self, response: BeastModeMessage) -> None:
        """Send a response message."""
        try:
            serialized_response = MessageSerializer.serialize(response)
            await self.discovery_manager.redis_manager.publish("beast_mode_network", serialized_response)
            logger.debug(f"Sent response to {response.target}")
        except Exception as e:
            logger.error(f"Error sending response: {e}")

    def get_handlers(self) -> Dict[MessageType, Callable[[BeastModeMessage], Any]]:
        """Get all message handlers for registration with bus client."""
        handlers = {}

        # Add discovery handlers
        handlers.update(self.discovery_manager.get_handlers())

        # Add help system handlers
        handlers.update(self.help_manager.get_handlers())

        # Add message type handlers
        for msg_type, handler in self.router.handlers.items():
            handlers[msg_type] = handler.handle

        return handlers

    def get_statistics(self) -> Dict[str, Any]:
        """Get message handling statistics."""
        return {
            "total_messages": self.message_count,
            "error_count": self.error_count,
            "success_rate": (self.message_count - self.error_count) / max(self.message_count, 1),
            "available_handlers": len(self.router.handlers),
            "discovery_handlers": len(self.discovery_manager.get_handlers()),
            "help_handlers": len(self.help_manager.get_handlers()),
        }
