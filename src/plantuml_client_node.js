#!/usr/bin/env node
/**
 * Node.js PlantUML Client
 * 
 * This module provides a reliable PlantUML client using Node.js
 * to bypass issues with the Python PlantUML library.
 */

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

class NodePlantUMLClient {
    /**
     * Initialize the PlantUML client.
     * 
     * @param {string} serverUrl - URL of the PlantUML server
     */
    constructor(serverUrl = 'http://localhost:20075') {
        this.serverUrl = serverUrl.replace(/\/$/, '');
        console.log(`🎨 Node.js PlantUML client initialized with server: ${this.serverUrl}`);
    }

    /**
     * Generate a diagram from PlantUML code.
     * 
     * @param {string} plantumlCode - PlantUML source code
     * @param {string} outputPath - Path to save the generated diagram
     * @param {string} format - Output format (png, svg, etc.)
     * @returns {Promise<string|null>} Path to generated diagram file, or null if failed
     */
    async generateDiagram(plantumlCode, outputPath, format = 'svg') {
        try {
            console.log(`🔄 Generating ${format.toUpperCase()} diagram...`);
            
            // Encode the PlantUML code
            const encodedCode = encodeURIComponent(plantumlCode);
            
            // Construct the URL with SVG format
            const url = `${this.serverUrl}/uml/${encodedCode}`;
            
            // Make the HTTP request
            console.log(`🔄 Requesting: ${url.substring(0, 100)}...`);
            
            const response = await this.makeHttpRequest(url);
            
            if (response.statusCode === 200 && response.data.length > 0) {
                // Save the diagram
                fs.writeFileSync(outputPath, response.data);
                
                console.log(`✅ Diagram generated successfully: ${outputPath}`);
                console.log(`   Size: ${response.data.length} bytes`);
                return outputPath;
            } else {
                console.error(`❌ HTTP request failed: ${response.statusCode}`);
                console.error(`   Content length: ${response.data.length} bytes`);
                return null;
            }
            
        } catch (error) {
            console.error(`❌ Diagram generation failed: ${error.message}`);
            return null;
        }
    }

    /**
     * Generate an activity diagram from class structure.
     * 
     * @param {Object} classStructure - Class structure information
     * @param {string} outputPath - Path to save the generated diagram
     * @returns {Promise<string|null>} Path to generated diagram file, or null if failed
     */
    async generateActivityDiagram(classStructure, outputPath) {
        // Generate PlantUML code
        const plantumlCode = this.generateActivityPlantUMLCode(classStructure);
        
        // Generate the diagram
        return await this.generateDiagram(plantumlCode, outputPath);
    }

    /**
     * Generate a sequence diagram from class structure.
     * 
     * @param {Object} classStructure - Class structure information
     * @param {string} outputPath - Path to save the generated diagram
     * @returns {Promise<string|null>} Path to generated diagram file, or null if failed
     */
    async generateSequenceDiagram(classStructure, outputPath) {
        // Generate PlantUML code
        const plantumlCode = this.generateSequencePlantUMLCode(classStructure);
        
        // Generate the diagram
        return await this.generateDiagram(plantumlCode, outputPath);
    }

    /**
     * Generate PlantUML code for activity diagram.
     * 
     * @param {Object} classStructure - Class structure information
     * @returns {string} PlantUML code
     */
    generateActivityPlantUMLCode(classStructure) {
        const classes = classStructure.classes || {};
        const functions = classStructure.functions || [];
        
        const plantumlLines = [
            '@startuml ActivityModel',
            '!theme plain',
            'skinparam backgroundColor white',
            'skinparam activityFontSize 12',
            'skinparam activityFontName Arial',
            '',
            'title Python Module Activity Model',
            '',
            'start',
            ''
        ];
        
        // Add class creation workflow
        plantumlLines.push(
            ':Parse Python Source;',
            'note right: AST analysis and structure extraction',
            '',
            `:Extract ${Object.keys(classes).length} Classes;`,
            'note right: Class structure analysis',
            ''
        );
        
        // Add class-specific activities (with shorter labels)
        for (const [className, classInfo] of Object.entries(classes)) {
            // Truncate long class names
            const displayName = className.length > 20 ? className.substring(0, 20) + '...' : className;
            
            plantumlLines.push(
                `:Process Class: ${displayName};`,
                `note right: ${(classInfo.methods || []).length} methods`
            );
            
            // Add method processing (limit to first few methods)
            const methods = (classInfo.methods || []).slice(0, 5); // Limit to 5 methods
            for (const method of methods) {
                const methodName = method.name.length > 15 ? method.name.substring(0, 15) + '...' : method.name;
                plantumlLines.push(`  :Generate Method: ${methodName};`);
            }
            
            if ((classInfo.methods || []).length > 5) {
                plantumlLines.push(`  :... and ${(classInfo.methods || []).length - 5} more;`);
            }
            
            plantumlLines.push('');
        }
        
        // Add function processing (limit to first few)
        if (functions.length > 0) {
            const displayFunctions = functions.slice(0, 3); // Limit to 3 functions
            plantumlLines.push(
                `:Process ${displayFunctions.length} Functions;`,
                'note right: Standalone function analysis'
            );
            
            for (const func of displayFunctions) {
                const funcName = func.name.length > 15 ? func.name.substring(0, 15) + '...' : func.name;
                plantumlLines.push(`  :Generate Function: ${funcName};`);
            }
            
            if (functions.length > 3) {
                plantumlLines.push(`  :... and ${functions.length - 3} more;`);
            }
            
            plantumlLines.push('');
        }
        
        // Add final workflow steps
        plantumlLines.push(
            ':Generate Activity Models;',
            'note right: Create UML diagrams',
            '',
            ':Save Results;',
            'note right: Persist models',
            '',
            'stop',
            '@enduml'
        );
        
        return plantumlLines.join('\n');
    }

