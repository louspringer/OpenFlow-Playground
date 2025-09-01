# Workflow Extraction Integration Plan

## OpenFlow Playground - AST-Based Workflow Analysis

**Date**: 2024-12-19\
**Status**: Planning Phase\
**Approach**: Integration-First Architecture with Fail-Fast Discovery

______________________________________________________________________

## 🎯 **Executive Summary**

This plan addresses the critical gap in our round-trip engineering system: **we lack reliable AST-based workflow extraction capability**. Instead of building custom tools, we will integrate proven solutions (PyCG, pyRegurgitator, ScaMaha) to extract activity flows from Python ASTs and generate accurate UML activity diagrams.

### **Core Problem**

- ❌ We have workflow analyzers that generate diagrams but don't extract actual activity flows
- ❌ We have AST parsers that extract structure but not workflow logic
- ❌ We have presentation tools without the core reverse engineering capability
- ❌ We're building custom tools when proven solutions exist

### **Updated Solution Strategy**

- ✅ **PyCG Replacement**: Use **pyan** for call graph generation (actively maintained)
- ✅ **ScaMaha Alternative**: Use **Understand** or **SonarQube** for comprehensive analysis
- ✅ **pyRegurgitator**: Confirmed working for AST analysis
- 🎯 **New Architecture**: pyan + pyRegurgitator + Understand/SonarQube integration

### **Solution Approach**

- ✅ **Integration-First**: Use existing tools instead of building from scratch
- ✅ **Fail-Fast Discovery**: Test each tool individually before integration
- ✅ **Progressive Integration**: Add tools one by one, validate each step
- ✅ **Model-Driven Design**: Extract requirements from actual tool capabilities

______________________________________________________________________

## 🏗️ **Concept Solution Modeling**

### **1. Core Concept: Integration-First Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     pyan        │    │ pyRegurgitator  │    │   Understand    │
│ Call Graph Gen  │    │   AST Analysis  │    │ Workflow Extract│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Integration     │
                    │ Layer           │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Workflow        │
                    │ Model Generator │
                    └─────────────────┘
