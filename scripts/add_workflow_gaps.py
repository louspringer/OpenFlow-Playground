#!/usr/bin/env python3
"""
Add TDD and Observatory gaps to GitHub Actions workflows.
Uses ruamel.yaml for deterministic editing.
"""

from ruamel.yaml import YAML
from pathlib import Path

yaml = YAML()
yaml.preserve_quotes = True
yaml.default_flow_style = False


def add_tests_to_quality_gates():
    """Add pytest execution to quality-gates.yml"""
    workflow_path = Path(".github/workflows/quality-gates.yml")
    
    with open(workflow_path) as f:
        workflow = yaml.load(f)
    
    steps = workflow['jobs']['quality-check']['steps']
    
    # Find the "Install dependencies" step
    install_idx = None
    for i, step in enumerate(steps):
        if step.get('name') == 'Install dependencies':
            install_idx = i
            break
    
    if install_idx is None:
        print("❌ Could not find 'Install dependencies' step")
        return False
    
    # Add test steps after install dependencies
    test_steps = [
        {
            'name': 'Run Tests',
            'run': 'uv run pytest tests/ -v --cov=src --cov-report=json --cov-report=html --cov-report=term --junitxml=test-results.xml\n'
        },
        {
            'name': 'Check Test Coverage',
            'run': 'uv run coverage report --fail-under=80 || echo "Coverage below 80% - will not block in development"\n'
        }
    ]
    
    # Insert after install dependencies
    for i, test_step in enumerate(test_steps):
        steps.insert(install_idx + 1 + i, test_step)
    
    # Update upload artifacts to include test results
    for step in steps:
        if step.get('name') == 'Upload quality report':
            if 'path' in step['with']:
                current_paths = step['with']['path']
                if isinstance(current_paths, str):
                    paths_list = [p.strip() for p in current_paths.split('\n') if p.strip()]
                else:
                    paths_list = current_paths
                
                # Add test artifacts
                paths_list.extend(['test-results.xml', 'htmlcov/', 'coverage.json'])
                step['with']['path'] = '\n'.join(paths_list) + '\n'
    
    with open(workflow_path, 'w') as f:
        yaml.dump(workflow, f)
    
    print("✅ Added tests to quality-gates.yml")
    return True


def add_observatory_notifications():
    """Add observatory notifications to all workflows"""
    
    workflows = [
        ('.github/workflows/copilot-review.yml', 'copilot-review', 'copilot-review'),
        ('.github/workflows/quality-gates.yml', 'quality-check', 'quality-gates'),
        ('.github/workflows/cloud-build.yml', 'build-and-deploy', 'cloud-build'),
    ]
    
    for workflow_path, job_name, workflow_name in workflows:
        with open(workflow_path) as f:
            workflow = yaml.load(f)
        
        steps = workflow['jobs'][job_name]['steps']
        
        # Add start notification after checkout
        start_notification = {
            'name': f'Notify Observatory - {workflow_name} Started',
            'if': 'always()',
            'run': f'''curl -X POST https://observatory.nkllon.com/api/events -H "Authorization: Bearer ${{{{ secrets.OBSERVATORY_TOKEN }}}}" -H "Content-Type: application/json" -d '{{"event_type": "ci_workflow_started", "source": "github-actions", "data": {{"workflow": "{workflow_name}", "repository": "${{{{ github.repository }}}}", "pr_number": "${{{{ github.event.number }}}}", "commit_sha": "${{{{ github.sha }}}}"}}}}' || echo "Observatory notification failed (non-blocking)"
'''
        }
        
        # Insert after checkout (usually step 0)
        steps.insert(1, start_notification)
        
        # Add end notification at the end
        end_notification = {
            'name': f'Notify Observatory - {workflow_name} Completed',
            'if': 'always()',
            'run': f'''curl -X POST https://observatory.nkllon.com/api/events -H "Authorization: Bearer ${{{{ secrets.OBSERVATORY_TOKEN }}}}" -H "Content-Type: application/json" -d '{{"event_type": "ci_workflow_completed", "source": "github-actions", "data": {{"workflow": "{workflow_name}", "repository": "${{{{ github.repository }}}}", "pr_number": "${{{{ github.event.number }}}}", "status": "${{{{ job.status }}}}", "run_id": "${{{{ github.run_id }}}}"}}}}' || echo "Observatory notification failed (non-blocking)"
'''
        }
        
        steps.append(end_notification)
        
        with open(workflow_path, 'w') as f:
            yaml.dump(workflow, f)
        
        print(f"✅ Added observatory notifications to {workflow_path}")
    
    return True


if __name__ == '__main__':
    print("🔧 Adding workflow gaps...")
    
    # Add TDD
    if add_tests_to_quality_gates():
        print("✅ TDD gap covered - tests added to CI")
    
    # Add Observatory  
    if add_observatory_notifications():
        print("✅ Observatory gap covered - real-time notifications added")
    
    print("\n✅ All gaps covered!")
    print("\nNext: Validate YAML syntax")