    /**
     * Generate PlantUML code for sequence diagram.
     * 
     * @param {Object} classStructure - Class structure information
     * @returns {string} PlantUML code
     */
    generateSequencePlantUMLCode(classStructure) {
        const classes = classStructure.classes || {};
        
        const plantumlLines = [
            '@startuml SequenceModel',
            '!theme plain',
            'skinparam backgroundColor white',
            'skinparam sequenceFontSize 12',
            'skinparam sequenceFontName Arial',
            '',
            'title Python Module Sequence Model',
            '',
            'actor User',
            'participant ClassAnalyzer',
            'participant PlantUMLGenerator',
            ''
        ];
        
        // Add sequence workflow
        plantumlLines.push(
            'User -> ClassAnalyzer: analyze_module()',
            'activate ClassAnalyzer',
            '',
            'ClassAnalyzer -> ClassAnalyzer: Parse AST',
            'ClassAnalyzer -> ClassAnalyzer: Extract classes',
            'ClassAnalyzer -> ClassAnalyzer: Extract methods',
            'ClassAnalyzer --> User: class_structure',
            'deactivate ClassAnalyzer',
            '',
            'User -> PlantUMLGenerator: generate_diagrams()',
            'activate PlantUMLGenerator',
            'PlantUMLGenerator -> PlantUMLGenerator: Create PlantUML code',
            'PlantUMLGenerator -> PlantUMLGenerator: Generate diagrams',
            'PlantUMLGenerator --> User: generated_diagrams',
            'deactivate PlantUMLGenerator',
            '',
            '@enduml'
        );
        
        return plantumlLines.join('\n');
    }

    /**
     * Make an HTTP request to the PlantUML server.
     * 
     * @param {string} url - URL to request
     * @returns {Promise<Object>} Response object with statusCode and data
     */
    makeHttpRequest(url) {
        return new Promise((resolve, reject) => {
            const urlObj = new URL(url);
            const isHttps = urlObj.protocol === 'https:';
            const client = isHttps ? https : http;
            
            const options = {
                hostname: urlObj.hostname,
                port: urlObj.port || (isHttps ? 443 : 80),
                path: urlObj.pathname + urlObj.search,
                method: 'GET',
                timeout: 30000 // 30 seconds
            };
            
            const req = client.request(options, (res) => {
                let data = [];
                
                res.on('data', (chunk) => {
                    data.push(chunk);
                });
                
                res.on('end', () => {
                    const buffer = Buffer.concat(data);
                    
                    // Handle redirects
                    if (res.statusCode === 302 || res.statusCode === 301) {
                        const location = res.headers.location;
                        if (location) {
                            console.log(`🔄 Following redirect to: ${location}`);
                            // Follow the redirect
                            this.makeHttpRequest(location)
                                .then(resolve)
                                .catch(reject);
                            return;
                        }
                    }
                    
                    resolve({
                        statusCode: res.statusCode,
                        data: buffer
                    });
                });
            });
            
            req.on('error', (error) => {
                reject(error);
            });
            
            req.on('timeout', () => {
                req.destroy();
                reject(new Error('Request timeout'));
            });
            
            req.end();
        });
    }

    /**
     * Test the connection to the PlantUML server.
     * 
     * @returns {Promise<boolean>} True if connection successful, false otherwise
     */
    async testConnection() {
        try {
            const response = await this.makeHttpRequest(this.serverUrl);
            if (response.statusCode === 200 || response.statusCode === 302) {
                console.log(`✅ PlantUML server connection successful: ${response.statusCode}`);
                return true;
            } else {
                console.error(`❌ PlantUML server connection failed: ${response.statusCode}`);
                return false;
            }
        } catch (error) {
            console.error(`❌ PlantUML server connection failed: ${error.message}`);
            return false;
        }
    }
}

/**
 * Test the Node.js PlantUML client.
 */
async function main() {
    console.log('🧪 Testing Node.js PlantUML Client');
    console.log('=' .repeat(40));
    
    // Initialize client
    const client = new NodePlantUMLClient();
    
    // Test connection
    if (!(await client.testConnection())) {
        console.log('❌ Cannot connect to PlantUML server');
        return;
    }
    
    // Test with simple diagram
    const simpleDiagram = `@startuml Test
start
:Hello World;
stop
@enduml`;
    
    console.log('🔄 Testing simple diagram generation...');
    const result = await client.generateDiagram(simpleDiagram, 'test_node_client.svg');
    
    if (result) {
        console.log(`✅ Diagram generated successfully: ${result}`);
        console.log('🎉 Node.js PlantUML client is working!');
    } else {
        console.log('❌ Diagram generation failed');
    }
}

// Run if called directly
if (require.main === module) {
    main().catch(console.error);
}

module.exports = NodePlantUMLClient;