```

### **2. Updated Tool Selection**

- **pyan**: Actively maintained Python call graph generator
- **pyRegurgitator**: Confirmed working AST analysis tool
- **Understand/SonarQube**: Professional-grade code analysis tools

### **2. Key Principles**

- **Fail-Fast Discovery**: Test each tool individually before integration
- **Progressive Integration**: Add tools one by one, validate each step
- **Model-Driven Design**: Extract requirements from actual tool capabilities
- **Interface-First**: Define clean interfaces before implementation

______________________________________________________________________

## 📋 **Requirements Analysis**

### **5 Key Use Cases (Prioritized by Risk)**

#### **🔴 CRITICAL - Must Address First (Week 1-2)**

1. **UC-1: Function Call Chain Analysis** - **Risk Score: 0.92**

   - **Objective**: Extract complete function call sequences from source code
   - **Success Criteria**: All function calls identified, call hierarchy preserved, no missing relationships
   - **Critical Unknowns**: Dynamic Python features, metaprogramming, decorators
   - **Tools**: pydeps (call graph) + pyRegurgitator (AST structure)

1. **UC-3: Method Workflow Extraction** - **Risk Score: 0.89**

   - **Objective**: Extract workflow within individual methods/functions
   - **Success Criteria**: Method entry/exit points, internal logic flow, variable state changes
   - **Critical Unknowns**: Exception handling, recursion, state-dependent logic
   - **Tools**: pyRegurgitator (AST) + Pylint (structural analysis)

1. **UC-7: Round-Trip Validation** - **Risk Score: 0.85**

   - **Objective**: Verify extracted model matches source code
   - **Success Criteria**: >95% accuracy, no missing critical paths, no false positives
   - **Critical Unknowns**: Validation strategy, accuracy measurement, performance cost
   - **Tools**: Custom validation engine

#### **🟡 IMPORTANT - Address Second (Week 3-4)**

1. **UC-2: Control Flow Pattern Recognition** - **Risk Score: 0.68**

   - **Objective**: Identify control flow structures (if/else, loops, try/catch)
   - **Success Criteria**: All conditionals mapped, loop structures identified, exception paths captured
   - **Tools**: pyRegurgitator (AST) + Radon (complexity analysis)

1. **UC-6: Multi-File Workflow Analysis** - **Risk Score: 0.64**

   - **Objective**: Analyze workflows across multiple Python files/modules
   - **Success Criteria**: Cross-file dependencies mapped, import relationships preserved
   - **Tools**: pydeps (dependencies) + pyRegurgitator (cross-file AST)

### **Functional Requirements**

1. **Call Graph Extraction**: Generate function call relationships
1. **AST Structure Analysis**: Extract code structure and flow control
1. **Workflow Pattern Recognition**: Identify loops, conditionals, sequences
1. **Model Generation**: Convert extracted data to UML activity diagrams
1. **Round-Trip Validation**: Ensure models match source code

### **Non-Functional Requirements**

1. **Performance**: Analysis must complete in \<30 seconds for typical files
1. **Accuracy**: Extracted models must be >95% accurate
1. **Maintainability**: Clean separation between tool integration and business logic
1. **Extensibility**: Easy to add new analysis tools

______________________________________________________________________

## ⚠️ **Enhanced Risk Assessment with Additional Criteria**

### **Risk Scoring Formula:**

```
Risk Score = (Failure Impact × Implementation Complexity × Tool Reliability × Known Unknowns) / 4
```

**Risk Levels:**

- **🔴 HIGH RISK**: 0.7 - 1.0 (Critical - Address First)
- **🟡 MEDIUM RISK**: 0.4 - 0.69 (Important - Address Second)
- **🟢 LOW RISK**: 0.0 - 0.39 (Nice-to-Have - Address Last)

### **🔴 CRITICAL RISK USE CASES (Address First)**

#### **UC-1: Function Call Chain Analysis** - **Risk Score: 0.92**

- **Failure Impact**: 10/10 (Complete system failure)
- **Implementation Complexity**: 9/10 (Complex AST + call graph integration)
- **Tool Reliability**: 7/10 (pydeps untested on complex code, pyRegurgitator unknown)
- **Known Unknowns**: 9/10 (Dynamic Python features, metaprogramming, decorators)
- **Critical Unknowns**: Dynamic imports, eval/exec, callback patterns

#### **UC-3: Method Workflow Extraction** - **Risk Score: 0.89**

- **Failure Impact**: 10/10 (Incomplete workflow models)
- **Implementation Complexity**: 9/10 (Complex control flow analysis)
- **Tool Reliability**: 8/10 (pyRegurgitator untested on complex methods)
- **Known Unknowns**: 8/10 (Exception handling, recursion, state machines)
- **Critical Unknowns**: Nested try/catch, recursive patterns, async/await

#### **UC-7: Round-Trip Validation** - **Risk Score: 0.85**

- **Failure Impact**: 10/10 (Cannot trust generated models)
- **Implementation Complexity**: 8/10 (Validation algorithm design)
- **Tool Reliability**: 6/10 (No existing validation tools)
- **Known Unknowns**: 8/10 (Accuracy metrics, validation strategies)
- **Critical Unknowns**: Validation strategy, accuracy measurement, performance cost

### **🟡 IMPORTANT RISK USE CASES (Address Second)**

#### **UC-2: Control Flow Pattern Recognition** - **Risk Score: 0.68**

- **Failure Impact**: 8/10 (Incomplete control flow)
- **Implementation Complexity**: 7/10 (Pattern recognition algorithms)
- **Tool Reliability**: 7/10 (pyRegurgitator + Radon combination untested)
- **Known Unknowns**: 6/10 (Boolean logic complexity, loop analysis)

#### **UC-6: Multi-File Workflow Analysis** - **Risk Score: 0.64**

- **Failure Impact**: 8/10 (Incomplete cross-file analysis)
- **Implementation Complexity**: 6/10 (Dependency resolution)
- **Tool Reliability**: 7/10 (pydeps cross-file capabilities untested)
- **Known Unknowns**: 6/10 (Circular imports, dynamic loading)

### **🟢 LOW RISK USE CASES (Address Last)**

#### **UC-4: UML Activity Diagram Generation** - **Risk Score: 0.32**

#### **UC-5: Workflow Complexity Assessment** - **Risk Score: 0.28**

#### **UC-9: Accuracy and Coverage Requirements** - **Risk Score: 0.24**

### **Medium Risk**

- **Integration Complexity**: Combining multiple tools may create maintenance burden
- **Version Dependencies**: Tools may have conflicting Python version requirements

### **Low Risk**

- **Interface Design**: Clean interfaces are straightforward to design
- **Model Generation**: Converting data to UML is well-understood

______________________________________________________________________

## 🎨 **Design Architecture**

### **1. Interface Definitions**

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class CallGraphExtractor(ABC):
    """Interface for call graph extraction tools"""
    
    @abstractmethod
    def extract_call_graph(self, source_path: str) -> Dict[str, Any]:
        """Extract function call relationships"""
        pass
    
    @abstractmethod
    def validate_extraction(self, result: Dict[str, Any]) -> bool:
        """Validate extraction quality"""
        pass

class ASTAnalyzer(ABC):
    """Interface for AST analysis tools"""
    
    @abstractmethod
    def analyze_structure(self, source_path: str) -> Dict[str, Any]:
        """Analyze AST structure and flow control"""
        pass
    
    @abstractmethod
    def extract_flow_patterns(self, ast_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract workflow patterns from AST"""
        pass

class WorkflowPatternExtractor(ABC):
    """Interface for workflow pattern extraction tools"""
    
    @abstractmethod
    def extract_patterns(self, source_path: str) -> List[Dict[str, Any]]:
        """Extract workflow patterns"""
        pass
    
    @abstractmethod
    def classify_patterns(self, patterns: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Classify patterns by type"""
        pass
```

