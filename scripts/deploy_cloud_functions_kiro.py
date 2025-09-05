#!/usr/bin/env python3
"""
Deploy Kiro Agent as Cloud Functions - RM Compliant
Simple, focused deployment script
"""

import subprocess
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudFunctionDeployer:
    """Simple Cloud Function deployer for Kiro agents"""
    
    def __init__(self):
        self.function_name = "kiro-agent-function"
        self.region = "us-central1"
        self.runtime = "python311"
        self.entry_point = "kiro_agent_http"
        self.source_dir = "src/kiro_agents/cloud_functions"
        
    def run_command(self, cmd: list) -> Dict[str, Any]:
        """Run a command and return result"""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "stdout": e.stdout,
                "stderr": e.stderr,
                "returncode": e.returncode
            }
    
    def deploy_function(self) -> bool:
        """Deploy the Cloud Function"""
        logger.info(f"🚀 Deploying Cloud Function: {self.function_name}")
        
        deploy_cmd = [
            "gcloud", "functions", "deploy", self.function_name,
            "--gen2",
            "--runtime", self.runtime,
            "--source", self.source_dir,
            "--entry-point", self.entry_point,
            "--region", self.region,
            "--trigger-http",
            "--allow-unauthenticated",
            "--memory", "256MB",
            "--timeout", "60s",
            "--max-instances", "10"
        ]
        
        result = self.run_command(deploy_cmd)
        if not result['success']:
            logger.error(f"❌ Deployment failed: {result['stderr']}")
            return False
        
        logger.info(f"✅ Cloud Function deployed successfully!")
        logger.info(f"Function URL: https://{self.region}-{self.function_name}.cloudfunctions.net/")
        return True
    
    def test_function(self) -> bool:
        """Test the deployed function"""
        logger.info("🧪 Testing Cloud Function...")
        
        # Get function URL
        url_cmd = [
            "gcloud", "functions", "describe", self.function_name,
            "--region", self.region,
            "--format", "value(serviceConfig.uri)"
        ]
        
        result = self.run_command(url_cmd)
        if not result['success']:
            logger.error(f"❌ Failed to get function URL: {result['stderr']}")
            return False
        
        function_url = result['stdout'].strip()
        logger.info(f"Function URL: {function_url}")
        
        # Test health check
        test_cmd = ["curl", "-f", f"{function_url}"]
        test_result = self.run_command(test_cmd)
        
        if test_result['success']:
            logger.info("✅ Health check passed!")
            return True
        else:
            logger.error(f"❌ Health check failed: {test_result['stderr']}")
            return False
    
    def deploy(self) -> bool:
        """Complete deployment process"""
        logger.info("🚀 Starting Cloud Function deployment for Kiro agents...")
        
        steps = [
            ("Deploy Cloud Function", self.deploy_function),
            ("Test deployment", self.test_function)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"📋 {step_name}...")
            if not step_func():
                logger.error(f"❌ {step_name} failed")
                return False
        
        logger.info("✅ Cloud Function deployment completed successfully!")
        return True

if __name__ == "__main__":
    deployer = CloudFunctionDeployer()
    success = deployer.deploy()
    exit(0 if success else 1)
