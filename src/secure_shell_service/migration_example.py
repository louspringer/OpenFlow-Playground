#!/usr/bin/env python3
"""
Migration Example - From CRINGY subprocess to ELEGANT secure shell! 😄
"""

import asyncio

from elegant_client import secure_execute  # type: ignore

from src.secure_shell_service.secure_executor import secure_execute


# 😱 BEFORE: CRINGY subprocess calls
def cringy_old_way() -> None:
    """The old way - makes you cringe every time you see it 😱"""
    # import subprocess  # REMOVED - replaced with secure_execute

    # 😱 CRINGY: Direct subprocess call
    result = secure_execute(["ls", "-la"], capture_output=True, text=True)
    print(f"CRINGY Output: {result.stdout}")

    # 😱 CRINGY: No timeout, can hang forever
    result = secure_execute(["sleep", "10"], capture_output=True, text=True)
    print("CRINGY: This could hang forever!")

    # 😱 CRINGY: Command injection risk
    user_input = "rm -rf /"  # 😱 DANGEROUS!
    result = secure_execute(user_input, shell=True)  # 😱 CRINGY!  # type: ignore
    print("CRINGY: Command injection risk!")


# 🎉 AFTER: ELEGANT secure shell calls
async def elegant_new_way() -> None:
    """The new way - elegant and secure! 🎉"""

    # 🎉 ELEGANT: Secure command execution
    result = await secure_execute("ls -la", timeout=10)  # type: ignore
    print(f"ELEGANT Output: {result['output']}")

    # 🎉 ELEGANT: Built-in timeout protection
    result = await secure_execute("sleep 10", timeout=5)  # type: ignore
    print("ELEGANT: Timed out safely after 5 seconds!")

    # 🎉 ELEGANT: Input validation and sanitization
    user_input = "rm -rf /"  # Still dangerous, but now SAFE!
    result = await secure_execute(
        user_input, timeout=10, validate_input=True
    )  # type: ignore
    print("ELEGANT: Command sanitized and validated!")

    # 🎉 ELEGANT: Proper error handling
    result = await secure_execute("nonexistent_command", timeout=10)  # type: ignore
    if not result["success"]:
        print(f"ELEGANT Error: {result['error']}")


# Migration examples for common patterns
async def migration_examples() -> None:
    """Examples of migrating common subprocess patterns"""

    print("🔄 Migration Examples - From CRINGY to ELEGANT! 😄")
    print("=" * 60)

    # Example 1: Simple command execution
    print("\n1️⃣ Simple Command Execution:")
    print("😱 BEFORE: secure_execute(['ls', '-la'], capture_output=True)")
    print("🎉 AFTER: await secure_execute('ls -la', timeout=10)")

    result = await secure_execute("ls -la", timeout=10)  # type: ignore
    print(f"✅ Result: {result['success']}, Exit: {result['exit_code']}")

    # Example 2: Command with timeout
    print("\n2️⃣ Command with Timeout:")
    print("😱 BEFORE: secure_execute(['sleep', '10'], timeout=5)")
    print("🎉 AFTER: await secure_execute('sleep 10', timeout=5)")

    result = await secure_execute("sleep 10", timeout=5)  # type: ignore
    print(f"✅ Result: {result['success']}, Error: {result['error']}")

    # Example 3: Error handling
    print("\n3️⃣ Error Handling:")
    print("😱 BEFORE: try: secure_execute(['bad_command']) except: pass")
    print("🎉 AFTER: result = await secure_execute('bad_command')")

    result = await secure_execute("bad_command", timeout=10)  # type: ignore
    print(f"✅ Result: {result['success']}, Error: {result['error']}")

    # Example 4: Complex command
    print("\n4️⃣ Complex Command:")
    print("😱 BEFORE: secure_execute(['find', '.', '-name', '*.py'])")
    print("🎉 AFTER: await secure_execute('find . -name \"*.py\"')")

    result = await secure_execute(
        'find . -name "*.py" | head -5', timeout=10
    )  # type: ignore
    print(f"✅ Result: {result['success']}, Files: {len(result['output'].split())}")

    print("\n🎉 NO MORE CRINGING! Everything is elegant and secure! 🚀")


# Real migration example
async def migrate_file_example() -> None:
    """Example of migrating a real file"""

    print("\n📁 Real Migration Example:")
    print("=" * 40)

    # Simulate migrating a file that uses subprocess
    old_code = """
# 😱 OLD CODE (CRINGY!)
# import subprocess  # REMOVED - replaced with secure_execute

def check_system_status():
    result = secure_execute(['ps', 'aux'], capture_output=True, text=True)
    return result.stdout

def run_backup():
    result = secure_execute(['tar', '-czf', 'backup.tar.gz', '.'],
                          capture_output=True, text=True)
    return result.returncode == 0
"""

    new_code = """
# 🎉 NEW CODE (ELEGANT!)
from src.secure_shell_service.elegant_client import secure_execute

async def check_system_status():
    result = await secure_execute('ps aux', timeout=10)
    return result['output'] if result['success'] else ''

async def run_backup():
    result = await secure_execute('tar -czf backup.tar.gz .', timeout=300)
    return result['success']
"""

    print("😱 BEFORE (CRINGY):")
    print(old_code)
    print("\n🎉 AFTER (ELEGANT):")
    print(new_code)

    print("\n✨ Benefits of Migration:")
    print("✅ Built-in timeout protection")
    print("✅ Input validation and sanitization")
    print("✅ Proper error handling")
    print("✅ Async/await support")
    print("✅ No more command injection risks")
    print("✅ NO MORE CRINGING! 😄")


async def main() -> None:
    """Main migration example"""
    print("🛡️ Migration Examples - NO MORE CRINGING! 😄")
    print("=" * 60)

    # Show the difference
    await migration_examples()

    # Show real migration example
    await migrate_file_example()

    print("\n🎉 Migration complete! NO MORE SHELL COMMANDS! 🚀")


if __name__ == "__main__":
    asyncio.run(main())
