import asyncio
import os
import redis.asyncio as redis
import logging

logger = logging.getLogger(__name__)


class RedisConnectionManager:
    def __init__(self, redis_url: str = None, max_retries: int = 5, retry_delay: float = 1.0):
        # Read from REDIS_URL environment variable if not provided
        if redis_url is None:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_url = redis_url
        self.client = None
        self.pubsub = None
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._is_connected = False

    async def connect(self) -> bool:
        for attempt in range(self.max_retries):
            try:
                self.client = redis.from_url(self.redis_url, decode_responses=True)
                await self.client.ping()
                self._is_connected = True
                logger.info(f"✅ Connected to Redis at {self.redis_url}")
                return True
            except Exception as e:
                logger.warning(f"❌ Redis connection attempt {attempt + 1}/{self.max_retries} failed: {e}")
                await asyncio.sleep(self.retry_delay * (2**attempt))
        logger.error(f"❌ Failed to connect to Redis after {self.max_retries} attempts.")
        self._is_connected = False
        return False

    async def disconnect(self):
        if self.pubsub:
            await self.pubsub.close()
            self.pubsub = None
        if self.client:
            await self.client.aclose()
            self.client = None
        self._is_connected = False
        logger.info("🔌 Disconnected from Redis.")

    async def is_healthy(self) -> bool:
        if not self._is_connected or not self.client:
            return False
        try:
            await self.client.ping()
            return True
        except Exception as e:
            logger.warning(f"💔 Redis health check failed: {e}")
            self._is_connected = False
            return False

    async def get_pubsub(self):
        if not self.pubsub:
            if not self._is_connected:
                await self.connect()
            if self._is_connected:
                self.pubsub = self.client.pubsub()
        return self.pubsub

    async def publish(self, channel: str, message: str):
        if not await self.is_healthy():
            logger.error("Cannot publish: Redis not connected or unhealthy.")
            return
        try:
            await self.client.publish(channel, message)
            logger.debug(f"📤 Published to {channel}: {message[:100]}...")
        except Exception as e:
            logger.error(f"❌ Error publishing message to {channel}: {e}")

    @property
    def connected(self) -> bool:
        return self._is_connected
