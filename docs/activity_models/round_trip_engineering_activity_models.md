# Round-Trip Engineering Activity Models

## Overview

This document defines the expected activity models and workflows for the Round-Trip Engineering system, enabling validation of expected vs actual behavior during testing and debugging.

## System Architecture

The Round-Trip Engineering system consists of these core components:

- **RoundTripSystem**: Main orchestrator
- **ModelManager**: Model creation, storage, and retrieval
- **VocabularyAligner**: Vocabulary alignment between different formats
- **CodeGenerator**: Code generation from models
- **DuplicationCleaner**: Code duplication detection and removal

## Activity Model 1: Complete Round-Trip Workflow

### Expected Behavior

```mermaid
sequenceDiagram
    participant User
    participant RTS as RoundTripSystem
    participant MM as ModelManager
    participant VA as VocabularyAligner
    participant CG as CodeGenerator
    participant DC as DuplicationCleaner

    User->>RTS: create_model_from_design(design_spec)
    RTS->>MM: create_model_from_design(design_spec)
    MM-->>RTS: model
    RTS-->>User: model

    User->>RTS: save_model(model_name, file_path)
    RTS->>MM: save_model(model_name, file_path)
    MM-->>RTS: success

    User->>RTS: load_model(file_path)
    RTS->>MM: load_model(file_path)
    MM-->>RTS: loaded_model
    RTS-->>User: loaded_model

    User->>RTS: generate_code_from_model(model_name)
    RTS->>MM: get_model(model_name)
    MM-->>RTS: model
    RTS->>VA: align_vocabulary(model)
    VA-->>RTS: aligned_model
    RTS->>CG: generate_from_model(aligned_model)
    CG->>CG: _build_complete_model()
    CG->>CG: _validate_complete_model()
    CG->>CG: _generate_from_complete_model()
    CG-->>RTS: generated_code
    RTS-->>User: generated_files
```

### Validation Points

1. **Model Creation**: Design spec → Complete model with components
2. **Model Persistence**: Save/load cycle maintains data integrity
3. **Vocabulary Alignment**: List format → Dict format conversion
4. **Complete Model Building**: All required fields populated
5. **Model Validation**: Structure validation before code generation
6. **Code Generation**: Full class structure, not just headers

## Activity Model 2: Code Generation with Complete Model

### Expected Behavior

```mermaid
flowchart TD
    A[Input: extracted_model] --> B[Build Complete Model]
    B --> C[Validate Model Structure]
    C --> D{Validation Pass?}
    D -->|Yes| E[Generate Code from Complete Model]
    D -->|No| F[Raise Validation Error]
    E --> G[Output: Generated Code]
    
    B --> B1[Ensure Required Fields]
    B --> B2[Build Complete Component Structure]
    B --> B3[Build Complete Method Structure]
    
    C --> C1[Validate Top-level Fields]
    C --> C2[Validate Components Structure]
    C --> C3[Validate Each Component]
    
    E --> E1[Build File Header]
    E --> E2[Generate Imports]
    E --> E3[Generate Classes]
    E --> E4[Generate Methods]
```

### Validation Points

1. **Complete Model Building**: All missing fields populated with defaults
2. **Structure Validation**: Required fields present and correct types
3. **Code Generation**: Full implementation, not just stubs
4. **Error Handling**: Proper validation errors for malformed models

## Activity Model 3: Vocabulary Alignment Workflow

### Expected Behavior

```mermaid
sequenceDiagram
    participant Input as Input Data
    participant VA as VocabularyAligner
    participant Output as Output Data

    Input->>VA: align_vocabulary(data)
    
    alt Components as List
        VA->>VA: Convert list to dict format
        VA->>VA: Key by component name
        VA-->>Output: Dict format components
    else Components as Dict
        VA->>VA: Keep existing dict format
        VA-->>Output: Unchanged dict format
    end
    
    Note over VA: Preserve all component data<br/>Only change structure format
```

### Validation Points

1. **List → Dict Conversion**: Components properly keyed by name
2. **Dict Preservation**: Existing dict format unchanged
3. **Data Integrity**: All component information preserved
4. **Format Consistency**: Output always in dict format for code generation

## Activity Model 4: Duplication Cleaning Workflow

### Expected Behavior

