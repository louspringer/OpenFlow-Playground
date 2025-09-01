#!/usr/bin/env python3
"""
Automated GUI Testing Script for Workflow Visualization System
Uses Playwright to automatically test all GUI components and capture screenshots
"""

import asyncio
import time
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser
import subprocess
import signal
import os


class AutomatedGUITester:
    def __init__(self):
        self.screenshot_dir = Path("gui_screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        self.gui_process = None
        self.test_results = []

    async def setup_gui(self):
        """Launch the GUI in the background."""
        print("🚀 Launching GUI...")

        # Kill any existing Streamlit processes
        subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
        time.sleep(2)

        # Launch GUI
        self.gui_process = subprocess.Popen(
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

        return self.gui_process is not None

    async def test_dashboard(self, page: Page):
        """Test the main dashboard."""
        print("🏠 Testing Dashboard...")

        try:
            # Navigate to dashboard
            await page.goto("http://localhost:8501")
            await page.wait_for_load_state("networkidle")

            # Take screenshot
            screenshot_path = self.screenshot_dir / "01_dashboard.png"
            await page.screenshot(path=str(screenshot_path))

            # Check for key elements
            title = await page.title()
            main_title = await page.locator("h1").first.text_content()

            result = {
                "component": "Dashboard",
                "status": "✅ PASS" if "Workflow Extraction" in str(main_title) else "❌ FAIL",
                "screenshot": str(screenshot_path),
                "details": f"Title: {title}, Main: {main_title}",
            }

            self.test_results.append(result)
            print(f"  {result['status']} - {result['details']}")

        except Exception as e:
            result = {
                "component": "Dashboard",
                "status": "❌ ERROR",
                "screenshot": "None",
                "details": f"Exception: {str(e)}",
            }
            self.test_results.append(result)
            print(f"  {result['status']} - {result['details']}")

    async def test_control_flow(self, page: Page):
        """Test Control Flow Pattern Recognition (UC-2)."""
        print("🔄 Testing Control Flow Analysis...")

        try:
            # Navigate to control flow component
            await page.goto("http://localhost:8501")
            await page.wait_for_load_state("networkidle")

            # Select control flow component from sidebar
            # Streamlit uses custom selectbox, not standard select elements
            await page.locator("div[data-testid='stSelectbox']").click()
            await page.locator("div[role='option']:has-text('UC-2: Control Flow Pattern Recognition')").click()
            await page.wait_for_timeout(2000)

            # Take screenshot
            screenshot_path = self.screenshot_dir / "02_control_flow.png"
            await page.screenshot(path=str(screenshot_path))

            # Check for file selector
            file_selector = await page.locator("select[data-testid='stSelectbox']").count()

            result = {
                "component": "Control Flow Analysis",
                "status": "✅ PASS" if file_selector > 0 else "❌ FAIL",
                "screenshot": str(screenshot_path),
                "details": f"File selectors found: {file_selector}",
            }

            self.test_results.append(result)
            print(f"  {result['status']} - {result['details']}")

        except Exception as e:
            result = {
                "component": "Control Flow Analysis",
                "status": "❌ ERROR",
                "screenshot": "None",
                "details": f"Exception: {str(e)}",
            }
            self.test_results.append(result)
            print(f"  {result['status']} - {result['details']}")

    async def test_uml_generation(self, page: Page):
        """Test UML Activity Diagram Generation (UC-4)."""
        print("🎨 Testing UML Generation...")

        try:
            # Navigate to UML component
            await page.goto("http://localhost:8501")
            await page.wait_for_load_state("networkidle")

            # Select UML component from sidebar
            # Streamlit uses custom selectbox, not standard select elements
            await page.locator("div[data-testid='stSelectbox']").click()
            await page.locator("div[role='option']:has-text('UC-4: UML Activity Diagram Generation')").click()
            await page.wait_for_timeout(2000)

            # Take screenshot
            screenshot_path = self.screenshot_dir / "03_uml_generation.png"
            await page.screenshot(path=str(screenshot_path))

            # Check for generate button
            generate_button = await page.locator("button:has-text('Generate UML Diagrams')").count()

            result = {
                "component": "UML Generation",
                "status": "✅ PASS" if generate_button > 0 else "❌ FAIL",
                "screenshot": str(screenshot_path),
                "details": f"Generate buttons found: {generate_button}",
            }

            self.test_results.append(result)
            print(f"  {result['status']} - {result['details']}")

        except Exception as e:
            result = {
                "component": "UML Generation",
                "status": "❌ ERROR",
                "screenshot": "None",
                "details": f"Exception: {str(e)}",
            }
            self.test_results.append(result)
            print(f"  {result['status']} - {result['details']}")

    async def test_quick_analysis(self, page: Page):
        """Test Quick Analysis buttons."""
        print("⚡ Testing Quick Analysis...")

        try:
            # Navigate to dashboard
            await page.goto("http://localhost:8501")
            await page.wait_for_load_state("networkidle")

            # Scroll to quick analysis section
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

            # Take screenshot
            screenshot_path = self.screenshot_dir / "04_quick_analysis.png"
            await page.screenshot(path=str(screenshot_path))

            # Check for quick analysis buttons
            quick_buttons = await page.locator("button:has-text('Quick')").count()

            result = {
                "component": "Quick Analysis",
                "status": "✅ PASS" if quick_buttons >= 3 else "❌ FAIL",
                "screenshot": str(screenshot_path),
                "details": f"Quick analysis buttons found: {quick_buttons}",
            }

            self.test_results.append(result)
            print(f"  {result['status']} - {result['details']}")

        except Exception as e:
            result = {
                "component": "Quick Analysis",
                "status": "❌ ERROR",
                "screenshot": "None",
                "details": f"Exception: {str(e)}",
            }
            self.test_results.append(result)
            print(f"  {result['status']} - {result['details']}")

    async def test_file_upload(self, page: Page):
        """Test File Upload functionality."""
        print("📁 Testing File Upload...")

        try:
            # Navigate to dashboard
            await page.goto("http://localhost:8501")
            await page.wait_for_load_state("networkidle")

            # Scroll to file upload section
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

            # Take screenshot
            screenshot_path = self.screenshot_dir / "05_file_upload.png"
            await page.screenshot(path=str(screenshot_path))

            # Check for file uploader
            file_uploader = await page.locator("input[type='file']").count()

            result = {
                "component": "File Upload",
                "status": "✅ PASS" if file_uploader > 0 else "❌ FAIL",
                "screenshot": str(screenshot_path),
                "details": f"File uploaders found: {file_uploader}",
            }

            self.test_results.append(result)
            print(f"  {result['status']} - {result['details']}")

        except Exception as e:
            result = {
                "component": "File Upload",
                "status": "❌ ERROR",
                "screenshot": "None",
                "details": f"Exception: {str(e)}",
            }
            self.test_results.append(result)
            print(f"  {result['status']} - {result['details']}")

    async def run_all_tests(self):
        """Run all automated tests."""
        print("🧪 Starting Automated GUI Testing...")

        # Setup GUI
        if not await self.setup_gui():
            print("❌ Failed to launch GUI")
            return

        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                # Run all tests
                await self.test_dashboard(page)
                await self.test_control_flow(page)
                await self.test_uml_generation(page)
                await self.test_quick_analysis(page)
                await self.test_file_upload(page)

            finally:
                await browser.close()

        # Generate test report
        self.generate_report()

        # Cleanup
        self.cleanup()

    def generate_report(self):
        """Generate a comprehensive test report."""
        print("\n" + "=" * 60)
        print("📊 AUTOMATED GUI TEST REPORT")
        print("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if "PASS" in r["status"])
        failed_tests = sum(1 for r in self.test_results if "FAIL" in r["status"])
        error_tests = sum(1 for r in self.test_results if "ERROR" in r["status"])

        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"🚨 Errors: {error_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

        print("\n📋 Detailed Results:")
        for result in self.test_results:
            print(f"  {result['component']}: {result['status']}")
            print(f"    Details: {result['details']}")
            print(f"    Screenshot: {result['screenshot']}")
            print()

        # Save report to file
        report_path = self.screenshot_dir / "test_report.txt"
        with open(report_path, "w") as f:
            f.write("AUTOMATED GUI TEST REPORT\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Total Tests: {total_tests}\n")
            f.write(f"Passed: {passed_tests}\n")
            f.write(f"Failed: {failed_tests}\n")
            f.write(f"Errors: {error_tests}\n")
            f.write(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%\n\n")

            for result in self.test_results:
                f.write(f"{result['component']}: {result['status']}\n")
                f.write(f"  Details: {result['details']}\n")
                f.write(f"  Screenshot: {result['screenshot']}\n\n")

        print(f"📄 Full report saved to: {report_path}")
        print(f"📸 Screenshots saved to: {self.screenshot_dir}")

    def cleanup(self):
        """Clean up resources."""
        if self.gui_process:
            print("🧹 Cleaning up...")
            self.gui_process.terminate()
            self.gui_process.wait()
            print("✅ Cleanup complete")


async def main():
    """Main entry point."""
    tester = AutomatedGUITester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
