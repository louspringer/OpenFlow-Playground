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
        
        # Start new Streamlit server
        self.process = subprocess.Popen([
            "uv", "run", "streamlit", "run", 
            "src/workflow_visualization_gui.py",
            "--server.port", str(self.port),
            "--server.address", "localhost",
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
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
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'python' and any('streamlit' in str(cmd) for cmd in proc.info['cmdline']):
                    if str(self.port) in str(proc.info['cmdline']):
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
        
        # Setup Playwright
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
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
        metadata_file = filepath.with_suffix('.txt')
        with open(metadata_file, 'w') as f:
            f.write(f"Test: {name}\n")
            f.write(f"Description: {description}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"URL: {self.page.url}\n")
            f.write(f"Title: {self.page.title()}\n")
        
        return filepath

class TestGUINavigation(GUITestBase):
    """Test GUI navigation and component switching."""
    
    def test_dashboard_loading(self):
        """Test that dashboard loads correctly."""
        # Wait for page to load
        self.page.wait_for_load_state("networkidle")
        
        # Check main title - use the main content area, not sidebar
        main_title = self.page.locator("#workflow-extraction-visualization-system")
        expect(main_title).to_contain_text("Workflow Extraction Visualization")
        
        # Check component count
        component_count = self.page.locator("text=Components").count()
        assert component_count > 0
        
        # Take screenshot
        self.take_screenshot("dashboard_loaded", "Main dashboard loaded successfully")
    
    def test_sidebar_navigation(self):
        """Test sidebar navigation between components."""
        # Test each component navigation
        components = [
            "UC-1: Function Call Chain Analysis",
            "UC-2: Control Flow Pattern Recognition", 
            "UC-3: Method Workflow Extraction",
            "UC-4: UML Activity Diagram Generation",
            "UC-5: Code Complexity Metrics",
            "UC-6: Multi-File Workflow Analysis",
            "UC-7: Round-Trip Validation Framework",
            "UC-9: Performance Optimization"
        ]
        
        for component in components:
            # Select component from sidebar
            self.page.locator("text=Select Component:").click()
            self.page.locator(f"text={component}").click()
            
            # Wait for component page to load
            self.page.wait_for_load_state("networkidle")
            
            # Verify component title is displayed - use the main content area
            main_content = self.page.locator("main")
            expect(main_content).to_contain_text(component.split(":")[0])
            
            # Take screenshot
            self.take_screenshot(f"component_{component.split(':')[0].lower()}", 
                               f"Navigated to {component}")
            
            # Go back to dashboard
            self.page.locator("text=🏠 Back to Dashboard").click()
            self.page.wait_for_load_state("networkidle")
    
    def test_quick_actions(self):
        """Test quick action buttons."""
        # Test Quick Control Flow
        self.page.locator("text=🚀 Quick Control Flow").click()
        time.sleep(2)  # Wait for analysis
        self.take_screenshot("quick_control_flow", "Quick Control Flow analysis completed")
        
        # Test Quick Complexity
        self.page.locator("text=📊 Quick Complexity").click()
        time.sleep(2)  # Wait for analysis
        self.take_screenshot("quick_complexity", "Quick Complexity analysis completed")
        
        # Test Quick UML Generation
        self.page.locator("text=🎨 Quick UML Generation").click()
        time.sleep(2)  # Wait for generation
        self.take_screenshot("quick_uml_generation", "Quick UML Generation completed")
    
    def test_file_selection(self):
        """Test file selection in component pages."""
        # Navigate to UC-2 (Control Flow)
        self.page.locator("text=Select Component:").click()
        self.page.locator("text=UC-2: Control Flow Pattern Recognition").click()
        self.page.wait_for_load_state("networkidle")
        
        # Check file selection dropdown - use the specific key for this component
        file_dropdown = self.page.locator('[data-testid="stSelectbox"]').first
        expect(file_dropdown).to_be_visible()
        
        # Select a test file
        file_dropdown.click()
        self.page.locator("text=src/enhanced_activity_generator.py").click()
        
        # Take screenshot
        self.take_screenshot("file_selection", "File selection working in component page")
    
    def test_analysis_execution(self):
        """Test actual analysis execution."""
        # Navigate to UC-2
        self.page.locator("text=Select Component:").click()
        self.page.locator("text=UC-2: Control Flow Pattern Recognition").click()
        self.page.wait_for_load_state("networkidle")
        
        # Select test file
        file_dropdown = self.page.locator('[data-testid="stSelectbox"]').first
        file_dropdown.click()
        self.page.locator("text=src/enhanced_activity_generator.py").click()
        
        # Click analyze button - use the specific key for this component
        self.page.locator("text=Analyze Control Flow").click()
        
        # Wait for analysis to complete
        self.page.wait_for_selector("text=✅ Control flow analysis completed!", timeout=30000)
        
        # Take screenshot of results
        self.take_screenshot("analysis_results", "Control flow analysis completed with results")
        
        # Verify results are displayed
        expect(self.page.locator("text=📊 Patterns")).to_be_visible()
        expect(self.page.locator("text=📈 Metrics")).to_be_visible()
        expect(self.page.locator("text=🔍 Details")).to_be_visible()
    
    def test_uml_generation(self):
        """Test UML diagram generation."""
        # Navigate to UC-4
        self.page.locator("text=Select Component:").click()
        self.page.locator("text=UC-4: UML Activity Diagram Generation").click()
        self.page.wait_for_load_state("networkidle")
        
        # Select test file
        file_dropdown = self.page.locator('[data-testid="stSelectbox"]').first
        file_dropdown.click()
        self.page.locator("text=src/enhanced_activity_generator.py").click()
        
        # Set output name
        self.page.locator("text=Output name (without extension):").fill("test_uml_generation")
        
        # Generate UML diagrams
        self.page.locator("text=Generate UML Diagrams").click()
        
        # Wait for generation to complete
        self.page.wait_for_selector("text=✅ UML generation completed!", timeout=60000)
        
        # Take screenshot of results
        self.take_screenshot("uml_generation", "UML diagram generation completed")
        
        # Verify diagram files are listed
        expect(self.page.locator("text=📋 Generated UML Diagrams")).to_be_visible()
    
    def test_error_handling(self):
        """Test error handling and fallbacks."""
        # Navigate to a component page
        self.page.locator("text=Select Component:").click()
        self.page.locator("text=UC-2: Control Flow Pattern Recognition").click()
        self.page.wait_for_load_state("networkidle")
        
        # Try to analyze without selecting a file
        self.page.locator("text=Analyze Control Flow").click()
        
        # Wait for error or success
        time.sleep(3)
        
        # Take screenshot
        self.take_screenshot("error_handling", "Error handling test")
    
    def test_responsive_design(self):
        """Test responsive design at different viewport sizes."""
        viewports = [
            (1920, 1080, "desktop"),
            (1024, 768, "tablet"),
            (375, 667, "mobile")
        ]
        
        for width, height, device in viewports:
            self.page.set_viewport_size({"width": width, "height": height})
            time.sleep(1)
            
            # Take screenshot
            self.take_screenshot(f"responsive_{device}", f"Responsive design test at {width}x{height}")
            
            # Verify basic functionality still works - use main content area
            main_content = self.page.locator("main")
            expect(main_content).to_be_visible()

class TestGUIComponents(GUITestBase):
    """Test individual GUI components and their functionality."""
    
    def test_control_flow_analyzer_page(self):
        """Test UC-2 Control Flow Analyzer page."""
        self.page.locator("text=Select Component:").click()
        self.page.locator("text=UC-2: Control Flow Pattern Recognition").click()
        self.page.wait_for_load_state("networkidle")
        
        # Test file selection
        file_dropdown = self.page.locator('[data-testid="stSelectbox"]').first
        file_dropdown.click()
        self.page.locator("text=src/enhanced_activity_generator.py").click()
        
        # Test analysis execution
        self.page.locator("text=Analyze Control Flow").click()
        self.page.wait_for_selector("text=✅ Control flow analysis completed!", timeout=30000)
        
        # Test results display
        self.page.locator("text=📊 Patterns").click()
        time.sleep(1)
        self.take_screenshot("control_flow_patterns", "Control flow patterns tab")
        
        self.page.locator("text=📈 Metrics").click()
        time.sleep(1)
        self.take_screenshot("control_flow_metrics", "Control flow metrics tab")
        
        self.page.locator("text=🔍 Details").click()
        time.sleep(1)
        self.take_screenshot("control_flow_details", "Control flow details tab")
    
    def test_complexity_analyzer_page(self):
        """Test UC-5 Code Complexity Metrics page."""
        self.page.locator("text=Select Component:").click()
        self.page.locator("text=UC-5: Code Complexity Metrics").click()
        self.page.wait_for_load_state("networkidle")
        
        # Test file selection
        file_dropdown = self.page.locator('[data-testid="stSelectbox"]').first
        file_dropdown.click()
        self.page.locator("text=src/enhanced_activity_generator.py").click()
        
        # Test analysis execution
        self.page.locator("text=Analyze Complexity").click()
        self.page.wait_for_selector("text=✅ Complexity analysis completed!", timeout=30000)
        
        # Test results display
        self.page.locator("text=📊 Overview").click()
        time.sleep(1)
        self.take_screenshot("complexity_overview", "Complexity overview tab")
        
        self.page.locator("text=📈 Metrics").click()
        time.sleep(1)
        self.take_screenshot("complexity_metrics", "Complexity metrics tab")
        
        self.page.locator("text=🔍 Distribution").click()
        time.sleep(1)
        self.take_screenshot("complexity_distribution", "Complexity distribution tab")

def run_gui_tests():
    """Run all GUI tests with screenshot capture."""
    print("🧪 Starting GUI Navigation Tests...")
    print(f"📸 Screenshots will be saved to: {SCREENSHOT_DIR.absolute()}")
    
    # Install Playwright browsers if needed
    subprocess.run(["playwright", "install", "chromium"], check=True)
    
    # Run tests
    subprocess.run([
        "uv", "run", "pytest", 
        "tests/test_gui_navigation.py", 
        "-v", 
        "--tb=short"
    ], check=True)
    
    print(f"✅ GUI tests completed! Check screenshots in: {SCREENSHOT_DIR.absolute()}")

if __name__ == "__main__":
    run_gui_tests()
