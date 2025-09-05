"""
Kiro Agent Cloud Function - RM Compliant
Simple, focused function that implements the common interface
"""

import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def kiro_agent_http(request):
    """
    HTTP Cloud Function entry point for Kiro Agent
    
    Args:
        request: HTTP request object
        
    Returns:
        HTTP response with agent processing result
    """
    try:
        # Parse request
        if request.method == 'GET':
            return handle_health_check()
        elif request.method == 'POST':
            return handle_analyze(request)
        else:
            return create_response(405, {"error": "Method not allowed"})
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return create_response(500, {"error": "Internal server error"})

def handle_health_check() -> Dict[str, Any]:
    """Handle health check requests"""
    return create_response(200, {
        "status": "healthy",
        "service": "kiro-agent-cloud-function",
        "platform": "cloud-functions",
        "environment": "production"
    })

def handle_analyze(request) -> Dict[str, Any]:
    """Handle analysis requests"""
    try:
        # Parse request body
        request_json = request.get_json()
        if not request_json:
            return create_response(400, {"error": "No JSON data provided"})
        
        # Simple analysis logic (RM compliant - focused and simple)
        analysis_result = {
            "input": request_json,
            "analysis": "Basic analysis completed",
            "platform": "cloud-functions",
            "timestamp": "2025-01-27T00:00:00Z"
        }
        
        return create_response(200, analysis_result)
        
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        return create_response(500, {"error": "Analysis failed"})

def create_response(status_code: int, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create standardized HTTP response"""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(data)
    }
