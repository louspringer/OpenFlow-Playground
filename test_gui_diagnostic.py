#!/usr/bin/env python3
"""
Simple GUI Diagnostic Script
Just takes screenshots to see what the GUI actually looks like
"""

import asyncio
import time
from pathlib import Path
from playwright.async_api import async_playwright
import subprocess


async def diagnostic_screenshot():
    """Take diagnostic screenshots of the GUI."""
    print("🔍 Taking diagnostic screenshots...")

    # Launch GUI
    print("🚀 Launching GUI...")
    subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
    time.sleep(2)

    gui_process = subprocess.Popen(
        [
            "uv",
            "run",
            "streamlit",
            "run",
            "src/workflow_visualization_gui.py",
            "--server.port",
            "8501",
            "--server.address",
            "localhost",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for GUI to start
    print("⏳ Waiting for GUI to start...")
    time.sleep(10)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True
        )  # Must be headless in this environment
        page = await browser.new_page()

        try:
            # Navigate to GUI
            await page.goto("http://localhost:8501")
            await page.wait_for_load_state("networkidle")

            # Take full page screenshot
            screenshot_path = Path("diagnostic_screenshot.png")
            await page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"📸 Full page screenshot saved: {screenshot_path}")

            # Try to find the selectbox
            print("🔍 Looking for selectbox elements...")

            # Check for different possible selectbox implementations
            selectbox_variants = [
                "div[data-testid='stSelectbox']",
                "div[role='combobox']",
                "div[aria-haspopup='listbox']",
                "div[class*='selectbox']",
                "div[class*='Select']",
                "div[class*='stSelectbox']",
            ]

            for variant in selectbox_variants:
                count = await page.locator(variant).count()
                if count > 0:
                    print(f"✅ Found {count} elements matching: {variant}")

                    # Take screenshot of this element
                    element = page.locator(variant).first
                    element_screenshot = f"selectbox_{variant.replace('[', '_').replace(']', '_').replace('=', '_')}.png"
                    await element.screenshot(path=element_screenshot)
                    print(f"📸 Element screenshot saved: {element_screenshot}")

                    # Try to click it
                    try:
                        await element.click()
                        print(f"✅ Successfully clicked: {variant}")

                        # Wait for dropdown to appear
                        await page.wait_for_timeout(1000)

                        # Look for dropdown options
                        options = await page.locator("div[role='option']").count()
                        print(f"📋 Found {options} dropdown options")

                        # Take screenshot of dropdown
                        dropdown_screenshot = "dropdown_open.png"
                        await page.screenshot(path=dropdown_screenshot)
                        print(f"📸 Dropdown screenshot saved: {dropdown_screenshot}")

                    except Exception as e:
                        print(f"❌ Failed to click {variant}: {e}")
                else:
                    print(f"❌ No elements found for: {variant}")

            # Also check for any elements with "UC-" text
            uc_elements = await page.locator("*:has-text('UC-')").count()
            print(f"📋 Found {uc_elements} elements containing 'UC-' text")

            # Take screenshot of sidebar specifically
            sidebar_screenshot = "sidebar.png"
            try:
                sidebar = page.locator("div[data-testid='stSidebar']")
                if await sidebar.count() > 0:
                    await sidebar.screenshot(path=sidebar_screenshot)
                    print(f"📸 Sidebar screenshot saved: {sidebar_screenshot}")
                else:
                    print("❌ No sidebar found")
            except Exception as e:
                print(f"❌ Failed to screenshot sidebar: {e}")

        except Exception as e:
            print(f"❌ Error during diagnostic: {e}")

        finally:
            await browser.close()
            gui_process.terminate()
            gui_process.wait()
            print("✅ Cleanup complete")


if __name__ == "__main__":
    asyncio.run(diagnostic_screenshot())
