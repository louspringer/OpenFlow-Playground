"""
Redis Pub/Sub Foundation for Beast Mode Agent Collaboration Network

Task 1: Set up Redis pub/sub foundation
- Install and configure Redis server for local development
- Create basic connection management utilities
- Implement health check and reconnection logic
- Write unit tests for Redis connectivity
- Requirements: 1.1, 1.2
"""

import asyncio
import logging
import time
from typing import Optional, Callable, Any
import redis.asyncio as redis
from redis.exceptions import ConnectionError, TimeoutError, RedisError


class RedisConnectionManager:
    """
    Manages Redis connection with health monitoring and automatic reconnection.

    Provides robust connection management for the Beast Mode Agent Collaboration Network
    with exponential backoff retry logic and graceful error handling.
    """

    def __init__(self, redis_url: str = "redis://localhost:6379", max_retries: int = 5, retry_delay: float = 1.0, health_check_interval: float = 30.0):
        """
        Initialize Redis connection manager.

        Args:
            redis_url: Redis server URL
            max_retries: Maximum number of reconnection attempts
            retry_delay: Initial delay between retry attempts (exponential backoff)
            health_check_interval: Interval for health checks in seconds
        """
        self.redis_url = redis_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.health_check_interval = health_check_interval

        self.client: Optional[redis.Redis] = None
        self.is_connected = False
        self.retry_count = 0
        self.last_health_check = 0
        self.logger = logging.getLogger(__name__)

        # Connection event callbacks
        self.on_connect: Optional[Callable] = None
        self.on_disconnect: Optional[Callable] = None
        self.on_error: Optional[Callable[[Exception], None]] = None

    async def connect(self) -> bool:
        """
        Establish connection to Redis server with retry logic.

        Returns:
            True if connection successful, False otherwise
        """
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Connecting to Redis at {self.redis_url} (attempt {attempt + 1})")

                self.client = redis.from_url(self.redis_url)
                await self.client.ping()

                self.is_connected = True
                self.retry_count = 0
                self.last_health_check = time.time()

                self.logger.info("✅ Successfully connected to Redis")

                if self.on_connect:
                    await self.on_connect()

                return True

            except (ConnectionError, TimeoutError, RedisError) as e:
                self.logger.warning(f"❌ Connection attempt {attempt + 1} failed: {e}")

                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)  # Exponential backoff
                    self.logger.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    self.logger.error(f"❌ Failed to connect after {self.max_retries} attempts")
                    if self.on_error:
                        await self.on_error(e)
                    return False

        return False

    async def disconnect(self) -> None:
        """Disconnect from Redis server."""
        if self.client:
            try:
                await self.client.aclose()
                self.logger.info("Disconnected from Redis")
            except Exception as e:
                self.logger.warning(f"Error during disconnect: {e}")
            finally:
                self.client = None
                self.is_connected = False

                if self.on_disconnect:
                    await self.on_disconnect()

    async def health_check(self) -> bool:
        """
        Perform health check on Redis connection.

        Returns:
            True if connection is healthy, False otherwise
        """
        if not self.client:
            return False

        try:
            await self.client.ping()
            self.last_health_check = time.time()
            return True
        except (ConnectionError, TimeoutError, RedisError) as e:
            self.logger.warning(f"Health check failed: {e}")
            self.is_connected = False
            return False

    async def ensure_connection(self) -> bool:
        """
        Ensure Redis connection is active, reconnect if necessary.

        Returns:
            True if connection is active, False if reconnection failed
        """
        if not self.is_connected or not self.client:
            return await self.connect()

        # Perform periodic health check
        if time.time() - self.last_health_check > self.health_check_interval:
            if not await self.health_check():
                self.logger.warning("Health check failed, attempting reconnection...")
                return await self.connect()

        return True

    async def publish(self, channel: str, message: str) -> bool:
        """
        Publish message to Redis channel.

        Args:
            channel: Redis channel name
            message: Message to publish

        Returns:
            True if message published successfully, False otherwise
        """
        if not await self.ensure_connection():
            return False

        try:
            await self.client.publish(channel, message)
            return True
        except (ConnectionError, TimeoutError, RedisError) as e:
            self.logger.error(f"Failed to publish message: {e}")
            self.is_connected = False
            return False

    async def subscribe(self, channel: str, message_handler: Callable[[str], None]) -> None:
        """
        Subscribe to Redis channel and handle messages.

        Args:
            channel: Redis channel name
            message_handler: Function to handle received messages
        """
        if not await self.ensure_connection():
            return

        try:
            pubsub = self.client.pubsub()
            await pubsub.subscribe(channel)

            self.logger.info(f"Subscribed to channel: {channel}")

            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        message_handler(message["data"].decode("utf-8"))
                    except Exception as e:
                        self.logger.error(f"Error handling message: {e}")

        except (ConnectionError, TimeoutError, RedisError) as e:
            self.logger.error(f"Subscription error: {e}")
            self.is_connected = False
        finally:
            if "pubsub" in locals():
                await pubsub.close()


class RedisHealthMonitor:
    """
    Monitors Redis connection health and triggers reconnection if needed.
    """

    def __init__(self, connection_manager: RedisConnectionManager):
        self.connection_manager = connection_manager
        self.monitoring = False
        self.logger = logging.getLogger(__name__)

    async def start_monitoring(self) -> None:
        """Start health monitoring in background."""
        self.monitoring = True
        self.logger.info("Starting Redis health monitoring")

        while self.monitoring:
            try:
                if not await self.connection_manager.health_check():
                    self.logger.warning("Health check failed, attempting reconnection...")
                    await self.connection_manager.connect()

                await asyncio.sleep(self.connection_manager.health_check_interval)

            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(5)  # Short delay before retry

    def stop_monitoring(self) -> None:
        """Stop health monitoring."""
        self.monitoring = False
        self.logger.info("Stopped Redis health monitoring")


# Example usage and testing
async def test_redis_connection():
    """Test Redis connection functionality."""
    manager = RedisConnectionManager()

    # Test connection
    if await manager.connect():
        print("✅ Redis connection test passed")

        # Test publish
        if await manager.publish("test_channel", "Hello, Beast Mode!"):
            print("✅ Redis publish test passed")

        # Test health check
        if await manager.health_check():
            print("✅ Redis health check test passed")

        await manager.disconnect()
        print("✅ Redis disconnect test passed")
    else:
        print("❌ Redis connection test failed")


if __name__ == "__main__":
    # Run connection test
    asyncio.run(test_redis_connection())
