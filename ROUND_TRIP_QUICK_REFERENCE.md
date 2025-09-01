# Round Trip System - Quick Reference

## 🚨 CRITICAL: Two Generation Methods

### ❌ WRONG METHOD (Generates Skeletons)

```python
system = RoundTripModelSystem()
model_obj = system.create_model_from_design(design_spec)
generated_files = system.generate_code_from_model(model_obj.name)  # SKELETONS!
```

### ✅ RIGHT METHOD (Generates Working Code)

```python
system = RoundTripModelSystem()
complete_code = system.generate_code_from_extracted_model(model)  # WORKING CODE!
```

## 🔄 Complete Workflow

1. **Extract Model**: `python enhanced_reverse_engineer.py <file.py>`
1. **Generate Code**: Use `generate_code_from_extracted_model(model)`
1. **Validate**: Compare original vs generated for functional equivalence

## 📁 Key Files

- **Enhanced AST Parser**: `enhanced_ast_wrapper.py` ✅
- **Model Extractor**: `enhanced_reverse_engineer.py` ✅
- **Code Generator**: `round_trip_model_system.py` ✅
- **Test Runner**: `enhanced_round_trip_test.py` ✅

## 🧪 Test Commands

```bash
# Test complete system
python enhanced_round_trip_test.py

# Test individual components
python enhanced_ast_wrapper.py
python enhanced_reverse_engineer.py scripts/simple_calculator.py
```

## 💡 Key Points

- **System is NOT broken** - Working perfectly as designed
- **Enhanced AST parser integration is complete** - No fixes needed
- **Generates complete, working Python code** - Not just skeletons
- **Use `generate_code_from_extracted_model()` for code regeneration**
- **Use `generate_code_from_model()` for new class structures**

## 🚫 Common Mistakes

- Using skeleton generator for code regeneration
- Assuming the system only generates TODO comments
- Trying to fix a system that isn't broken
- Not understanding the two different generation methods

## ✅ Status

| Component | Status |
|-----------|--------|
| Enhanced AST Parser | ✅ Working |
| Model Extraction | ✅ Working |
| Code Generation | ✅ Working |
| Round Trip Workflow | ✅ Working |

**The system works perfectly - just use the right method!**
