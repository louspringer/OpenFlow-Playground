#!/usr/bin/env python3
"""
Python Wrapper for Node.js PlantUML Client

This module provides a Python interface to the Node.js PlantUML client,
combining the reliability of Node.js with the convenience of Python.
"""

import json
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NodePlantUMLWrapper:
    """
    Python wrapper for the Node.js PlantUML client.
    
    This wrapper provides a Python interface to the reliable Node.js
    PlantUML client, bypassing issues with the Python PlantUML library.
    """
    
    def __init__(self, node_client_path: str = "src/plantuml_client_node.js"):
        """
        Initialize the Node.js PlantUML wrapper.
        
        Args:
            node_client_path: Path to the Node.js PlantUML client
        """
        self.node_client_path = Path(node_client_path)
        if not self.node_client_path.exists():
            raise FileNotFoundError(f"Node.js client not found: {node_client_path}")
        
        logger.info(f"🎨 Node.js PlantUML wrapper initialized with client: {node_client_path}")
    
    def test_connection(self) -> bool:
        """
        Test the connection to the PlantUML server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            result = subprocess.run(
                ["node", str(self.node_client_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and "✅ PlantUML server connection successful" in result.stdout:
                logger.info("✅ Node.js PlantUML client connection test passed")
                return True
            else:
                logger.error(f"❌ Node.js PlantUML client connection test failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Node.js PlantUML client test failed: {e}")
            return False
    
    def generate_diagram(self, plantuml_code: str, output_path: str, 
                         format: str = "svg") -> Optional[str]:
        """
        Generate a diagram from PlantUML code using Node.js client.
        
        Args:
            plantuml_code: PlantUML source code
            output_path: Path to save the generated diagram
            format: Output format (png, svg, etc.)
            
        Returns:
            Path to generated diagram file, or None if failed
        """
        try:
            logger.info(f"🔄 Generating {format.upper()} diagram using Node.js client...")
            
            # Create a temporary Node.js script that embeds the PlantUML code
            node_script = f"""
const http = require('http');
const https = require('https');
const fs = require('fs');
const {{ URL }} = require('url');

class SimplePlantUMLClient {{
    constructor(serverUrl = 'http://localhost:20075') {{
        this.serverUrl = serverUrl.replace(/\\/$/, '');
    }}
    
    async generateDiagram(plantumlCode, outputPath) {{
        try {{
            // Encode the PlantUML code
            const encodedCode = encodeURIComponent(plantumlCode);
            
            // Construct the URL
            const url = `${{this.serverUrl}}/uml/${{encodedCode}}`;
            
            // Make the HTTP request
            const response = await this.makeHttpRequest(url);
            
            if (response.statusCode === 200 && response.data.length > 0) {{
                // Save the diagram
                fs.writeFileSync(outputPath, response.data);
                console.log('SUCCESS:' + outputPath);
                return outputPath;
            }} else {{
                console.log('FAILED:HTTP request failed');
                return null;
            }}
            
        }} catch (error) {{
            console.log('ERROR:' + error.message);
            return null;
        }}
    }}
    
    makeHttpRequest(url) {{
        return new Promise((resolve, reject) => {{
            const urlObj = new URL(url);
            const isHttps = urlObj.protocol === 'https:';
            const client = isHttps ? https : http;
            
            const options = {{
                hostname: urlObj.hostname,
                port: urlObj.port || (isHttps ? 443 : 80),
                path: urlObj.pathname + urlObj.search,
                method: 'GET',
                timeout: 30000
            }};
            
            const req = client.request(options, (res) => {{
                let data = [];
                
                res.on('data', (chunk) => {{
                    data.push(chunk);
                }});
                
                res.on('end', () => {{
                    const buffer = Buffer.concat(data);
                    
                    // Handle redirects
                    if (res.statusCode === 302 || res.statusCode === 301) {{
                        const location = res.headers.location;
                        if (location) {{
                            // Follow the redirect
                            this.makeHttpRequest(location)
                                .then(resolve)
                                .catch(reject);
                            return;
                        }}
                    }}
                    
                    resolve({{
                        statusCode: res.statusCode,
                        data: buffer
                    }});
                }});
            }});
            
            req.on('error', (error) => {{
                reject(error);
            }});
            
            req.on('timeout', () => {{
                req.destroy();
                reject(new Error('Request timeout'));
            }});
            
            req.end();
        }});
    }}
}}

