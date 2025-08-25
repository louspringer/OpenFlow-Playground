# Round-Trip Engineering Activity Models

## **🎯 Expected Workflow: Round-Trip Code Generation**

### **Phase 1: Model Input & Vocabulary Alignment**

```mermaid
sequenceDiagram
    participant RE as Reverse Engineering
    participant VA as Vocabulary Aligner
    participant OG as Ontology Bridge
    participant CG as Code Generator
    
    RE->>VA: extracted_model (list format)
    Note over VA: Components field is list
    VA->>OG: analyze_vocabulary_mismatch()
    OG-->>VA: vocabulary_analysis
    Note over VA: Detects list_to_dict mismatch
    VA->>OG: resolve_vocabulary_mismatch(list, "dict")
    OG-->>VA: transformed_components (dict format)
    VA->>VA: _align_vocabulary_ontologically()
    VA-->>CG: aligned_model (dict format)
    Note over CG: Components field is now dict
```

### **Phase 2: Code Generation Pipeline**

```mermaid
sequenceDiagram
    participant CG as Code Generator
    participant IG as Import Generator
    participant CLG as Class Generator
    participant MG as Method Generator
    participant DC as Duplication Cleaner
    
    CG->>IG: generate_imports(aligned_model)
    IG-->>CG: import_statements
    CG->>CLG: generate_class(class_name, class_info)
    CLG->>MG: generate_method(method_info)
    MG-->>CLG: method_code
    CLG-->>CG: class_code
    CG->>CG: _build_file_header()
    CG->>DC: clean_code(generated_code)
    DC-->>CG: cleaned_code
    CG-->>VA: final_generated_code
```

### **Phase 3: Duplication Cleaning**

```mermaid
flowchart TD
    A[Generated Code] --> B[Split into Lines]
    B --> C{Line starts with 'def '?}
    C -->|Yes| D[Check Method Signature]
    C -->|No| E{Line starts with 'return '?}
    D --> F{Method already seen?}
    F -->|Yes| G[Skip until next method]
    F -->|No| H[Add to seen_methods]
    E -->|Yes| I{Return already seen?}
    E -->|No| J[Add line to output]
    I -->|Yes| K[Skip duplicate return]
    I -->|No| L[Add to seen_returns]
    G --> M[Continue processing]
    H --> J
    K --> M
    L --> J
    J --> N[Next line]
    M --> N
    N --> O{More lines?}
    O -->|Yes| C
    O -->|No| P[Return cleaned code]
```

## **🔍 Expected vs Actual Behavior**

### **Expected Behavior**

1. **Vocabulary Alignment**: List → Dict transformation
2. **Code Generation**: Clean, structured Python code
3. **Duplication Removal**: No duplicate methods or returns
4. **Logging**: Comprehensive profiling at each step

### **Actual Behavior (To be validated)**

- [ ] Vocabulary alignment works correctly
- [ ] Code generation produces valid Python
- [ ] Duplication cleaning removes all duplicates
- [ ] Logging provides full visibility

## **📊 Key Metrics to Track**

### **Performance Metrics**

- Vocabulary alignment time
- Code generation time
- Duplication cleaning time
- Total round-trip time

### **Quality Metrics**

- Input/output format consistency
- Generated code validity
- Duplication removal effectiveness
- Error handling robustness

### **Logging Coverage**

- Method entry/exit logging
- Data transformation logging
- Error condition logging
- Performance timing logging