### **2. Core Classes & Behaviors**

#### **WorkflowExtractionOrchestrator**

```python
class WorkflowExtractionOrchestrator:
    """Orchestrates workflow extraction using multiple tools"""
    
    def __init__(self):
        self.call_graph_extractor: Optional[CallGraphExtractor] = None
        self.ast_analyzer: Optional[ASTAnalyzer] = None
        self.pattern_extractor: Optional[WorkflowPatternExtractor] = None
        self.extraction_results: Dict[str, Any] = {}
    
    def discover_available_tools(self) -> Dict[str, bool]:
        """Discover which tools are available and working"""
        return {
            'pycg': self._test_pycg_availability(),
            'pyregurgitator': self._test_pyregurgitator_availability(),
            'scamaha': self._test_scamaha_availability()
        }
    
    def extract_workflow(self, source_path: str) -> Dict[str, Any]:
        """Extract workflow using available tools"""
        # Discover available tools
        available_tools = self.discover_available_tools()
        
        # Extract using available tools
        if available_tools['pycg']:
            self.extraction_results['call_graph'] = self.call_graph_extractor.extract_call_graph(source_path)
        
        if available_tools['pyregurgitator']:
            self.extraction_results['ast_structure'] = self.ast_analyzer.analyze_structure(source_path)
        
        if available_tools['scamaha']:
            self.extraction_results['workflow_patterns'] = self.pattern_extractor.extract_patterns(source_path)
        
        # Combine and validate results
        return self._combine_extraction_results()
    
    def _combine_extraction_results(self) -> Dict[str, Any]:
        """Combine results from multiple tools"""
        combined = {
            'extraction_successful': True,
            'tools_used': [],
            'call_graph': self.extraction_results.get('call_graph'),
            'ast_structure': self.extraction_results.get('ast_structure'),
            'workflow_patterns': self.extraction_results.get('workflow_patterns'),
            'combined_workflow': self._generate_combined_workflow()
        }
        
        # Track which tools were used
        for tool, result in self.extraction_results.items():
            if result is not None:
                combined['tools_used'].append(tool)
        
        return combined
```

#### **WorkflowModelGenerator**

```python
class WorkflowModelGenerator:
    """Generates UML activity diagrams from extracted workflow data"""
    
    def __init__(self):
        self.node_generator = WorkflowNodeGenerator()
        self.edge_generator = WorkflowEdgeGenerator()
        self.diagram_generator = MermaidDiagramGenerator()
    
    def generate_activity_model(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate UML activity model from workflow data"""
        try:
            # Generate nodes from call graph and AST
            nodes = self.node_generator.generate_nodes(workflow_data)
            
            # Generate edges from call relationships
            edges = self.edge_generator.generate_edges(workflow_data)
            
            # Generate Mermaid diagram
            mermaid_code = self.diagram_generator.generate_mermaid(nodes, edges)
            
            return {
                'success': True,
                'nodes': nodes,
                'edges': edges,
                'mermaid_code': mermaid_code,
                'model_quality_score': self._calculate_quality_score(workflow_data, nodes, edges)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'partial_results': {
                    'nodes': getattr(self, 'last_nodes', []),
                    'edges': getattr(self, 'last_edges', [])
                }
            }
    
    def _calculate_quality_score(self, workflow_data: Dict[str, Any], nodes: List[Dict], edges: List[Dict]) -> float:
        """Calculate quality score of generated model"""
        # Implement quality scoring algorithm
        # Consider factors like coverage, accuracy, completeness
        pass
```

______________________________________________________________________

## 🧪 **Discovery Test Plan**

### **Test 1: PyCG Discovery**

```bash
# Test PyCG installation and basic functionality
make test-pycg-discovery

# Expected: Call graph generation for simple Python files
# Success criteria: Generate call graph in <5 seconds
# Failure: Tool doesn't install, crashes, or produces invalid output
```

### **Test 2: pyRegurgitator Discovery**

