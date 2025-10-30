#!/usr/bin/env python3
"""
Deploy Kiro agents to Cloud Run.
Provides hot-swap capability with existing GKE deployment.
"""

import subprocess
import json
import sys
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CloudRunDeployer:
    """Deploy Kiro agents to Cloud Run"""
    
    def __init__(self, project_id: str = "gen-lang-client-0128452200"):
        self.project_id = project_id
        self.region = "us-central1"
        self.service_name = "kiro-agent"
        self.image_name = f"gcr.io/{project_id}/kiro-agent:cloudrun"
        
    def run_command(self, command: list, capture_output: bool = True) -> Dict[str, Any]:
        """Run a command and return results"""
        try:
            logger.info(f"Running: {' '.join(command)}")
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                check=True
            )
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(command)}")
            logger.error(f"Error: {e.stderr}")
            return {
                'success': False,
                'stdout': e.stdout,
                'stderr': e.stderr,
                'returncode': e.returncode
            }
    
    def build_and_push_image(self) -> bool:
        """Build and push Docker image to GCR"""
        logger.info("Building and pushing Docker image...")
        
        # Use gcloud run deploy with source build
        build_cmd = [
            "gcloud", "run", "deploy", self.service_name,
            "--source", ".",
            "--platform", "managed",
            "--region", self.region,
            "--allow-unauthenticated",
            "--memory", "512Mi",
            "--cpu", "1",
            "--concurrency", "100",
            "--timeout", "300",
            "--min-instances", "0",
            "--max-instances", "10",
            "--set-env-vars", "PLATFORM=cloudrun,ENVIRONMENT=production",
            "--port", "8080",
            "--no-traffic"
        ]
        
        result = self.run_command(build_cmd)
        if not result['success']:
            logger.error("Failed to build and deploy image")
            return False
        
        logger.info(f"✅ Image built and deployed: {self.service_name}")
        return True
    
    def create_service_account(self) -> bool:
        """Create service account for Cloud Run"""
        logger.info("Creating service account...")
        
        sa_name = f"{self.service_name}-sa"
        sa_email = f"{sa_name}@{self.project_id}.iam.gserviceaccount.com"
        
        # Check if service account exists
        check_cmd = [
            "gcloud", "iam", "service-accounts", "describe",
            sa_email
        ]
        
        result = self.run_command(check_cmd)
        if result['success']:
            logger.info(f"✅ Service account already exists: {sa_email}")
            return True
        
        # Create service account
        create_cmd = [
            "gcloud", "iam", "service-accounts", "create",
            sa_name,
            "--display-name", "Kiro Agent Service Account",
            "--description", "Service account for Kiro agents on Cloud Run"
        ]
        
        result = self.run_command(create_cmd)
        if not result['success']:
            logger.error("Failed to create service account")
            return False
        
        # Grant necessary permissions
        permissions = [
            "roles/logging.logWriter",
            "roles/monitoring.metricWriter",
            "roles/cloudtrace.agent"
        ]
        
        for permission in permissions:
            grant_cmd = [
                "gcloud", "projects", "add-iam-policy-binding", self.project_id,
                "--member", f"serviceAccount:{sa_email}",
                "--role", permission
            ]
            
            result = self.run_command(grant_cmd)
            if not result['success']:
                logger.warning(f"Failed to grant permission: {permission}")
        
        logger.info(f"✅ Service account created: {sa_email}")
        return True
    
    def deploy_cloud_run_service(self) -> bool:
        """Deploy Cloud Run service"""
        logger.info("Deploying Cloud Run service...")
        
        sa_email = f"{self.service_name}-sa@{self.project_id}.iam.gserviceaccount.com"
        
        deploy_cmd = [
            "gcloud", "run", "deploy", self.service_name,
            "--image", self.image_name,
            "--platform", "managed",
            "--region", self.region,
            "--service-account", sa_email,
            "--allow-unauthenticated",
            "--memory", "512Mi",
            "--cpu", "1",
            "--concurrency", "100",
            "--timeout", "300",
            "--min-instances", "0",
            "--max-instances", "10",
            "--set-env-vars", "PLATFORM=cloudrun,ENVIRONMENT=production",
            "--port", "8080"
        ]
        
        result = self.run_command(deploy_cmd)
        if not result['success']:
            logger.error("Failed to deploy Cloud Run service")
            return False
        
        logger.info("✅ Cloud Run service deployed successfully")
        return True
    
    def get_service_url(self) -> Optional[str]:
        """Get the Cloud Run service URL"""
        cmd = [
            "gcloud", "run", "services", "describe", self.service_name,
            "--region", self.region,
            "--format", "value(status.url)"
        ]
        
        result = self.run_command(cmd)
        if result['success']:
            return result['stdout'].strip()
        return None
    
    def test_deployment(self) -> bool:
        """Test the Cloud Run deployment"""
        logger.info("Testing Cloud Run deployment...")
        
        service_url = self.get_service_url()
        if not service_url:
            logger.error("Could not get service URL")
            return False
        
        # Test health endpoint
        health_url = f"{service_url}/health"
        test_cmd = ["curl", "-f", health_url]
        
        result = self.run_command(test_cmd)
        if not result['success']:
            logger.error("Health check failed")
            return False
        
        # Test info endpoint
        info_url = f"{service_url}/info"
        test_cmd = ["curl", "-f", info_url]
        
        result = self.run_command(test_cmd)
        if not result['success']:
            logger.error("Info endpoint test failed")
            return False
        
        logger.info("✅ Cloud Run deployment tests passed")
        return True
    
    def deploy(self) -> bool:
        """Complete deployment process"""
        logger.info("🚀 Starting Cloud Run deployment for Kiro agents...")
        
        steps = [
            ("Build and deploy Cloud Run service", self.build_and_push_image),
            ("Create service account", self.create_service_account),
            ("Test deployment", self.test_deployment)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"📋 {step_name}...")
            if not step_func():
                logger.error(f"❌ {step_name} failed")
                return False
            logger.info(f"✅ {step_name} completed")
        
        service_url = self.get_service_url()
        logger.info(f"🎉 Cloud Run deployment completed successfully!")
        logger.info(f"🌐 Service URL: {service_url}")
        logger.info(f"🔗 Health check: {service_url}/health")
        logger.info(f"📊 Metrics: {service_url}/metrics")
        
        return True
    
    def get_deployment_status(self) -> Dict[str, Any]:
        """Get deployment status"""
        cmd = [
            "gcloud", "run", "services", "describe", self.service_name,
            "--region", self.region,
            "--format", "json"
        ]
        
        result = self.run_command(cmd)
        if result['success']:
            try:
                return json.loads(result['stdout'])
            except json.JSONDecodeError:
                return {'error': 'Failed to parse service description'}
        else:
            return {'error': 'Failed to get service description'}

def main():
    """Main deployment function"""
    deployer = CloudRunDeployer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        # Show deployment status
        status = deployer.get_deployment_status()
        print(json.dumps(status, indent=2))
        return
    
    # Run full deployment
    success = deployer.deploy()
    
    if success:
        print("\n🎉 Cloud Run deployment completed successfully!")
        print("🔄 Hot-swap capability is now available between GKE and Cloud Run")
        sys.exit(0)
    else:
        print("\n❌ Cloud Run deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
