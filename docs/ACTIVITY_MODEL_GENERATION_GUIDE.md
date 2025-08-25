# Activity Model Generation Guide

## Overview

The Activity Model Generation System provides automated generation of UML activity and sequence diagrams from Python source code. This system integrates with the Round-Trip Engineering workflow and supports both standalone usage and CI/CD integration.

## Features

- **SVG Output**: Generates high-quality vector graphics (SVG format)
- **Multiple Diagram Types**: Activity diagrams and sequence diagrams
- **Round-Trip Integration**: Seamless integration with the round-trip engineering system
- **CI/CD Ready**: Automated generation for continuous integration pipelines
- **Performance Monitoring**: Built-in performance metrics and validation
- **Error Handling**: Comprehensive error reporting and recovery

## Quick Start

### Prerequisites

1. **PlantUML Server**: Ensure PlantUML server is running

   ```bash
   # Start PlantUML server (if using Docker)
   docker run -d -p 20075:8080 plantuml/plantuml-server
   ```

2. **Dependencies**: Install required Python packages

   ```bash
   uv sync
   ```

### Basic Usage

#### Using Make Targets (Recommended)

```bash
# Generate activity models with round-trip integration
make activity-models

# Generate activity models without round-trip integration (faster)
make activity-models-quick

# Run CI/CD integration
make ci-activity-models
```

#### Direct Python Usage

```bash
# Generate models for specific source paths
uv run python src/round_trip_engineering/activity_model_integration.py src/round_trip_engineering/ --verbose

# Generate models without round-trip integration
uv run python src/round_trip_engineering/activity_model_integration.py src/ --no-round-trip --output-dir custom_output/

# Run CI/CD integration
uv run python scripts/ci_activity_models.py --verbose
```

## Command Line Interface

### Activity Model Integration

```bash
python src/round_trip_engineering/activity_model_integration.py [OPTIONS] SOURCE_PATHS...

Arguments:
  SOURCE_PATHS...    Source files or directories to analyze

Options:
  --output-dir DIR   Output directory for generated models (default: generated_activity_models)
  --no-round-trip    Skip round-trip system integration
  --verbose          Enable verbose logging
  --report-only      Generate report without running generation
  -h, --help         Show help message
```

### CI/CD Integration

```bash
python scripts/ci_activity_models.py [OPTIONS]

Options:
  --config FILE      Configuration file path
  --source-paths PATHS...  Override source paths from config
  --output-dir DIR   Override output directory from config
  --no-round-trip    Disable round-trip system integration
  --verbose          Enable verbose logging
  -h, --help         Show help message
```

## Configuration

### CI/CD Configuration File

Create a `ci_config.json` file to customize CI/CD behavior:

```json
{
  "source_paths": ["src/", "tests/"],
  "include_round_trip": true,
  "performance_threshold": 30.0,
  "error_threshold": 0.1,
  "artifacts_to_keep": 10,
  "notifications": {
    "slack_webhook": "https://hooks.slack.com/...",
    "email": "team@example.com"
  }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `source_paths` | array | `["src/"]` | Source directories to analyze |
| `include_round_trip` | boolean | `true` | Enable round-trip system integration |
| `performance_threshold` | float | `30.0` | Maximum generation time in seconds |
| `error_threshold` | float | `0.1` | Maximum error rate (10%) |
| `artifacts_to_keep` | integer | `10` | Number of artifact directories to retain |
| `notifications` | object | `{}` | Notification configuration |

## Output Structure

### Generated Files

```
generated_activity_models/
├── activity_diagram.svg          # Activity diagram
├── sequence_diagram.svg          # Sequence diagram
├── generation_report.txt         # Generation report
└── plantuml_code/               # PlantUML source code
    ├── activity_diagram.puml
    └── sequence_diagram.puml
```

### CI/CD Artifacts

```
ci_activity_models/
├── ci_metadata.json             # CI environment metadata
├── generation_results.json      # Complete generation results
├── ci_summary.json             # CI summary
├── ci_report.txt               # Human-readable CI report
└── [SVG diagrams and PlantUML code]
```

## Integration with Round-Trip Engineering

### Automatic Integration

When `include_round_trip` is enabled, the system automatically:

1. **Analyzes Source Code**: Parses Python files to extract class and method information
2. **Generates Models**: Creates UML diagrams from the extracted information
3. **Integrates with Round-Trip System**: Stores model summaries for validation
4. **Provides Validation Reports**: Reports on model consistency and quality

### Manual Integration

```python
from round_trip_engineering.activity_model_integration import ActivityModelIntegration

# Initialize integration
integration = ActivityModelIntegration("output_directory")

# Generate models with round-trip integration
results = integration.generate_activity_models(
    source_paths=["src/my_module/"],
    include_round_trip=True
)