```bash
# Test pyRegurgitator AST analysis
make test-pyregurgitator-discovery

# Expected: AST structure analysis and visualization
# Success criteria: Generate AST representation in <3 seconds
# Failure: Tool doesn't install, crashes, or produces invalid output
```

### **Test 3: ScaMaha Discovery**

```bash
# Test ScaMaha workflow extraction
make test-scamaha-discovery

# Expected: Workflow pattern recognition
# Success criteria: Extract patterns in <10 seconds
# Failure: Tool doesn't install, crashes, or produces invalid output
```

### **Test 4: Integration Discovery**

```bash
# Test tool combinations
make test-tool-integration-discovery

# Expected: Tools work together without conflicts
# Success criteria: Combined analysis in <20 seconds
# Failure: Tools conflict, performance degradation, or data incompatibility
```

______________________________________________________________________

## 🎯 **Success Criteria & Exit Conditions**

### **Success Criteria**

- ✅ All three tools install and run successfully
- ✅ Tools can analyze our codebase in \<30 seconds total
- ✅ Extracted models are >95% accurate
- ✅ Integration layer works without conflicts

### **Exit Conditions (Fail-Fast)**

- ❌ Any tool fails to install or crashes
- ❌ Analysis takes >30 seconds for typical files
- ❌ Extracted models are \<80% accurate
- ❌ Tools have unresolvable conflicts

### **Fallback Strategy**

If integration approach fails:

1. **Fallback to single tool**: Use best-performing tool only
1. **Fallback to custom solution**: Build minimal custom extractor
1. **Fallback to manual analysis**: Document workflow manually

______________________________________________________________________

## 🚀 **Implementation Timeline**

### **Week 1: Discovery Phase**

- [ ] Tool availability matrix
- [ ] Performance benchmarks
- [ ] Accuracy validation results
- [ ] Integration feasibility assessment

### **Week 2: Integration Phase**

- [ ] Integration layer design
- [ ] Interface definitions
- [ ] Core class implementations
- [ ] Integration testing results

### **Week 3: Production Phase**

- [ ] Complete workflow extraction system
- [ ] Performance optimization
- [ ] Accuracy improvements
- [ ] Production readiness assessment

______________________________________________________________________

## 📝 **Project Model Integration**

### **Workflow Extraction Domain**

```json
{
  "domains": {
    "workflow_extraction": {
      "description": "Extract workflow models from Python code using proven tools",
      "patterns": ["**/*.py"],
      "content_indicators": ["python", "workflow", "activity"],
      "linter": "pycg",
      "validator": "scamaha",
      "formatter": "pyRegurgitator",
      "requirements": [
        "Use PyCG for call graph generation",
        "Use pyRegurgitator for AST visualization", 
        "Use ScaMaha for workflow pattern extraction",
        "Build integration layer, not custom tools",
        "Fail-fast discovery of tool capabilities",
        "Progressive integration approach"
      ],
      "risk_mitigation": [
        "Test each tool individually before integration",
        "Validate extraction accuracy on real code",
        "Performance benchmarking for large files",
        "Fallback mechanisms for tool failures"
      ]
    }
  }
}
```

______________________________________________________________________

## 🔄 **Round-Trip Engineering Integration**

This workflow extraction system will integrate with our existing round-trip engineering infrastructure:

1. **Extract**: Use integrated tools to extract workflow models
1. **Transform**: Convert to UML activity diagrams
1. **Validate**: Ensure models match source code
1. **Generate**: Create visual representations
1. **Verify**: Round-trip validation of generated models

______________________________________________________________________

## 📊 **Metrics & KPIs**

### **Performance Metrics**

- **Extraction Time**: Target \<30 seconds for typical files
- **Memory Usage**: Target \<500MB for large files
- **CPU Usage**: Target \<80% during analysis

### **Quality Metrics**

- **Accuracy**: Target >95% model accuracy
- **Coverage**: Target >90% code coverage
- **Completeness**: Target >85% workflow completeness

### **Maintenance Metrics**

- **Tool Updates**: Frequency of dependency updates
- **Integration Issues**: Number of tool conflicts
- **Fallback Usage**: Frequency of fallback mechanisms

______________________________________________________________________

## 🎯 **The Meta-Rule**

## "When proven tools exist for AST analysis and workflow extraction, integrate them instead of building custom solutions. Focus on the integration layer and model presentation, not the core analysis capabilities."

This approach will give us:

1. **Reliable workflow extraction** using proven tools
1. **Accurate activity flow modeling** from actual call graphs
1. **Fast development** by leveraging existing solutions
1. **Maintainable code** that doesn't reinvent wheels

**The era of intelligent tool integration has begun!** 🚀
