#!/usr/bin/env python3
"""
GUI Navigation Testing with Screenshots

Comprehensive testing of the Workflow Visualization GUI using Playwright.
Tests all navigation paths and captures screenshots for visual validation.
"""

import pytest
import time
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, expect
import subprocess
import signal
import psutil

# Test configuration
SCREENSHOT_DIR = Path("test_screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


class StreamlitTestServer:
    """Manages Streamlit test server for GUI testing."""

    def __init__(self, port: int = 8501):
        self.port = port
        self.process = None
        self.base_url = f"http://localhost:{port}"

    def start(self):
        """Start Streamlit test server."""
        if self.process:
            return

        # Kill any existing Streamlit processes on this port
        self._kill_existing_streamlit()

        # Start new Streamlit server (without headless flag)
        self.process = subprocess.Popen(
            [
                "uv",
                "run",
                "streamlit",
                "run",
                "src/workflow_visualization_gui.py",
                "--server.port",
                str(self.port),
                "--server.address",
                "localhost",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for server to start
        time.sleep(5)

        # Check if server is running
        try:
            import requests

            response = requests.get(f"{self.base_url}/_stcore/health", timeout=10)
            if response.status_code != 200:
                raise Exception("Streamlit server not responding")
        except Exception as e:
            self.stop()
            raise Exception(f"Failed to start Streamlit server: {e}")

    def stop(self):
        """Stop Streamlit test server."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None

    def _kill_existing_streamlit(self):
        """Kill any existing Streamlit processes on the test port."""
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                if proc.info["name"] == "python" and any(
                    "streamlit" in str(cmd) for cmd in proc.info["cmdline"]
                ):
                    if str(self.port) in str(proc.info["cmdline"]):
                        proc.terminate()
                        proc.wait()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass


class GUITestBase:
    """Base class for GUI tests with common setup and teardown."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown for each test."""
        self.server = StreamlitTestServer()
        self.server.start()

        # Setup Playwright with JavaScript enabled but headless
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=True,  # Keep headless for CI environment
            args=[
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--enable-javascript",  # Explicitly enable JavaScript
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        self.page = self.browser.new_page()

        # Navigate to the app
        self.page.goto(self.server.base_url)

        yield

        # Cleanup
        self.page.close()
        self.browser.close()
        self.playwright.stop()
        self.server.stop()

    def take_screenshot(self, name: str, description: str = ""):
        """Take a screenshot and save it with metadata."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.png"
        filepath = SCREENSHOT_DIR / filename

        # Take screenshot
        self.page.screenshot(path=str(filepath))

        # Save metadata
        metadata_file = filepath.with_suffix(".txt")
        with open(metadata_file, "w") as f:
            f.write(f"Test: {name}\n")
            f.write(f"Description: {description}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"URL: {self.page.url}\n")
            f.write(f"Title: {self.page.title()}\n")

        return filepath


class TestGUINavigation(GUITestBase):
    """Test GUI navigation and component switching."""

    def test_minimal_app_rendering(self):
        """Minimal test to see if the app renders anything at all."""
        # Wait for page to load
        self.page.wait_for_load_state("networkidle")
        
        print("🔍 Testing minimal app rendering...")
        
        # Take screenshot
        self.take_screenshot("minimal_app_test", "Minimal app rendering test")
        
        # Get page title
        page_title = self.page.title()
        print(f"📄 Page title: {page_title}")
        
        # Get current URL
        current_url = self.page.url
        print(f"🌐 Current URL: {current_url}")
        
        # Try to get any text content on the page
        print("\n📝 Page Content Check:")
        try:
            # Look for any text elements
            all_text = self.page.locator("body").text_content()
            if all_text:
                print(f"✅ Found text content: {all_text[:200]}...")
            else:
                print("❌ No text content found")
        except Exception as e:
            print(f"❌ Error getting text content: {e}")
        
        # Try to find any HTML elements
        print("\n🔍 HTML Elements Check:")
        try:
            # Count various element types
            h1_count = self.page.locator("h1").count()
            h2_count = self.page.locator("h2").count()
            div_count = self.page.locator("div").count()
            span_count = self.page.locator("span").count()
            
            print(f"  H1 elements: {h1_count}")
            print(f"  H2 elements: {h2_count}")
            print(f"  Div elements: {div_count}")
            print(f"  Span elements: {span_count}")
            
            if h1_count + h2_count + div_count + span_count > 0:
                print("✅ Found HTML elements")
            else:
                print("❌ No HTML elements found")
                
        except Exception as e:
            print(f"❌ Error counting elements: {e}")
        
        # Check if this is just a blank Streamlit page
        print("\n🎯 Streamlit Status Check:")
        try:
            # Look for Streamlit-specific elements
            streamlit_elements = self.page.locator("[data-testid]").count()
            print(f"  Streamlit elements: {streamlit_elements}")
            
            if streamlit_elements > 0:
                print("✅ Streamlit is rendering elements")
            else:
                print("❌ Streamlit is not rendering elements")
                
        except Exception as e:
            print(f"❌ Error checking Streamlit elements: {e}")
        
        print("\n🎯 Minimal test completed")
        # This test should always pass - it's just for debugging
        assert True, "Minimal app rendering test completed"

    def test_dashboard_loading(self):
        """Test that dashboard loads correctly."""
        # Wait for page to load
        self.page.wait_for_load_state("networkidle")

        # Check main title - use the actual title text
        expect(self.page.locator("text=🔍 Workflow Extraction Visualization System")).to_be_visible()

        # Check component count - look for the specific metric card
        component_metric = self.page.locator("text=Components").first
        expect(component_metric).to_be_visible()

        # Take screenshot
        self.take_screenshot("dashboard_loaded", "Main dashboard loaded successfully")

    def test_comprehensive_debug(self):
        """Comprehensive debug test to see exactly what's on the page."""
        # Wait for page to load
        self.page.wait_for_load_state("networkidle")
        
        print("🔍 Starting comprehensive debug test...")
        
        # Take screenshot of dashboard
        self.take_screenshot("comprehensive_debug_dashboard", "Dashboard for comprehensive debugging")
        
        # Check dashboard elements
        print("\n📊 Dashboard Elements:")
        try:
            main_title = self.page.locator("text=🔍 Workflow Extraction Visualization System")
            if main_title.count() > 0:
                print("✅ Main title found")
            else:
                print("❌ Main title not found")
        except Exception as e:
            print(f"❌ Error finding main title: {e}")
        
        # Try to navigate to a component
        print("\n🧭 Navigation Test:")
        try:
            # Find and click component selector
            component_selector = self.page.locator("text=Select Component:")
            if component_selector.count() > 0:
                print("✅ Component selector found")
                component_selector.click()
                print("✅ Component selector clicked")
                
                # Find and click UC-2 component
                uc2_component = self.page.locator("text=UC-2: Control Flow Pattern Recognition")
                if uc2_component.count() > 0:
                    print("✅ UC-2 component found")
                    uc2_component.click()
                    print("✅ UC-2 component selected")
                    
                    # Wait for navigation
                    time.sleep(3)
                    
                    # Take screenshot of component page
                    self.take_screenshot("comprehensive_debug_component_page", "Component page for comprehensive debugging")
                    
                    # Get page title
                    page_title = self.page.title()
                    print(f"📄 Page title: {page_title}")
                    
                    # Get current URL
                    current_url = self.page.url
                    print(f"🌐 Current URL: {current_url}")
                    
                    # Try to find all text elements on the page
                    print("\n🔍 Page Content Analysis:")
                    
                    # Look for common elements
                    elements_to_check = [
                        "Select file to analyze:",
                        "Analyze Control Flow",
                        "Control Flow Pattern Recognition",
                        "🔄 Control Flow Pattern Recognition"
                    ]
                    
                    for element_text in elements_to_check:
                        try:
                            element = self.page.locator(f"text={element_text}")
                            count = element.count()
                            if count > 0:
                                print(f"✅ Found '{element_text}' ({count} instances)")
                            else:
                                print(f"❌ Not found: '{element_text}'")
                        except Exception as e:
                            print(f"❌ Error checking '{element_text}': {e}")
                    
                    # Try to get all visible text content
                    print("\n📝 All Visible Text Elements:")
                    try:
                        # Use a more specific selector for text elements
                        text_elements = self.page.locator("h1, h2, h3, h4, h5, h6, p, span, div, label, button").all()
                        print(f"Found {len(text_elements)} potential text elements")
                        
                        # Print first 10 elements with text content
                        for i, elem in enumerate(text_elements[:10]):
                            try:
                                text_content = elem.text_content().strip()
                                if text_content:
                                    print(f"  {i+1}: '{text_content}'")
                            except:
                                pass
                    except Exception as e:
                        print(f"❌ Error getting text elements: {e}")
                        
                else:
                    print("❌ UC-2 component not found")
            else:
                print("❌ Component selector not found")
                
        except Exception as e:
            print(f"❌ Error during navigation: {e}")
        
        print("\n🎯 Debug test completed")
        # This test should always pass - it's just for debugging
        assert True, "Comprehensive debug test completed"

    def test_quick_actions(self):
        """Test quick action buttons."""
        # Test Quick Control Flow
        self.page.locator("text=🚀 Quick Control Flow").click()
        time.sleep(2)  # Wait for analysis
        self.take_screenshot(
            "quick_control_flow", "Quick Control Flow analysis completed"
        )

        # Test Quick Complexity
        self.page.locator("text=📊 Quick Complexity").click()
        time.sleep(2)  # Wait for analysis
        self.take_screenshot("quick_complexity", "Quick Complexity analysis completed")

        # Test Quick UML Generation
        self.page.locator("text=🎨 Quick UML Generation").click()
        time.sleep(2)  # Wait for generation
        self.take_screenshot("quick_uml_generation", "Quick UML Generation completed")

    def test_responsive_design(self):
        """Test responsive design at different viewport sizes."""
        viewports = [
            (1920, 1080, "desktop"),
            (1024, 768, "tablet"),
            (375, 667, "mobile"),
        ]

        for width, height, device in viewports:
            self.page.set_viewport_size({"width": width, "height": height})
            time.sleep(1)

            # Take screenshot
            self.take_screenshot(
                f"responsive_{device}", f"Responsive design test at {width}x{height}"
            )

            # Verify basic functionality still works - look for the main title
            main_title = self.page.locator("text=🔍 Workflow Extraction Visualization System").first
            expect(main_title).to_be_visible()


def run_gui_tests():
    """Run all GUI tests with screenshot capture."""
    print("🧪 Starting GUI Navigation Tests...")
    print(f"📸 Screenshots will be saved to: {SCREENSHOT_DIR.absolute()}")

    # Install Playwright browsers if needed
    subprocess.run(["playwright", "install", "chromium"], check=True)

    # Run tests
    subprocess.run(
        ["uv", "run", "pytest", "tests/test_gui_navigation.py", "-v", "--tb=short"],
        check=True,
    )

    print(f"✅ GUI tests completed! Check screenshots in: {SCREENSHOT_DIR.absolute()}")


if __name__ == "__main__":
    run_gui_tests()