```mermaid
flowchart TD
    A[Input: Generated Code] --> B[Parse Method Signatures]
    B --> C[Identify Duplicate Methods]
    C --> D{Duplicates Found?}
    D -->|Yes| E[Remove Duplicate Methods]
    D -->|No| F[Check Unreachable Returns]
    E --> F
    F --> G{Unreachable Returns?}
    G -->|Yes| H[Remove Unreachable Returns]
    G -->|No| I[Output: Cleaned Code]
    H --> I
    
    B --> B1[Extract Method Name + Parameters]
    C --> C1[Compare Method Signatures]
    E --> E1[Skip Entire Method Body]
    E --> E2[Preserve First Occurrence]
```

### Validation Points

1. **Method Signature Detection**: Full signature (name + parameters)
2. **Duplicate Removal**: Entire method body skipped
3. **Return Statement Handling**: Unreachable returns removed
4. **Loop Safety**: No infinite loops during cleaning
5. **Data Preservation**: Non-duplicate code unchanged

## Activity Model 5: Error Handling and Logging

### Expected Behavior

```mermaid
sequenceDiagram
    participant Operation as System Operation
    participant Logger as Logging System
    participant Profiler as cProfile
    participant Error as Error Handler

    Operation->>Profiler: Start profiling
    Operation->>Logger: Log operation start
    Operation->>Operation: Execute operation
    
    alt Success
        Operation->>Logger: Log success
        Operation->>Profiler: Stop profiling
        Operation->>Logger: Log performance metrics
    else Error
        Operation->>Error: Capture error context
        Error->>Logger: Log error with full context
        Error->>Profiler: Stop profiling
        Error->>Error: Raise exception
    end
```

### Validation Points

1. **Comprehensive Logging**: All major operations logged
2. **Error Context**: Full context captured for debugging
3. **Profiling Integration**: cProfile properly integrated
4. **Performance Metrics**: Timing and resource usage tracked

## Testing and Validation Strategy

### 1. Expected vs Actual Behavior Comparison

For each activity model, we validate:

- **Input/Output Formats**: Data structures match expectations
- **Processing Steps**: Each step executes as designed
- **Error Conditions**: Proper error handling and logging
- **Performance**: Operations complete within expected timeframes

### 2. Validation Test Cases

```python
# Example validation test
def test_activity_model_validation():
    """Validate that actual behavior matches expected activity models"""
    
    # Test vocabulary alignment workflow
    input_data = {"components": [{"name": "Test", "type": "class"}]}
    expected_output = {"components": {"Test": {"name": "Test", "type": "class"}}}
    
    actual_output = system.vocabulary_aligner.align_vocabulary(input_data)
    assert actual_output == expected_output
    
    # Test complete model building
    complete_model = system.code_generator._build_complete_model(input_data)
    assert "system_name" in complete_model
    assert "components" in complete_model
    assert isinstance(complete_model["components"], dict)
    
    # Test code generation from complete model
    generated_code = system.code_generator._generate_from_complete_model(complete_model, "python")
    assert "class Test" in generated_code
    assert "def __init__" in generated_code
```

### 3. Performance Validation

- **Model Building**: Complete model construction < 100ms
- **Code Generation**: Full class generation < 500ms
- **Duplication Cleaning**: 1000 lines processed < 1s
- **Vocabulary Alignment**: 100 components aligned < 50ms

### 4. Integration Validation

- **End-to-End Workflow**: Complete round-trip < 2s
- **Data Persistence**: Save/load cycle maintains integrity
- **Error Recovery**: System recovers gracefully from failures
- **Resource Usage**: Memory and CPU usage within bounds

## Current Status

✅ **Activity Models Defined**: Expected behavior documented  
✅ **Validation Strategy**: Testing approach established  
🔄 **Implementation**: Core system working, validation in progress  
📋 **Next Steps**: Implement validation tests and performance monitoring  

## Success Criteria

The `validate_activity_models` todo will be marked complete when:

1. **All activity models validated** against actual system behavior
2. **Performance benchmarks met** for all critical operations
3. **Error handling verified** for all failure scenarios
4. **Integration tests passing** for complete workflows
5. **Expected vs actual behavior** documented and aligned

This will ensure the Round-Trip Engineering system behaves exactly as designed and can be relied upon for production use.