async function generateDiagram() {{
    try {{
        const client = new SimplePlantUMLClient();
        const plantumlCode = `{plantuml_code.replace('`', '\\`')}`;
        const outputPath = '{output_path}';
        
        const result = await client.generateDiagram(plantumlCode, outputPath);
        if (result) {{
            console.log('SUCCESS:' + result);
        }} else {{
            console.log('FAILED:Diagram generation failed');
        }}
    }} catch (error) {{
        console.log('ERROR:' + error.message);
    }}
}}

generateDiagram();
"""
            
            # Write the temporary Node.js script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as temp_script:
                temp_script.write(node_script)
                temp_script_path = temp_script.name
            
            # Execute the Node.js script
            result = subprocess.run(
                ["node", temp_script_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Clean up temporary files
            Path(temp_script_path).unlink(missing_ok=True)
            
            if result.returncode == 0:
                if "SUCCESS:" in result.stdout:
                    success_line = [line for line in result.stdout.split('\n') if line.startswith('SUCCESS:')][0]
                    output_file = success_line.replace('SUCCESS:', '')
                    logger.info(f"✅ Diagram generated successfully: {output_file}")
                    return output_file
                elif "FAILED:" in result.stdout:
                    error_line = [line for line in result.stdout.split('\n') if line.startswith('FAILED:')][0]
                    error_msg = error_line.replace('FAILED:', '')
                    logger.error(f"❌ Diagram generation failed: {error_msg}")
                    return None
                elif "ERROR:" in result.stdout:
                    error_line = [line for line in result.stdout.split('\n') if line.startswith('ERROR:')][0]
                    error_msg = error_line.replace('ERROR:', '')
                    logger.error(f"❌ Node.js client error: {error_msg}")
                    return None
                else:
                    logger.error(f"❌ Unexpected Node.js output: {result.stdout}")
                    return None
            else:
                logger.error(f"❌ Node.js execution failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Diagram generation failed with exception: {e}")
            return None
    
    def generate_activity_diagram(self, class_structure: Dict[str, Any], 
                                 output_path: str) -> Optional[str]:
        """
        Generate an activity diagram from class structure.
        
        Args:
            class_structure: Class structure information
            output_path: Path to save the generated diagram
            
        Returns:
            Path to generated diagram file, or None if failed
        """
        # Generate PlantUML code
        plantuml_code = self._generate_activity_plantuml_code(class_structure)
        
        # Generate the diagram
        return self.generate_diagram(plantuml_code, output_path)
    
    def generate_sequence_diagram(self, class_structure: Dict[str, Any], 
                                 output_path: str) -> Optional[str]:
        """
        Generate a sequence diagram from class structure.
        
        Args:
            class_structure: Class structure information
            output_path: Path to save the generated diagram
            
        Returns:
            Path to generated diagram file, or None if failed
        """
        # Generate PlantUML code
        plantuml_code = self._generate_sequence_plantuml_code(class_structure)
        
        # Generate the diagram
        return self.generate_diagram(plantuml_code, output_path)
    
    def _generate_activity_plantuml_code(self, class_structure: Dict[str, Any]) -> str:
        """Generate PlantUML code for activity diagram"""
        
        classes = class_structure.get('classes', {})
        functions = class_structure.get('functions', [])
        
        plantuml_lines = [
            "@startuml ActivityModel",
            "!theme plain",
            "skinparam backgroundColor white",
            "skinparam activityFontSize 12",
            "skinparam activityFontName Arial",
            "",
            "title Python Module Activity Model",
            "",
            "start",
            ""
        ]
        
        # Add class creation workflow
        plantuml_lines.extend([
            ":Parse Python Source;",
            "note right: AST analysis and structure extraction",
            "",
            f":Extract {len(classes)} Classes;",
            "note right: Class structure analysis",
            ""
        ])
        
        # Add class-specific activities (with shorter labels)
        for class_name, class_info in classes.items():
            # Truncate long class names
            display_name = class_name[:20] + "..." if len(class_name) > 20 else class_name
            
            plantuml_lines.extend([
                f":Process Class: {display_name};",
                f"note right: {len(class_info.get('methods', []))} methods"
            ])
            
            # Add method processing (limit to first few methods)
            methods = class_info.get('methods', [])[:5]  # Limit to 5 methods
            for method in methods:
                method_name = method['name'][:15] + "..." if len(method['name']) > 15 else method['name']
                plantuml_lines.append(f"  :Generate Method: {method_name};")
            
            if len(class_info.get('methods', [])) > 5:
                plantuml_lines.append(f"  :... and {len(class_info.get('methods', [])) - 5} more;")
            
            plantuml_lines.append("")
        
        # Add function processing (limit to first few)
        if functions:
            display_functions = functions[:3]  # Limit to 3 functions
            plantuml_lines.extend([
                f":Process {len(display_functions)} Functions;",
                "note right: Standalone function analysis"
            ])
            
            for func in display_functions:
                func_name = func['name'][:15] + "..." if len(func['name']) > 15 else func['name']
                plantuml_lines.append(f"  :Generate Function: {func_name};")
            
            if len(functions) > 3:
                plantuml_lines.append(f"  :... and {len(functions) - 3} more;")
            
            plantuml_lines.append("")
        
        # Add final workflow steps
        plantuml_lines.extend([
            ":Generate Activity Models;",
            "note right: Create UML diagrams",
            "",
            ":Save Results;",
            "note right: Persist models",
            "",
            "stop",
            "@enduml"
        ])
        
        return "\n".join(plantuml_lines)
    
    def _generate_sequence_plantuml_code(self, class_structure: Dict[str, Any]) -> str:
        """Generate PlantUML code for sequence diagram"""
        
        classes = class_structure.get('classes', {})
        
        plantuml_lines = [
            "@startuml SequenceModel",
            "!theme plain",
            "skinparam backgroundColor white",
            "skinparam sequenceFontSize 12",
            "skinparam sequenceFontName Arial",
            "",
            "title Python Module Sequence Model",
            "",
            "actor User",
            "participant ClassAnalyzer",
            "participant PlantUMLGenerator",
            ""
        ]
        
        # Add sequence workflow
        plantuml_lines.extend([
            "User -> ClassAnalyzer: analyze_module()",
            "activate ClassAnalyzer",
            "",
            "ClassAnalyzer -> ClassAnalyzer: Parse AST",
            "ClassAnalyzer -> ClassAnalyzer: Extract classes",
            "ClassAnalyzer -> ClassAnalyzer: Extract methods",
            "ClassAnalyzer --> User: class_structure",
            "deactivate ClassAnalyzer",
            "",
            "User -> PlantUMLGenerator: generate_diagrams()",
            "activate PlantUMLGenerator",
            "PlantUMLGenerator -> PlantUMLGenerator: Create PlantUML code",
            "PlantUMLGenerator -> PlantUMLGenerator: Generate diagrams",
            "PlantUMLGenerator --> User: generated_diagrams",
            "deactivate PlantUMLGenerator",
            "",
            "@enduml"
        ])
        
        return "\n".join(plantuml_lines)


def main():
    """Test the Node.js PlantUML wrapper"""
    print("🧪 Testing Node.js PlantUML Wrapper")
    print("=" * 40)
    
    try:
        # Initialize wrapper
        wrapper = NodePlantUMLWrapper()
        
        # Test connection
        if not wrapper.test_connection():
            print("❌ Cannot connect to PlantUML server")
            return
        
        # Test with simple diagram
        simple_diagram = """@startuml Test
start
:Hello World;
stop
@enduml"""
        
        print("🔄 Testing simple diagram generation...")
        result = wrapper.generate_diagram(simple_diagram, "test_wrapper.svg")
        
        if result:
            print(f"✅ Diagram generated successfully: {result}")
            print("🎉 Node.js PlantUML wrapper is working!")
        else:
            print("❌ Diagram generation failed")
            
    except Exception as e:
        print(f"❌ Wrapper test failed: {e}")


if __name__ == "__main__":
    main()
