#!/usr/bin/env python3
"""
Cloud Run implementation of Kiro agent.
Implements the common interface for serverless deployment.
"""

import os
import logging
from flask import Flask, request, jsonify
from typing import Dict, Any, Optional
from datetime import datetime
import json

# Import the common interface
from ..common.interface import (
    KiroAgentInterface, 
    KiroRequest, 
    KiroResponse, 
    KiroMetrics,
    create_kiro_request_from_flask,
    create_flask_response_from_kiro,
    log_request
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CloudRunKiroAgent(KiroAgentInterface):
    """Cloud Run implementation of Kiro agent"""
    
    def __init__(self):
        self.platform = 'cloudrun'
        self.app = Flask(__name__)
        self.setup_routes()
        self.logger = logging.getLogger(f"{__name__}.cloudrun")
        
        # Cloud Run specific configuration
        self.service_name = os.environ.get('K_SERVICE', 'kiro-agent')
        self.revision_name = os.environ.get('K_REVISION', 'kiro-agent-v1')
        self.project_id = os.environ.get('GCP_PROJECT_ID', 'aardvark-linkedin-grepper')
        
        self.logger.info(f"Initialized Cloud Run Kiro Agent: {self.service_name}")
    
    def setup_routes(self):
        """Setup Flask routes for Cloud Run"""
        self.app.route('/analyze', methods=['POST'])(self.analyze_endpoint)
        self.app.route('/health', methods=['GET'])(self.health_endpoint)
        self.app.route('/metrics', methods=['GET'])(self.metrics_endpoint)
        self.app.route('/info', methods=['GET'])(self.info_endpoint)
        self.app.route('/', methods=['GET'])(self.root_endpoint)
    
    def analyze_endpoint(self):
        """Cloud Run analyze endpoint"""
        try:
            kiro_request = create_kiro_request_from_flask(request)
            response = self.process_request(kiro_request)
            
            # Log the request for monitoring
            log_request(self.platform, kiro_request, response)
            
            return create_flask_response_from_kiro(response)
            
        except Exception as e:
            self.logger.error(f"Error in analyze endpoint: {e}")
            error_response = self.create_error_response(str(e), 500)
            return create_flask_response_from_kiro(error_response)
    
    def health_endpoint(self):
        """Cloud Run health check endpoint"""
        try:
            health_data = self.health_check()
            return jsonify(health_data), 200
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return jsonify({'status': 'unhealthy', 'error': str(e)}), 500
    
    def metrics_endpoint(self):
        """Cloud Run metrics endpoint"""
        try:
            metrics = self.get_metrics()
            return jsonify({
                'platform': metrics.platform,
                'instance_id': metrics.instance_id,
                'timestamp': metrics.timestamp,
                'request_count': metrics.request_count,
                'error_count': metrics.error_count,
                'avg_response_time': metrics.avg_response_time,
                'memory_usage': metrics.memory_usage,
                'cpu_usage': metrics.cpu_usage
            }), 200
        except Exception as e:
            self.logger.error(f"Metrics collection failed: {e}")
            return jsonify({'error': str(e)}), 500
    
    def info_endpoint(self):
        """Cloud Run info endpoint"""
        try:
            info = self.get_platform_info()
            return jsonify(info), 200
        except Exception as e:
            self.logger.error(f"Info collection failed: {e}")
            return jsonify({'error': str(e)}), 500
    
    def root_endpoint(self):
        """Root endpoint for Cloud Run"""
        return jsonify({
            'service': 'kiro-agent',
            'platform': 'cloudrun',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'analyze': '/analyze',
                'health': '/health',
                'metrics': '/metrics',
                'info': '/info'
            }
        }), 200
    
    def process_request(self, request: KiroRequest) -> KiroResponse:
        """Process Kiro agent request for Cloud Run"""
        try:
            # Validate request
            if not self.validate_request(request):
                return self.create_error_response("Invalid request", 400)
            
            # Perform analysis using common logic
            result = self.analyze_data(request.data)
            
            # Create success response
            return self.create_success_response(result)
            
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return self.create_error_response(str(e), 500)
    
    def health_check(self) -> Dict[str, Any]:
        """Health check for Cloud Run"""
        try:
            # Cloud Run specific health checks
            health_status = {
                'status': 'healthy',
                'platform': 'cloudrun',
                'service_name': self.service_name,
                'revision_name': self.revision_name,
                'project_id': self.project_id,
                'timestamp': datetime.utcnow().isoformat(),
                'checks': {
                    'service_available': True,
                    'memory_usage': self._get_memory_usage(),
                    'cpu_usage': self._get_cpu_usage(),
                    'request_count': self.request_count,
                    'error_count': self.error_count
                }
            }
            
            # Check if we're within Cloud Run limits
            if health_status['checks']['memory_usage'] > 0.9:
                health_status['status'] = 'warning'
                health_status['warnings'] = ['High memory usage']
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return {
                'status': 'unhealthy',
                'platform': 'cloudrun',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def get_metrics(self) -> KiroMetrics:
        """Get Cloud Run-specific metrics"""
        try:
            return KiroMetrics(
                platform='cloudrun',
                instance_id=self._get_instance_id(),
                timestamp=datetime.utcnow().isoformat(),
                request_count=self.request_count,
                error_count=self.error_count,
                avg_response_time=self._get_avg_response_time(),
                memory_usage=self._get_memory_usage(),
                cpu_usage=self._get_cpu_usage()
            )
        except Exception as e:
            self.logger.error(f"Metrics collection failed: {e}")
            # Return default metrics on error
            return KiroMetrics(
                platform='cloudrun',
                instance_id='unknown',
                timestamp=datetime.utcnow().isoformat(),
                request_count=0,
                error_count=1,
                avg_response_time=0.0,
                memory_usage=0.0,
                cpu_usage=0.0
            )
    
    def _get_instance_id(self) -> str:
        """Get Cloud Run instance ID"""
        # Cloud Run provides instance ID via environment variable
        return os.environ.get('K_REVISION', 'unknown')
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage (simplified)"""
        try:
            import psutil
            return psutil.virtual_memory().percent / 100.0
        except ImportError:
            # Fallback if psutil not available
            return 0.0
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage (simplified)"""
        try:
            import psutil
            return psutil.cpu_percent() / 100.0
        except ImportError:
            # Fallback if psutil not available
            return 0.0
    
    def _get_avg_response_time(self) -> float:
        """Get average response time"""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    def run(self, host='0.0.0.0', port=8080):
        """Run the Cloud Run agent"""
        port = int(os.environ.get('PORT', port))
        self.logger.info(f"Starting Cloud Run Kiro Agent on {host}:{port}")
        self.app.run(host=host, port=port, debug=False)

# Cloud Run entry point
if __name__ == '__main__':
    agent = CloudRunKiroAgent()
    agent.run()
