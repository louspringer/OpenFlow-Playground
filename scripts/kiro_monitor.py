#!/usr/bin/env python3
"""
🎯 Kiro Agent Live Fire Monitor
Real-time monitoring CLI for Kiro Agent coordination
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class KiroMonitor:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_status(self):
        """Get agent status"""
        async with self.session.get(f"{self.base_url}/status") as resp:
            return await resp.json()

    async def get_tasks(self):
        """Get active tasks"""
        async with self.session.get(f"{self.base_url}/tasks") as resp:
            return await resp.json()

    async def get_metrics(self):
        """Get Prometheus metrics"""
        async with self.session.get(f"{self.base_url}/metrics") as resp:
            return await resp.text()

    def display_status(self, status):
        """Display formatted status"""
        coord = status.get("coordinator", {})
        stats = coord.get("stats", {})

        print(f"🤖 Agents: {coord.get('registered_agents', 0)} | 📋 Tasks: {coord.get('active_tasks', 0)}")
        print(f"🔄 Cycles: {stats.get('coordination_cycles', 0)} | ✅ Done: {stats.get('tasks_completed', 0)}")
        print(f"❌ Failed: {stats.get('tasks_failed', 0)} | 🔍 Validations: {stats.get('validation_requests', 0)}")
        print()

    def display_tasks(self, tasks_data):
        """Display active tasks"""
        tasks = tasks_data.get("tasks", [])

        if not tasks:
            print("📭 No active tasks")
            return

        print("📋 ACTIVE TASKS:")
        for i, task in enumerate(tasks[:3]):  # Show first 3
            desc = task.get("description", "No description")[:50]
            print(f"  🎯 {task.get('task_id', 'unknown')}: {task.get('type', 'unknown')} - {desc}...")

        if len(tasks) > 3:
            print(f"  ... and {len(tasks) - 3} more")
        print()

    def display_metrics(self, metrics_text):
        """Display key metrics"""
        lines = metrics_text.strip().split("\n")
        print("📊 KEY METRICS:")
        for line in lines:
            if line.startswith("kiro_agent_") and not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 2:
                    metric_name = parts[0].replace("kiro_agent_", "").replace("_", " ").title()
                    value = parts[1]
                    print(f"  📈 {metric_name}: {value}")
        print()

    async def monitor_loop(self, interval=3):
        """Main monitoring loop"""
        print("🎯 LIVE FIRE EXERCISE - Kiro Agent Monitor")
        print("=" * 50)
        print("Press Ctrl+C to stop")
        print()

        try:
            while True:
                # Clear screen
                print("\033[2J\033[H", end="")
                print(f"🎯 LIVE FIRE - {datetime.now().strftime('%H:%M:%S')}")
                print("=" * 50)

                try:
                    # Get data
                    status = await self.get_status()
                    tasks = await self.get_tasks()
                    metrics = await self.get_metrics()

                    # Display
                    self.display_status(status)
                    self.display_tasks(tasks)
                    self.display_metrics(metrics)

                    print(f"⏰ Next update in {interval}s... (Ctrl+C to stop)")
                    await asyncio.sleep(interval)

                except Exception as e:
                    print(f"❌ Error: {e}")
                    await asyncio.sleep(5)

        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped")


async def main():
    """Main entry point"""
    async with KiroMonitor() as monitor:
        await monitor.monitor_loop()


if __name__ == "__main__":
    asyncio.run(main())