# Access results
print(f"Generated {results['performance_metrics']['models_generated']} models")
print(f"Success rate: {results['performance_metrics']['success_rate']:.1%}")
```

## Performance and Monitoring

### Performance Metrics

The system tracks several key performance indicators:

- **Generation Time**: Total time to generate all models
- **Success Rate**: Percentage of successful model generations
- **Error Count**: Number of errors encountered
- **Model Count**: Number of models successfully generated

### Performance Validation

Performance is automatically validated against configurable thresholds:

- **Time Threshold**: Maximum allowed generation time
- **Error Threshold**: Maximum allowed error rate

### Monitoring Output

```bash
🎯 Generation completed: 5 models, 0 errors
📊 Performance validation completed
✅ Performance thresholds met
🗂️  Artifact management completed
```

## Error Handling

### Common Errors

1. **PlantUML Server Unavailable**

   ```
   ⚠️  PlantUML server not available: Connection refused
   💾 PlantUML code saved (server not available): output.puml
   ```

2. **Source File Issues**

   ```
   ❌ Error processing src/broken_file.py: SyntaxError: invalid syntax
   ```

3. **Round-Trip Integration Failures**

   ```
   ⚠️  Round-trip system integration failed: Module not found
   ```

### Error Recovery

- **Graceful Degradation**: System continues processing other files
- **Detailed Logging**: Comprehensive error information for debugging
- **Fallback Options**: PlantUML code saved even when diagram generation fails
- **Error Reporting**: Structured error reporting for CI/CD pipelines

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Activity Model Generation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  generate-models:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        uv sync
    
    - name: Start PlantUML server
      run: |
        docker run -d -p 20075:8080 plantuml/plantuml-server
        sleep 10
    
    - name: Generate activity models
      run: |
        uv run python scripts/ci_activity_models.py --verbose
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: activity-models
        path: ci_activity_models/
```

### Jenkins Pipeline Example

```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'curl -LsSf https://astral.sh/uv/install.sh | sh'
                sh 'uv sync'
            }
        }
        
        stage('PlantUML Server') {
            steps {
                sh 'docker run -d -p 20075:8080 plantuml/plantuml-server'
                sh 'sleep 10'
            }
        }
        
        stage('Generate Models') {
            steps {
                sh 'uv run python scripts/ci_activity_models.py --verbose'
            }
        }
        
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'ci_activity_models/**/*', fingerprint: true
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
```

## Troubleshooting

### PlantUML Server Issues

1. **Check Server Status**

   ```bash
   curl http://localhost:20075/
   ```

2. **Verify Port Configuration**

   ```bash
   netstat -tlnp | grep 20075
   ```

3. **Check Docker Container**

   ```bash
   docker ps | grep plantuml
   ```

### Performance Issues

1. **Large Codebases**: Consider processing directories separately
2. **Memory Usage**: Monitor system resources during generation
3. **Network Latency**: Ensure PlantUML server is accessible

### Integration Issues

1. **Import Errors**: Check Python path and dependencies
2. **Round-Trip System**: Verify round-trip system availability
3. **Configuration**: Validate configuration file syntax

## Best Practices

### Development Workflow

1. **Use Make Targets**: Leverage the provided Make targets for consistency
2. **Incremental Generation**: Generate models for specific modules during development
3. **Version Control**: Commit generated models for documentation purposes

### CI/CD Pipeline

1. **Parallel Execution**: Run model generation in parallel with other CI tasks
2. **Artifact Management**: Configure appropriate artifact retention policies
3. **Performance Monitoring**: Set realistic performance thresholds
4. **Error Handling**: Implement proper error notification and escalation

### Output Management

1. **Organized Structure**: Use consistent output directory naming
2. **Cleanup Policies**: Implement artifact cleanup to manage disk space
3. **Backup Strategy**: Consider backing up important generated models

## Advanced Usage

### Custom PlantUML Templates

The system generates standard PlantUML code, but you can customize the output by modifying the generator classes:

```python
# Customize PlantUML generation in activity_model_generator_simple.py
def _generate_plantuml_code(self, class_structure: Dict[str, Any]) -> str:
    # Custom PlantUML generation logic
    pass
```

### Batch Processing

For large codebases, consider processing in batches:

```bash
# Process specific modules
for module in src/*/; do
    echo "Processing $module"
    uv run python src/round_trip_engineering/activity_model_integration.py "$module" --output-dir "models_${module#src/}"
done
```

### Custom Validation

Extend the system with custom validation logic:

```python
class CustomActivityModelIntegration(ActivityModelIntegration):
    def _validate_custom_rules(self, results):
        # Custom validation logic
        pass
```

## Support and Contributing

### Getting Help

1. **Check Logs**: Enable verbose logging for detailed information
2. **Review Configuration**: Verify configuration file syntax and values
3. **Test Components**: Test individual components in isolation

### Contributing

1. **Report Issues**: Use GitHub issues for bug reports
2. **Feature Requests**: Submit feature requests with use case descriptions
3. **Code Contributions**: Follow the project's coding standards and testing requirements

## Conclusion

The Activity Model Generation System provides a robust, production-ready solution for automatically generating UML diagrams from Python source code. With its integration capabilities, CI/CD support, and comprehensive error handling, it serves as a valuable tool for both development and documentation workflows.

For additional information or support, refer to the project documentation or submit issues through the project's issue tracker.
