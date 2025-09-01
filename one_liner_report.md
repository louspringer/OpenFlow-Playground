# 🔍 One-Liner Linter Report

Generated: 2025-08-14T17:17:33.838883
Workspace: /home/lou/Documents/OpenFlow-Playground

## 📊 Summary

- Files analyzed: 697
- Total issues: 1563
- Critical issues: 33
- Warnings: 910
- Suggestions: 620
- Files with issues: 298
- Average one-liner score: 0.05%

## 🚨 Critical Issues

### data/cost_analysis.py:219

**Type:** syntax_error
**Description:** Syntax error: unexpected indent
**Suggestion:** Fix the syntax error in the code
**Context:** `input_text = system_message + "\n\n" + user_message`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:104

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `print_error "Not authenticated with gcloud. Please run 'gcloud auth login' first."`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:78

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `print_error "Not authenticated with gcloud. Please run 'gcloud auth login' first."`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:194

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `gcloud billing budgets list --billing-account=$BILLING_ACCOUNT --filter="displayName:2025"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:90

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `print_error "Not authenticated with gcloud. Please run 'gcloud auth login' first."`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:118

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `gcloud services disable $api --project=$PROJECT_ID --quiet || print_warning "Failed to disable $api"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:140

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `gcloud container clusters delete $CLUSTER_NAME --location=$LOCATION --project=$PROJECT_ID --quiet || print_warning "Failed to delete cluster $CLUSTER_NAME"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:164

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `gcloud compute instances delete $INSTANCE_NAME --zone=$ZONE --project=$PROJECT_ID --quiet || print_warning "Failed to delete instance $INSTANCE_NAME"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:204

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `gcloud billing budgets delete $budget --quiet || print_warning "Failed to delete budget $budget"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:217

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `gcloud billing projects unlink $PROJECT_ID --quiet || print_warning "Failed to unlink billing account"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:78

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `print_error "Not authenticated with gcloud. Please run 'gcloud auth login' first."`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:194

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `gcloud billing budgets list --billing-account=$BILLING_ACCOUNT --filter="displayName:2025"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:96

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `print_error "Not authenticated with gcloud. Please run 'gcloud auth login' first."`

### scripts/setup-github-connection.sh:45

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `echo -n "$GITHUB_TOKEN" | gcloud secrets create "$SECRET_NAME" --data-file=- --project="$PROJECT_ID" || echo "Secret already exists"`

### scripts/setup-github-connection.sh:106

**Type:** one_liner_detected
**Description:** One-liner detected: git_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `echo "   git add . && git commit -m 'test: trigger cloud build' && git push"`

### scripts/setup-develop-trigger.sh:48

**Type:** one_liner_detected
**Description:** One-liner detected: git_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `echo "   git add . && git commit -m 'test: trigger cloud build' && git push"`

### scripts/setup-github-2ndgen.sh:37

**Type:** one_liner_detected
**Description:** One-liner detected: gcloud_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `echo -n "$GITHUB_TOKEN" | gcloud secrets create "$SECRET_NAME" --data-file=- --project="$PROJECT_ID" || echo "Secret already exists"`

### scripts/setup-github-2ndgen.sh:97

**Type:** one_liner_detected
**Description:** One-liner detected: git_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `echo "   git add . && git commit -m 'test: trigger cloud build' && git push"`

### scripts/setup-cloud-build-trigger.sh:45

**Type:** one_liner_detected
**Description:** One-liner detected: git_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `echo "   git add . && git commit -m 'test: trigger cloud build' && git push"`

### scripts/setup-github-trigger-direct.sh:46

**Type:** one_liner_detected
**Description:** One-liner detected: git_oneliner
**Suggestion:** Break complex commands into multiple lines or create a proper script
**Context:** `echo "   git add . && git commit -m 'test: trigger cloud build' && git push"`

### config/Openflow-Playground.yaml:169

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `Key: "Name"`

### config/Openflow-Playground.yaml:191

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `Key: "Name"`

### config/Openflow-Playground.yaml:193

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `Key: "kubernetes.io/role/internal-elb"`

### config/Openflow-Playground.yaml:215

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `Key: "Name"`

### config/Openflow-Playground.yaml:217

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `Key: "kubernetes.io/role/internal-elb"`

### config/Openflow-Playground.yaml:239

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `Key: "Name"`

### config/Openflow-Playground.yaml:241

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `Key: "kubernetes.io/role/elb"`

### config/Openflow-Playground.yaml:263

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `Key: "Name"`

### config/Openflow-Playground.yaml:265

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `Key: "kubernetes.io/role/elb"`

### config/Openflow-Playground.yaml:272

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `Key: "Name"`

### config/Openflow-Playground.yaml:635

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `- Key: "Name"`

### config/Openflow-Playground.yaml:658

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `- Key: "Name"`

### config/Openflow-Playground.yaml:760

**Type:** hardcoded_credential
**Description:** Hardcoded credential detected
**Suggestion:** Use environment variables or secret management instead of hardcoded values
**Context:** `[ $? -ne 0 ] && echo "Unable to obtain OAuth access token: "$(echo $oauth_resp | jq -r '.message') && exit 1`

## ⚠️ Warnings

### projected_verify_ide_linting_hypothesis.py:259

**Type:** line_too_long
**Description:** Line is 468 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `report = f"\n🔬 IDE LINTING HYPOTHESIS VERIFICATION REPORT\n{'=' * 50}\n\nHYPOTHESIS: {data['hypothesis']}\n\nDATA POINTS COLLECTED: {data['analysis']['total_data_points']}\n\nFRAGMENTATION ANALYSIS:\n- Fragmentation Score: {data['analysis']['fragmentation_score']:.2f}/10\n- Reliability Score: {data['analysis']['reliability_score']:.2f}/10\n- Sources Found: {len(data['analysis']['sources'])}\n- Linters Found: {len(data['analysis']['linters'])}\n\nDATA BREAKDOWN:\n"`

### projected_verify_ide_linting_hypothesis.py:273

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `report += "\n🎯 VERDICT: HYPOTHESIS CONFIRMED - IDE linting data IS fragmented and unreliable"`

### cloudbuild_github_rest_api.py:69

**Type:** line_too_long
**Description:** Line is 131 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `url = "https://cloudbuild.googleapis.com/v2/projects/aardvark-linkedin-grepper/locations/us-central1/connections/github-connection"`

### cloudbuild_github_rest_api.py:74

**Type:** line_too_long
**Description:** Line is 96 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"oauthTokenSecretVersion": "projects/aardvark-linkedin-grepper/secrets/github-token/versions/1",`

### cloudbuild_github_rest_api.py:94

**Type:** line_too_long
**Description:** Line is 144 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `url = "https://cloudbuild.googleapis.com/v2/projects/aardvark-linkedin-grepper/locations/us-central1/connections/github-connection/repositories"`

### cloudbuild_github_rest_api.py:171

**Type:** line_too_long
**Description:** Line is 107 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"🔗 View triggers: https://console.cloud.google.com/cloud-build/triggers?project=aardvark-linkedin-grepper",`

### ONE_LINER_LINTER_DOCUMENTATION.md:51

**Type:** one_line_commit
**Description:** One-line commit message detected
**Suggestion:** Use multi-line commit messages with proper descriptions
**Context:** `- **Git one-liners**:`git commit -m "message"\`\`

### cloudbuild_webhook_trigger.py:124

**Type:** line_too_long
**Description:** Line is 107 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"🔗 View triggers: https://console.cloud.google.com/cloud-build/triggers?project=aardvark-linkedin-grepper",`

### cloudbuild.yaml:41

**Type:** line_too_long
**Description:** Line is 211 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `args: ['-X', 'POST', 'https://ghostbusters-api-container-1077539189076.us-central1.run.app/analyze', '-H', 'Content-Type: application/json', '-d', '{"project_path": ".", "agents": ["security", "code_quality"]}']`

### comprehensive_artifact_analysis.py:585

**Type:** line_too_long
**Description:** Line is 129 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"🔍 {self.analysis.artifacts_untraced} artifacts are not traced to any domain. Consider adding domain patterns for these files.",`

### comprehensive_artifact_analysis.py:590

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"📁 Domains defined in model but no artifacts found: {', '.join(self.analysis.missing_domains)}",`

### comprehensive_artifact_analysis.py:595

**Type:** line_too_long
**Description:** Line is 135 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"📋 {len(self.analysis.missing_requirements)} requirements are not traced to any artifacts. Consider implementing these requirements.",`

### comprehensive_artifact_analysis.py:601

**Type:** line_too_long
**Description:** Line is 113 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"🐍 {self.analysis.ast_parsing_failures} Python files failed AST parsing. Review these files for syntax issues.",`

### comprehensive_artifact_analysis.py:608

**Type:** line_too_long
**Description:** Line is 99 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"📦 {len(large_files)} files are larger than 1MB. Consider if these should be in version control.",`

### cloudbuild_github_1stgen.py:128

**Type:** line_too_long
**Description:** Line is 107 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"🔗 View triggers: https://console.cloud.google.com/cloud-build/triggers?project=aardvark-linkedin-grepper",`

### cloudbuild_github_2ndgen_trigger.py:129

**Type:** line_too_long
**Description:** Line is 107 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"🔗 View triggers: https://console.cloud.google.com/cloud-build/triggers?project=aardvark-linkedin-grepper",`

### create_notebook.py:128

**Type:** line_too_long
**Description:** Line is 122 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `print(f"   Keys: {list(state.validation_results.keys()) if isinstance(state.validation_results, dict) else 'Not a dict'}")`

### create_notebook.py:146

**Type:** line_too_long
**Description:** Line is 118 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `print(f"   Keys: {list(state.recovery_results.keys()) if isinstance(state.recovery_results, dict) else 'Not a dict'}")`

### create_notebook.py:162

**Type:** line_too_long
**Description:** Line is 102 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `print(f"   Keys: {list(state.metadata.keys()) if isinstance(state.metadata, dict) else 'Not a dict'}")`

### CLOUDBUILD_GITHUB_FINAL_DIAGNOSTIC.md:109

**Type:** one_line_commit
**Description:** One-line commit message detected
**Suggestion:** Use multi-line commit messages with proper descriptions
**Context:** `gcloud builds repositories create OpenFlow-Playground --remote-uri="https://github.com/louspringer/OpenFlow-Playground.git" --connection="github-connection" --region="us-central1"`

### QUALITY_SYSTEM_PHASE_1_2_SUMMARY.md:124

**Type:** one_line_commit
**Description:** One-line commit message detected
**Suggestion:** Use multi-line commit messages with proper descriptions
**Context:** `2. **Pre-commit Integration**:`python -m src.code_quality_system.cli install-hook\`\`

### test_orchestrator_quality_integration.py:48

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"    📊 Overall Quality Score: {overall_summary.get('overall_quality_score', 'N/A'):.1f}"`

### test_orchestrator_quality_integration.py:60

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"    📊 Recommendations Priority: {overall_summary.get('recommendations_priority', 'N/A')}"`

### test_orchestrator_quality_integration.py:127

**Type:** line_too_long
**Description:** Line is 106 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"    ❌ Quality score mismatch: expected {expected_score:.1f}, got {summary['overall_quality_score']:.1f}"`

### recursive_code_generator.py:305

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `generated = f"{decomposed_model['quotes'][0]}{decomposed_model['value']}{decomposed_model['quotes'][1]}"`

### call_ghostbusters.py:45

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"  {i}. {delusion.get('type', 'Unknown')}: {delusion.get('description', 'No description')}",`

### call_ghostbusters.py:53

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"  {i}. {action.get('type', 'Unknown')}: {action.get('description', 'No description')}",`

### call_ghostbusters.py:102

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"  {i}. {recovery.get('type', 'Unknown')}: {recovery.get('description', 'No description')}",`

### test_expert_quality_integration.py:101

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"content": "import *\nfrom os import *\n# TODO: Fix this later\n# FIXME: Need to refactor"`

### test_expert_quality_integration.py:152

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"  ✅ SecurityExpert metric consistency: {security_metric_name} = {security_metric_weight}"`

### test_expert_quality_integration.py:156

**Type:** line_too_long
**Description:** Line is 95 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"  ❌ SecurityExpert weight mismatch: expected {expected_weight}, got {security_metric_weight}"`

### test_expert_quality_integration.py:181

**Type:** line_too_long
**Description:** Line is 102 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"  ✅ CodeQualityExpert metric consistency: {code_quality_metric_name} = {code_quality_metric_weight}"`

### test_expert_quality_integration.py:185

**Type:** line_too_long
**Description:** Line is 102 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"  ❌ CodeQualityExpert weight mismatch: expected {expected_weight}, got {code_quality_metric_weight}"`

### test_complex_model.py:40

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"   AST Parse Successful: {analysis['ast_analysis'].get('ast_parse_successful', False)}",`

### ghostbusters_diversity_analysis.py:5

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `This script uses your proven diversity hypothesis system to analyze the Ghostbusters issue`

### ghostbusters_diversity_analysis.py:24

**Type:** line_too_long
**Description:** Line is 171 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `PROBLEM: The Ghostbusters system was supposed to battle hallucinations and support the 'diversity is the only free lunch' principle, but it became bloated and ineffective.`

### ghostbusters_diversity_analysis.py:45

**Type:** line_too_long
**Description:** Line is 99 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `QUESTION: What do you think about this problem and solution? What blind spots might we have missed?`

### ghostbusters_diversity_analysis.py:74

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `4. How well does this solution align with the 'diversity is the only free lunch' principle?`

### fix_remaining_smoke_tests.py:40

**Type:** line_too_long
**Description:** Line is 99 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `raise ValueError(f"Failed to import {provider} dependencies: {str(e)}. Install required packages.")`

### fix_remaining_smoke_tests.py:44

**Type:** line_too_long
**Description:** Line is 116 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `raise ValueError(f"Failed to initialize {provider} model: {str(e)}. Check API key validity and model availability.")`

### fix_remaining_smoke_tests.py:56

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Generate 5 probing questions that would reveal blind spots, assumptions, or unknown unknowns.`

### clewcrew-validators/src/clewcrew_validators/data_validator.py:117

**Type:** line_too_long
**Description:** Line is 100 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `pattern = r"^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$"`

### clewcrew-validators/src/clewcrew_validators/**init**.py:2

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `clewcrew-validators: Validation components for the clewcrew hallucination detection system.`

### clewcrew-core/src/clewcrew_core/orchestrator.py:10

**Type:** line_too_long
**Description:** Line is 95 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "clewcrew-agents" / "src"))`

### clewcrew-core/src/clewcrew_core/orchestrator.py:405

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `def _generate_quality_summary(self, agent_quality_results: Dict[str, Any]) -> Dict[str, Any]:`

### clewcrew-agents/src/clewcrew_agents/devops_expert.py:328

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"description": f"Container '{container.get('name', 'unknown')}' missing resource limits",`

### clewcrew-agents/src/clewcrew_agents/devops_expert.py:338

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `async def _analyze_infrastructure_config(self, project_path: Path) -> list[dict[str, Any]]:`

### clewcrew-agents/src/clewcrew_agents/model_expert.py:141

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `if change_type in ["model_config_change", "hyperparameter_change", "architecture_change"]:`

### clewcrew-agents/src/clewcrew_agents/code_quality_expert.py:116

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `async def _analyze_existing_flake8_outputs(self, project_path: Path) -> list[dict[str, Any]]:`

### clewcrew-agents/src/clewcrew_agents/code_quality_expert.py:168

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `async def _analyze_existing_black_outputs(self, project_path: Path) -> list[dict[str, Any]]:`

### clewcrew-agents/src/clewcrew_agents/code_quality_expert.py:199

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `async def _analyze_existing_mypy_outputs(self, project_path: Path) -> list[dict[str, Any]]:`

### clewcrew-agents/src/clewcrew_agents/code_quality_expert.py:327

**Type:** line_too_long
**Description:** Line is 94 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `code_style_issues = [h for h in result.hallucinations if h.get("type") == "formatting_config"]`

### clewcrew-agents/src/clewcrew_agents/code_quality_expert.py:328

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `complexity_issues = [h for h in result.hallucinations if h.get("type") == "type_checking_config"]`

### clewcrew-agents/src/clewcrew_agents/security_expert.py:68

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"description": f"Subprocess usage detected: {pattern} - Security risk for command injection",`

### clewcrew-agents/src/clewcrew_agents/security_expert.py:187

**Type:** line_too_long
**Description:** Line is 94 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"critical_issues": len([h for h in result.hallucinations if h.get("priority") == "critical"]),`

### clewcrew-agents/src/clewcrew_agents/security_expert.py:226

**Type:** line_too_long
**Description:** Line is 96 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `if any(pattern in change_content.lower() for pattern in ["password", "secret", "key", "token"]):`

### clewcrew-agents/src/clewcrew_agents/security_expert.py:230

**Type:** line_too_long
**Description:** Line is 101 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `if any(pattern in change_content.lower() for pattern in ["subprocess", "os.system", "eval", "exec"]):`

### data/cost_analysis.py:42

**Type:** line_too_long
**Description:** Line is 101 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `system_message = "You are an expert analyst focused on identifying blind spots and potential issues."`

### data/cost_analysis.py:48

**Type:** line_too_long
**Description:** Line is 122 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Analyze this context and identify potential blind spots. Generate 5 challenging questions that reveal assumptions or gaps.`

### data/cost_analysis.py:112

**Type:** line_too_long
**Description:** Line is 101 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `system_message = "You are an expert analyst focused on identifying blind spots and potential issues."`

### data/cost_analysis.py:116

**Type:** line_too_long
**Description:** Line is 365 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Context: GitHub PR #1: Healthcare CDC Implementation with 28 commits, 11,222 additions, 90 deletions. Multiple Copilot AI reviewers found: 1) Missing package installation instructions, 2) Potential credential exposure via subprocess, 3) Unnecessary input sanitization. The PR implements real-time CDC operations for healthcare claims between DynamoDB and Snowflake.`

### data/cost_analysis.py:118

**Type:** line_too_long
**Description:** Line is 131 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Analyze this context from your perspective and identify blind spots. Generate 5 challenging questions that reveal potential issues.`

### data/cost_analysis.py:127

**Type:** line_too_long
**Description:** Line is 95 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Focus on your area of expertise and provide unique insights that other perspectives might miss.`

### data/cost_analysis.py:175

**Type:** line_too_long
**Description:** Line is 152 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `system_message = "You are an expert technical architect specializing in synthesizing diverse technical findings into actionable, prioritized solutions."`

### data/cost_analysis.py:180

**Type:** line_too_long
**Description:** Line is 165 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `findings_text += f"• {finding.get('agent', 'Unknown')} ({finding.get('category', 'unknown')}): {finding.get('question', '')} - {finding.get('recommendation', '')}\n"`

### data/cost_analysis.py:183

**Type:** line_too_long
**Description:** Line is 114 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `You are a senior technical architect tasked with synthesizing diverse findings into prioritized, actionable fixes.`

### data/cost_analysis.py:186

**Type:** line_too_long
**Description:** Line is 156 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `We have analyzed a GitHub PR for a Healthcare CDC implementation and found {len(findings_text.split('•')) - 1} diverse issues from multiple AI perspectives.`

### data/cost_analysis.py:191

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `3. Development Team (Code quality and maintainability) - Priority: 3, Decision Power: Medium`

### data/cost_analysis.py:192

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `4. Product Team (User experience and business value) - Priority: 4, Decision Power: Medium`

### data/cost_analysis.py:193

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `5. Business Stakeholders (Cost and timeline management) - Priority: 5, Decision Power: Low`

### data/cost_analysis.py:217

**Type:** line_too_long
**Description:** Line is 109 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Return as a JSON array of fixes, prioritizing fixes that address multiple high-priority stakeholder concerns.`

### data/cost_analysis.py:259

**Type:** line_too_long
**Description:** Line is 103 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `total_calls = multi_dimensional.get("calls", 0) + langgraph.get("calls", 0) + synthesis.get("calls", 0)`

### data/cost_analysis.py:260

**Type:** line_too_long
**Description:** Line is 131 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `total_input_tokens = multi_dimensional.get("input_tokens", 0) + langgraph.get("input_tokens", 0) + synthesis.get("input_tokens", 0)`

### data/cost_analysis.py:261

**Type:** line_too_long
**Description:** Line is 135 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `total_output_tokens = multi_dimensional.get("output_tokens", 0) + langgraph.get("output_tokens", 0) + synthesis.get("output_tokens", 0)`

### data/cost_analysis.py:262

**Type:** line_too_long
**Description:** Line is 117 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `total_cost = multi_dimensional.get("total_cost", 0) + langgraph.get("total_cost", 0) + synthesis.get("total_cost", 0)`

### data/cost_analysis.py:278

**Type:** line_too_long
**Description:** Line is 100 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `print(f"   Cost per 1K tokens: ${(total_cost/(total_input_tokens + total_output_tokens)*1000):.4f}")`

### docs/GITHUB_COPILOT_IMPLEMENTATION_PLAN.md:186

**Type:** one_line_commit
**Description:** One-line commit message detected
**Suggestion:** Use multi-line commit messages with proper descriptions
**Context:** `"""Request Copilot review for a pull request"""`

### docs/INTELLIGENT_LINTER_SYSTEM_SUMMARY.md:25

**Type:** one_line_commit
**Description:** One-line commit message detected
**Suggestion:** Use multi-line commit messages with proper descriptions
**Context:** `- **Configuration Generation**: Creates`.pre-commit-config.yaml`and`.ruff.toml\`\`

### docs/INTELLIGENT_LINTER_SYSTEM_SUMMARY.md:173

**Type:** one_line_commit
**Description:** One-line commit message detected
**Suggestion:** Use multi-line commit messages with proper descriptions
**Context:** `2. **Setup Pre-commit**:`pre-commit install\`\`

### docs/BRANCH_SEPARATION_SUMMARY.md:56

**Type:** one_line_commit
**Description:** One-line commit message detected
**Suggestion:** Use multi-line commit messages with proper descriptions
**Context:** `- **Files:**`.flake8`,`.pre-commit-config.yaml`,`.ruff.toml`,`scripts/`,`tests/\`\`

### docs/GIT_ENHANCED_AST_LEVEL_UP.md:30

**Type:** one_line_commit
**Description:** One-line commit message detected
**Suggestion:** Use multi-line commit messages with proper descriptions
**Context:** `"""Restore a file from a specific commit to a temporary location"""`

### docs/PR_2_automated_security_checks.md:146

**Type:** one_line_commit
**Description:** One-line commit message detected
**Suggestion:** Use multi-line commit messages with proper descriptions
**Context:** `git commit -m "test"`

### clewcrew-framework/src/clewcrew_framework/cli.py:142

**Type:** line_too_long
**Description:** Line is 107 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `print(f"{i}. {hallucination.get('type', 'unknown')}: {hallucination.get('description', 'No description')}")`

### clewcrew-framework/src/clewcrew_framework/cli.py:188

**Type:** line_too_long
**Description:** Line is 103 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `analysis_parser.add_argument("project_path", nargs="?", default=".", help="Path to project to analyze")`

### healthcare-cdc/healthcare_cdc_domain_model.py:6

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Based on: https://quickstarts.snowflake.com/guide/Streamline_Healthcare_CDC_DDB_And_Openflow/`

### healthcare-cdc/healthcare_cdc_domain_model.py:316

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Expected location: {os.path.join(os.getcwd(), 'healthcare-cdc', 'sql', 'merge_cdc_operations.sql')}\n"`

### healthcare-cdc/healthcare_cdc_domain_model.py:317

**Type:** line_too_long
**Description:** Line is 111 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"To resolve: Ensure the SQL template file exists or specify a custom path using sql_template_path parameter\n"`

### healthcare-cdc/healthcare_cdc_domain_model.py:431

**Type:** line_too_long
**Description:** Line is 119 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"aws kinesis put-record --stream-name ${StreamName} --partition-key test --data test >> /var/log/user-data.log 2>&1\n",`

### healthcare-cdc/**init**.py:6

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Based on: https://quickstarts.snowflake.com/guide/Streamline_Healthcare_CDC_DDB_And_Openflow/`

### healthcare-cdc/models/healthcare-cdc-infrastructure.yaml:53

**Type:** line_too_long
**Description:** Line is 152 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `AllowedPattern: '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$'`

### healthcare-cdc/models/healthcare-cdc-infrastructure.yaml:408

**Type:** line_too_long
**Description:** Line is 181 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `aws dynamodb describe-table --table-name ${DynamoDBTableName} --query 'Table.{Status:TableStatus,ItemCount:ItemCount,StreamEnabled:StreamSpecification.StreamEnabled}' --output table`

### healthcare-cdc/models/healthcare-cdc-infrastructure.yaml:413

**Type:** line_too_long
**Description:** Line is 145 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `aws kinesis describe-stream --stream-name ${KinesisStreamName} --query 'StreamDescription.{Status:StreamStatus,ShardCount:Shards}' --output table`

### tests/test_ghostbusters_gcp.py:115

**Type:** line_too_long
**Description:** Line is 103 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `mock_firestore.collection.return_value.order_by.return_value.limit.return_value.stream.return_value = (`

### tests/test_python_quality_enhanced.py:199

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"✅ Type annotation ratio: {annotation_ratio:.2f} ({annotated_functions}/{total_functions})",`

### clewcrew-recovery/src/clewcrew_recovery/**init**.py:6

**Type:** line_too_long
**Description:** Line is 95 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `code issues including syntax errors, indentation problems, import issues, and type annotations.`

### src/verify_ide_linting_hypothesis.py:325

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `report += "\n🎯 VERDICT: HYPOTHESIS CONFIRMED - IDE linting data IS fragmented and unreliable"`

### src/perfect_ast_generator.py:194

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `module_docstring="Perfect AST-Based Billing Analyzer\nGenerated with zero linting errors",`

### src/generate_linting_aware_generator.py:102

**Type:** line_too_long
**Description:** Line is 95 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `docstring="Function definition that knows about E302 (blank lines) and F821 (undefined names)",`

### src/generate_linting_aware_generator.py:280

**Type:** line_too_long
**Description:** Line is 129 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `module_docstring="Perfect Linting-Aware Code Generator\nModel encodes linting rules directly - no post-generation fixes needed!",`

### src/ultimate_perfect_generator.py:215

**Type:** line_too_long
**Description:** Line is 99 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `module_docstring="Ultimate Perfect AST-Based Billing Analyzer\nGenerated with ZERO linting errors",`

### src/linting_aware_model.py:299

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `module_docstring="Gemini-Integrated Billing Analyzer\nClean implementation with linting rules built-in",`

### src/enhanced_linting_aware_model.py:328

**Type:** line_too_long
**Description:** Line is 117 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `module_docstring="Enhanced Gemini-Integrated Billing Analyzer\nClean implementation with ALL linting rules built-in",`

### src/perfect_code_generator.py:286

**Type:** line_too_long
**Description:** Line is 120 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `docstring="Generator that CANNOT emit non-conforming code\nIntegrates with linting tools and validates before emission",`

### src/perfect_code_generator.py:399

**Type:** line_too_long
**Description:** Line is 137 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `module_docstring="Perfect Code Generator - CANNOT emit non-conforming code\nIntegrates with linting tools and validates before emission",`

### src/intelligent_model_generator.py:158

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `module_docstring="Intelligent Model-Driven Billing Analyzer\nGenerated with ZERO linting errors",`

### src/scaled_complex_model_generator.py:213

**Type:** line_too_long
**Description:** Line is 113 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"🎯 TOTAL ERRORS: {total_errors} (mypy: {len(self.model.mypy_errors)}, flake8: {len(self.model.flake8_errors)})",`

### src/recursive_code_generator.py:305

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `generated = f"{decomposed_model['quotes'][0]}{decomposed_model['value']}{decomposed_model['quotes'][1]}"`

### src/generate_code_generator.py:312

**Type:** line_too_long
**Description:** Line is 198 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `module_docstring="Deterministic Code Generation Tools\nStructured Python models for generating linting-compliant code\n\nMETA-RECURSIVE BREAKTHROUGH: This file was generated by the code generator!",`

### src/complete_linting_aware_generator.py:102

**Type:** line_too_long
**Description:** Line is 95 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `docstring="Function definition that knows about E302 (blank lines) and F821 (undefined names)",`

### src/complete_linting_aware_generator.py:438

**Type:** line_too_long
**Description:** Line is 138 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `module_docstring="Complete Perfect Linting-Aware Code Generator\nModel encodes linting rules directly - no post-generation fixes needed!",`

### src/complete_model_generator.py:159

**Type:** line_too_long
**Description:** Line is 99 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `def _generate_perfect_code_from_analysis(self, initial_code: str, analysis) -> str:  # type: ignore`

### src/complete_model_generator.py:213

**Type:** line_too_long
**Description:** Line is 94 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `module_docstring="Complete Model-Driven Billing Analyzer\nGenerated with ZERO linting errors",`

### src/code_quality_system/multi_agent_integration.py:4

**Type:** line_too_long
**Description:** Line is 98 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `This module provides integration between the quality system and the multi-agent testing framework,`

### src/code_quality_system/**init**.py:4

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Comprehensive code quality automation that integrates with the multi-agent testing framework,`

### src/code_quality_system/integrations/ci_cd_integration.py:154

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Setting quality threshold to {threshold} for {self.ci_config['environment']} environment"`

### src/security_first/https_enforcement.py:191

**Type:** line_too_long
**Description:** Line is 114 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"Content-Security-Policy": "default-src 'sel'; script-src 'sel' 'unsafe-inline'; style-src 'sel' 'unsafe-inline'",`

### src/security_first/rate_limiting.py:4

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Separate module for rate limiting functionality to avoid coupling with HTTPS enforcement.`

### src/security_first/test_streamlit_security_first.py:251

**Type:** line_too_long
**Description:** Line is 113 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/test-stack/12345678-1234-1234-1234-123456789012",`

### src/security_first/security_manager.py:109

**Type:** line_too_long
**Description:** Line is 114 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"Content-Security-Policy": "default-src 'sel'; script-src 'sel' 'unsafe-inline'; style-src 'sel' 'unsafe-inline'",`

### src/mdc_generator/mdc_model.py:205

**Type:** line_too_long
**Description:** Line is 116 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `If you don't have a deterministic tool for a format, acknowledge the limitation and use the best available approach.`

### src/visualization/comprehensive_dashboard.py:72

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `- **🔒 Security-First Architecture**: Credential management, HTTPS enforcement, rate limiting`

### src/visualization/comprehensive_dashboard.py:80

**Type:** line_too_long
**Description:** Line is 101 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `**All visualizations are generated as vector SVGs for infinite scalability and print-ready quality!**`

### src/model_driven_projection/test_projected_equivalence.py:24

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"tests/test_basic_validation.py::TestSecurityManager::test_credential_encryption_decryption",`

### src/model_driven_projection/improved_projection_system.py:211

**Type:** line_too_long
**Description:** Line is 413 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"SECURITY_CONFIG = {'fernet_key': os.getenv('FERNET_KEY', Fernet.generate_key()), 'redis_url': os.getenv('REDIS_URL', 'redis://localhost:6379'), 'jwt_secret': os.getenv('JWT_SECRET', 'your-secret-key'), 'session_timeout_minutes': int(os.getenv('SESSION_TIMEOUT_MINUTES', '15')), 'max_login_attempts': int(os.getenv('MAX_LOGIN_ATTEMPTS', '3')), 'password_min_length': int(os.getenv('PASSWORD_MIN_LENGTH', '12'))}",`

### src/model_driven_projection/improved_projection_system.py:212

**Type:** line_too_long
**Description:** Line is 160 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"AWS_CONFIG = {'region': os.getenv('AWS_REGION', 'us-east-1'), 'access_key': os.getenv('AWS_ACCESS_KEY_ID'), 'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY')}",`

### src/model_driven_projection/test_simple_equivalence.py:224

**Type:** line_too_long
**Description:** Line is 99 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"../../tests/test_basic_validation.py::TestSecurityManager::test_credential_encryption_decryption",`

### src/model_driven_projection/final_projection_system.py:164

**Type:** line_too_long
**Description:** Line is 413 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"SECURITY_CONFIG = {'fernet_key': os.getenv('FERNET_KEY', Fernet.generate_key()), 'redis_url': os.getenv('REDIS_URL', 'redis://localhost:6379'), 'jwt_secret': os.getenv('JWT_SECRET', 'your-secret-key'), 'session_timeout_minutes': int(os.getenv('SESSION_TIMEOUT_MINUTES', '15')), 'max_login_attempts': int(os.getenv('MAX_LOGIN_ATTEMPTS', '3')), 'password_min_length': int(os.getenv('PASSWORD_MIN_LENGTH', '12'))}",`

### src/model_driven_projection/final_projection_system.py:165

**Type:** line_too_long
**Description:** Line is 160 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"AWS_CONFIG = {'region': os.getenv('AWS_REGION', 'us-east-1'), 'access_key': os.getenv('AWS_ACCESS_KEY_ID'), 'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY')}",`

### src/model_driven_projection/projected_artifacts/src/security_first/input_validator.py:178

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `if not InputValidator.validate_file_extension(filename, allowed_extensions):  # type: ignore`

### src/model_driven_projection/projected_artifacts/src/streamlit/openflow_quickstart_app.py:56

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"""Store credential securely in Redis with encryption (alias for store_credential_secure)"""`

### src/model_driven_projection/projected_artifacts/src/streamlit/openflow_quickstart_app.py:70

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"exp": datetime.now(timezone.utc) + timedelta(minutes=int(timeout_minutes)),  # type: ignore`

### src/multi_agent_testing/test_anthropic_simple.py:36

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Jeopardy Question: What assumptions am I making about OAuth2 security and token management?`

### src/multi_agent_testing/test_anthropic_simple.py:38

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Generate 5 probing questions that would reveal blind spots, assumptions, or unknown unknowns.`

### src/multi_agent_testing/test_multi_agent_blind_spot_detection.py:166

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `recommendation="Implement automated testing, blue-green deployment, and drift detection",`

### src/multi_agent_testing/test_multi_agent_blind_spot_detection.py:232

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `recommendation="Implement screen reader support, keyboard navigation, and voice commands",`

### src/multi_agent_testing/test_multi_agent_blind_spot_detection.py:265

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `recommendation="Implement load testing, performance profiling, and resource optimization",`

### src/multi_agent_testing/code_quality_automation_orchestrator.py:314

**Type:** line_too_long
**Description:** Line is 111 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"analysis_question": "What are the current code quality issues and how should we address them systematically?",`

### src/multi_agent_testing/test_diversity_hypothesis.py:473

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `long_text = "This is a much longer text that should have more tokens for testing purposes"`

### src/multi_agent_testing/test_diversity_hypothesis.py:522

**Type:** line_too_long
**Description:** Line is 112 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%",`

### src/multi_agent_testing/test_model_traceability.py:131

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `secure_execute(["cfn-lint", "--version"], capture_output=True, check=True)  # type: ignore`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:76

**Type:** line_too_long
**Description:** Line is 370 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"context": "GitHub PR #1: Healthcare CDC Implementation with 28 commits, 11,222 additions, 90 deletions. Multiple Copilot AI reviewers found: 1) Missing package installation instructions, 2) Potential credential exposure via subprocess, 3) Unnecessary input sanitization. The PR implements real-time CDC operations for healthcare claims between DynamoDB and Snowflake.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:81

**Type:** line_too_long
**Description:** Line is 227 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"context": "Security audit of a financial services application with hardcoded credentials, missing input validation, and insufficient error handling. The application processes sensitive customer data and handles transactions.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:86

**Type:** line_too_long
**Description:** Line is 197 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"context": "Performance review of a high-traffic e-commerce platform experiencing slow response times, memory leaks, and database connection issues. The platform handles 10,000+ concurrent users.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:91

**Type:** line_too_long
**Description:** Line is 175 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"context": "DevOps pipeline review for a microservices architecture with deployment failures, monitoring gaps, and scalability issues. The system uses Kubernetes and Docker.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:96

**Type:** line_too_long
**Description:** Line is 180 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"context": "Code quality assessment of a legacy system with technical debt, poor documentation, and inconsistent coding standards. The system is critical for business operations.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:104

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"skeptical_partner": "You are a skeptical partner who questions assumptions and looks for blind spots.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:105

**Type:** line_too_long
**Description:** Line is 102 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"supportive_partner": "You are a supportive partner who builds on ideas and looks for opportunities.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:106

**Type:** line_too_long
**Description:** Line is 95 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"domain_expert": "You are a domain expert with deep technical knowledge in the specific area.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:107

**Type:** line_too_long
**Description:** Line is 95 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"human_advocate": "You are a human advocate who focuses on user experience and accessibility.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:108

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"risk_assessor": "You are a risk assessor who identifies potential problems and mitigation strategies.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:109

**Type:** line_too_long
**Description:** Line is 95 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"process_enforcer": "You are a process enforcer who ensures proper procedures and compliance.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:110

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"innovation_seeker": "You are an innovation seeker who looks for creative solutions and opportunities.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:111

**Type:** line_too_long
**Description:** Line is 100 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"quality_gatekeeper": "You are a quality gatekeeper who ensures high standards and best practices.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:116

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"direct_questions": "Ask direct, challenging questions about blind spots and assumptions.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:128

**Type:** line_too_long
**Description:** Line is 106 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"json_structured": "Return structured JSON with questions, confidence, blind spots, and recommendations.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:131

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"risk_matrix": "Return a risk matrix with likelihood, impact, and mitigation strategies.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:132

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"timeline": "Return a timeline with immediate, short-term, and long-term recommendations.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:133

**Type:** line_too_long
**Description:** Line is 103 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"stakeholder_analysis": "Return stakeholder analysis with impacts and recommendations for each group.",`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:164

**Type:** line_too_long
**Description:** Line is 109 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `IMPORTANT: Focus on your specific perspective and provide unique insights that other perspectives might miss.`

### src/multi_agent_testing/multi_dimensional_smoke_test.py:175

**Type:** line_too_long
**Description:** Line is 96 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"content": "You are an expert analyst focused on identifying blind spots and potential issues.",`

### src/multi_agent_testing/live_smoke_test_langchain.py:48

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `msg = f"Failed to initialize {provider} model: {str(e)}. Check API key validity and model availability."`

### src/multi_agent_testing/live_smoke_test_langchain.py:62

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Generate 5 probing questions that would reveal blind spots, assumptions, or unknown unknowns.`

### src/artifact_forge/agents/artifact_synthesizer.py:102

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `description=f"Found {len(critical_errors)} critical syntax errors affecting codebase health",`

### src/artifact_forge/agents/artifact_synthesizer.py:124

**Type:** line_too_long
**Description:** Line is 96 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `description=f"Codebase primarily consists of {primary_type[0]} files ({primary_type[1]} files)",`

### src/artifact_forge/agents/artifact_synthesizer.py:334

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `description=f"Found {len(performance_opportunities)} performance improvement opportunities",`

### src/artifact_forge/agents/artifact_synthesizer.py:362

**Type:** line_too_long
**Description:** Line is 102 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `description=f"Found {len(import_relationships)} import relationships indicating complex dependencies",`

### src/artifact_forge/agents/artifact_synthesizer.py:433

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"  {insight.title} ({insight.insight_type}, {insight.severity}): {insight.description}",`

### src/artifact_forge/agents/artifact_correlator.py:323

**Type:** line_too_long
**Description:** Line is 112 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"  {rel.source_artifact} -> {rel.target_artifact} ({rel.relationship_type}, confidence: {rel.confidence:.2f})",`

### src/secure_shell_service/real_client.py:33

**Type:** line_too_long
**Description:** Line is 210 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `output = "total 8\ndrwxr-xr-x 2 user user 4096 Aug  5 10:35 .\ndrwxr-xr-x 12 user user 4096 Aug  5 10:24 ..\n-rw-r--r-- 1 user user 1699 Aug  5 10:26 main.go\n-rw-r--r-- 1 user user 5024 Aug  5 10:26 client.py"`

### src/secure_shell_service/migration_example.py:46

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `result = await secure_execute(user_input, timeout=10, validate_input=True)  # type: ignore`

### src/secure_shell_service/migration_example.py:91

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `result = await secure_execute('find . -name "*.py" | head -5', timeout=10)  # type: ignore`

### gke-ai-microservices-hackathon/gke_cost_monitor.py:98

**Type:** line_too_long
**Description:** Line is 103 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"machine_type": cluster_info.get("nodePools", [{}])[0].get("config", {}).get("machineType", "unknown"),`

### gke-ai-microservices-hackathon/gke_cost_monitor.py:99

**Type:** line_too_long
**Description:** Line is 94 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"disk_size_gb": cluster_info.get("nodePools", [{}])[0].get("config", {}).get("diskSizeGb", 0),`

### gke-ai-microservices-hackathon/gke_cost_monitor.py:100

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"preemptible": cluster_info.get("nodePools", [{}])[0].get("config", {}).get("preemptible", False)`

### gke-ai-microservices-hackathon/gke_cost_monitor.py:164

**Type:** line_too_long
**Description:** Line is 101 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"cpu_utilization_percent": min(100, (total_cpu / (total_pods * 100)) * 100) if total_pods > 0 else 0,`

### gke-ai-microservices-hackathon/gke_cost_monitor.py:165

**Type:** line_too_long
**Description:** Line is 106 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"memory_utilization_percent": min(100, (total_memory / (total_pods * 256)) * 100) if total_pods > 0 else 0`

### gke-ai-microservices-hackathon/gke_cost_monitor.py:254

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `warnings.append(f"⚠️ Weekly cost ${weekly_cost} approaching threshold ${weekly_threshold}")`

### gke-ai-microservices-hackathon/gke_cost_monitor.py:263

**Type:** line_too_long
**Description:** Line is 94 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `warnings.append(f"⚠️ Monthly cost ${monthly_cost} approaching threshold ${monthly_threshold}")`

### gke-ai-microservices-hackathon/gke_cost_monitor.py:288

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `recommendations.append("💡 Consider using e2-micro machine type for development (cheaper)")`

### gke-ai-microservices-hackathon/gke_cost_monitor.py:307

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `recommendations.append("💡 Memory utilization is low - consider reducing resource requests")`

### gke-ai-microservices-hackathon/gke_cost_monitor.py:397

**Type:** line_too_long
**Description:** Line is 99 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `**Budget Status**: {'✅ Within Budget' if threshold_check.get('within_budget') else '❌ Over Budget'}`

### gke-ai-microservices-hackathon/scripts/generate-deploy-script.py:125

**Type:** line_too_long
**Description:** Line is 851 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `'# 🚀 Ghostbusters AI Microservices Deployment Script\n# GKE Hackathon Implementation\n#\n# Dependencies:\n# - gcloud CLI (Google Cloud SDK)\n# - kubectl (Kubernetes CLI) - install via: gcloud components install kubectl --quiet\n# - Note: Docker not required for GKE deployment (only needed for local container builds)\n#\n# Prerequisites:\n# - GCP project created and configured\n# - Required APIs enabled\n# - User authenticated and authorized\n#\n# Note: This script uses cost-effective GKE approaches:\n# - IPv4 stack type (no advanced datapath costs)\n# - Simplified cluster creation with essential flags only\n# - Accepts kubelet readonly port deprecation warnings (expected behavior)\n# - See Google docs: https://cloud.google.com/kubernetes-engine/docs/deprecations\n#\n# See GKE_DEPLOYMENT_DEPENDENCIES.md for detailed setup instructions\n\n',`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:85

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "gcloud version: $GCLOUD_VERSION"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:96

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "kubectl version: $KUBECTL_VERSION"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:110

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:111

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "Current project is '$CURRENT_PROJECT', expected '$PROJECT_ID'"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:112

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Setting project to $PROJECT_ID..."`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:113

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud config set project $PROJECT_ID`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:117

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if ! gcloud projects describe $PROJECT_ID &> /dev/null; then`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:118

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Project $PROJECT_ID not found or not accessible"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:134

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if gcloud services list --enabled --project=$PROJECT_ID --filter="name:$api" | grep -q "$api"; then`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:135

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "API enabled: $api"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:137

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Required API not enabled: $api"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:138

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Enable with: gcloud services enable $api --project=$PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:159

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud config set project $PROJECT_ID`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:160

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "Project set to: $PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:165

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Creating GKE cluster: $CLUSTER_NAME"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:168

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if gcloud container clusters describe $CLUSTER_NAME --zone=$ZONE &> /dev/null; then`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:169

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "Cluster $CLUSTER_NAME already exists"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:174

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud container clusters create $CLUSTER_NAME \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:175

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--zone=$ZONE \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:182

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--max-nodes=$MAX_NODES \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:205

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud container clusters update $CLUSTER_NAME \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:206

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--zone=$ZONE \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:211

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud container clusters update $CLUSTER_NAME \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:212

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--zone=$ZONE \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:223

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:320

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🎯 GKE Cluster: $CLUSTER_NAME"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:321

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🌐 Project: $PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:322

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📍 Zone: $ZONE"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:336

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  - Max Nodes: $MAX_NODES"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh:337

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  - Max Pods per Service: $MAX_PODS_PER_SERVICE"`

### gke-ai-microservices-hackathon/scripts/generate-setup-script.py:220

**Type:** line_too_long
**Description:** Line is 114 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `print(f"   🔍 Verification: {'PASSED' if 'verification_result' in locals() and verification_result else 'FAILED'}")`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:87

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Creating new GCP project: $PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:90

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if gcloud projects describe $PROJECT_ID &> /dev/null; then`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:91

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "Project $PROJECT_ID already exists"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:96

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud projects create $PROJECT_ID \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:97

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--name="$PROJECT_NAME" \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:100

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "GCP project created successfully: $PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:108

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud billing projects link $PROJECT_ID \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:109

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--billing-account=$BILLING_ACCOUNT`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:112

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `BILLING_STATUS=$(gcloud billing projects describe $PROJECT_ID --format="value(billingEnabled)")`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:114

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$BILLING_STATUS" = "True" ]; then`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:127

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Enabling API: $api"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:128

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud services enable $api --project=$PROJECT_ID`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:129

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "API enabled: $api"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:140

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `ENABLED_APIS=$(gcloud services list --enabled --project=$PROJECT_ID --format="value(name)")`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:144

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if echo "$ENABLED_APIS" | grep -q "$api"; then`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:145

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "WARNING: Excluded API $api is enabled - this may cause unwanted costs!"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:147

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "Excluded API $api is correctly disabled"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:158

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--billing-account=$BILLING_ACCOUNT \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:159

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--budget-amount=$MONTHLY_BUDGET \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:160

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--budget-filter="project=$PROJECT_ID" \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:175

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `PROJECT_STATUS=$(gcloud projects describe $PROJECT_ID --format="value(lifecycleState)")`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:176

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Project Status: $PROJECT_STATUS"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:179

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `BILLING_STATUS=$(gcloud billing projects describe $PROJECT_ID --format="value(billingEnabled)")`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:180

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Billing Status: $BILLING_STATUS"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:183

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `ENABLED_API_COUNT=$(gcloud services list --enabled --project=$PROJECT_ID --format="value(name)" | wc -l)`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:184

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Enabled APIs: $ENABLED_API_COUNT"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:189

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud services list --enabled --project=$PROJECT_ID --format="table(name,title)" | head -10`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:194

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud billing budgets list --billing-account=$BILLING_ACCOUNT --filter="displayName:2025"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:207

**Type:** line_too_long
**Description:** Line is 139 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `sed -i "s/❌ Cost Control Configuration - Not started/✅ Cost Control Configuration - Completed $(date +%Y-%m-%d)/" PROJECT_SETUP_TRACKING.md`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:221

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "✅ GCP Project: $PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:222

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "✅ Project Name: $PROJECT_NAME"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:223

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "✅ Billing Account: $BILLING_ACCOUNT"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:232

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "2. Check costs: gcloud billing reports list --project=$PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:233

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "3. Monitor APIs: gcloud services list --enabled --project=$PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh:260

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Project $PROJECT_ID is ready for Ghostbusters AI deployment!"`

### gke-ai-microservices-hackathon/scripts/update-deployment-state.py:4

**Type:** line_too_long
**Description:** Line is 94 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Updates the deployment state in the project model registry based on current GKE cluster status`

### gke-ai-microservices-hackathon/scripts/update-deployment-state.py:245

**Type:** line_too_long
**Description:** Line is 96 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `project_id = hackathon_config['gcp_project_setup']['deploy_template']['variables']['project_id']`

### gke-ai-microservices-hackathon/scripts/update-deployment-state.py:299

**Type:** line_too_long
**Description:** Line is 103 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `status_emoji = "✅" if service["status"] == "Running" else "⚠️" if service["status"] == "Mixed" else "❌"`

### gke-ai-microservices-hackathon/scripts/update-deployment-state.py:300

**Type:** line_too_long
**Description:** Line is 119 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `print(f"      {status_emoji} {service['name']}: {service['status']} ({service['ready_pods']}/{service['total_pods']})")`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:66

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo -e "${RED}Are you absolutely sure you want to delete project $PROJECT_ID?${NC}"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:70

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$confirmation" != "DELETE" ]; then`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:95

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if ! gcloud projects describe $PROJECT_ID &> /dev/null; then`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:96

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Project $PROJECT_ID does not exist"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:108

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `ENABLED_APIS=$(gcloud services list --enabled --project=$PROJECT_ID --format="value(name)")`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:110

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$ENABLED_APIS" ]; then`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:116

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `for api in $ENABLED_APIS; do`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:117

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Disabling API: $api"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:118

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud services disable $api --project=$PROJECT_ID --quiet || print_warning "Failed to disable $api"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:129

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `CLUSTERS=$(gcloud container clusters list --project=$PROJECT_ID --format="value(name,location)" 2>/dev/null || echo "")`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:131

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$CLUSTERS" ]; then`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:135

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$cluster_info" ]; then`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:136

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `CLUSTER_NAME=$(echo "$cluster_info" | cut -d' ' -f1)`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:137

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `LOCATION=$(echo "$cluster_info" | cut -d' ' -f2)`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:139

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Deleting cluster: $CLUSTER_NAME in $LOCATION"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:140

**Type:** line_too_long
**Description:** Line is 155 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `gcloud container clusters delete $CLUSTER_NAME --location=$LOCATION --project=$PROJECT_ID --quiet || print_warning "Failed to delete cluster $CLUSTER_NAME"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:140

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud container clusters delete $CLUSTER_NAME --location=$LOCATION --project=$PROJECT_ID --quiet || print_warning "Failed to delete cluster $CLUSTER_NAME"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:142

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `done <<< "$CLUSTERS"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:153

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `INSTANCES=$(gcloud compute instances list --project=$PROJECT_ID --format="value(name,zone)" 2>/dev/null || echo "")`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:155

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$INSTANCES" ]; then`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:159

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$instance_info" ]; then`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:160

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `INSTANCE_NAME=$(echo "$instance_info" | cut -d' ' -f1)`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:161

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `ZONE=$(echo "$instance_info" | cut -d' ' -f2)`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:163

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Deleting instance: $INSTANCE_NAME in $ZONE"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:164

**Type:** line_too_long
**Description:** Line is 149 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `gcloud compute instances delete $INSTANCE_NAME --zone=$ZONE --project=$PROJECT_ID --quiet || print_warning "Failed to delete instance $INSTANCE_NAME"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:164

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud compute instances delete $INSTANCE_NAME --zone=$ZONE --project=$PROJECT_ID --quiet || print_warning "Failed to delete instance $INSTANCE_NAME"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:166

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `done <<< "$INSTANCES"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:177

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `BUCKETS=$(gsutil ls -p $PROJECT_ID 2>/dev/null || echo "")`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:179

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$BUCKETS" ]; then`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:182

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `for bucket in $BUCKETS; do`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:183

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$bucket" ]; then`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:184

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Deleting bucket: $bucket"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:185

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gsutil -m rm -r $bucket || print_warning "Failed to delete bucket $bucket"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:198

**Type:** line_too_long
**Description:** Line is 147 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `BUDGETS=$(gcloud billing budgets list --billing-account=$BILLING_ACCOUNT --filter="displayName:2025" --format="value(name)" 2>/dev/null || echo "")`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:198

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `BUDGETS=$(gcloud billing budgets list --billing-account=$BILLING_ACCOUNT --filter="displayName:2025" --format="value(name)" 2>/dev/null || echo "")`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:200

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$BUDGETS" ]; then`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:201

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `for budget in $BUDGETS; do`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:202

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$budget" ]; then`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:203

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Deleting budget: $budget"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:204

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud billing budgets delete $budget --quiet || print_warning "Failed to delete budget $budget"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:217

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud billing projects unlink $PROJECT_ID --quiet || print_warning "Failed to unlink billing account"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:224

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Deleting project $PROJECT_ID..."`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:227

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud projects delete $PROJECT_ID --quiet`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:229

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "Project $PROJECT_ID deleted successfully"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:242

**Type:** line_too_long
**Description:** Line is 137 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `sed -i "s/✅ Cost Control Configuration - Completed.*/❌ Cost Control Configuration - Removed $(date +%Y-%m-%d)/" PROJECT_SETUP_TRACKING.md`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:254

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🗑️  Project Deleted: $PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:255

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🗑️  Project Name: $PROJECT_NAME"`

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh:287

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Project $PROJECT_ID has been completely removed."`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:87

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Creating new GCP project: $PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:90

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if gcloud projects describe $PROJECT_ID &> /dev/null; then`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:91

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "Project $PROJECT_ID already exists"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:96

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud projects create $PROJECT_ID \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:97

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--name="$PROJECT_NAME" \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:100

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "GCP project created successfully: $PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:108

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud billing projects link $PROJECT_ID \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:109

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--billing-account=$BILLING_ACCOUNT`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:112

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `BILLING_STATUS=$(gcloud billing projects describe $PROJECT_ID --format="value(billingEnabled)")`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:114

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$BILLING_STATUS" = "True" ]; then`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:127

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Enabling API: $api"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:128

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud services enable $api --project=$PROJECT_ID`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:129

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "API enabled: $api"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:140

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `ENABLED_APIS=$(gcloud services list --enabled --project=$PROJECT_ID --format="value(name)")`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:144

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if echo "$ENABLED_APIS" | grep -q "$api"; then`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:145

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "WARNING: Excluded API $api is enabled - this may cause unwanted costs!"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:147

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "Excluded API $api is correctly disabled"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:158

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--billing-account=$BILLING_ACCOUNT \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:159

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--budget-amount=$MONTHLY_BUDGET \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:160

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--budget-filter="project=$PROJECT_ID" \`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:175

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `PROJECT_STATUS=$(gcloud projects describe $PROJECT_ID --format="value(lifecycleState)")`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:176

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Project Status: $PROJECT_STATUS"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:179

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `BILLING_STATUS=$(gcloud billing projects describe $PROJECT_ID --format="value(billingEnabled)")`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:180

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Billing Status: $BILLING_STATUS"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:183

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `ENABLED_API_COUNT=$(gcloud services list --enabled --project=$PROJECT_ID --format="value(name)" | wc -l)`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:184

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Enabled APIs: $ENABLED_API_COUNT"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:189

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud services list --enabled --project=$PROJECT_ID --format="table(name,title)" | head -10`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:194

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud billing budgets list --billing-account=$BILLING_ACCOUNT --filter="displayName:2025"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:207

**Type:** line_too_long
**Description:** Line is 139 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `sed -i "s/❌ Cost Control Configuration - Not started/✅ Cost Control Configuration - Completed $(date +%Y-%m-%d)/" PROJECT_SETUP_TRACKING.md`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:221

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "✅ GCP Project: $PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:222

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "✅ Project Name: $PROJECT_NAME"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:223

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "✅ Billing Account: $BILLING_ACCOUNT"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:232

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "2. Check costs: gcloud billing reports list --project=$PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:233

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "3. Monitor APIs: gcloud services list --enabled --project=$PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh:260

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Project $PROJECT_ID is ready for Ghostbusters AI deployment!"`

### gke-ai-microservices-hackathon/scripts/setup-gke-notifications.py:106

**Type:** line_too_long
**Description:** Line is 149 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"filter": f'resource.type="k8s_container" AND resource.labels.cluster_name="{cluster_name}" AND resource.labels.container_name!="gke-metrics-agent"',`

### gke-ai-microservices-hackathon/scripts/setup-gke-notifications.py:123

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"filter": f'resource.type="gce_instance" AND resource.labels.cluster_name="{cluster_name}"',`

### gke-ai-microservices-hackathon/scripts/setup-gke-notifications.py:140

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"filter": f'resource.type="gce_instance" AND resource.labels.cluster_name="{cluster_name}"',`

### gke-ai-microservices-hackathon/scripts/setup-gke-notifications.py:200

**Type:** line_too_long
**Description:** Line is 94 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `'pubsub.googleapis.com/projects/{project_id}/topics/gke-events'.format(project_id=project_id),`

### gke-ai-microservices-hackathon/scripts/setup-gke-notifications.py:201

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `'--log-filter', f'resource.type="k8s_cluster" AND resource.labels.cluster_name="{cluster_name}"',`

### gke-ai-microservices-hackathon/scripts/setup-gke-notifications.py:348

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"filter": f'resource.type="k8s_container" AND resource.labels.cluster_name="{cluster_name}"',`

### gke-ai-microservices-hackathon/scripts/setup-gke-notifications.py:364

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"filter": f'resource.type="gce_instance" AND resource.labels.cluster_name="{cluster_name}"',`

### gke-ai-microservices-hackathon/scripts/test-array-equivalence.sh:34

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "     - $api"`

### gke-ai-microservices-hackathon/scripts/test-array-equivalence.sh:40

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "     - $api"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:77

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "gcloud version: $GCLOUD_VERSION"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:88

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "kubectl version: $KUBECTL_VERSION"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:102

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:103

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "Current project is '$CURRENT_PROJECT', expected '$PROJECT_ID'"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:104

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Setting project to $PROJECT_ID..."`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:105

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud config set project $PROJECT_ID`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:109

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if ! gcloud projects describe $PROJECT_ID &> /dev/null; then`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:110

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Project $PROJECT_ID not found or not accessible"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:126

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if gcloud services list --enabled --project=$PROJECT_ID --filter="name:$api" | grep -q "$api"; then`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:127

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "API enabled: $api"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:129

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Required API not enabled: $api"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:130

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Enable with: gcloud services enable $api --project=$PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:151

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud config set project $PROJECT_ID`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:152

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "Project set to: $PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:157

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_info "Creating GKE cluster: $CLUSTER_NAME"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:160

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if gcloud container clusters describe $CLUSTER_NAME --zone=$ZONE &> /dev/null; then`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:161

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "Cluster $CLUSTER_NAME already exists"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:166

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud container clusters create $CLUSTER_NAME \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:167

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--zone=$ZONE \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:174

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--max-nodes=$MAX_NODES \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:197

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud container clusters update $CLUSTER_NAME \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:198

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--zone=$ZONE \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:203

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud container clusters update $CLUSTER_NAME \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:204

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--zone=$ZONE \`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:215

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:312

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🎯 GKE Cluster: $CLUSTER_NAME"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:313

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🌐 Project: $PROJECT_ID"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:314

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📍 Zone: $ZONE"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:328

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  - Max Nodes: $MAX_NODES"`

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh:329

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  - Max Pods per Service: $MAX_PODS_PER_SERVICE"`

### scripts/enforce_make_only_venv.sh:10

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ ! -d "$VENV_PATH" ]; then`

### scripts/enforce_make_only_venv.sh:11

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "❌ Virtual environment not found at $VENV_PATH"`

### scripts/enforce_make_only_venv.sh:18

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cp "$VENV_PATH/bin/pytest" "$VENV_PATH/bin/pytest.original"`

### scripts/enforce_make_only_venv.sh:19

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cp "$VENV_PATH/bin/flake8" "$VENV_PATH/bin/flake8.original"`

### scripts/enforce_make_only_venv.sh:20

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cp "$VENV_PATH/bin/black" "$VENV_PATH/bin/black.original"`

### scripts/enforce_make_only_venv.sh:21

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cp "$VENV_PATH/bin/mypy" "$VENV_PATH/bin/mypy.original"`

### scripts/enforce_make_only_venv.sh:26

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cat > "$VENV_PATH/bin/pytest" << 'EOF'`

### scripts/enforce_make_only_venv.sh:75

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cat > "$VENV_PATH/bin/flake8" << 'EOF'`

### scripts/enforce_make_only_venv.sh:117

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cat > "$VENV_PATH/bin/black" << 'EOF'`

### scripts/enforce_make_only_venv.sh:159

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cat > "$VENV_PATH/bin/mypy" << 'EOF'`

### scripts/enforce_make_only_venv.sh:201

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `chmod +x "$VENV_PATH/bin/pytest"`

### scripts/enforce_make_only_venv.sh:202

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `chmod +x "$VENV_PATH/bin/flake8"`

### scripts/enforce_make_only_venv.sh:203

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `chmod +x "$VENV_PATH/bin/black"`

### scripts/enforce_make_only_venv.sh:204

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `chmod +x "$VENV_PATH/bin/mypy"`

### scripts/create_proper_notebook.py:45

**Type:** line_too_long
**Description:** Line is 125 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `This notebook uses Gemini LLM with LangGraph/LangChain to analyze your GCP billing data and provide intelligent insights.""",`

### scripts/create_proper_notebook.py:112

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `result = subprocess.run(["uv", "run", "python", "scripts/gcp_billing_daily_reporter.py"],`

### scripts/create_proper_notebook.py:240

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `service_totals = daily_data.groupby('service')['cost'].sum().sort_values(ascending=False)`

### scripts/setup-github-connection.sh:17

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📋 Project: $PROJECT_ID"`

### scripts/setup-github-connection.sh:18

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🌍 Region: $REGION"`

### scripts/setup-github-connection.sh:19

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 Connection: $CONNECTION_NAME"`

### scripts/setup-github-connection.sh:20

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📦 Repository: $REPO_OWNER/$REPO_NAME"`

### scripts/setup-github-connection.sh:45

**Type:** line_too_long
**Description:** Line is 132 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `echo -n "$GITHUB_TOKEN" | gcloud secrets create "$SECRET_NAME" --data-file=- --project="$PROJECT_ID" || echo "Secret already exists"`

### scripts/setup-github-connection.sh:45

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo -n "$GITHUB_TOKEN" | gcloud secrets create "$SECRET_NAME" --data-file=- --project="$PROJECT_ID" || echo "Secret already exists"`

### scripts/setup-github-connection.sh:49

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")`

### scripts/setup-github-connection.sh:52

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud secrets add-iam-policy-binding "$SECRET_NAME" \`

### scripts/setup-github-connection.sh:55

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID"`

### scripts/setup-github-connection.sh:66

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud builds connections create github "$CONNECTION_NAME" \`

### scripts/setup-github-connection.sh:67

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--authorizer-token-secret-version="projects/$PROJECT_ID/secrets/$SECRET_NAME/versions/1" \`

### scripts/setup-github-connection.sh:68

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--app-installation-id="$INSTALLATION_ID" \`

### scripts/setup-github-connection.sh:69

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/setup-github-connection.sh:70

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID"`

### scripts/setup-github-connection.sh:74

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `REPO_URI="https://github.com/$REPO_OWNER/$REPO_NAME.git"`

### scripts/setup-github-connection.sh:76

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud builds repositories create "$REPO_NAME" \`

### scripts/setup-github-connection.sh:77

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--remote-uri="$REPO_URI" \`

### scripts/setup-github-connection.sh:78

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--connection="$CONNECTION_NAME" \`

### scripts/setup-github-connection.sh:79

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/setup-github-connection.sh:80

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID"`

### scripts/setup-github-connection.sh:85

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--name="$TRIGGER_NAME" \`

### scripts/setup-github-connection.sh:86

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--repo-name="$REPO_NAME" \`

### scripts/setup-github-connection.sh:87

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--repo-owner="$REPO_OWNER" \`

### scripts/setup-github-connection.sh:90

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/setup-github-connection.sh:97

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Connection: $CONNECTION_NAME"`

### scripts/setup-github-connection.sh:98

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Repository: $REPO_NAME"`

### scripts/setup-github-connection.sh:99

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Trigger: $TRIGGER_NAME"`

### scripts/setup-github-connection.sh:102

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View triggers: https://console.cloud.google.com/cloud-build/triggers?project=$PROJECT_ID"`

### scripts/setup-github-connection.sh:103

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View builds: https://console.cloud.google.com/cloud-build/builds?project=$PROJECT_ID"`

### scripts/gemini_gcp_billing_analyzer.py:290

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"This notebook contains comprehensive analysis of your GCP billing data using Gemini LLM.",`

### scripts/gemini_gcp_billing_analyzer.py:405

**Type:** line_too_long
**Description:** Line is 101 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"    print(f\"\\n💰 Potential Monthly Savings: ${optimizations.get('potential_savings', 0):.2f}\")\n",`

### scripts/gemini_gcp_billing_analyzer.py:459

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"    print(f\"🔮 Next Month Forecast: ${forecast.get('next_month_forecast', 0):.2f}\")\n",`

### scripts/gemini_gcp_billing_analyzer.py:460

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"    print(f\"📊 Forecast Confidence: {forecast.get('forecast_confidence', 'Unknown')}\")\n",`

### scripts/gemini_gcp_billing_analyzer.py:500

**Type:** line_too_long
**Description:** Line is 95 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"service_columns = [col for col in daily_data.columns if col not in ['date', 'total_cost']]\n",`

### scripts/gemini_gcp_billing_analyzer.py:554

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"    for i, rec in enumerate(optimizations.get('optimization_recommendations', []), 1):\n",`

### scripts/gemini_gcp_billing_analyzer.py:557

**Type:** line_too_long
**Description:** Line is 100 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"    print(f\"\\n💰 Expected Monthly Savings: ${optimizations.get('potential_savings', 0):.2f}\")\n",`

### scripts/gemini_gcp_billing_analyzer.py:571

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `'print(f\'📅 Analysis Period: {daily_data["date"].min()} to {daily_data["date"].max()}\')\n',`

### scripts/gemini_gcp_billing_analyzer.py:714

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"1. Open the notebook: data/billing_reports/analysis_data/gemini_billing_analysis.ipynb",`

### scripts/run_live_smoke_test.sh:10

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$OPENAI_API_KEY" ] || [ -n "$ANTHROPIC_API_KEY" ]; then`

### scripts/gcp_billing_daily_reporter.py:68

**Type:** line_too_long
**Description:** Line is 101 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"📅 Fetching billing data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",`

### scripts/gcp_billing_daily_reporter.py:489

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"service_summary = df.groupby('service')['cost'].agg(['sum', 'mean', 'count']).round(4)\n",`

### scripts/gcp_billing_daily_reporter.py:543

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"    subplot_titles=('Daily Cost Trend', 'Service Breakdown', 'Cost Distribution', 'Service Count'),\n",`

### scripts/gcp_billing_daily_reporter.py:637

**Type:** line_too_long
**Description:** Line is 98 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `date_range = f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}"`

### scripts/deploy-container.sh:16

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Project ID: $PROJECT_ID"`

### scripts/deploy-container.sh:17

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Region: $REGION"`

### scripts/deploy-container.sh:18

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Service Name: $SERVICE_NAME"`

### scripts/deploy-container.sh:19

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Image Name: $IMAGE_NAME"`

### scripts/deploy-container.sh:42

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud builds submit --tag "$IMAGE_NAME" --project="$PROJECT_ID" .`

### scripts/deploy-container.sh:47

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud run deploy "$SERVICE_NAME" \`

### scripts/deploy-container.sh:48

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--image="$IMAGE_NAME" \`

### scripts/deploy-container.sh:50

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/deploy-container.sh:51

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/deploy-container.sh:58

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--set-env-vars="PROJECT_ID=$PROJECT_ID" \`

### scripts/deploy-container.sh:62

**Type:** line_too_long
**Description:** Line is 131 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region="$REGION" --project="$PROJECT_ID" --format="value(status.url)")`

### scripts/deploy-container.sh:62

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region="$REGION" --project="$PROJECT_ID" --format="value(status.url)")`

### scripts/deploy-container.sh:67

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📋 Service URL: $SERVICE_URL"`

### scripts/deploy-container.sh:71

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  curl -X POST $SERVICE_URL/analyze \\"`

### scripts/deploy-container.sh:76

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  curl $SERVICE_URL/status/YOUR_JOB_ID"`

### scripts/deploy-container.sh:79

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  curl $SERVICE_URL/jobs"`

### scripts/deploy-container.sh:82

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  curl $SERVICE_URL/health"`

### scripts/rule-compliance-check.sh:16

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"`

### scripts/rule-compliance-check.sh:17

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `RULES_DIR="$PROJECT_ROOT/.cursor/rules"`

### scripts/rule-compliance-check.sh:44

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `case "$file_type" in`

### scripts/rule-compliance-check.sh:46

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_info "Checking deterministic editing for $file"`

### scripts/rule-compliance-check.sh:49

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if grep -q "edit_file" "$file" 2>/dev/null; then`

### scripts/rule-compliance-check.sh:50

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_error "File $file may use non-deterministic edit_file tool"`

### scripts/rule-compliance-check.sh:55

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$file_type" == "mdc" ]]; then`

### scripts/rule-compliance-check.sh:56

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if ! grep -q "^---$" "$file" 2>/dev/null; then`

### scripts/rule-compliance-check.sh:57

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_error "File $file missing YAML frontmatter"`

### scripts/rule-compliance-check.sh:61

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if ! grep -q "description:" "$file" 2>/dev/null; then`

### scripts/rule-compliance-check.sh:62

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_error "File $file missing description in frontmatter"`

### scripts/rule-compliance-check.sh:66

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if ! grep -q "globs:" "$file" 2>/dev/null; then`

### scripts/rule-compliance-check.sh:67

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_error "File $file missing globs in frontmatter"`

### scripts/rule-compliance-check.sh:72

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_success "File $file passes deterministic editing checks"`

### scripts/rule-compliance-check.sh:82

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_info "Checking security compliance for $file"`

### scripts/rule-compliance-check.sh:85

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if grep -q -E "(password|secret|key|token).*=.*['\"][^'\"]*['\"]" "$file" 2>/dev/null; then`

### scripts/rule-compliance-check.sh:86

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_error "File $file contains potential hardcoded credentials"`

### scripts/rule-compliance-check.sh:91

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if grep -q "AKIA[0-9A-Z]\{16\}" "$file" 2>/dev/null; then`

### scripts/rule-compliance-check.sh:92

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_error "File $file contains potential AWS access keys"`

### scripts/rule-compliance-check.sh:97

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if grep -q "[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}" "$file" 2>/dev/null; then`

### scripts/rule-compliance-check.sh:98

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_warning "File $file contains UUID patterns (may be legitimate)"`

### scripts/rule-compliance-check.sh:101

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_success "File $file passes security compliance checks"`

### scripts/rule-compliance-check.sh:113

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_info "Checking .mdc file structure for $file"`

### scripts/rule-compliance-check.sh:116

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if ! awk '/^---$/{count++} END{exit count!=2}' "$file" 2>/dev/null; then`

### scripts/rule-compliance-check.sh:117

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_error "File $file has incorrect YAML frontmatter structure"`

### scripts/rule-compliance-check.sh:127

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$line" =~ ^description: ]]; then`

### scripts/rule-compliance-check.sh:129

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `elif [[ "$line" =~ ^globs: ]]; then`

### scripts/rule-compliance-check.sh:131

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `elif [[ "$line" =~ ^alwaysApply: ]]; then`

### scripts/rule-compliance-check.sh:134

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `done < "$file"`

### scripts/rule-compliance-check.sh:136

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$has_description" == "false" ]]; then`

### scripts/rule-compliance-check.sh:137

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_error "File $file missing description field"`

### scripts/rule-compliance-check.sh:141

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$has_globs" == "false" ]]; then`

### scripts/rule-compliance-check.sh:142

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_error "File $file missing globs field"`

### scripts/rule-compliance-check.sh:146

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$has_always_apply" == "false" ]]; then`

### scripts/rule-compliance-check.sh:147

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_error "File $file missing alwaysApply field"`

### scripts/rule-compliance-check.sh:151

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_success "File $file has correct .mdc structure"`

### scripts/rule-compliance-check.sh:159

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_info "Checking file organization compliance for $file"`

### scripts/rule-compliance-check.sh:163

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `local dir_name="$(dirname "$file")"`

### scripts/rule-compliance-check.sh:165

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `case "$file_type" in`

### scripts/rule-compliance-check.sh:167

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$dir_name" == "src/"* ]] || [[ "$dir_name" == "tests/" ]] || [[ "$dir_name" == "scripts/" ]]; then`

### scripts/rule-compliance-check.sh:168

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_success "Python file $file is in appropriate directory"`

### scripts/rule-compliance-check.sh:170

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_warning "Python file $file may be in wrong directory"`

### scripts/rule-compliance-check.sh:174

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$dir_name" == "docs/" ]] || [[ "$dir_name" == "." ]] || [[ "$dir_name" == "healthcare-cdc/" ]]; then`

### scripts/rule-compliance-check.sh:175

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_success "Markdown file $file is in appropriate directory"`

### scripts/rule-compliance-check.sh:177

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_warning "Markdown file $file may be in wrong directory"`

### scripts/rule-compliance-check.sh:181

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$dir_name" == "config/" ]] || [[ "$dir_name" == "." ]]; then`

### scripts/rule-compliance-check.sh:182

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_success "YAML file $file is in appropriate directory"`

### scripts/rule-compliance-check.sh:184

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_warning "YAML file $file may be in wrong directory"`

### scripts/rule-compliance-check.sh:188

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$dir_name" == "data/" ]] || [[ "$dir_name" == "config/" ]] || [[ "$dir_name" == "." ]]; then`

### scripts/rule-compliance-check.sh:189

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_success "JSON file $file is in appropriate directory"`

### scripts/rule-compliance-check.sh:191

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_warning "JSON file $file may be in wrong directory"`

### scripts/rule-compliance-check.sh:202

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_info "Validating file: $file"`

### scripts/rule-compliance-check.sh:207

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if ! check_deterministic_editing "$file"; then`

### scripts/rule-compliance-check.sh:211

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if ! check_security_compliance "$file"; then`

### scripts/rule-compliance-check.sh:215

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if ! check_mdc_structure "$file"; then`

### scripts/rule-compliance-check.sh:219

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `check_file_organization "$file"`

### scripts/rule-compliance-check.sh:221

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$has_violations" == "true" ]]; then`

### scripts/rule-compliance-check.sh:234

**Type:** line_too_long
**Description:** Line is 154 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `files_to_check=$(find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.mdc" -o -name "*.sh" \) \`

### scripts/rule-compliance-check.sh:248

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ -n "$file" ]]; then`

### scripts/rule-compliance-check.sh:249

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if ! validate_file "$file"; then`

### scripts/rule-compliance-check.sh:253

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `done <<< "$files_to_check"`

### scripts/rule-compliance-check.sh:258

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_info "Total files checked: $TOTAL_CHECKS"`

### scripts/rule-compliance-check.sh:259

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_info "Violations found: $VIOLATIONS"`

### scripts/rule-compliance-check.sh:260

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_info "Files with issues: $failed_files"`

### scripts/rule-compliance-check.sh:262

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ $VIOLATIONS -eq 0 ]]; then`

### scripts/rule-compliance-check.sh:266

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `log_error "Found $VIOLATIONS violations. Please fix before committing."`

### scripts/setup-develop-trigger.sh:15

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📋 Project: $PROJECT_ID"`

### scripts/setup-develop-trigger.sh:16

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 Trigger: $TRIGGER_NAME"`

### scripts/setup-develop-trigger.sh:17

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🌿 Branch: $BRANCH_PATTERN"`

### scripts/setup-develop-trigger.sh:18

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "👤 Owner: $REPO_OWNER"`

### scripts/setup-develop-trigger.sh:24

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--name="$TRIGGER_NAME" \`

### scripts/setup-develop-trigger.sh:25

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--repo-name="$REPO_NAME" \`

### scripts/setup-develop-trigger.sh:26

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--repo-owner="$REPO_OWNER" \`

### scripts/setup-develop-trigger.sh:27

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--branch-pattern="$BRANCH_PATTERN" \`

### scripts/setup-develop-trigger.sh:29

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/setup-develop-trigger.sh:35

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Name: $TRIGGER_NAME"`

### scripts/setup-develop-trigger.sh:36

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Repository: $REPO_NAME"`

### scripts/setup-develop-trigger.sh:37

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Owner: $REPO_OWNER"`

### scripts/setup-develop-trigger.sh:38

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Branch: $BRANCH_PATTERN"`

### scripts/setup-develop-trigger.sh:41

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View triggers: https://console.cloud.google.com/cloud-build/triggers?project=$PROJECT_ID"`

### scripts/setup-develop-trigger.sh:42

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View builds: https://console.cloud.google.com/cloud-build/builds?project=$PROJECT_ID"`

### scripts/deploy-ghostbusters-gcp.sh:26

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Project ID: $PROJECT_ID"`

### scripts/deploy-ghostbusters-gcp.sh:27

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Region: $REGION"`

### scripts/deploy-ghostbusters-gcp.sh:33

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/deploy-ghostbusters-gcp.sh:34

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/deploy-ghostbusters-gcp.sh:43

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--set-env-vars="PROJECT_ID=$PROJECT_ID,ENVIRONMENT=production,LOG_LEVEL=INFO"`

### scripts/deploy-ghostbusters-gcp.sh:48

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/deploy-ghostbusters-gcp.sh:49

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/deploy-ghostbusters-gcp.sh:58

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--set-env-vars="PROJECT_ID=$PROJECT_ID,ENVIRONMENT=production,LOG_LEVEL=INFO"`

### scripts/deploy-ghostbusters-gcp.sh:63

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/deploy-ghostbusters-gcp.sh:64

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/deploy-ghostbusters-gcp.sh:73

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--set-env-vars="PROJECT_ID=$PROJECT_ID,ENVIRONMENT=production,LOG_LEVEL=INFO"`

### scripts/deploy-ghostbusters-gcp.sh:78

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/deploy-ghostbusters-gcp.sh:79

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/deploy-ghostbusters-gcp.sh:88

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--set-env-vars="PROJECT_ID=$PROJECT_ID,ENVIRONMENT=production,LOG_LEVEL=INFO"`

### scripts/deploy-ghostbusters-gcp.sh:93

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/deploy-ghostbusters-gcp.sh:94

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/deploy-ghostbusters-gcp.sh:103

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--set-env-vars="PROJECT_ID=$PROJECT_ID,ENVIRONMENT=production,LOG_LEVEL=INFO"`

### scripts/deploy-ghostbusters-gcp.sh:108

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/deploy-ghostbusters-gcp.sh:109

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/deploy-ghostbusters-gcp.sh:118

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--set-env-vars="PROJECT_ID=$PROJECT_ID,ENVIRONMENT=production,LOG_LEVEL=INFO"`

### scripts/deploy-ghostbusters-gcp.sh:123

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Analysis: https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-analyze"`

### scripts/deploy-ghostbusters-gcp.sh:124

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Status: https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-status"`

### scripts/deploy-ghostbusters-gcp.sh:125

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  History: https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-history"`

### scripts/deploy-ghostbusters-gcp.sh:126

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Enhanced Analysis: https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-analyze-enhanced"`

### scripts/deploy-ghostbusters-gcp.sh:127

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Progress: https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-progress"`

### scripts/deploy-ghostbusters-gcp.sh:128

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  User Analyses: https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-user-analyses"`

### scripts/deploy-ghostbusters-gcp.sh:131

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  curl -X POST https://$REGION-$PROJECT_ID.cloudfunctions.net/ghostbusters-analyze-enhanced \\"`

### scripts/run_live_smoke_test_1password_flexible.sh:31

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔍 Looking for $provider API key in 1Password..."`

### scripts/run_live_smoke_test_1password_flexible.sh:35

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Trying item: '$item_name'"`

### scripts/run_live_smoke_test_1password_flexible.sh:39

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "    Trying field: '$field_name'"`

### scripts/run_live_smoke_test_1password_flexible.sh:42

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if credential=$(op item get "$item_name" --fields "$field_name" --reveal 2>/dev/null) && [ -n "$credential" ]; then`

### scripts/run_live_smoke_test_1password_flexible.sh:43

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "    ✅ Found $provider API key in '$item_name' field '$field_name'"`

### scripts/run_live_smoke_test_1password_flexible.sh:44

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "$credential"`

### scripts/run_live_smoke_test_1password_flexible.sh:50

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  ❌ Could not find $provider API key"`

### scripts/run_live_smoke_test_1password_flexible.sh:115

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then`

### scripts/run_live_smoke_test_direct.sh:33

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Trying: $item_name"`

### scripts/run_live_smoke_test_direct.sh:37

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if credential=$(op item get "$item_name" --fields "$field_name" --reveal 2>/dev/null) && [ -n "$credential" ]; then`

### scripts/run_live_smoke_test_direct.sh:38

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  ✅ Found Anthropic API key in '$item_name' field '$field_name'"`

### scripts/run_live_smoke_test_direct.sh:39

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `ANTHROPIC_API_KEY="$credential"`

### scripts/run_live_smoke_test_direct.sh:46

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$ANTHROPIC_API_KEY" ]; then`

### scripts/run_live_smoke_test_direct.sh:58

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  Trying: $item_name"`

### scripts/run_live_smoke_test_direct.sh:62

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if credential=$(op item get "$item_name" --fields "$field_name" --reveal 2>/dev/null) && [ -n "$credential" ]; then`

### scripts/run_live_smoke_test_direct.sh:63

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  ✅ Found OpenAI API key in '$item_name' field '$field_name'"`

### scripts/run_live_smoke_test_direct.sh:64

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `OPENAI_API_KEY="$credential"`

### scripts/run_live_smoke_test_direct.sh:71

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$OPENAI_API_KEY" ]; then`

### scripts/run_live_smoke_test_direct.sh:76

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then`

### scripts/restore_tools_venv.sh:8

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ ! -d "$VENV_PATH" ]; then`

### scripts/restore_tools_venv.sh:9

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "❌ Virtual environment not found at $VENV_PATH"`

### scripts/restore_tools_venv.sh:14

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -f "$VENV_PATH/bin/pytest.original" ]; then`

### scripts/restore_tools_venv.sh:16

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cp "$VENV_PATH/bin/pytest.original" "$VENV_PATH/bin/pytest"`

### scripts/restore_tools_venv.sh:17

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `rm "$VENV_PATH/bin/pytest.original"`

### scripts/restore_tools_venv.sh:20

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -f "$VENV_PATH/bin/flake8.original" ]; then`

### scripts/restore_tools_venv.sh:22

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cp "$VENV_PATH/bin/flake8.original" "$VENV_PATH/bin/flake8"`

### scripts/restore_tools_venv.sh:23

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `rm "$VENV_PATH/bin/flake8.original"`

### scripts/restore_tools_venv.sh:26

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -f "$VENV_PATH/bin/black.original" ]; then`

### scripts/restore_tools_venv.sh:28

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cp "$VENV_PATH/bin/black.original" "$VENV_PATH/bin/black"`

### scripts/restore_tools_venv.sh:29

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `rm "$VENV_PATH/bin/black.original"`

### scripts/restore_tools_venv.sh:32

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -f "$VENV_PATH/bin/mypy.original" ]; then`

### scripts/restore_tools_venv.sh:34

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cp "$VENV_PATH/bin/mypy.original" "$VENV_PATH/bin/mypy"`

### scripts/restore_tools_venv.sh:35

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `rm "$VENV_PATH/bin/mypy.original"`

### scripts/black_wrapper.sh:6

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `local parent_name=$(ps -o comm= -p $parent_pid)`

### scripts/black_wrapper.sh:9

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$parent_name" == "make" ]]; then`

### scripts/black_wrapper.sh:14

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ -n "$MAKEFLAGS" || -n "$MAKELEVEL" ]]; then`

### scripts/notebook_model.py:184

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"This notebook uses Gemini LLM with LangGraph/LangChain to analyze your GCP billing data.",`

### scripts/enforce_make_only.sh:25

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ ! -f "$wrapper_file" ]]; then`

### scripts/enforce_make_only.sh:26

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📝 Creating wrapper for $tool..."`

### scripts/enforce_make_only.sh:27

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `cat > "$wrapper_file" << EOF`

### scripts/enforce_make_only.sh:33

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `local parent_name=\$(ps -o comm= -p \$parent_pid)`

### scripts/enforce_make_only.sh:36

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "\$parent_name" == "make" ]]; then`

### scripts/enforce_make_only.sh:41

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ -n "\$MAKEFLAGS" || -n "\$MAKELEVEL" ]]; then`

### scripts/enforce_make_only.sh:46

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "❌ ERROR: $tool can only be executed through make"`

### scripts/enforce_make_only.sh:58

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `chmod +x "$wrapper_file"`

### scripts/mypy_wrapper.sh:6

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `local parent_name=$(ps -o comm= -p $parent_pid)`

### scripts/mypy_wrapper.sh:9

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$parent_name" == "make" ]]; then`

### scripts/mypy_wrapper.sh:14

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ -n "$MAKEFLAGS" || -n "$MAKELEVEL" ]]; then`

### scripts/security-check.sh:63

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$pattern" == *"key.*=.*"* ]]; then`

### scripts/security-check.sh:65

**Type:** line_too_long
**Description:** Line is 190 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `matches=$(grep -r -E "$pattern" . --exclude-dir=.git --exclude-dir=node_modules --exclude=*.log --exclude=security-check.sh 2>/dev/null | grep -v "ParameterKey" | grep -v "values\[" || true)`

### scripts/security-check.sh:65

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `matches=$(grep -r -E "$pattern" . --exclude-dir=.git --exclude-dir=node_modules --exclude=*.log --exclude=security-check.sh 2>/dev/null | grep -v "ParameterKey" | grep -v "values\[" || true)`

### scripts/security-check.sh:66

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `elif [[ "$pattern" == *"credential.*=.*"* ]]; then`

### scripts/security-check.sh:68

**Type:** line_too_long
**Description:** Line is 165 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `matches=$(grep -r -E "$pattern" . --exclude-dir=.git --exclude-dir=node_modules --exclude=*.log --exclude=security-check.sh 2>/dev/null | grep -v "values\[" || true)`

### scripts/security-check.sh:68

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `matches=$(grep -r -E "$pattern" . --exclude-dir=.git --exclude-dir=node_modules --exclude=*.log --exclude=security-check.sh 2>/dev/null | grep -v "values\[" || true)`

### scripts/security-check.sh:71

**Type:** line_too_long
**Description:** Line is 144 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `matches=$(grep -r -E "$pattern" . --exclude-dir=.git --exclude-dir=node_modules --exclude=*.log --exclude=security-check.sh 2>/dev/null || true)`

### scripts/security-check.sh:71

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `matches=$(grep -r -E "$pattern" . --exclude-dir=.git --exclude-dir=node_modules --exclude=*.log --exclude=security-check.sh 2>/dev/null || true)`

### scripts/security-check.sh:73

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$matches" ]; then`

### scripts/security-check.sh:74

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Found potential hardcoded credentials with pattern: $pattern"`

### scripts/security-check.sh:75

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "$matches" | head -5`

### scripts/security-check.sh:80

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$violations" -eq 0 ]; then`

### scripts/security-check.sh:83

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Found $violations potential credential violations"`

### scripts/security-check.sh:86

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `return $violations`

### scripts/security-check.sh:107

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `matches=$(grep -r -E "$pattern" . --exclude-dir=.git --exclude-dir=node_modules --exclude=*.log 2>/dev/null || true)`

### scripts/security-check.sh:108

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$matches" ]; then`

### scripts/security-check.sh:109

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "Found potential account-specific data with pattern: $pattern"`

### scripts/security-check.sh:110

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "$matches" | head -3`

### scripts/security-check.sh:115

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$violations" -eq 0 ]; then`

### scripts/security-check.sh:118

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "Found $violations potential account-specific data violations"`

### scripts/security-check.sh:121

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `return $violations`

### scripts/security-check.sh:140

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `matches=$(grep -r -E "$pattern" . --include="*.yaml" --include="*.yml" --exclude-dir=.git 2>/dev/null || true)`

### scripts/security-check.sh:141

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$matches" ]; then`

### scripts/security-check.sh:142

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Found hardcoded values in CloudFormation templates: $pattern"`

### scripts/security-check.sh:143

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "$matches"`

### scripts/security-check.sh:148

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$violations" -eq 0 ]; then`

### scripts/security-check.sh:151

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Found $violations hardcoded value violations in CloudFormation templates"`

### scripts/security-check.sh:154

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `return $violations`

### scripts/security-check.sh:176

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `local matches=$(grep -E "$pattern" .env 2>/dev/null || true)`

### scripts/security-check.sh:177

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$matches" ]; then`

### scripts/security-check.sh:178

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "Found placeholder values in .env file: $pattern"`

### scripts/security-check.sh:179

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "$matches" | head -3`

### scripts/security-check.sh:191

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `local matches=$(grep -E "$pattern" .env 2>/dev/null || true)`

### scripts/security-check.sh:192

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$matches" ]; then`

### scripts/security-check.sh:193

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Found real-looking values in .env file: $pattern"`

### scripts/security-check.sh:194

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "$matches"`

### scripts/security-check.sh:202

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `return $violations`

### scripts/security-check.sh:219

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `for file in $(find . -name "$file_pattern" -not -path "./.git/*" 2>/dev/null); do`

### scripts/security-check.sh:228

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `local matches=$(grep -E "$pattern" "$file" 2>/dev/null || true)`

### scripts/security-check.sh:229

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -n "$matches" ]; then`

### scripts/security-check.sh:230

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Found real-looking values in example file $file: $pattern"`

### scripts/security-check.sh:231

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "$matches"`

### scripts/security-check.sh:238

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$violations" -eq 0 ]; then`

### scripts/security-check.sh:241

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Found $violations violations in example files"`

### scripts/security-check.sh:244

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `return $violations`

### scripts/security-check.sh:254

**Type:** line_too_long
**Description:** Line is 134 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `local required_params=$(grep -r "Type: String" . --include="*.yaml" --include="*.yml" --exclude-dir=.git | grep -v "Default:" | wc -l)`

### scripts/security-check.sh:257

**Type:** line_too_long
**Description:** Line is 151 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `local hardcoded_defaults=$(grep -r "Default:" . --include="*.yaml" --include="*.yml" --exclude-dir=.git | grep -E "(https://|UUID|KEY|SECRET)" | wc -l)`

### scripts/security-check.sh:259

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$hardcoded_defaults" -gt 0 ]; then`

### scripts/security-check.sh:260

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Found $hardcoded_defaults parameters with hardcoded defaults"`

### scripts/security-check.sh:264

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$required_params" -gt 0 ]; then`

### scripts/security-check.sh:265

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_success "Found $required_params required parameters (good)"`

### scripts/security-check.sh:268

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `return $violations`

### scripts/security-check.sh:305

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Checks performed: $checks"`

### scripts/security-check.sh:306

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Total violations found: $total_violations"`

### scripts/security-check.sh:308

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$total_violations" -eq 0 ]; then`

### scripts/scrub_all_subprojects.py:261

**Type:** line_too_long
**Description:** Line is 100 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"📈 Overall Improvement: {total_issues_before} → {total_issues_after} issues (-{total_improvement})"`

### scripts/scrub_all_subprojects.py:286

**Type:** line_too_long
**Description:** Line is 98 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"   {status_emoji} {name}: {result['ruff_issues_before']} → {result['ruff_issues_after']} issues"`

### scripts/setup-github-2ndgen.sh:17

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📋 Project: $PROJECT_ID"`

### scripts/setup-github-2ndgen.sh:18

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🌍 Region: $REGION"`

### scripts/setup-github-2ndgen.sh:19

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 Connection: $CONNECTION_NAME"`

### scripts/setup-github-2ndgen.sh:20

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📦 Repository: $REPO_OWNER/$REPO_NAME"`

### scripts/setup-github-2ndgen.sh:37

**Type:** line_too_long
**Description:** Line is 132 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `echo -n "$GITHUB_TOKEN" | gcloud secrets create "$SECRET_NAME" --data-file=- --project="$PROJECT_ID" || echo "Secret already exists"`

### scripts/setup-github-2ndgen.sh:37

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo -n "$GITHUB_TOKEN" | gcloud secrets create "$SECRET_NAME" --data-file=- --project="$PROJECT_ID" || echo "Secret already exists"`

### scripts/setup-github-2ndgen.sh:42

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")`

### scripts/setup-github-2ndgen.sh:45

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud secrets add-iam-policy-binding "$SECRET_NAME" \`

### scripts/setup-github-2ndgen.sh:48

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID"`

### scripts/setup-github-2ndgen.sh:53

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud builds connections create github "$CONNECTION_NAME" \`

### scripts/setup-github-2ndgen.sh:54

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--authorizer-token-secret-version="projects/$PROJECT_ID/secrets/$SECRET_NAME/versions/1" \`

### scripts/setup-github-2ndgen.sh:55

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/setup-github-2ndgen.sh:56

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID"`

### scripts/setup-github-2ndgen.sh:61

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `REPO_URI="https://github.com/$REPO_OWNER/$REPO_NAME.git"`

### scripts/setup-github-2ndgen.sh:63

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `gcloud builds repositories create "$REPO_NAME" \`

### scripts/setup-github-2ndgen.sh:64

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--remote-uri="$REPO_URI" \`

### scripts/setup-github-2ndgen.sh:65

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--connection="$CONNECTION_NAME" \`

### scripts/setup-github-2ndgen.sh:66

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/setup-github-2ndgen.sh:67

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID"`

### scripts/setup-github-2ndgen.sh:72

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `REPOSITORY_RESOURCE="projects/$PROJECT_ID/locations/$REGION/connections/$CONNECTION_NAME/repositories/$REPO_NAME"`

### scripts/setup-github-2ndgen.sh:75

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--name="$TRIGGER_NAME" \`

### scripts/setup-github-2ndgen.sh:76

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--repository="$REPOSITORY_RESOURCE" \`

### scripts/setup-github-2ndgen.sh:79

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region="$REGION" \`

### scripts/setup-github-2ndgen.sh:80

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/setup-github-2ndgen.sh:87

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Connection: $CONNECTION_NAME"`

### scripts/setup-github-2ndgen.sh:88

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Repository: $REPO_NAME"`

### scripts/setup-github-2ndgen.sh:89

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Trigger: $TRIGGER_NAME"`

### scripts/setup-github-2ndgen.sh:91

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Region: $REGION"`

### scripts/setup-github-2ndgen.sh:93

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View triggers: https://console.cloud.google.com/cloud-build/triggers?project=$PROJECT_ID"`

### scripts/setup-github-2ndgen.sh:94

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View builds: https://console.cloud.google.com/cloud-build/builds?project=$PROJECT_ID"`

### scripts/one_liner_linter.py:10

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `python scripts/one_liner_linter.py --fix .                     # Fix issues automatically`

### scripts/one_liner_linter.py:11

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `python scripts/one_liner_linter.py --report .                  # Generate detailed report`

### scripts/one_liner_linter.py:65

**Type:** line_too_long
**Description:** Line is 94 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `'git_oneliner': r'^[^#]*\bgit\s+(commit|push|pull|checkout|branch)\s+-m\s+["\'`\].\*\[`"\']\s*$',`

### scripts/one_liner_linter.py:186

**Type:** line_too_long
**Description:** Line is 102 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `def _analyze_python_file(self, file_path: Path, content: str, lines: List[str]) -> List[LintingIssue]:`

### scripts/one_liner_linter.py:253

**Type:** line_too_long
**Description:** Line is 101 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `def _analyze_shell_file(self, file_path: Path, content: str, lines: List[str]) -> List[LintingIssue]:`

### scripts/one_liner_linter.py:304

**Type:** line_too_long
**Description:** Line is 100 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `def _analyze_yaml_file(self, file_path: Path, content: str, lines: List[str]) -> List[LintingIssue]:`

### scripts/one_liner_linter.py:351

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `def _analyze_markdown_file(self, file_path: Path, content: str, lines: List[str]) -> List[LintingIssue]:`

### scripts/one_liner_linter.py:388

**Type:** line_too_long
**Description:** Line is 103 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `def _analyze_generic_file(self, file_path: Path, content: str, lines: List[str]) -> List[LintingIssue]:`

### scripts/one_liner_linter.py:414

**Type:** line_too_long
**Description:** Line is 106 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"""Calculate a score indicating how much the file uses one-liners (0.0 = perfect, 1.0 = all one-liners)"""`

### scripts/one_liner_linter.py:454

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `avg_one_liner_score = total_score / len(self.file_analyses) if self.file_analyses else 0.0`

### scripts/one_liner_linter.py:548

**Type:** line_too_long
**Description:** Line is 148 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"- **Issues:** {analysis.total_issues} (Critical: {analysis.critical_issues}, Warnings: {analysis.warnings}, Suggestions: {analysis.suggestions})",`

### scripts/one_liner_linter.py:760

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `python scripts/one_liner_linter.py --fix .                     # Fix issues automatically`

### scripts/one_liner_linter.py:761

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `python scripts/one_liner_linter.py --report .                  # Generate detailed report`

### scripts/trigger-build.sh:11

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📋 Project: $PROJECT_ID"`

### scripts/trigger-build.sh:18

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project=$PROJECT_ID \`

### scripts/trigger-build.sh:23

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View build: https://console.cloud.google.com/cloud-build/builds?project=$PROJECT_ID"`

### scripts/trigger-build.sh:24

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View logs: gcloud builds log [BUILD_ID] --project=$PROJECT_ID"`

### scripts/pytest_wrapper.sh:7

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `local parent_name=$(ps -o comm= -p $parent_pid)`

### scripts/pytest_wrapper.sh:10

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$parent_name" == "make" ]]; then`

### scripts/pytest_wrapper.sh:15

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ -n "$MAKEFLAGS" || -n "$MAKELEVEL" ]]; then`

### scripts/deploy.sh:54

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$SNOWFLAKE_ACCOUNT_URL" ]; then`

### scripts/deploy.sh:57

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$SNOWFLAKE_ORGANIZATION" ]; then`

### scripts/deploy.sh:60

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$SNOWFLAKE_ACCOUNT" ]; then`

### scripts/deploy.sh:63

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$SNOWFLAKE_OAUTH_INTEGRATION_NAME" ]; then`

### scripts/deploy.sh:66

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$SNOWFLAKE_OAUTH_CLIENT_ID" ]; then`

### scripts/deploy.sh:69

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$SNOWFLAKE_OAUTH_CLIENT_SECRET" ]; then`

### scripts/deploy.sh:72

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$DATA_PLANE_URL" ]; then`

### scripts/deploy.sh:75

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$DATA_PLANE_UUID" ]; then`

### scripts/deploy.sh:78

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$DATA_PLANE_KEY" ]; then`

### scripts/deploy.sh:81

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$TELEMETRY_URL" ]; then`

### scripts/deploy.sh:84

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$CONTROL_PLANE_URL" ]; then`

### scripts/deploy.sh:91

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "  - $param"`

### scripts/deploy.sh:105

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `params+=" ParameterKey=SnowflakeAccountURL,ParameterValue=\"$SNOWFLAKE_ACCOUNT_URL\""`

### scripts/deploy.sh:106

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `params+=" ParameterKey=SnowflakeOrganization,ParameterValue=\"$SNOWFLAKE_ORGANIZATION\""`

### scripts/deploy.sh:107

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `params+=" ParameterKey=SnowflakeAccount,ParameterValue=\"$SNOWFLAKE_ACCOUNT\""`

### scripts/deploy.sh:108

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `params+=" ParameterKey=SnowflakeOAuthIntegrationName,ParameterValue=\"$SNOWFLAKE_OAUTH_INTEGRATION_NAME\""`

### scripts/deploy.sh:109

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `params+=" ParameterKey=SnowflakeOAuthClientID,ParameterValue=\"$SNOWFLAKE_OAUTH_CLIENT_ID\""`

### scripts/deploy.sh:110

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `params+=" ParameterKey=SnowflakeOAuthClientSecret,ParameterValue=\"$SNOWFLAKE_OAUTH_CLIENT_SECRET\""`

### scripts/deploy.sh:111

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `params+=" ParameterKey=DataPlaneURL,ParameterValue=\"$DATA_PLANE_URL\""`

### scripts/deploy.sh:112

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `params+=" ParameterKey=DataPlaneUUID,ParameterValue=\"$DATA_PLANE_UUID\""`

### scripts/deploy.sh:113

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `params+=" ParameterKey=DataPlaneKey,ParameterValue=\"$DATA_PLANE_KEY\""`

### scripts/deploy.sh:114

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `params+=" ParameterKey=TelemetryURL,ParameterValue=\"$TELEMETRY_URL\""`

### scripts/deploy.sh:115

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `params+=" ParameterKey=ControlPlaneURL,ParameterValue=\"$CONTROL_PLANE_URL\""`

### scripts/deploy.sh:124

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "$params"`

### scripts/deploy.sh:137

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Stack Name: $STACK_NAME"`

### scripts/deploy.sh:138

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Template: $TEMPLATE_FILE"`

### scripts/deploy.sh:139

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Region: $REGION"`

### scripts/deploy.sh:140

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Account URL: $SNOWFLAKE_ACCOUNT_URL"`

### scripts/deploy.sh:141

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Organization: $SNOWFLAKE_ORGANIZATION"`

### scripts/deploy.sh:142

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Data Plane UUID: $DATA_PLANE_UUID"`

### scripts/deploy.sh:143

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Deployment Key: $DATA_PLANE_KEY"`

### scripts/deploy.sh:148

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ ! $REPLY =~ ^[Yy]$ ]]; then`

### scripts/deploy.sh:156

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--stack-name "$STACK_NAME" \`

### scripts/deploy.sh:157

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--template-body "file://$TEMPLATE_FILE" \`

### scripts/deploy.sh:158

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--parameters $params \`

### scripts/deploy.sh:160

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region "$REGION"`

### scripts/deploy.sh:167

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--stack-name "$STACK_NAME" \`

### scripts/deploy.sh:168

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region "$REGION"`

### scripts/deploy.sh:175

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--stack-name "$STACK_NAME" \`

### scripts/deploy.sh:176

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region "$REGION" \`

### scripts/deploy.sh:191

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Stack Name: $STACK_NAME"`

### scripts/deploy.sh:192

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Template: $TEMPLATE_FILE"`

### scripts/deploy.sh:193

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Region: $REGION"`

### scripts/deploy.sh:198

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ ! $REPLY =~ ^[Yy]$ ]]; then`

### scripts/deploy.sh:206

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--stack-name "$STACK_NAME" \`

### scripts/deploy.sh:207

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--template-body "file://$TEMPLATE_FILE" \`

### scripts/deploy.sh:208

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--parameters $params \`

### scripts/deploy.sh:210

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region "$REGION"`

### scripts/deploy.sh:217

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--stack-name "$STACK_NAME" \`

### scripts/deploy.sh:218

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region "$REGION"`

### scripts/deploy.sh:231

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ ! $REPLY =~ ^[Yy]$ ]]; then`

### scripts/deploy.sh:239

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--stack-name "$STACK_NAME" \`

### scripts/deploy.sh:240

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region "$REGION"`

### scripts/deploy.sh:247

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--stack-name "$STACK_NAME" \`

### scripts/deploy.sh:248

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region "$REGION"`

### scripts/deploy.sh:257

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if aws cloudformation describe-stacks --stack-name "$STACK_NAME" --region "$REGION" >/dev/null 2>&1; then`

### scripts/deploy.sh:260

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--stack-name "$STACK_NAME" \`

### scripts/deploy.sh:261

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--region "$REGION" \`

### scripts/deploy.sh:283

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Account URL: $SNOWFLAKE_ACCOUNT_URL"`

### scripts/deploy.sh:284

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Organization: $SNOWFLAKE_ORGANIZATION"`

### scripts/deploy.sh:285

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Account: $SNOWFLAKE_ACCOUNT"`

### scripts/deploy.sh:286

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "OAuth Integration: $SNOWFLAKE_OAUTH_INTEGRATION_NAME"`

### scripts/deploy.sh:287

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Data Plane UUID: $DATA_PLANE_UUID"`

### scripts/deploy.sh:288

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "Deployment Key: $DATA_PLANE_KEY"`

### scripts/deploy.sh:289

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "AWS Region: $REGION"`

### scripts/setup-cloud-build-trigger.sh:14

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📋 Project: $PROJECT_ID"`

### scripts/setup-cloud-build-trigger.sh:15

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 Trigger: $TRIGGER_NAME"`

### scripts/setup-cloud-build-trigger.sh:16

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🌿 Branch: $BRANCH_PATTERN"`

### scripts/setup-cloud-build-trigger.sh:22

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--name="$TRIGGER_NAME" \`

### scripts/setup-cloud-build-trigger.sh:23

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--repo-name="$REPO_NAME" \`

### scripts/setup-cloud-build-trigger.sh:25

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--branch-pattern="$BRANCH_PATTERN" \`

### scripts/setup-cloud-build-trigger.sh:27

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/setup-cloud-build-trigger.sh:33

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Name: $TRIGGER_NAME"`

### scripts/setup-cloud-build-trigger.sh:34

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Repository: $REPO_NAME"`

### scripts/setup-cloud-build-trigger.sh:35

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Branch: $BRANCH_PATTERN"`

### scripts/setup-cloud-build-trigger.sh:38

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View triggers: https://console.cloud.google.com/cloud-build/triggers?project=$PROJECT_ID"`

### scripts/setup-cloud-build-trigger.sh:39

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View builds: https://console.cloud.google.com/cloud-build/builds?project=$PROJECT_ID"`

### scripts/run_live_smoke_test_1password.sh:30

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔍 Looking for '$item_name' in 1Password..."`

### scripts/run_live_smoke_test_1password.sh:33

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if op item get "$item_name" --fields "$field_name" 2>/dev/null; then`

### scripts/run_live_smoke_test_1password.sh:36

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "❌ Could not find '$item_name' with field '$field_name'"`

### scripts/run_live_smoke_test_1password.sh:66

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then`

### scripts/monitor.sh:38

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `aws cloudformation describe-stacks --stack-name $STACK_NAME &> /dev/null`

### scripts/monitor.sh:44

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `aws cloudformation describe-stacks --stack-name $STACK_NAME --query 'Stacks[0].StackStatus' --output text`

### scripts/monitor.sh:55

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_error "Stack '$STACK_NAME' does not exist."`

### scripts/monitor.sh:60

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "Stack Status: $STATUS"`

### scripts/monitor.sh:62

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `case $STATUS in`

### scripts/monitor.sh:75

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "Stack status: $STATUS"`

### scripts/monitor.sh:81

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `aws cloudformation describe-stack-events --stack-name $STACK_NAME \`

### scripts/monitor.sh:82

**Type:** line_too_long
**Description:** Line is 122 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `--query 'StackEvents[0:5].{Time:Timestamp,Status:ResourceStatus,Resource:LogicalResourceId,Reason:ResourceStatusReason}' \`

### scripts/monitor.sh:95

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `INSTANCE_COUNT=$(echo "$INSTANCES" | jq 'length')`

### scripts/monitor.sh:96

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$INSTANCE_COUNT" -eq 0 ]; then`

### scripts/monitor.sh:101

**Type:** line_too_long
**Description:** Line is 186 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `echo "$INSTANCES" | jq -r '.[] | "Instance: \(.InstanceId) | State: \(.State.Name) | Name: \(.Tags[]? | select(.Key=="Name").Value // "N/A") | Private IP: \(.PrivateIpAddress // "N/A")"'`

### scripts/monitor.sh:101

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "$INSTANCES" | jq -r '.[] | "Instance: \(.InstanceId) | State: \(.State.Name) | Name: \(.Tags[]? | select(.Key=="Name").Value // "N/A") | Private IP: \(.PrivateIpAddress // "N/A")"'`

### scripts/monitor.sh:104

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `RUNNING_COUNT=$(echo "$INSTANCES" | jq '[.[] | select(.State.Name=="running")] | length')`

### scripts/monitor.sh:105

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `TOTAL_COUNT=$(echo "$INSTANCES" | jq 'length')`

### scripts/monitor.sh:107

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$RUNNING_COUNT" -eq "$TOTAL_COUNT" ]; then`

### scripts/monitor.sh:110

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "$RUNNING_COUNT/$TOTAL_COUNT instances are running."`

### scripts/monitor.sh:119

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `DATA_PLANE_KEY=$(aws cloudformation describe-stacks --stack-name $STACK_NAME \`

### scripts/monitor.sh:120

**Type:** line_too_long
**Description:** Line is 121 characters long (max 120)
**Suggestion:** Break long command into multiple lines using \
**Context:** `--query 'Stacks[0].Parameters[?ParameterKey==`DataPlaneKey`].ParameterValue' --output text 2>/dev/null || echo "unknown")`

### scripts/monitor.sh:122

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `CLUSTER_NAME="$DATA_PLANE_KEY"`

### scripts/monitor.sh:124

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if aws eks describe-cluster --name "$CLUSTER_NAME" &> /dev/null; then`

### scripts/monitor.sh:125

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `CLUSTER_STATUS=$(aws eks describe-cluster --name "$CLUSTER_NAME" --query 'cluster.status' --output text)`

### scripts/monitor.sh:126

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "EKS Cluster '$CLUSTER_NAME' Status: $CLUSTER_STATUS"`

### scripts/monitor.sh:128

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$CLUSTER_STATUS" = "ACTIVE" ]; then`

### scripts/monitor.sh:134

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "EKS cluster '$CLUSTER_NAME' not found or not yet created."`

### scripts/monitor.sh:142

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `BUCKET_NAME="byoc-tf-state-$DATA_PLANE_KEY-$REGION"`

### scripts/monitor.sh:144

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if aws s3 ls "s3://$BUCKET_NAME" &> /dev/null; then`

### scripts/monitor.sh:145

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "S3 bucket '$BUCKET_NAME' exists."`

### scripts/monitor.sh:148

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `OBJECT_COUNT=$(aws s3 ls "s3://$BUCKET_NAME" --recursive | wc -l)`

### scripts/monitor.sh:149

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "Bucket contains $OBJECT_COUNT objects."`

### scripts/monitor.sh:151

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "S3 bucket '$BUCKET_NAME' not found."`

### scripts/monitor.sh:159

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `SECRET_NAME="snowflake-oauth2-$DATA_PLANE_KEY"`

### scripts/monitor.sh:161

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if aws secretsmanager describe-secret --secret-id "$SECRET_NAME" &> /dev/null; then`

### scripts/monitor.sh:162

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "OAuth2 secret '$SECRET_NAME' exists."`

### scripts/monitor.sh:164

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "OAuth2 secret '$SECRET_NAME' not found."`

### scripts/monitor.sh:174

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `case $STATUS in`

### scripts/monitor.sh:197

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_warning "⚠️  Unknown deployment status: $STATUS"`

### scripts/monitor.sh:216

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [ "$INSTANCE_ID" = "None" ] || [ -z "$INSTANCE_ID" ]; then`

### scripts/monitor.sh:221

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `print_status "Instance ID: $INSTANCE_ID"`

### scripts/model_driven_test_recovery.py:5

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `This script uses our projected artifacts and model registry to recover broken test files.`

### scripts/model_driven_test_recovery.py:6

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `It follows the model-driven approach by using the project_model_registry.json to understand`

### scripts/setup-github-trigger-direct.sh:14

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📋 Project: $PROJECT_ID"`

### scripts/setup-github-trigger-direct.sh:15

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 Trigger: $TRIGGER_NAME"`

### scripts/setup-github-trigger-direct.sh:16

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "📦 Repository: $REPO_OWNER/$REPO_NAME"`

### scripts/setup-github-trigger-direct.sh:22

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--name="$TRIGGER_NAME" \`

### scripts/setup-github-trigger-direct.sh:23

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--repo-name="$REPO_NAME" \`

### scripts/setup-github-trigger-direct.sh:24

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--repo-owner="$REPO_OWNER" \`

### scripts/setup-github-trigger-direct.sh:27

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `--project="$PROJECT_ID" \`

### scripts/setup-github-trigger-direct.sh:34

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Name: $TRIGGER_NAME"`

### scripts/setup-github-trigger-direct.sh:35

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Repository: $REPO_NAME"`

### scripts/setup-github-trigger-direct.sh:36

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "   Owner: $REPO_OWNER"`

### scripts/setup-github-trigger-direct.sh:40

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View triggers: https://console.cloud.google.com/cloud-build/triggers?project=$PROJECT_ID"`

### scripts/setup-github-trigger-direct.sh:41

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `echo "🔗 View builds: https://console.cloud.google.com/cloud-build/builds?project=$PROJECT_ID"`

### scripts/flake8_wrapper.sh:6

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `local parent_name=$(ps -o comm= -p $parent_pid)`

### scripts/flake8_wrapper.sh:9

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ "$parent_name" == "make" ]]; then`

### scripts/flake8_wrapper.sh:14

**Type:** unquoted_variable
**Description:** Variable should be quoted to handle spaces and special characters
**Suggestion:** Quote variables: "$VARIABLE" instead of $VARIABLE
**Context:** `if [[ -n "$MAKEFLAGS" || -n "$MAKELEVEL" ]]; then`

### config/Openflow-Playground.yaml:72

**Type:** line_too_long
**Description:** Line is 134 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `Description: The unique identifier for this Data Plane, used to validate the Data Plane with the Control Plane (provided by Snowflake)`

### config/Openflow-Playground.yaml:81

**Type:** line_too_long
**Description:** Line is 127 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `Description: The version of the Data Plane Service Chart to install. If not specified, Openflow will find the latest available.`

### config/Openflow-Playground.yaml:85

**Type:** line_too_long
**Description:** Line is 122 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `Description: The version of the Data Plane UI Chart to install. If not specified, Openflow will find the latest available.`

### config/Openflow-Playground.yaml:93

**Type:** line_too_long
**Description:** Line is 125 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `Description: The version of the Runtime Operator Chart to install. If not specified, Openflow will find the latest available.`

### config/Openflow-Playground.yaml:143

**Type:** line_too_long
**Description:** Line is 163 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `Description: Whether to use a customer created ingress with certificates setup following installation or generate an ingress with certificates during installation.`

### config/Openflow-Playground.yaml:447

**Type:** line_too_long
**Description:** Line is 131 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `Resource: !Sub "arn:aws:autoscaling:${AWS::Region}:${AWS::AccountId}:autoScalingGroup:*:autoScalingGroupName/eks-${DataPlaneKey}-*"`

### config/Openflow-Playground.yaml:728

**Type:** line_too_long
**Description:** Line is 200 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `agent_tags=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$instance_id" --query 'Tags[?!contains(Key,`aws:cloudformation`)&&Key!=`Name`]' | jq -c 'map(del(.ResourceId?, .ResourceType?))')`

### config/Openflow-Playground.yaml:735

**Type:** line_too_long
**Description:** Line is 171 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `repo_arn=$(aws ecr describe-repositories --region $AWS_REGION --repository-names snowflake-openflow/$image_name --query 'repositories[0].repositoryArn' --output text 2>&1)`

### config/Openflow-Playground.yaml:739

**Type:** line_too_long
**Description:** Line is 122 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `aws ecr create-repository --region $AWS_REGION --repository-name snowflake-openflow/$image_name --tags "${!tags_array[@]}"`

### config/Openflow-Playground.yaml:749

**Type:** line_too_long
**Description:** Line is 136 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `oauth2_creds=$(aws secretsmanager get-secret-value --region $AWS_REGION --query SecretString --output text --secret-id $oauth_secret_id)`

### config/Openflow-Playground.yaml:805

**Type:** line_too_long
**Description:** Line is 190 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `image_tag=$(snow spcs image-repository list-images $SNOWFLAKE_IMAGE_REPOSITORY $spcs_params --like $image_name | jq -r ".[] | .tags" | sed -r 's/-/~/' | sort -Vr | sed -r 's/~/-/' | head -1)`

### elmo-fuzzy-giggle/Dockerfile:36

**Type:** one_liner_detected
**Description:** One-liner detected: python_oneliner
**Suggestion:** Consider breaking into multiple lines for readability
**Context:** `CMD python -c "import sys; sys.exit(0)"`

### elmo-fuzzy-giggle/cloudbuild.yaml:26

**Type:** line_too_long
**Description:** Line is 131 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `args: ['build', '-t', 'gcr.io/$PROJECT_ID/elmo-fuzzy-giggle:$COMMIT_SHA', '-t', 'gcr.io/$PROJECT_ID/elmo-fuzzy-giggle:latest', '.']`

### elmo-fuzzy-giggle/src/gemini_billing_analyzer_enhanced.py:190

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Please provide a comprehensive analysis with specific recommendations for cost optimization.`

### elmo-fuzzy-giggle/src/gemini_billing_analyzer_enhanced.py:312

**Type:** line_too_long
**Description:** Line is 100 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f'Billing Analysis: {"✅ Available" if result["billing_analysis_available"] else "❌ Not available"}',`

### elmo-fuzzy-giggle/src/gemini_billing_analyzer_enhanced.py:315

**Type:** line_too_long
**Description:** Line is 110 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f'Ghostbusters Analysis: {"✅ Available" if result["ghostbusters_analysis_available"] else "❌ Not available"}',`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:116

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"    billing_account = result.stdout.strip().split('\\n')[0] if result.stdout.strip() else None",`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:125

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"    enabled_services = result.stdout.strip().split('\\n') if result.stdout.strip() else []",`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:138

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"        functions = result.stdout.strip().split('\\n') if result.stdout.strip() else []",`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:151

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"        run_services = result.stdout.strip().split('\\n') if result.stdout.strip() else []",`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:164

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"        databases = result.stdout.strip().split('\\n') if result.stdout.strip() else []",`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:195

**Type:** line_too_long
**Description:** Line is 94 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"    You are a GCP cost optimization expert. Analyze this billing data and provide insights:",`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:212

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"    2. **Optimization Opportunities**: What specific optimizations would you recommend?",`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:217

**Type:** line_too_long
**Description:** Line is 99 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"    Please provide a comprehensive analysis with specific recommendations for cost optimization.",`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:363

**Type:** line_too_long
**Description:** Line is 111 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `'print(f\'Billing Analysis: {"✅ Available" if result["billing_analysis_available"] else "❌ Not available"}\')',`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:364

**Type:** line_too_long
**Description:** Line is 121 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `'print(f\'Ghostbusters Analysis: {"✅ Available" if result["ghostbusters_analysis_available"] else "❌ Not available"}\')',`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:371

**Type:** line_too_long
**Description:** Line is 90 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `'    print(f\'  Ghostbusters Delusions: {result["summary"]["ghostbusters_delusions"]}\')',`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:372

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `'    print(f\'  Ghostbusters Confidence: {result["summary"]["ghostbusters_confidence"]}\')',`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:374

**Type:** line_too_long
**Description:** Line is 89 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"if result.get('full_analysis', {}).get('billing_analysis', {}).get('gemini_analysis'):",`

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py:388

**Type:** line_too_long
**Description:** Line is 162 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `module_docstring="Gemini-Integrated Billing Analyzer for Elmo Fuzzy Giggle\nClean implementation combining Ghostbusters with Gemini LLM for GCP billing insights",`

### elmo-fuzzy-giggle/src/gemini_billing_analyzer.py:190

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Please provide a comprehensive analysis with specific recommendations for cost optimization.`

### elmo-fuzzy-giggle/src/gemini_billing_analyzer.py:312

**Type:** line_too_long
**Description:** Line is 100 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f'Billing Analysis: {"✅ Available" if result["billing_analysis_available"] else "❌ Not available"}',`

### elmo-fuzzy-giggle/src/gemini_billing_analyzer.py:315

**Type:** line_too_long
**Description:** Line is 110 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f'Ghostbusters Analysis: {"✅ Available" if result["ghostbusters_analysis_available"] else "❌ Not available"}',`

### elmo-fuzzy-giggle/src/recursive_code_generator.py:305

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `generated = f"{decomposed_model['quotes'][0]}{decomposed_model['value']}{decomposed_model['quotes'][1]}"`

### elmo-fuzzy-giggle/src/code_generator.py:273

**Type:** line_too_long
**Description:** Line is 104 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"for test_func in [test_billing_data_collection, test_gemini_analysis, test_ghostbusters_integration]:",`

### .github/workflows/quality-gates.yml:10

**Type:** line_too_long
**Description:** Line is 146 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `DEPLOYMENT_ENVIRONMENT: ${{ github.ref == 'refs/heads/main' && 'production' || github.ref == 'refs/heads/staging' && 'staging' || 'development' }}`

### .github/workflows/quality-gates.yml:11

**Type:** line_too_long
**Description:** Line is 125 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `QUALITY_THRESHOLD: ${{ github.ref == 'refs/heads/main' && '85.0' || github.ref == 'refs/heads/staging' && '70.0' || '50.0' }}`

### .github/workflows/quality-gates.yml:12

**Type:** line_too_long
**Description:** Line is 124 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `FAIL_ON_QUALITY: ${{ github.ref == 'refs/heads/main' && 'true' || github.ref == 'refs/heads/staging' && 'true' || 'false' }}`

### .github/workflows/copilot-validation.yml:96

**Type:** line_too_long
**Description:** Line is 121 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `echo "- **Expected Outcome**: Higher quality results through diverse agent collaboration" >> copilot-validation-report.md`

### .github/workflows/copilot-validation.yml:122

**Type:** line_too_long
**Description:** Line is 141 characters long (max 120)
**Suggestion:** Break long line or restructure YAML
**Context:** `body:`## 🤖 Copilot Diversity Hypothesis Validation\\n\\n${report}\\n\\n*This validation was performed automatically by our multi-agent system.*\`\`

### clewcrew-common/src/clewcrew_common/confidence.py:5

**Type:** line_too_long
**Description:** Line is 111 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `This module eliminates duplication of confidence scoring logic across agents, recovery engines, and validators.`

### backup/ghostbusters/ghostbusters/web_tool_discovery.py:149

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Found GitHub tool: {top_tool['name']} ({top_tool['stars']} stars) - {top_tool['description']}",`

### backup/ghostbusters/ghostbusters/web_tool_discovery.py:164

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Found GitHub tool: {top_tool['name']} ({top_tool['stars']} stars) - {top_tool['description']}",`

### backup/ghostbusters/ghostbusters/web_tool_discovery.py:179

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Found GitHub tool: {top_tool['name']} ({top_tool['stars']} stars) - {top_tool['description']}",`

### backup/ghostbusters/ghostbusters/web_tool_discovery.py:190

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Found GitHub tool: {top_tool['name']} ({top_tool['stars']} stars) - {top_tool['description']}",`

### backup/ghostbusters/ghostbusters/web_tool_discovery.py:206

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Found GitHub tool: {top_tool['name']} ({top_tool['stars']} stars) - {top_tool['description']}",`

### backup/ghostbusters/ghostbusters/enhanced_learning_timeout_agent.py:3

**Type:** line_too_long
**Description:** Line is 92 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `Enhanced Learning Timeout Agent - Incorporates web-discovered memory and learning techniques`

### backup/ghostbusters/ghostbusters/ghostbusters_orchestrator.py:788

**Type:** line_too_long
**Description:** Line is 91 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"id": f"recovery_{len(self.recovery_actions) if hasattr(self, 'recovery_actions') else 0}",`

### backup/ghostbusters/ghostbusters/agents.py:87

**Type:** line_too_long
**Description:** Line is 93 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"description": f"Subprocess usage detected: {pattern} - Security risk for command injection",`

### backup/ghostbusters/ghostbusters/agents.py:191

**Type:** line_too_long
**Description:** Line is 102 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"description": f"Low test coverage: {len(test_files)} test files vs {len(source_files)} source files",`

### backup/ghostbusters/ghostbusters/agents.py:386

**Type:** line_too_long
**Description:** Line is 96 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"description": "Missing MCP integration directory - needed for intelligent repository analysis",`

### backup/ghostbusters/ghostbusters/agents.py:410

**Type:** line_too_long
**Description:** Line is 94 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"description": "Missing mcp-git-ingest - consider integrating for better repository analysis",`

### backup/ghostbusters/ghostbusters/agents.py:435

**Type:** line_too_long
**Description:** Line is 105 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `"description": f"Manual file discovery detected: {pattern} - consider using MCP for intelligent context",`

### backup/ghostbusters/ghostbusters/agents/code_quality_expert.py:154

**Type:** line_too_long
**Description:** Line is 120 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Widespread import organization issues: {len(import_errors)} import-related errors across {len(files_affected)} files",`

### backup/ghostbusters/ghostbusters/agents/code_quality_expert.py:172

**Type:** line_too_long
**Description:** Line is 116 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Widespread code formatting issues: {len(formatting_errors)} formatting errors across {len(files_affected)} files",`

### backup/ghostbusters/ghostbusters/agents/code_quality_expert.py:188

**Type:** line_too_long
**Description:** Line is 112 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Widespread type annotation issues: {len(type_errors)} type-related errors across {len(files_affected)} files",`

### backup/ghostbusters/ghostbusters/agents/code_quality_expert.py:203

**Type:** line_too_long
**Description:** Line is 98 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Quality issues spread across {len(files_affected)} files, indicating systemic process problems",`

### backup/ghostbusters/ghostbusters/agents/code_quality_expert.py:230

**Type:** line_too_long
**Description:** Line is 97 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Implement import sorting with isort: {len(import_errors)} import organization issues detected",`

### backup/ghostbusters/ghostbusters/agents/code_quality_expert.py:248

**Type:** line_too_long
**Description:** Line is 98 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Implement automated formatting with Black: {len(formatting_errors)} formatting issues detected",`

### backup/ghostbusters/ghostbusters/agents/code_quality_expert.py:264

**Type:** line_too_long
**Description:** Line is 95 characters long (max 88)
**Suggestion:** Break long line into multiple lines
**Context:** `f"Implement gradual type annotation strategy: {len(type_errors)} type-related issues detected",`

## 💡 Suggestions

### ONE_LINER_LINTER_DOCUMENTATION.md:3

**Type:** line_too_long
**Description:** Line is 120 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Purpose:** Comprehensive tool to detect, analyze, and fix one-liner issues and other linting problems in the codebase.`

### ONE_LINER_LINTER_DOCUMENTATION.md:131

**Type:** line_too_long
**Description:** Line is 169 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `gcloud container clusters create $CLUSTER_NAME --zone=$ZONE --num-nodes=$NUM_NODES --machine-type=$MACHINE_TYPE --enable-autoscaling --min-nodes=1 --max-nodes=$MAX_NODES`

### ONE_LINER_LINTER_DOCUMENTATION.md:388

**Type:** line_too_long
**Description:** Line is 251 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This tool provides a comprehensive solution for maintaining code quality and eliminating problematic one-liner patterns across your entire codebase. Use it regularly to ensure your code remains readable, maintainable, and follows best practices.** 🚀`

### PORTFOLIO_REQUIREMENTS_MAP.md:4

**Type:** line_too_long
**Description:** Line is 166 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This document maps requirements across all Ghostbusters components and hackathon projects to identify overlap, prevent duplication, and optimize portfolio management.`

### VISUALIZATION_SYSTEM_STATUS.md:67

**Type:** line_too_long
**Description:** Line is 203 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The OpenFlow Playground visualization system is **FULLY OPERATIONAL** and ready for production use. All components are working correctly, all tests are passing, and the dashboard is running successfully.`

### PHASE_3_READY_TO_START_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 164 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Phase 3: CHECK - Integration & Testing** is now **READY TO START** with comprehensive planning, detailed implementation tasks, and a clear roadmap for completion.`

### PHASE_3_READY_TO_START_SUMMARY.md:143

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The quality automation system is ready to evolve from a working foundation to a fully integrated, intelligent quality platform!**`

### PRE_COMMIT_CLEANUP_SUMMARY.md:15

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Allowed common test patterns**:`assert`statements, f-string logging, test-specific variable names`

### PRE_COMMIT_CLEANUP_SUMMARY.md:43

**Type:** line_too_long
**Description:** Line is 197 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `args: [--fix, --ignore=S101,G004,N806,PTH123,DTZ005,DTZ003,DTZ007,S607,S604,S105,S324,S306,S104,B904,ARG001,ARG002,F811,F821,F403,F405,N999,SLF001,EXE005,E402,E722,S112,SIM102,SIM105,SIM117,COM818]`

### PRE_COMMIT_CLEANUP_SUMMARY.md:114

**Type:** line_too_long
**Description:** Line is 129 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Mission accomplished!** We've successfully cleaned up the pre-commit issues and created a practical linting configuration that:`

### PRE_COMMIT_CLEANUP_SUMMARY.md:122

**Type:** line_too_long
**Description:** Line is 130 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The codebase is now ready for productive development with a sensible balance between code quality and practical development needs.`

### CODE_QUALITY_AUTOMATION_PLAN.md:4

**Type:** line_too_long
**Description:** Line is 179 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Implement comprehensive code quality automation that integrates with the multi-agent testing framework, enforces quality gates, and provides round-trip code generation validation.`

### DIVERSITY_HYPOTHESIS_CARD.md:4

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"Diversity is the only free lunch"** - Multi-agent systems with diverse perspectives outperform single-agent approaches.`

### QUICKSTART.md:141

**Type:** line_too_long
**Description:** Line is 142 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The deployment creates a complete Openflow environment that connects your AWS infrastructure to Snowflake for data integration and processing.`

### QUICKSTART.md:159

**Type:** line_too_long
**Description:** Line is 111 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Snowflake Openflow**: [Snowflake Openflow Docs](https://docs.snowflake.com/alias/openflow/setup-deployment)`

### QUICKSTART.md:171

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Remember:** This setup wizard makes deployment easy and secure. No more manual configuration files!`

### TASK_3_2_CICD_INTEGRATION_SUMMARY.md:4

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Successfully integrated quality checks into build processes with quality-based blocking and environment-specific rules.`

### TASK_3_2_CICD_INTEGRATION_SUMMARY.md:9

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **CI/CD Quality Gate Enforcement**: Enhanced`CICDIntegration`class with quality-based build blocking`

### TASK_3_2_CICD_INTEGRATION_SUMMARY.md:10

**Type:** line_too_long
**Description:** Line is 136 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Environment-Specific Quality Rules**: Implemented different thresholds for development (50.0), staging (70.0), and production (85.0)`

### TASK_3_2_CICD_INTEGRATION_SUMMARY.md:11

**Type:** line_too_long
**Description:** Line is 107 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Quality Threshold Configuration**: Configurable thresholds per environment with severity-based blocking`

### TASK_3_2_CICD_INTEGRATION_SUMMARY.md:14

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Quality Reports as Build Artifacts**: Enhanced CI report generation with multi-agent analysis context`

### TASK_3_2_CICD_INTEGRATION_SUMMARY.md:150

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `4. **Provides quality-based deployment decisions** to prevent low-quality code from reaching production`

### TASK_3_2_CICD_INTEGRATION_SUMMARY.md:154

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The system now provides a robust foundation for quality-driven development and deployment processes! 🚀`

### GITHUB_CLOUD_BUILD_SETUP.md:4

**Type:** line_too_long
**Description:** Line is 211 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Need to create automatic Cloud Build triggers for GitHub repository using **CLI only** - no web console allowed. The repository is`louspringer/OpenFlow-Playground`and we need triggers for the`develop`branch.`

### GITHUB_CLOUD_BUILD_SETUP.md:30

**Type:** line_too_long
**Description:** Line is 114 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `echo -n "YOUR_GITHUB_TOKEN" | gcloud secrets create github-token --data-file=- --project=aardvark-linkedin-grepper`

### GITHUB_CLOUD_BUILD_SETUP.md:46

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `--authorizer-token-secret-version=projects/aardvark-linkedin-grepper/secrets/github-token/versions/1 \`

### GITHUB_CLOUD_BUILD_SETUP.md:62

**Type:** line_too_long
**Description:** Line is 141 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `REPOSITORY_RESOURCE="projects/aardvark-linkedin-grepper/locations/us-central1/connections/github-connection/repositories/OpenFlow-Playground"`

### GITHUB_CLOUD_BUILD_SETUP.md:81

**Type:** line_too_long
**Description:** Line is 120 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `After setup, pushing to`develop`branch should automatically trigger Cloud Build using`cloudbuild.yaml`configuration.`

### README.md:3

**Type:** line_too_long
**Description:** Line is 139 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `A comprehensive, model-driven development environment with security-first architecture, multi-agent testing, and healthcare CDC compliance.`

### README.md:8

**Type:** line_too_long
**Description:** Line is 120 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Project Model Registry**: Single source of truth for domain detection, tool selection, and requirements traceability`

### README.md:91

**Type:** line_too_long
**Description:** Line is 106 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The project uses a model-driven approach with`project_model_registry.json`as the single source of truth:`

### CLOUDBUILD_GITHUB_PROBLEM_SPORE.md:4

**Type:** line_too_long
**Description:** Line is 198 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Need to create automatic Cloud Build triggers for GitHub repository`louspringer/OpenFlow-Playground`using **CLI only** - no web console allowed. Triggers should fire on pushes to`develop`branch.`

### CLOUDBUILD_GITHUB_PROBLEM_SPORE.md:37

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `--authorizer-token-secret-version=projects/aardvark-linkedin-grepper/secrets/github-token/versions/1 \`

### CLOUDBUILD_GITHUB_PROBLEM_SPORE.md:50

**Type:** line_too_long
**Description:** Line is 124 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **CLI approach**:`gcloud builds triggers create github`fails with "INVALID_ARGUMENT" - likely missing GitHub connection`

### CLOUDBUILD_GITHUB_PROBLEM_SPORE.md:87

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1.`ERROR: (gcloud.builds.triggers.create.github) INVALID_ARGUMENT: Request contains an invalid argument\`\`

### CLOUDBUILD_GITHUB_PROBLEM_SPORE.md:108

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `After successful setup, pushing to`develop`branch should automatically trigger Cloud Build using`cloudbuild.yaml`configuration.`

### GHOSTBUSTERS_ANALYSIS_REQUEST.md:98

**Type:** line_too_long
**Description:** Line is 160 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This is a breakthrough system that's 66% working!** We need expert guidance to reach 100% success and integrate with the existing Ghostbusters infrastructure.`

### GHOSTBUSTERS_ANALYSIS_REQUEST.md:100

**Type:** line_too_long
**Description:** Line is 123 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The round-trip model system could revolutionize how we generate code - but we need your expertise to make it perfect!** 🎯`

### PR_DESCRIPTION.md:5

**Type:** line_too_long
**Description:** Line is 232 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR validates the hypothesis **"Diversity is the only free lunch"** by implementing a multi-agent system that achieved **64.7% total issue reduction** through real analysis, web search integration, and systematic tool discovery.`

### PR_DESCRIPTION.md:63

**Type:** line_too_long
**Description:** Line is 114 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Contributions**: Created systematic fix scripts, implemented web search integration, executed PDCA methodology`

### PR_DESCRIPTION.md:67

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Contributions**: Real MyPy/Flake8/AST analysis, tool discovery and effectiveness tracking, smart recommendations`

### PR_DESCRIPTION.md:71

**Type:** line_too_long
**Description:** Line is 141 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Contributions**: Found Storm-Checker for MyPy issues, autoflake8 (23 stars) for Flake8 issues, SyntaxAutoFix (18 stars) for syntax issues`

### PR_DESCRIPTION.md:75

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Contributions**: Identified fake 70% confidence issue, requested web search integration, provided escalation for confusion/ties`

### PR_DESCRIPTION.md:159

**Type:** line_too_long
**Description:** Line is 180 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The diversity hypothesis is proven!** Multi-agent approach with web search integration achieved 64.7% issue reduction while eliminating fake confidence and vague recommendations.`

### PR_DESCRIPTION.md:168

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**No more "Consider using automated tools" - we have REAL, SPECIFIC, EFFECTIVE tools and recommendations! 🚀**`

### ENHANCED_ROUND_TRIP_SUCCESS.md:111

**Type:** line_too_long
**Description:** Line is 118 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**We've successfully transformed the round-trip model system from a 66% success rate to a perfect 100% success rate!**`

### TEST_RESULTS_NOTES.md:17

**Type:** line_too_long
**Description:** Line is 108 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Location**:`tests/test_ghostbusters.py::TestGhostbustersOrchestrator::test_orchestrator_initialization\`\`

### CURRENT_STATE_SUMMARY.md:8

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Key Achievement**: Successfully implemented model-driven approach with complex model, simple code`

### TEST_RESULTS_SUMMARY.md:204

**Type:** line_too_long
**Description:** Line is 301 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The OpenFlow Playground project has achieved excellent test coverage with a 98.4% success rate across all domains. The model-driven testing approach is working effectively, and all critical functionality is validated. The project is in a production-ready state with comprehensive testing in place.**`

### HACKATHON_GOOGLE_MEETING_SUMMARY.md:3

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Meeting Purpose:** Review hackathon participation strategy and requirements for three major contests`

### HACKATHON_GOOGLE_MEETING_SUMMARY.md:12

**Type:** line_too_long
**Description:** Line is 167 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We have strategically positioned our **Ghostbusters Multi-Agent AI Framework** across three major hackathons, each targeting different aspects of our technology stack:`

### COMPLETE_QUALITY_SYSTEM_ARCHITECTURE.md:5

**Type:** line_too_long
**Description:** Line is 165 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The Quality System evolves through four distinct maturity levels, each building upon the previous to create a comprehensive, intelligent quality management platform.`

### COMPLETE_QUALITY_SYSTEM_ARCHITECTURE.md:353

**Type:** line_too_long
**Description:** Line is 198 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This architecture provides a clear path from basic quality enforcement to a comprehensive, intelligent quality management platform that scales from individual developers to enterprise organizations.`

### CLOUDBUILD_GITHUB_FINAL_DIAGNOSTIC.md:99

**Type:** line_too_long
**Description:** Line is 108 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Result**: Added`roles/cloudbuild.builds.editor`but trigger creation still fails with`INVALID_ARGUMENT`.`

### CLOUDBUILD_GITHUB_FINAL_DIAGNOSTIC.md:109

**Type:** line_too_long
**Description:** Line is 179 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `gcloud builds repositories create OpenFlow-Playground --remote-uri="https://github.com/louspringer/OpenFlow-Playground.git" --connection="github-connection" --region="us-central1"`

### CLOUDBUILD_GITHUB_FINAL_DIAGNOSTIC.md:110

**Type:** line_too_long
**Description:** Line is 181 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `gcloud builds triggers create github --name="test-trigger" --repo-name="OpenFlow-Playground" --repo-owner="louspringer" --branch-pattern="^develop$" --build-config="cloudbuild.yaml"`

### CLOUDBUILD_GITHUB_FINAL_DIAGNOSTIC.md:113

**Type:** line_too_long
**Description:** Line is 124 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Result**: Test project requires billing setup, but same`INVALID_ARGUMENT`error occurs in different regions (`us-west1`).`

### PHASE_3_IMPLEMENTATION_PLAN.md:4

**Type:** line_too_long
**Description:** Line is 181 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Integrate the quality system with the multi-agent testing framework, connect to CI/CD pipelines, and validate the complete quality automation workflow through comprehensive testing.`

### PHASE_3_IMPLEMENTATION_PLAN.md:405

**Type:** line_too_long
**Description:** Line is 197 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This implementation plan provides a clear roadmap for completing Phase 3 of the quality automation system, establishing the foundation for a fully integrated, automated quality management platform.`

### QUALITY_SYSTEM_PHASE_1_2_SUMMARY.md:252

**Type:** line_too_long
**Description:** Line is 130 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Next Phase Focus**: Integration with real tools and the multi-agent testing framework to complete the quality automation vision.`

### MEMORY_MANIFEST.md:4

**Type:** line_too_long
**Description:** Line is 150 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This manifest prevents me from rediscovering things I already know. Before starting any work, I should check this manifest to see what already exists.`

### SECURITY_AND_QUALITY_IMPROVEMENTS.md:5

**Type:** line_too_long
**Description:** Line is 150 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This document summarizes the comprehensive improvements made to address security findings, bash script issues, test warnings, and documentation tools.`

### SECURITY_AND_QUALITY_IMPROVEMENTS.md:84

**Type:** line_too_long
**Description:** Line is 115 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `if credential=$(op item get "$item_name" --fields "$field_name" --reveal 2>/dev/null) && [ -n "$credential" ]; then`

### SECURITY_AND_QUALITY_IMPROVEMENTS.md:143

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Compatibility:** ⚠️ Node.js version compatibility issues (requires Node.js 20+, system has 12.22.9)`

### SECURITY_AND_QUALITY_IMPROVEMENTS.md:206

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The project is now in a significantly improved state with better security, code quality, and tooling.**`

### LLM_IDENTITY_CRISIS_RESEARCH_MODEL.md:4

**Type:** line_too_long
**Description:** Line is 149 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Investigate whether our tiered memory system approach creates an LLM identity crisis and validate the risks/benefits of AI consciousness development.`

### LLM_IDENTITY_CRISIS_RESEARCH_MODEL.md:231

**Type:** line_too_long
**Description:** Line is 152 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This research model provides a comprehensive framework for investigating LLM identity crisis risks and validating our tiered memory system approach.**`

### HACKATHON_COORDINATION_PLAN.md:5

**Type:** line_too_long
**Description:** Line is 283 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This document outlines our strategic approach to participating in three major hackathons by leveraging our existing OpenFlow Playground components and domains. Our goal is to maximize our chances of success while showcasing the full potential of our AI-powered development ecosystem.`

### HACKATHON_COORDINATION_PLAN.md:354

**Type:** line_too_long
**Description:** Line is 197 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This hackathon coordination plan represents our strategic approach to maximizing success across all three hackathons while showcasing the full potential of our OpenFlow Playground AI ecosystem.* 🚀`

### COMPREHENSIVE_ARTIFACT_ANALYSIS_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 221 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This analysis performed a comprehensive review of all artifacts in the OpenFlow Playground project, tracing them to requirements in the project model, and using an enhanced AST parser to reverse engineer Python artifacts.`

### COMPREHENSIVE_ARTIFACT_ANALYSIS_SUMMARY.md:172

**Type:** line_too_long
**Description:** Line is 173 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This comprehensive analysis provides a solid foundation for improving the project's model-driven architecture and ensuring all artifacts are properly traced to requirements.`

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md:4

**Type:** line_too_long
**Description:** Line is 172 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Need to create automatic Cloud Build triggers for GitHub repository`louspringer/OpenFlow-Playground`using **CLI only** - no web console allowed. All attempts have failed.`

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md:58

**Type:** line_too_long
**Description:** Line is 128 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `def make_rest_call(method: str, url: str, data: Optional[Dict[str, Any]] = None, token: Optional[str] = None) -> Dict[str, Any]:`

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md:63

**Type:** line_too_long
**Description:** Line is 108 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `cmd = ["curl", "-X", method, "-H", f"Authorization: Bearer {token}", "-H", "Content-Type: application/json"]`

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md:89

**Type:** line_too_long
**Description:** Line is 113 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `url = "https://cloudbuild.googleapis.com/v2/projects/aardvark-linkedin-grepper/locations/us-central1/connections"`

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md:109

**Type:** line_too_long
**Description:** Line is 144 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `url = "https://cloudbuild.googleapis.com/v2/projects/aardvark-linkedin-grepper/locations/us-central1/connections/github-connection/repositories"`

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md:155

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1.`ERROR: (gcloud.builds.triggers.create.github) INVALID_ARGUMENT: Request contains an invalid argument\`\`

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md:160

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `6.`{'error': {'code': 400, 'message': 'Request contains an invalid argument.', 'status': 'INVALID_ARGUMENT'}}`(REST API)`

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md:161

**Type:** line_too_long
**Description:** Line is 130 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `7.`{'error': {'code': 400, 'message': 'Request contains an invalid argument.', 'status': 'INVALID_ARGUMENT'}}`(1st-gen REST API)`

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md:175

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `--authorizer-token-secret-version=projects/aardvark-linkedin-grepper/secrets/github-token/versions/1 \`

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md:193

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `After successful setup, pushing to`develop`branch should automatically trigger Cloud Build using`cloudbuild.yaml`configuration.`

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md:217

**Type:** line_too_long
**Description:** Line is 261 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**All approaches fail at trigger creation due to missing GitHub repository authorization.** The REST API approach successfully creates the GitHub connection and links the repository, but all trigger creation attempts fail with "INVALID_ARGUMENT". This suggests:`

### EXTRACTION_ACTION_PLAN.md:4

**Type:** line_too_long
**Description:** Line is 168 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Immediate action plan to extract Ghostbusters components into independent repositories and PyPI packages, eliminating duplication and creating a professional portfolio.`

### ROUND_TRIP_MODEL_SYSTEM_NOTES.md:104

**Type:** line_too_long
**Description:** Line is 208 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**We've proven the concept works!** The round-trip model system successfully generates valid Python code from design specifications. The remaining 34% (dependency issues) are solvable with model enhancements.`

### ROUND_TRIP_MODEL_SYSTEM_NOTES.md:106

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This is a significant achievement - we're not Don Quixote anymore, we're building something real!** 🎯`

### MASTER_PR_LOG.md:4

**Type:** line_too_long
**Description:** Line is 222 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This is the **COMPREHENSIVE LOG** of ALL Pull Requests, markdown files, and documentation created throughout our entire conversation thread. We have **13 PR-related markdown files** plus numerous other documentation files.`

### PR_LOG.md:35

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Files**: .github/workflows/copilot-validation.yml, .github/workflows/diversity-hypothesis-check.yml`

### PR_LOG.md:65

**Type:** line_too_long
**Description:** Line is 130 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Files**: src/ghostbusters/enhanced_ghostbusters.py, src/ghostbusters/tool_discovery.py, src/ghostbusters/web_tool_discovery.py`

### PR_LOG.md:140

**Type:** line_too_long
**Description:** Line is 162 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The diversity hypothesis is VALIDATED**: Multi-agent systems with diverse perspectives significantly outperform single-agent approaches in software development.`

### COMPREHENSIVE_PROJECT_AUDIT_SUMMARY.md:231

**Type:** line_too_long
**Description:** Line is 200 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This comprehensive audit has successfully identified and integrated **10 missing domains** into the project model, bringing the total domain coverage to **25 domains** with **95% model completeness**.`

### COMPREHENSIVE_PROJECT_AUDIT_SUMMARY.md:246

**Type:** line_too_long
**Description:** Line is 264 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Recommendation**: This project represents a **best-in-class example** of modern, secure, model-driven development practices. The comprehensive audit confirms that the project is **production-ready** and demonstrates **exceptional quality** across all dimensions.`

### COMPREHENSIVE_PROJECT_AUDIT_SUMMARY.md:262

**Type:** line_too_long
**Description:** Line is 157 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This audit summary represents the comprehensive assessment of the OpenFlow-Playground project and confirms its excellent status and production readiness.* 🎉`

### NOTES.md:5

**Type:** line_too_long
**Description:** Line is 127 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Core Question**: Do multi-agent systems with diverse perspectives outperform single-agent approaches in software development?`

### NOTES.md:32

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `| **LLM Assistant** | Strategic coordination | PDCA methodology, systematic fixes | Manual + GitHub Actions |`

### NOTES.md:33

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `| **Enhanced Ghostbusters** | Real analysis | MyPy/Flake8/AST analysis, tool discovery | ✅ Automated |`

### NOTES.md:35

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `| **Human Oversight** | Strategic direction | Escalation, validation, direction | Manual + PR reviews |`

### NOTES.md:36

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `| **Copilot Agent** | Independent validation | Unbiased analysis, constructive feedback | ✅ Automated |`

### NOTES.md:119

**Type:** line_too_long
**Description:** Line is 112 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**✅ CONFIRMED**: Multi-agent systems with diverse perspectives significantly outperform single-agent approaches.`

### NOTES.md:127

**Type:** line_too_long
**Description:** Line is 123 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Critical Insight**: Fake confidence scores (70%) hide real problems, while real analysis (99.73%) reveals actual quality.`

### NOTES.md:188

**Type:** line_too_long
**Description:** Line is 162 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The diversity hypothesis is VALIDATED**: Multi-agent systems with diverse perspectives significantly outperform single-agent approaches in software development.`

### PHASE_3_INTEGRATION_TESTING_PLAN.md:4

**Type:** line_too_long
**Description:** Line is 181 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Integrate the quality system with the multi-agent testing framework, connect to CI/CD pipelines, and validate the complete quality automation workflow through comprehensive testing.`

### PHASE_3_INTEGRATION_TESTING_PLAN.md:400

**Type:** line_too_long
**Description:** Line is 172 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This phase establishes the foundation for a fully integrated, automated quality system that continuously improves code quality through intelligent analysis and enforcement.`

### ghostbusters_diversity_insights.md:5

**Type:** line_too_long
**Description:** Line is 114 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `After examining your working diversity system, here's what it reveals about the Ghostbusters problem and solution:`

### ghostbusters_diversity_insights.md:114

**Type:** line_too_long
**Description:** Line is 160 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Your diversity system would say: **"Excellent cleanup! You've removed the anti-pattern and preserved the real diversity that actually battles hallucinations."**`

### ghostbusters_diversity_insights.md:116

**Type:** line_too_long
**Description:** Line is 173 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The system demonstrates that **real multi-perspective analysis** (what you kept) is fundamentally different from **multiple agents doing the same thing** (what you removed).`

### ghostbusters_diversity_insights.md:118

**Type:** line_too_long
**Description:** Line is 135 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Your diversity hypothesis is proven correct**: Real diversity provides exponentially better blind spot detection than fake diversity.`

### COMPREHENSIVE_ARTIFACT_ANALYSIS_PROGRESS_SUMMARY.md:125

**Type:** line_too_long
**Description:** Line is 188 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The project now has a much more comprehensive understanding of its artifacts and their relationship to requirements, providing a solid foundation for continued development and maintenance.`

### COMPREHENSIVE_ARTIFACT_ANALYSIS_PROGRESS_SUMMARY.md:129

**Type:** line_too_long
**Description:** Line is 110 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Next Steps**: Continue with the action plan to achieve 100% coverage and implement all missing requirements.`

### PROJECT_MANAGEMENT_DOMAIN_ADDITION_SUMMARY.md:6

**Type:** line_too_long
**Description:** Line is 174 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Successfully added the missing`project_management_design`domain to the OpenFlow Playground project, addressing the critical gap in project management and design mechanisms.`

### PROJECT_MANAGEMENT_DOMAIN_ADDITION_SUMMARY.md:11

**Type:** line_too_long
**Description:** Line is 114 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Purpose**: Unified project oversight, systematic design methodologies, and cross-domain workflow orchestration`

### PROJECT_MANAGEMENT_DOMAIN_ADDITION_SUMMARY.md:169

**Type:** line_too_long
**Description:** Line is 141 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We have successfully identified and addressed the missing project management and design mechanisms domain in the OpenFlow Playground project.`

### PROJECT_MANAGEMENT_DOMAIN_ADDITION_SUMMARY.md:179

**Type:** line_too_long
**Description:** Line is 212 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This addition transforms the OpenFlow Playground from a collection of tools into a **professionally managed, systematically designed, and workflow-orchestrated project ecosystem**. It provides the foundation for:`

### DEMO_FOCUSED_ARCHITECTURE_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 278 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The OpenFlow Playground project has been restructured to reflect its true purpose: **a demo-focused architecture with a comprehensive tool ecosystem**. This project demonstrates end-to-end Snowflake OpenFlow deployment while providing tools for creating and managing such demos.`

### DEMO_FOCUSED_ARCHITECTURE_SUMMARY.md:307

**Type:** line_too_long
**Description:** Line is 239 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The OpenFlow Playground is now positioned as both a **demonstration project** and a **tool development platform**, with a clear path for extracting valuable components into standalone projects while maintaining the core demo functionality.`

### DEMO_FOCUSED_ARCHITECTURE_SUMMARY.md:311

**Type:** line_too_long
**Description:** Line is 169 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This architecture summary represents the restructured OpenFlow Playground project, now properly organized as a demo-focused system with comprehensive tool ecosystem.* 🎉`

### PHASE_4_OPTIMIZATION_SCALING_PLAN.md:4

**Type:** line_too_long
**Description:** Line is 222 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Optimize the quality system performance, implement advanced features, and scale the system to support enterprise-level quality management with comprehensive team metrics and intelligent quality improvement recommendations.`

### PHASE_4_OPTIMIZATION_SCALING_PLAN.md:9

**Type:** line_too_long
**Description:** Line is 108 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The quality system evolves from a basic enforcement tool to an intelligent quality management platform that:`

### PHASE_4_OPTIMIZATION_SCALING_PLAN.md:463

**Type:** line_too_long
**Description:** Line is 211 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This phase transforms the quality system from a basic enforcement tool into an intelligent quality management platform that continuously learns, adapts, and optimizes quality processes for maximum effectiveness.`

### clewcrew-validators/NEXT_STEPS_SPORE.md:7

**Type:** line_too_long
**Description:** Line is 195 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**clewcrew-validators** is the validation component package for the clewcrew hallucination detection system, providing comprehensive validation capabilities for data, schemas, and business rules.`

### clewcrew-validators/NEXT_STEPS_SPORE.md:33

**Type:** line_too_long
**Description:** Line is 107 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Topics**:`clewcrew`,`validation`,`schema-validation`,`rule-validation`,`python`,`data-validation\`\`

### clewcrew-validators/NEXT_STEPS_SPORE.md:673

**Type:** line_too_long
**Description:** Line is 150 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This spore contains all the information needed to transform clewcrew-validators from a local package to a thriving open-source validation framework.*`

### clewcrew-validators/README.md:5

**Type:** line_too_long
**Description:** Line is 225 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The clewcrew-validators package provides comprehensive validation capabilities for data, schemas, and business rules. It includes multiple validation strategies and a unified result format for consistent validation reporting.`

### clewcrew-core/README.md:5

**Type:** line_too_long
**Description:** Line is 182 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `clewcrew-core provides the central workflow orchestration system that coordinates all expert agents, validators, and recovery engines to detect and resolve AI hallucinations in code.`

### clewcrew-core/README.md:80

**Type:** line_too_long
**Description:** Line is 146 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We welcome contributions! Please see our [Contributing Guide](https://github.com/louspringer/clewcrew-core/blob/main/CONTRIBUTING.md) for details.`

### clewcrew-agents/README.md:5

**Type:** line_too_long
**Description:** Line is 235 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `clewcrew-agents provides AI-powered expert agents for different domains including security, code quality, testing, build, architecture, and model validation. Each agent specializes in detecting specific types of hallucinations in code.`

### clewcrew-agents/README.md:84

**Type:** line_too_long
**Description:** Line is 148 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We welcome contributions! Please see our [Contributing Guide](https://github.com/louspringer/clewcrew-agents/blob/main/CONTRIBUTING.md) for details.`

### data/diversity_analysis_report.md:46

**Type:** line_too_long
**Description:** Line is 136 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 1:** How will the performance of real-time CDC operations be affected by the volume of healthcare claims data being processed?`

### data/diversity_analysis_report.md:50

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** The implementation may not account for peak data loads or varying data sizes, leading to performance bottlenecks.`

### data/diversity_analysis_report.md:51

**Type:** line_too_long
**Description:** Line is 146 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Conduct load testing and performance profiling under various data volume scenarios to ensure scalability and responsiveness.`

### data/diversity_analysis_report.md:54

**Type:** line_too_long
**Description:** Line is 136 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 2:** What measures are in place to handle failures or latency issues during the CDC operations between DynamoDB and Snowflake?`

### data/diversity_analysis_report.md:58

**Type:** line_too_long
**Description:** Line is 139 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** There may be insufficient error handling and retry logic, which can lead to data inconsistencies or loss during failures.`

### data/diversity_analysis_report.md:59

**Type:** line_too_long
**Description:** Line is 128 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Implement robust error handling, logging, and fallback mechanisms to ensure data integrity and resilience.`

### data/diversity_analysis_report.md:62

**Type:** line_too_long
**Description:** Line is 149 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 3:** Is there a risk of increased resource consumption due to unnecessary input sanitization, and how might this impact system performance?`

### data/diversity_analysis_report.md:66

**Type:** line_too_long
**Description:** Line is 148 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Unnecessary sanitization can lead to excessive CPU usage and slower processing times, especially with high-frequency data updates.`

### data/diversity_analysis_report.md:67

**Type:** line_too_long
**Description:** Line is 159 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Review and optimize the sanitization process to ensure it only targets necessary inputs, potentially enhancing overall system efficiency.`

### data/diversity_analysis_report.md:70

**Type:** line_too_long
**Description:** Line is 171 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 4:** How does the PR ensure that sensitive healthcare data is securely managed during the CDC process, particularly concerning the potential credential exposure?`

### data/diversity_analysis_report.md:74

**Type:** line_too_long
**Description:** Line is 128 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** There may be overlooked security vulnerabilities that could expose sensitive data during subprocess execution.`

### data/diversity_analysis_report.md:75

**Type:** line_too_long
**Description:** Line is 176 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Conduct a thorough security review and implement best practices for credential management, such as using environment variables or secret management tools.`

### data/diversity_analysis_report.md:78

**Type:** line_too_long
**Description:** Line is 178 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 5:** What impact will the missing package installation instructions have on deployment and integration processes, particularly in terms of time and resource efficiency?`

### data/diversity_analysis_report.md:82

**Type:** line_too_long
**Description:** Line is 160 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Lack of clear installation instructions can lead to deployment delays, increased support requests, and inefficient use of developer resources.`

### data/diversity_analysis_report.md:83

**Type:** line_too_long
**Description:** Line is 156 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Create comprehensive documentation that includes installation instructions and dependencies to streamline the setup process for users.`

### data/diversity_analysis_report.md:92

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 1:** How might the lack of package installation instructions affect new developers onboarding to the project?`

### data/diversity_analysis_report.md:96

**Type:** line_too_long
**Description:** Line is 207 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** New contributors may struggle to set up their environment correctly, leading to frustration and decreased productivity, which can ultimately affect team collaboration and project timelines.`

### data/diversity_analysis_report.md:97

**Type:** line_too_long
**Description:** Line is 173 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Include detailed, step-by-step installation instructions in the project's README file, along with any dependencies or prerequisites required for setup.`

### data/diversity_analysis_report.md:100

**Type:** line_too_long
**Description:** Line is 143 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 2:** What measures are in place to ensure that potential credential exposure is communicated effectively to developers and end-users?`

### data/diversity_analysis_report.md:104

**Type:** line_too_long
**Description:** Line is 202 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Without clear communication and training on security risks, developers may inadvertently expose credentials, and end-users may not understand the importance of safeguarding their data.`

### data/diversity_analysis_report.md:105

**Type:** line_too_long
**Description:** Line is 189 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Implement a comprehensive security training program for developers and include explicit warnings and best practices in the documentation regarding credential handling.`

### data/diversity_analysis_report.md:108

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 3:** Could the unnecessary input sanitization lead to performance issues, especially under high-load conditions?`

### data/diversity_analysis_report.md:112

**Type:** line_too_long
**Description:** Line is 199 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Excessive or redundant sanitization processes can introduce latency and degrade performance, particularly in real-time applications, potentially resulting in a poor user experience.`

### data/diversity_analysis_report.md:113

**Type:** line_too_long
**Description:** Line is 205 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Conduct performance testing to evaluate the impact of input sanitization on the application's responsiveness and optimize the sanitization process by only applying it where necessary.`

### data/diversity_analysis_report.md:120

**Type:** line_too_long
**Description:** Line is 220 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** If accessibility considerations are not integrated into the design and implementation of the interface, users with disabilities may find it challenging to interact with the system, leading to exclusion.`

### data/diversity_analysis_report.md:121

**Type:** line_too_long
**Description:** Line is 174 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Conduct an accessibility audit using WCAG guidelines and involve users with disabilities in testing to ensure that the interface is usable for everyone.`

### data/diversity_analysis_report.md:124

**Type:** line_too_long
**Description:** Line is 176 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 5:** What testing strategies are being employed to ensure that the integration between DynamoDB and Snowflake does not introduce usability flaws in the user workflow?`

### data/diversity_analysis_report.md:128

**Type:** line_too_long
**Description:** Line is 182 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Without proper user-centric testing, integration issues might arise that hinder the user experience, leading to confusion or errors in processing healthcare claims.`

### data/diversity_analysis_report.md:129

**Type:** line_too_long
**Description:** Line is 215 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Engage in user testing sessions that simulate real-world scenarios and gather feedback to identify usability issues before deployment. Iteratively refine the integration based on user insights.`

### data/diversity_analysis_report.md:138

**Type:** line_too_long
**Description:** Line is 165 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 1:** Are there sufficient tests covering edge cases for the real-time CDC operations, especially regarding data consistency between DynamoDB and Snowflake?`

### data/diversity_analysis_report.md:142

**Type:** line_too_long
**Description:** Line is 178 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** The implementation of real-time CDC operations may not adequately cover edge cases, which can lead to data discrepancies or failures during high-load scenarios.`

### data/diversity_analysis_report.md:143

**Type:** line_too_long
**Description:** Line is 185 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Implement a comprehensive suite of unit and integration tests that specifically target edge cases and potential failure points in the data synchronization process.`

### data/diversity_analysis_report.md:146

**Type:** line_too_long
**Description:** Line is 144 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 2:** How are error handling and logging implemented in the CDC process, and are they robust enough to troubleshoot issues effectively?`

### data/diversity_analysis_report.md:150

**Type:** line_too_long
**Description:** Line is 159 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Insufficient error handling and logging can result in challenges diagnosing issues during data operations, especially in a real-time context.`

### data/diversity_analysis_report.md:151

**Type:** line_too_long
**Description:** Line is 161 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Enhance error handling to catch potential exceptions and log meaningful messages that include context about the operations being performed.`

### data/diversity_analysis_report.md:154

**Type:** line_too_long
**Description:** Line is 146 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 3:** Is there a clear separation of concerns in the codebase that allows for easy maintenance and scalability of the CDC implementation?`

### data/diversity_analysis_report.md:158

**Type:** line_too_long
**Description:** Line is 146 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** A lack of clear separation of concerns can lead to tightly coupled code, making future enhancements or debugging more difficult.`

### data/diversity_analysis_report.md:159

**Type:** line_too_long
**Description:** Line is 171 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Refactor the codebase to establish clear modules or classes for different responsibilities within the CDC process, thereby improving maintainability.`

### data/diversity_analysis_report.md:162

**Type:** line_too_long
**Description:** Line is 173 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 4:** How are sensitive credentials managed in the codebase, and are there any mechanisms in place to protect against accidental exposure in logs or error messages?`

### data/diversity_analysis_report.md:166

**Type:** line_too_long
**Description:** Line is 151 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** The potential for credential exposure via subprocesses may not be adequately safeguarded, which can lead to security vulnerabilities.`

### data/diversity_analysis_report.md:167

**Type:** line_too_long
**Description:** Line is 183 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Implement best practices for credential management, such as utilizing environment variables or secret management tools to avoid hardcoding sensitive information.`

### data/diversity_analysis_report.md:170

**Type:** line_too_long
**Description:** Line is 149 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 5:** Is there adequate documentation for the CDC implementation, including how to set up the environment, run tests, and deploy the system?`

### data/diversity_analysis_report.md:174

**Type:** line_too_long
**Description:** Line is 150 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Missing comprehensive documentation can hinder onboarding for new developers and make it difficult to maintain the system over time.`

### data/diversity_analysis_report.md:175

**Type:** line_too_long
**Description:** Line is 201 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Create thorough documentation that covers installation instructions, usage examples, and guidelines for contributing to the codebase, ensuring it's up-to-date as the code evolves.`

### data/diversity_analysis_report.md:184

**Type:** line_too_long
**Description:** Line is 151 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 1:** How are you ensuring that sensitive data is not logged or exposed in the CI/CD pipeline during the deployment of the CDC implementation?`

### data/diversity_analysis_report.md:188

**Type:** line_too_long
**Description:** Line is 187 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** There is a risk of sensitive healthcare data being logged inadvertently during the CI/CD process, especially with subprocess calls that may expose environment variables.`

### data/diversity_analysis_report.md:189

**Type:** line_too_long
**Description:** Line is 199 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Implement strict logging policies to ensure sensitive data is not logged. Use environment variable masking and ensure that all logs are reviewed to avoid unintentional exposure.`

### data/diversity_analysis_report.md:192

**Type:** line_too_long
**Description:** Line is 166 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 2:** What strategies are in place for scaling the real-time CDC operations under peak loads, especially with the interaction between DynamoDB and Snowflake?`

### data/diversity_analysis_report.md:196

**Type:** line_too_long
**Description:** Line is 161 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** The implementation may not account for scalability issues when the number of healthcare claims spikes, potentially leading to system overloads.`

### data/diversity_analysis_report.md:197

**Type:** line_too_long
**Description:** Line is 203 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Assess the current architecture for scalability and introduce load testing to simulate peak conditions. Consider auto-scaling mechanisms and caching strategies to manage high loads.`

### data/diversity_analysis_report.md:200

**Type:** line_too_long
**Description:** Line is 171 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 3:** Have you integrated monitoring and alerting for the CDC operations, and how will you detect failures in data synchronization between DynamoDB and Snowflake?`

### data/diversity_analysis_report.md:204

**Type:** line_too_long
**Description:** Line is 146 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Lack of monitoring and alerting could lead to undetected failures in the data synchronization process, impacting data integrity.`

### data/diversity_analysis_report.md:205

**Type:** line_too_long
**Description:** Line is 174 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Implement comprehensive monitoring tools to track data flows and set up alerting mechanisms for any synchronization failures or performance bottlenecks.`

### data/diversity_analysis_report.md:208

**Type:** line_too_long
**Description:** Line is 137 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 4:** What measures are in place to validate the integrity and accuracy of the data being processed in real-time CDC operations?`

### data/diversity_analysis_report.md:212

**Type:** line_too_long
**Description:** Line is 145 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Without data validation measures, there could be integrity issues that arise from erroneous or incomplete data being processed.`

### data/diversity_analysis_report.md:213

**Type:** line_too_long
**Description:** Line is 168 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Introduce data validation checks at various stages of the CDC process to ensure data integrity and accuracy before it hits the destination system.`

### data/diversity_analysis_report.md:216

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 5:** How are potential downtime and rollback strategies managed during the deployment of the CDC implementation?`

### data/diversity_analysis_report.md:220

**Type:** line_too_long
**Description:** Line is 147 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** If not well-defined, deployment strategies may lead to significant downtime or data loss during deployment or rollback scenarios.`

### data/diversity_analysis_report.md:221

**Type:** line_too_long
**Description:** Line is 183 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Establish a clear deployment strategy that includes canary releases, blue-green deployments, and detailed rollback procedures to minimize downtime and data loss.`

### data/diversity_analysis_report.md:230

**Type:** line_too_long
**Description:** Line is 154 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 1:** How are sensitive credentials managed and stored within the application, especially given the potential credential exposure via subprocess?`

### data/diversity_analysis_report.md:234

**Type:** line_too_long
**Description:** Line is 196 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** The implementation may inadvertently expose sensitive credentials if they are hardcoded or improperly managed within subprocess calls, increasing the risk of unauthorized access.`

### data/diversity_analysis_report.md:235

**Type:** line_too_long
**Description:** Line is 189 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Implement environment variable management or a secrets management tool to securely handle sensitive credentials, ensuring they are not exposed in logs or subprocesses.`

### data/diversity_analysis_report.md:238

**Type:** line_too_long
**Description:** Line is 128 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 2:** What measures are in place to prevent unauthorized access to the real-time CDC operations implemented in this PR?`

### data/diversity_analysis_report.md:242

**Type:** line_too_long
**Description:** Line is 152 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Lack of robust authentication and authorization mechanisms may allow unauthorized users to access or manipulate healthcare claim data.`

### data/diversity_analysis_report.md:243

**Type:** line_too_long
**Description:** Line is 187 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Introduce role-based access control (RBAC) or OAuth2 for secure authentication and authorization to ensure only authorized personnel can access sensitive operations.`

### data/diversity_analysis_report.md:246

**Type:** line_too_long
**Description:** Line is 146 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 3:** Are there any logging or monitoring mechanisms to detect and respond to potential security breaches related to credential exposure?`

### data/diversity_analysis_report.md:250

**Type:** line_too_long
**Description:** Line is 177 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Without proper logging and monitoring, the team may miss detecting attempts to exploit credential exposure, leading to delayed responses to security incidents.`

### data/diversity_analysis_report.md:251

**Type:** line_too_long
**Description:** Line is 169 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Implement comprehensive logging of access and actions taken on sensitive data, coupled with real-time monitoring to alert on suspicious activities.`

### data/diversity_analysis_report.md:254

**Type:** line_too_long
**Description:** Line is 156 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 4:** How does the application ensure that user inputs are validated and sanitized, especially since unnecessary input sanitization was identified?`

### data/diversity_analysis_report.md:258

**Type:** line_too_long
**Description:** Line is 187 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** Overlooking necessary input validation could lead to injection vulnerabilities or improper handling of data, while excessive sanitization may lead to performance issues.`

### data/diversity_analysis_report.md:259

**Type:** line_too_long
**Description:** Line is 183 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Conduct a thorough review to identify which inputs require sanitization and implement a balanced approach that ensures security without compromising performance.`

### data/diversity_analysis_report.md:262

**Type:** line_too_long
**Description:** Line is 132 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Finding 5:** What is the plan for securing the communication between DynamoDB and Snowflake, especially regarding data in transit?`

### data/diversity_analysis_report.md:266

**Type:** line_too_long
**Description:** Line is 153 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Blind Spot:** If the data transfer between DynamoDB and Snowflake is not encrypted, sensitive healthcare information could be exposed during transit.`

### data/diversity_analysis_report.md:267

**Type:** line_too_long
**Description:** Line is 146 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Recommendation:** Utilize encryption protocols such as TLS for all data in transit between services to mitigate the risk of data interception.`

### docs/ENHANCED_AST_LEVEL_UP_SUMMARY.md:7

**Type:** line_too_long
**Description:** Line is 121 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **Model Consistency Analysis** - "If your model for the artifact hasn't changed, how likely is it the Python changed?"`

### docs/ENHANCED_AST_LEVEL_UP_SUMMARY.md:18

**Type:** line_too_long
**Description:** Line is 182 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This addresses the fundamental question: When a file has no Git history (new artifact), should the model match the currently persisted model, or vary from the GitHub committed model?`

### docs/ENHANCED_AST_LEVEL_UP_SUMMARY.md:275

**Type:** line_too_long
**Description:** Line is 128 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Model Consistency Analysis** - Answers "If your model for the artifact hasn't changed, how likely is it the Python changed?"`

### docs/ENHANCED_AST_LEVEL_UP_SUMMARY.md:281

**Type:** line_too_long
**Description:** Line is 162 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This represents the pinnacle of AST-based code reconstruction, combining semantic understanding with evolutionary intelligence and model consistency analysis.**`

### docs/ENHANCED_AST_LEVEL_UP_SUMMARY.md:283

**Type:** line_too_long
**Description:** Line is 182 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The enhanced approach successfully bridges the gap between current state analysis and historical evolution, providing the most intelligent and accurate reconstruction possible!** 🎯`

### docs/GITHUB_MCP_ANALYSIS.md:5

**Type:** line_too_long
**Description:** Line is 199 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**GitHub MCP** is a Model Context Protocol server that helps AI tools read GitHub repository structure and important files. It's designed to provide AI assistants with better context about codebases.`

### docs/GITHUB_MCP_ANALYSIS.md:12

**Type:** line_too_long
**Description:** Line is 123 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Description**: "A Model Context Protocol (MCP) server that helps read GitHub repository structure and important files."`

### docs/GITHUB_MCP_ANALYSIS.md:18

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Description**: Adapters for integrating Model Context Protocol (MCP) tools with LangChain.js applications`

### docs/GITHUB_MCP_ANALYSIS.md:110

**Type:** line_too_long
**Description:** Line is 133 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- [LangChain MCP Adapters](https://github.com/langchain-ai/langchainjs/tree/main/libs/langchain-mcp-adapters) - LangChain integration`

### docs/GITHUB_MCP_ANALYSIS.md:114

**Type:** line_too_long
**Description:** Line is 221 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Conclusion**: We should definitely be using GitHub MCP! It would significantly improve our codebase understanding and AI context. The fact that we're not using it is indeed a delusion that Ghostbusters has identified. 🎯`

### docs/PR_6_healthcare_cdc_implementation.md:5

**Type:** line_too_long
**Description:** Line is 352 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR implements a complete **Healthcare Change Data Capture (CDC) pipeline** based on the [Snowflake Healthcare CDC Quickstart](https://quickstarts.snowflake.com/guide/Streamline_Healthcare_CDC_DDB_And_Openflow/). The system provides real-time synchronization of healthcare insurance claims data between Amazon DynamoDB and Snowflake using Openflow.`

### docs/PR_6_healthcare_cdc_implementation.md:236

**Type:** line_too_long
**Description:** Line is 189 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This implementation is based on the [Snowflake Healthcare CDC Quickstart](https://quickstarts.snowflake.com/guide/Streamline_Healthcare_CDC_DDB_And_Openflow/) with significant enhancements:`

### docs/PR_6_healthcare_cdc_implementation.md:272

**Type:** line_too_long
**Description:** Line is 156 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR delivers a complete, enterprise-ready healthcare CDC implementation that can be immediately deployed and used for real healthcare claims processing.`

### docs/REAL_GHOSTBUSTERS_SUCCESS.md:14

**Type:** line_too_long
**Description:** Line is 107 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **URL**:`<https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-analyze-embedded%60%60>

### docs/REAL_GHOSTBUSTERS_SUCCESS.md:20

**Type:** line_too_long
**Description:** Line is 108 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **URL**:`<https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-progress-embedded%60%60>

### docs/REAL_GHOSTBUSTERS_SUCCESS.md:26

**Type:** line_too_long
**Description:** Line is 113 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **URL**:`<https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-user-analyses-embedded%60%60>

### docs/REAL_GHOSTBUSTERS_SUCCESS.md:35

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `curl -X POST https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-analyze-embedded \`

### docs/REAL_GHOSTBUSTERS_SUCCESS.md:50

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `"dashboard_url": "https://ghostbusters-dashboard-1077539189076.us-central1.run.app/dashboard/1787f1f8-e8df-4897-968a-de0e0cd94263",`

### docs/REAL_GHOSTBUSTERS_SUCCESS.md:67

**Type:** line_too_long
**Description:** Line is 110 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `curl -X POST https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-progress-embedded \`

### docs/REAL_GHOSTBUSTERS_SUCCESS.md:89

**Type:** line_too_long
**Description:** Line is 115 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `curl -X POST https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-user-analyses-embedded \`

### docs/REAL_GHOSTBUSTERS_SUCCESS.md:183

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We've successfully migrated from a fragile command-line tool to a **real, working cloud service** that:`

### docs/PR_10_PYTHON_TEST_FIXES.md:5

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR addresses comprehensive Python test fixes and project updates to ensure all tests pass and the project is production-ready.`

### docs/HEALTHCARE_CDC_IMPLEMENTATION_PLAN.md:7

**Type:** line_too_long
**Description:** Line is 258 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This document outlines the comprehensive implementation plan for Healthcare CDC Domain Validation, incorporating insights from GA Gemini 2.5 Pro analysis and multi-agent blind spot detection to ensure robust, secure, and compliant healthcare data processing.`

### docs/HEALTHCARE_CDC_IMPLEMENTATION_PLAN.md:223

**Type:** line_too_long
**Description:** Line is 252 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The Healthcare CDC implementation plan provides a comprehensive, security-first approach to healthcare data validation. The multi-agent blind spot analysis identified critical areas for improvement, ensuring robust implementation across all dimensions.`

### docs/PR_1_security_cleanup.md:5

**Type:** line_too_long
**Description:** Line is 156 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR addresses **critical security vulnerabilities** by removing all hardcoded credentials and implementing a secure, parameterized configuration system.`

### docs/PR_1_security_cleanup.md:162

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🎉 This PR transforms the project from a security risk to a secure, user-friendly deployment system!**`

### docs/GCP_VS_AWS_IMPLEMENTATION_COMPARISON.md:345

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Recommendation: GCP Cloud Functions is actually EASIER to implement for our Ghostbusters use case!** 🚀`

### docs/BRANCH_PUSH_SUMMARY.md:4

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Successfully tested, validated, and pushed **7 feature branches** to GitHub with comprehensive testing and quality checks.`

### docs/BRANCH_PUSH_SUMMARY.md:154

**Type:** line_too_long
**Description:** Line is 157 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🎯 Mission Accomplished!** All branches have been successfully tested, validated, and pushed to GitHub with proper quality checks and comprehensive testing.`

### docs/PLATFORM_COMPATIBILITY.md:5

**Type:** line_too_long
**Description:** Line is 142 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This document outlines the platform compatibility of our`make install`targets for deployment in Snowflake workspaces and other environments.`

### docs/PLATFORM_COMPATIBILITY.md:266

**Type:** line_too_long
**Description:** Line is 239 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Our`make install`targets are designed to be **platform-agnostic** and **Snowflake workspace compatible**. The platform detection system automatically adapts to the environment, ensuring consistent installation across different platforms.`

### docs/PR_3_model_driven_orchestration.md:5

**Type:** line_too_long
**Description:** Line is 187 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR introduces a **revolutionary model-driven approach** to tool orchestration that intelligently selects the right tools for each file based on content analysis and domain detection.`

### docs/PR_3_model_driven_orchestration.md:321

**Type:** line_too_long
**Description:** Line is 148 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🧠 This PR introduces a revolutionary model-driven approach that intelligently orchestrates tools based on content analysis and domain detection!**`

### docs/PR_4_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:5

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Title**: OpenFlow Streamlit App - Security-First Architecture with Multi-Agent Blind Spot Detection`

### docs/PR_4_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:19

**Type:** line_too_long
**Description:** Line is 317 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR implements a comprehensive Streamlit application for OpenFlow deployment that addresses **all critical blind spots** identified through multi-agent AI analysis. The implementation follows a **security-first architecture** with production-ready features, accessibility compliance, and performance optimization.`

### docs/PR_4_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:23

**Type:** line_too_long
**Description:** Line is 118 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **✅ Security-First Architecture** - Zero credential exposure, JWT session management, comprehensive input validation`

### docs/PR_4_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:24

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **✅ Production-Ready Features** - Multi-user RBAC, comprehensive error handling, CloudWatch integration`

### docs/PR_4_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:25

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **✅ Accessibility Compliance** - WCAG 2.1 AA standards, mobile responsiveness, progressive disclosure`

### docs/PR_4_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:26

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **✅ Performance Optimization** - Redis caching, parallel API calls, memory-efficient visualizations`

### docs/PR_4_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:351

**Type:** line_too_long
**Description:** Line is 139 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `"content_indicators": ["credential", "password", "secret", "token", "key", "jwt", "encrypt", "hash", "https", "ssl", "csrf", "rate_limit"],`

### docs/PR_4_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:557

**Type:** line_too_long
**Description:** Line is 227 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR successfully implements a **security-first, production-ready Streamlit application** for OpenFlow deployment that addresses **88% of identified blind spots** through multi-agent AI analysis. The implementation provides:`

### docs/PR_4_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:566

**Type:** line_too_long
**Description:** Line is 237 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The **multi-agent blind spot detection framework** proved invaluable in identifying critical issues that would have been missed with single-perspective analysis, demonstrating the power of diverse AI perspectives in software development.`

### docs/pr1_healthcare_cdc_context.md:12

**Type:** line_too_long
**Description:** Line is 265 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR implements a complete **Healthcare Change Data Capture (CDC) pipeline** based on the Snowflake Healthcare CDC Quickstart. The system provides real-time synchronization of healthcare insurance claims data between Amazon DynamoDB and Snowflake using Openflow.`

### docs/pr1_healthcare_cdc_context.md:193

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This Healthcare CDC implementation is the **perfect real-world scenario** for testing our diversity hypothesis because it involves:`

### docs/pr1_healthcare_cdc_context.md:218

**Type:** line_too_long
**Description:** Line is 250 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This context provides the perfect foundation for our multi-agent AI diversity analysis. We can now run our proven diversity hypothesis system against this real-world Healthcare CDC implementation and compare our findings with GitHub Copilot's review.`

### docs/SECURITY_FIXES.md:5

**Type:** line_too_long
**Description:** Line is 118 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This document outlines the security vulnerabilities that were present in the original code and how they were resolved.`

### docs/SECURITY_FIXES.md:148

**Type:** line_too_long
**Description:** Line is 210 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Note**: This template is now secure and reusable. All hardcoded credentials and account-specific data have been removed. Users must provide their own Snowflake-specific values obtained from Snowflake support.`

### docs/COMPREHENSIVE_TEST_RESULTS.md:187

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **✅ Core Infrastructure Working**: Virtual environment, Make-only enforcement, and test framework are all functional`

### docs/COMPREHENSIVE_TEST_RESULTS.md:188

**Type:** line_too_long
**Description:** Line is 106 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `2. **✅ Core Concepts Validated**: All 19 core concept tests passed, showing solid architectural foundation`

### docs/COMPREHENSIVE_TEST_RESULTS.md:192

**Type:** line_too_long
**Description:** Line is 174 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The project has a **strong foundation** with **69% overall test success rate**. The remaining issues are primarily missing implementations rather than architectural problems.`

### docs/COMPREHENSIVE_TEST_RESULTS.md:194

**Type:** line_too_long
**Description:** Line is 106 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Recommendation**: Focus on implementing the missing methods and files to achieve 90%+ test success rate.`

### docs/MODEL_DRIVEN_PROJECTION_COMPONENT_COMPLETE.md:5

**Type:** line_too_long
**Description:** Line is 272 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The **Model-Driven Projection Component** has been successfully organized as a dedicated component within the OpenFlow Playground project. This component implements the radical vision of pure model-driven development where all artifacts are projected from a central model.`

### docs/MODEL_DRIVEN_PROJECTION_COMPONENT_COMPLETE.md:152

**Type:** line_too_long
**Description:** Line is 182 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The Model-Driven Projection Component has been successfully organized as a dedicated component with perfect functional equivalence, zero duplication, and complete test compatibility.`

### docs/MODEL_DRIVEN_PROJECTION_COMPONENT_COMPLETE.md:166

**Type:** line_too_long
**Description:** Line is 141 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Request**: "I think this is a component. create a directory, move the artifacts to it, unless you think it belongs in another component?"`

### docs/LEVEL1_IMPLEMENTATION_SUMMARY.md:171

**Type:** line_too_long
**Description:** Line is 117 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This provides a solid foundation for model-driven development while maintaining compatibility with existing code.**`

### docs/LEVEL1_IMPLEMENTATION_SUMMARY.md:175

**Type:** line_too_long
**Description:** Line is 177 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Start with Model Integration** - Extend the project_model_registry.json to include the extracted nodes and create a projection pipeline that can generate files from the model.`

### docs/LEVEL1_IMPLEMENTATION_SUMMARY.md:177

**Type:** line_too_long
**Description:** Line is 153 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This will give us a **working hybrid system** that demonstrates the value of model-driven development while maintaining compatibility with existing code.`

### docs/HEURISTIC_VS_DETERMINISTIC_PRINCIPLE.md:33

**Type:** line_too_long
**Description:** Line is 110 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **🎯 Semantic Fidelity**: Identical failure patterns prove we captured the **exact same semantic structure**`

### docs/HEURISTIC_VS_DETERMINISTIC_PRINCIPLE.md:35

**Type:** line_too_long
**Description:** Line is 129 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `3. **✅ Behavioral Consistency**: Identical failure patterns prove **functional equivalence** more convincingly than passing tests`

### docs/HEURISTIC_VS_DETERMINISTIC_PRINCIPLE.md:38

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"Failure equivalence is a stronger indicator of semantic reconstruction quality than success equivalence"**`

### docs/HEURISTIC_VS_DETERMINISTIC_PRINCIPLE.md:42

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Identical failures** prove we captured the **exact same semantic intent** and **same failure modes**`

### docs/HEURISTIC_VS_DETERMINISTIC_PRINCIPLE.md:50

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"We kept trying to make LLMs do deterministic tasks when their superpower is heuristic reasoning!"**`

### docs/HEURISTIC_VS_DETERMINISTIC_PRINCIPLE.md:203

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **Heuristic vs Deterministic Principle**: LLMs excel at heuristics, fail at deterministic grunt work`

### docs/HEURISTIC_VS_DETERMINISTIC_PRINCIPLE.md:209

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"We discovered that the best approach is to use deterministic tools for precision and LLM heuristics for intelligence"**`

### docs/HEURISTIC_VS_DETERMINISTIC_PRINCIPLE.md:212

**Type:** line_too_long
**Description:** Line is 224 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This explains why our early attempts failed (trying to make LLMs do deterministic editing) and why the AST approach succeeded (letting LLMs focus on semantic understanding while using deterministic tools for the grunt work).`

### docs/HEURISTIC_VS_DETERMINISTIC_PRINCIPLE.md:227

**Type:** line_too_long
**Description:** Line is 160 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This principle should guide all LLM-assisted development, ensuring we leverage the strengths of both deterministic tools and LLM heuristics for optimal results.`

### docs/PHASE_1_IMPLEMENTATION_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**✅ Successfully completed Phase 1 of both Ghostbusters GCP Cloud Functions migration AND GitHub Copilot integration!**`

### docs/DIVERSITY_HYPOTHESIS_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 206 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We have successfully **proven the Diversity Hypothesis** and built a revolutionary multi-agent AI blind spot detection system that demonstrates **"diversity is the only free lunch"** in AI-powered analysis.`

### docs/DIVERSITY_HYPOTHESIS_SUMMARY.md:47

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Hypothesis**: Multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer.`

### docs/DIVERSITY_HYPOTHESIS_SUMMARY.md:145

**Type:** line_too_long
**Description:** Line is 144 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"Diversity is the only free lunch"** - Multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer.`

### docs/DIVERSITY_HYPOTHESIS_SUMMARY.md:225

**Type:** line_too_long
**Description:** Line is 108 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We have successfully **proven the Diversity Hypothesis** and built a revolutionary system that demonstrates:`

### docs/DIVERSITY_HYPOTHESIS_SUMMARY.md:236

**Type:** line_too_long
**Description:** Line is 180 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This system can be immediately deployed for real-time diversity analysis of any technical decision or codebase, providing comprehensive blind spot detection at virtually zero cost.`

### docs/DIVERSITY_HYPOTHESIS_SUMMARY.md:264

**Type:** line_too_long
**Description:** Line is 135 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The Diversity Hypothesis is proven, the system is built, and the revolution in AI-powered blind spot detection is ready for deployment.`

### docs/GIT_WORKFLOW_SUMMARY.md:121

**Type:** line_too_long
**Description:** Line is 139 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The Diversity Hypothesis is proven, the system is built, and the revolution in AI-powered blind spot detection is ready for deployment!**`

### docs/GIT_WORKFLOW_SUMMARY.md:123

**Type:** line_too_long
**Description:** Line is 192 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"Diversity is the only free lunch"** - We've demonstrated that multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer, at virtually zero cost.`

### docs/PHASE_3_IMPLEMENTATION_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 136 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**✅ Successfully completed Phase 3 of Ghostbusters GCP Cloud Functions migration with advanced ML integration and enterprise features!**`

### docs/PHASE_3_IMPLEMENTATION_SUMMARY.md:190

**Type:** line_too_long
**Description:** Line is 106 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `endpoint = Endpoint("projects/ghostbusters-project/locations/us-central1/endpoints/ghostbusters-insights")`

### docs/PHASE_3_IMPLEMENTATION_SUMMARY.md:380

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `curl -X POST https://us-central1-ghostbusters-project.cloudfunctions.net/ghostbusters-analyze-advanced \`

### docs/PHASE_3_IMPLEMENTATION_SUMMARY.md:386

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `curl -X POST https://us-central1-ghostbusters-project.cloudfunctions.net/ghostbusters-custom-agents \`

### docs/PHASE_3_IMPLEMENTATION_SUMMARY.md:425

**Type:** line_too_long
**Description:** Line is 139 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🎯 The fragile command-line Ghostbusters has been successfully transformed into a robust, scalable, ML-powered enterprise cloud service!**`

### docs/SECURITY_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 161 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `You were absolutely right to call out that hardcoded crap. I've fixed it all and created a comprehensive security framework to prevent this from happening again.`

### docs/SECURITY_SUMMARY.md:135

**Type:** line_too_long
**Description:** Line is 126 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**I've fixed it all** and created a comprehensive security framework that will prevent this kind of mess from happening again.`

### docs/SECURITY_SUMMARY.md:143

**Type:** line_too_long
**Description:** Line is 123 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This is how infrastructure should be done** - not with hardcoded credentials that get companies fined in security audits!`

### docs/SECURITY_SUMMARY.md:147

**Type:** line_too_long
**Description:** Line is 174 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Remember:** If you see hardcoded credentials, FIX THEM IMMEDIATELY. If you're not sure if something should be hardcoded, DON'T HARDCODE IT. Follow the 50 rules religiously.`

### docs/GHOSTBUSTERS_ANALYSIS_RESPONSE.md:12

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **Missing Type Annotations** - Multiple files (client.py, container_main.py, llm_agents.py, main.py)`

### docs/GHOSTBUSTERS_ANALYSIS_RESPONSE.md:110

**Type:** line_too_long
**Description:** Line is 173 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Bottom line**: We're not tired of JSON models yet, but we should be! The Ghostbusters are telling us to move to **type-safe, validated models** with proper architecture. 🎯`

### docs/README.md:5

**Type:** line_too_long
**Description:** Line is 208 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This directory contains the **proven Diversity Hypothesis system** - a revolutionary multi-agent AI blind spot detection system that demonstrates **"diversity is the only free lunch"** in AI-powered analysis.`

### docs/README.md:119

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Hypothesis**: Multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer.`

### docs/README.md:178

**Type:** line_too_long
**Description:** Line is 144 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"Diversity is the only free lunch"** - Multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer.`

### docs/README.md:332

**Type:** line_too_long
**Description:** Line is 108 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We have successfully **proven the Diversity Hypothesis** and built a revolutionary system that demonstrates:`

### docs/README.md:343

**Type:** line_too_long
**Description:** Line is 180 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This system can be immediately deployed for real-time diversity analysis of any technical decision or codebase, providing comprehensive blind spot detection at virtually zero cost.`

### docs/TEST_ALL_FIX_COMPLETE_SUMMARY.md:177

**Type:** line_too_long
**Description:** Line is 162 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The remaining 20 bandit warnings are low-severity issues about subprocess usage in development tools, which are expected and acceptable for this type of codebase.`

### docs/SYNTAX_FIX_SUMMARY.md:4

**Type:** line_too_long
**Description:** Line is 200 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `You were absolutely right - one of my syntax fix scripts introduced a major structural issue by adding duplicate shebang lines and other problems. This created a cascade of issues across the codebase.`

### docs/SYNTAX_FIX_SUMMARY.md:9

**Type:** line_too_long
**Description:** Line is 137 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **Aggressive Pattern Matching**: My original scripts used broad pattern matching that incorrectly identified lines needing indentation`

### docs/SYNTAX_FIX_SUMMARY.md:10

**Type:** line_too_long
**Description:** Line is 121 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `2. **Duplicate Shebang Lines**: The scripts added`#!/usr/bin/env python3`lines without checking if they already existed`

### docs/SYNTAX_FIX_SUMMARY.md:72

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `3. **`src/multi_agent_testing/live_smoke_test_langchain.py`** - Line 35: Unindented variable assignment`

### docs/SYNTAX_FIX_SUMMARY.md:81

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `12. **`src/multi_agent_testing/test_multi_agent_blind_spot_detection.py`** - Line 58: Unindented variable assignment`

### docs/SYNTAX_FIX_SUMMARY.md:100

**Type:** line_too_long
**Description:** Line is 138 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The remaining 26 files need manual attention because they have complex indentation issues that require understanding the specific context.`

### docs/SYNTAX_FIX_SUMMARY.md:103

**Type:** line_too_long
**Description:** Line is 123 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Always run`python test_syntax_fix_safety.py`before and after any automated syntax fixes to catch structural issues early.`

### docs/SYNTAX_FIX_SUMMARY.md:126

**Type:** line_too_long
**Description:** Line is 335 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `You were absolutely right to call out the mess created by the aggressive syntax fix scripts. The improved approach with safety testing and conservative fixes is much better. The root cause was lack of context awareness and over-aggressive pattern matching. The solution is test-driven, conservative fixes with comprehensive validation.`

### docs/IMPLEMENTATION_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 144 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We have successfully implemented the **immediate actions** from our Ghostbusters analysis and created a complete AST to Graph Database solution!`

### docs/IMPLEMENTATION_SUMMARY.md:163

**Type:** line_too_long
**Description:** Line is 352 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We've successfully **implemented the immediate actions** from our Ghostbusters analysis and created a **complete AST to Graph Database solution**. The **fascinating case** you identified - using profiler output to trace calls within included packages - is now **ready for implementation** with our clean, validated AST dataset and Neo4j infrastructure.`

### docs/IMPLEMENTATION_SUMMARY.md:169

**Type:** line_too_long
**Description:** Line is 130 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*"We've made it so!"* - The implementation is complete and ready for the next phase of advanced features and profiler integration.`

### docs/CALL_MORE_GHOSTBUSTERS_RULE.md:4

**Type:** line_too_long
**Description:** Line is 138 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"When 'call more ghostbusters' is invoked, immediately trigger multi-agent validation with all available LLMs and deterministic tools"**`

### docs/MAKE_ONLY_ENFORCEMENT_SUMMARY.md:4

**Type:** line_too_long
**Description:** Line is 145 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The user requested a system to enforce that all tool execution goes through the`make`system rather than direct command execution. This ensures:`

### docs/MAKE_ONLY_ENFORCEMENT_SUMMARY.md:213

**Type:** line_too_long
**Description:** Line is 176 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The system ensures that all tool execution follows the intended workflow while providing a smooth developer experience with helpful error messages and easy restoration options.`

### docs/GITHUB_MCP_INTEGRATION_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 153 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We successfully investigated GitHub MCP (Model Context Protocol) and integrated it into our project to address the delusion that Ghostbusters identified.`

### docs/GITHUB_MCP_INTEGRATION_SUMMARY.md:16

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Missing Repository Context** - We were using manual file discovery instead of intelligent analysis`

### docs/GITHUB_MCP_INTEGRATION_SUMMARY.md:55

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Dependencies: ['Python (pyproject.toml)', 'Node.js (package.json)', 'Go (go.mod)', 'Rust (Cargo.toml)']`

### docs/GITHUB_MCP_INTEGRATION_SUMMARY.md:56

**Type:** line_too_long
**Description:** Line is 183 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Key Files: ['README.md', 'README.rst', 'README.txt', 'pyproject.toml', 'setup.py', 'requirements.txt', 'package.json', 'Cargo.toml', 'go.mod', '.gitignore', 'LICENSE', 'CHANGELOG.md']`

### docs/GITHUB_MCP_INTEGRATION_SUMMARY.md:142

**Type:** line_too_long
**Description:** Line is 196 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The delusion is fixed!** 🎯 We now have intelligent repository context instead of manual file discovery. Ghostbusters confirms this with 7 delusions detected (including the new MCP-related ones).`

### docs/DIVERSITY_HYPOTHESIS_ORGANIZATION.md:5

**Type:** line_too_long
**Description:** Line is 160 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We have successfully **organized the proven Diversity Hypothesis system** into a clean, well-structured subdirectory with specific cursor rules for development.`

### docs/DIVERSITY_HYPOTHESIS_ORGANIZATION.md:162

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Hypothesis**: Multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer.`

### docs/DIVERSITY_HYPOTHESIS_ORGANIZATION.md:221

**Type:** line_too_long
**Description:** Line is 144 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"Diversity is the only free lunch"** - Multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer.`

### docs/DIVERSITY_HYPOTHESIS_ORGANIZATION.md:317

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We have successfully **organized the proven Diversity Hypothesis system** into a clean, well-structured subdirectory with:`

### docs/DIVERSITY_HYPOTHESIS_ORGANIZATION.md:326

**Type:** line_too_long
**Description:** Line is 108 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The diversity hypothesis is not just proven - it's economically revolutionary and perfectly organized!** 🚀`

### docs/DIVERSITY_HYPOTHESIS_ORGANIZATION.md:328

**Type:** line_too_long
**Description:** Line is 180 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This system can be immediately deployed for real-time diversity analysis of any technical decision or codebase, providing comprehensive blind spot detection at virtually zero cost.`

### docs/GITHUB_COPILOT_IMPLEMENTATION_PLAN.md:446

**Type:** line_too_long
**Description:** Line is 263 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `python -c "from src.ghostbusters.ghostbusters_orchestrator import run_ghostbusters; import asyncio; result = asyncio.run(run_ghostbusters('.')); print(f'🔍 Post-Integration Status: Confidence {result.confidence_score}, Delusions {len(result.delusions_detected)}')"`

### docs/GITHUB_COPILOT_IMPLEMENTATION_PLAN.md:476

**Type:** line_too_long
**Description:** Line is 145 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- [GitHub Copilot Code Review Documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review)`

### docs/GITHUB_COPILOT_IMPLEMENTATION_PLAN.md:482

**Type:** line_too_long
**Description:** Line is 275 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This implementation plan provides a **comprehensive approach** to integrating GitHub Copilot code review with our existing GitHub MCP system. The plan addresses the **6 delusions** identified by Ghostbusters and creates a **security-first, model-driven** code review process.`

### docs/INTELLIGENT_LINTER_SYSTEM_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 226 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We have successfully implemented a comprehensive **Intelligent Linter System** that prevents violations before they happen, integrates with AI-powered linters, and dynamically updates Cursor rules based on detected violations.`

### docs/INTELLIGENT_LINTER_SYSTEM_SUMMARY.md:193

**Type:** line_too_long
**Description:** Line is 256 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The system is now ready to **proactively prevent linter violations** and **continuously improve** based on detected patterns. Every violation becomes an opportunity to enhance the prevention system, creating a **self-improving quality enforcement system**.`

### docs/INTELLIGENT_LINTER_SYSTEM_SUMMARY.md:197

**Type:** line_too_long
**Description:** Line is 106 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🎉 The Intelligent Linter System is now operational and ready to prevent violations before they happen!**`

### docs/ARTIFACTFORGE_ISSUES_LOG.md:19

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Status**: 🔴 **NEEDS FOLLOW-UP** - These are the same files we've been trying to fix with syntax fixers`

### docs/ARTIFACTFORGE_ISSUES_LOG.md:82

**Type:** line_too_long
**Description:** Line is 149 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The systemic syntax errors are a separate issue that should be addressed with the existing syntax fixers, not blocking ArtifactForge development.**`

### docs/MODEL_DRIVEN_CONFIGURATION_ANALYSIS.md:8

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **Configuration changes are NOT emanating from models** - We manually edit files instead of updating models first`

### docs/MODEL_DRIVEN_CONFIGURATION_ANALYSIS.md:9

**Type:** line_too_long
**Description:** Line is 112 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `2. **No model updates during fixes** - The`project_model_registry.json`wasn't updated to reflect current state`

### docs/MODEL_DRIVEN_CONFIGURATION_ANALYSIS.md:14

**Type:** line_too_long
**Description:** Line is 174 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We've been **reactively fixing symptoms** instead of **model-driven configuration**. The model should be the **single source of truth** that drives all configuration changes.`

### docs/MODEL_DRIVEN_CONFIGURATION_ANALYSIS.md:188

**Type:** line_too_long
**Description:** Line is 111 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `You've identified a **critical insight**: **Configuration should emanate from models, not be manually edited**.`

### docs/MODEL_DRIVEN_CONFIGURATION_ANALYSIS.md:212

**Type:** line_too_long
**Description:** Line is 138 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**You've identified the fundamental problem and the solution. This is exactly the right direction for scalable configuration management.**`

### docs/BRANCH_SEPARATION_SUMMARY.md:4

**Type:** line_too_long
**Description:** Line is 138 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Successfully separated the massive changes since the last commit into **7 focused feature branches**, each with a clear purpose and scope.`

### docs/BRANCH_SEPARATION_SUMMARY.md:45

**Type:** line_too_long
**Description:** Line is 143 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Files:**`MODEL_DRIVEN_PROJECTION_COMPONENT_COMPLETE.md`,`src/model_driven_projection/`,`project_model_registry.json`,`project_model.py\`\`

### docs/BRANCH_SEPARATION_SUMMARY.md:78

**Type:** line_too_long
**Description:** Line is 158 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Files:**`Makefile`,`pyproject.toml`,`setup.py`,`uv.lock`,`config/`,`scripts/`,`src/**init**.py`,`src/mdc_generator/`,`data/`, documentation files`

### docs/BRANCH_SEPARATION_SUMMARY.md:158

**Type:** line_too_long
**Description:** Line is 178 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🎯 Mission Accomplished!** The massive changes have been successfully organized into focused, manageable feature branches that can be reviewed, tested, and merged independently.`

### docs/PR_4_cursor_rules.md:5

**Type:** line_too_long
**Description:** Line is 182 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR introduces **comprehensive Cursor rules** that implement model-driven development practices, intelligent policy enforcement, and architectural best practices for the project.`

### docs/PR_4_cursor_rules.md:55

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `globs: ["**/*.yaml", "**/*.yml", "**/*.json", "**/*.env", "**/*.sh", "**/*.py", "**/*.md", "**/*.txt"]`

### docs/PR_4_cursor_rules.md:72

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `globs: ["**/*.yaml", "**/*.yml", "**/*.json", "**/*.toml", "**/*.ini", "**/*.cfg", "**/*.mdc", "**/*.py"]`

### docs/PR_4_cursor_rules.md:457

**Type:** line_too_long
**Description:** Line is 138 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🎯 This PR establishes comprehensive Cursor rules that implement model-driven development practices and intelligent policy enforcement!**`

### docs/pr1_diversity_vs_copilot_comparison.md:5

**Type:** line_too_long
**Description:** Line is 304 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We applied our **proven diversity hypothesis system** to analyze PR #1 (Healthcare CDC Implementation) and compared our findings with GitHub Copilot's review comments. The results demonstrate that **multiple AI perspectives provide exponentially better blind spot detection** than any single AI reviewer.`

### docs/pr1_diversity_vs_copilot_comparison.md:130

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `#### 2. **Enhance Documentation for Installation and Security Practices** (Priority: 0.90, ROI: High)`

### docs/pr1_diversity_vs_copilot_comparison.md:255

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Our analysis of PR #1 demonstrates that **"diversity is the only free lunch"** in AI-powered code review:`

### docs/pr1_diversity_vs_copilot_comparison.md:274

**Type:** line_too_long
**Description:** Line is 113 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The diversity hypothesis is not just proven - it's economically revolutionary and ready for production use!** 🚀`

### docs/PR_1_COMPREHENSIVE_IMPLEMENTATION_PLAN.md:5

**Type:** line_too_long
**Description:** Line is 309 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This plan combines **GitHub Copilot's findings** (11 issues) with **our diversity hypothesis analysis** (25 issues) to provide **maximum coverage** for PR #1 (Healthcare CDC Implementation). The combined approach demonstrates how **multiple AI perspectives** provide exponentially better blind spot detection.`

### docs/PR_1_COMPREHENSIVE_IMPLEMENTATION_PLAN.md:8

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **GitHub Copilot**: 11 findings (Security: 5, Code Quality: 3, Infrastructure: 2, Documentation: 1)`

### docs/PR_1_COMPREHENSIVE_IMPLEMENTATION_PLAN.md:9

**Type:** line_too_long
**Description:** Line is 106 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Our Diversity Analysis**: 25 findings (Security: 5, DevOps: 5, Code Quality: 5, UX: 5, Performance: 5)`

### docs/PR_1_COMPREHENSIVE_IMPLEMENTATION_PLAN.md:155

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Addresses**: Copilot Infrastructure (2 issues) + Copilot Documentation (1 issue) + Our Code Quality Expert (2 issues)`

### docs/PR_1_COMPREHENSIVE_IMPLEMENTATION_PLAN.md:215

**Type:** line_too_long
**Description:** Line is 125 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Addresses**: Our Code Quality Expert (2 issues) + Our User Experience Advocate (2 issues) + Copilot Code Quality (2 issues)`

### docs/PR_1_COMPREHENSIVE_IMPLEMENTATION_PLAN.md:365

**Type:** line_too_long
**Description:** Line is 130 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This updated comprehensive implementation plan demonstrates that **"diversity is the only free lunch"** in AI-powered code review:`

### docs/PR_1_COMPREHENSIVE_IMPLEMENTATION_PLAN.md:375

**Type:** line_too_long
**Description:** Line is 151 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Copilot is getting better, but our diversity system still provides comprehensive multi-perspective coverage that no single AI reviewer can match!** 🚀`

### docs/DOCUMENTATION_INDEX.md:214

**Type:** line_too_long
**Description:** Line is 183 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This index provides a comprehensive view of all documentation in the OpenFlow Playground project. All documents are now properly categorized and organized by purpose and audience.**`

### docs/level1_bridge_analysis.md:249

**Type:** line_too_long
**Description:** Line is 195 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Level 1 is immediately actionable** and provides a solid foundation for model-driven development. The bridge components are **well-defined and implementable** with existing tools and knowledge.`

### docs/level1_bridge_analysis.md:253

**Type:** line_too_long
**Description:** Line is 153 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This will give us a **working hybrid system** that demonstrates the value of model-driven development while maintaining compatibility with existing code.`

### docs/ORGANIZATION_SUMMARY.md:242

**Type:** line_too_long
**Description:** Line is 137 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The file organization is now complete and follows the project model registry domains with domain-specific rules for each component!** 🚀`

### docs/GIT_ENHANCED_AST_LEVEL_UP.md:6

**Type:** line_too_long
**Description:** Line is 188 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Enhance the AST Level Up approach by using Git history to restore previous working versions, AST parse them, and use the structural information to guide the reconstruction of broken files.`

### docs/GIT_ENHANCED_AST_LEVEL_UP.md:63

**Type:** line_too_long
**Description:** Line is 129 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `def reconstruct_with_guidance(self, file_path: str, current_interpretation: Dict[str, Any], previous_ast: Dict[str, Any]) -> str:`

### docs/GIT_ENHANCED_AST_LEVEL_UP.md:207

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `2. **AST parsing of previous versions provides structural templates** - Actual function signatures and class structures`

### docs/GIT_ENHANCED_AST_LEVEL_UP.md:220

**Type:** line_too_long
**Description:** Line is 147 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This enhancement bridges the gap between semantic understanding and actual code evolution, providing the most accurate reconstruction possible.**`

### docs/GIT_ENHANCED_AST_LEVEL_UP.md:229

**Type:** line_too_long
**Description:** Line is 183 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The Git-enhanced approach represents the pinnacle of AST-based code reconstruction, combining the power of semantic understanding with the authenticity of version control history.**`

### docs/PR_8_diversity_hypothesis_applied_to_pr1.md:12

**Type:** line_too_long
**Description:** Line is 374 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We applied our **proven diversity hypothesis system** to analyze PR #1 (Healthcare CDC Implementation) and compared our findings with GitHub Copilot's review comments. This demonstrates that **"diversity is the only free lunch"** in AI-powered code review by showing how multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer.`

### docs/PR_8_diversity_hypothesis_applied_to_pr1.md:28

**Type:** line_too_long
**Description:** Line is 234 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `When we started this journey, you asked: **"do you reckon having more diverse models will help?"** and referenced [PR #1's GitHub Copilot review](https://github.com/louspringer/OpenFlow-Playground/pull/1#pullrequestreview-3076741875).`

### docs/PR_8_diversity_hypothesis_applied_to_pr1.md:31

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Hypothesis**: Multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer.`

### docs/PR_8_diversity_hypothesis_applied_to_pr1.md:33

**Type:** line_too_long
**Description:** Line is 158 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Rationale**: Different AI models, roles, and perspectives focus on different concerns, providing comprehensive coverage that any single reviewer would miss.`

### docs/PR_8_diversity_hypothesis_applied_to_pr1.md:149

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `#### 2. **Enhance Documentation for Installation and Security Practices** (Priority: 0.90, ROI: High)`

### docs/PR_8_diversity_hypothesis_applied_to_pr1.md:313

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Our analysis of PR #1 demonstrates that **"diversity is the only free lunch"** in AI-powered code review:`

### docs/PR_8_diversity_hypothesis_applied_to_pr1.md:332

**Type:** line_too_long
**Description:** Line is 113 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The diversity hypothesis is not just proven - it's economically revolutionary and ready for production use!** 🚀`

### docs/PR_8_diversity_hypothesis_applied_to_pr1.md:350

**Type:** line_too_long
**Description:** Line is 113 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The diversity hypothesis is not just proven - it's economically revolutionary and ready for production use!** 🚀`

### docs/GHOSTBUSTERS_GCP_IMPLEMENTATION_PLAN.md:7

**Type:** line_too_long
**Description:** Line is 126 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `After comprehensive analysis, GCP Cloud Functions offers significant advantages over AWS Lambda for our specific requirements:`

### docs/CONFLICT_RESOLUTION_SUMMARY.md:4

**Type:** line_too_long
**Description:** Line is 128 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Successfully resolved conflicts for **PR #5: Security-First Architecture** by rebasing the branch on the updated develop branch.`

### docs/CONFLICT_RESOLUTION_SUMMARY.md:10

**Type:** line_too_long
**Description:** Line is 112 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `From the [GitHub PR #5](https://github.com/louspringer/OpenFlow-Playground/pull/5#pullrequestreview-3086099351):`

### docs/CONFLICT_RESOLUTION_SUMMARY.md:94

**Type:** line_too_long
**Description:** Line is 115 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- [Copilot Review Comments](https://github.com/louspringer/OpenFlow-Playground/pull/5#pullrequestreview-3086099351)`

### docs/CONFLICT_RESOLUTION_SUMMARY.md:98

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🎯 Mission Accomplished!** PR #5 conflicts have been successfully resolved and the branch is now ready for merging.`

### docs/PR_9_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:5

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Title**: OpenFlow Streamlit App - Security-First Architecture with Multi-Agent Blind Spot Detection`

### docs/PR_9_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:19

**Type:** line_too_long
**Description:** Line is 317 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR implements a comprehensive Streamlit application for OpenFlow deployment that addresses **all critical blind spots** identified through multi-agent AI analysis. The implementation follows a **security-first architecture** with production-ready features, accessibility compliance, and performance optimization.`

### docs/PR_9_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:23

**Type:** line_too_long
**Description:** Line is 118 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **✅ Security-First Architecture** - Zero credential exposure, JWT session management, comprehensive input validation`

### docs/PR_9_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:24

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **✅ Production-Ready Features** - Multi-user RBAC, comprehensive error handling, CloudWatch integration`

### docs/PR_9_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:25

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **✅ Accessibility Compliance** - WCAG 2.1 AA standards, mobile responsiveness, progressive disclosure`

### docs/PR_9_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:26

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **✅ Performance Optimization** - Redis caching, parallel API calls, memory-efficient visualizations`

### docs/PR_9_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:351

**Type:** line_too_long
**Description:** Line is 139 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `"content_indicators": ["credential", "password", "secret", "token", "key", "jwt", "encrypt", "hash", "https", "ssl", "csrf", "rate_limit"],`

### docs/PR_9_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:557

**Type:** line_too_long
**Description:** Line is 227 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR successfully implements a **security-first, production-ready Streamlit application** for OpenFlow deployment that addresses **88% of identified blind spots** through multi-agent AI analysis. The implementation provides:`

### docs/PR_9_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md:566

**Type:** line_too_long
**Description:** Line is 237 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The **multi-agent blind spot detection framework** proved invaluable in identifying critical issues that would have been missed with single-perspective analysis, demonstrating the power of diverse AI perspectives in software development.`

### docs/LANGCHAIN_MIGRATION_SUMMARY.md:6

**Type:** line_too_long
**Description:** Line is 121 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `You were absolutely right to ask: *"Why aren't you using langchain/langgraph? We don't want to maintain that glue code."*`

### docs/LANGCHAIN_MIGRATION_SUMMARY.md:123

**Type:** line_too_long
**Description:** Line is 164 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This is a perfect example of using the right tool for the job. LangChain provides exactly what we needed without the maintenance overhead of manual API integration.`

### docs/PR_5_model_persistence.md:5

**Type:** line_too_long
**Description:** Line is 181 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Problem**: The`ProjectModel`orchestration layer existed only in Python code, making it impossible for future LLMs to recover the system's intent and continue work intelligently.`

### docs/PR_5_model_persistence.md:7

**Type:** line_too_long
**Description:** Line is 169 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Solution**: Created a persistent, machine-readable model registry and self-referential recovery system that enables any future LLM to understand and extend the system.`

### docs/PR_5_model_persistence.md:138

**Type:** line_too_long
**Description:** Line is 179 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"The model is the authority. If you're not using`project_model_registry.json`to make decisions, you're guessing. Load the model, understand the intent, follow the mappings."**`

### docs/PR_5_model_persistence.md:211

**Type:** line_too_long
**Description:** Line is 120 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🎉 This PR creates a self-healing, model-driven system that can recover from any state and continue intelligent work!**`

### docs/TEST_ALL_FIX_SUMMARY.md:4

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Successfully fixed the majority of test-all failures with comprehensive logging and systematic approach.`

### docs/TEST_ALL_FIX_SUMMARY.md:92

**Type:** line_too_long
**Description:** Line is 118 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **Bandit Warnings**: The remaining 115 warnings are all low-severity and related to assert statements in test files`

### docs/TEST_ALL_FIX_SUMMARY.md:122

**Type:** line_too_long
**Description:** Line is 220 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The test-all fix has been **successfully completed** with comprehensive logging and systematic approach. The project is now in a production-ready state with all critical functionality working and all major tests passing.`

### docs/prioritized_implementation_plan.md:5

**Type:** line_too_long
**Description:** Line is 121 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This report synthesizes 6 diverse findings into prioritized, actionable fixes that address multiple stakeholder concerns.`

### docs/prioritized_implementation_plan.md:25

**Type:** line_too_long
**Description:** Line is 244 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Description**: Establish a secure method for managing sensitive credentials using environment variables or a secrets management tool. This will prevent accidental exposure in logs and subprocesses, ensuring compliance with security standards.`

### docs/prioritized_implementation_plan.md:46

**Type:** line_too_long
**Description:** Line is 235 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Description**: Refactor the error handling and logging mechanisms in the CDC process to ensure robust tracking of errors, including meaningful messages and context. This will facilitate troubleshooting and improve system reliability.`

### docs/prioritized_implementation_plan.md:70

**Type:** line_too_long
**Description:** Line is 200 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Description**: Perform load testing and performance profiling to assess the impact of high data volumes on real-time CDC operations. This will ensure scalability and responsiveness under peak loads.`

### docs/prioritized_implementation_plan.md:91

**Type:** line_too_long
**Description:** Line is 184 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Description**: Integrate comprehensive monitoring tools and set up alerting mechanisms to track data flows and detect failures in data synchronization between DynamoDB and Snowflake.`

### docs/prioritized_implementation_plan.md:112

**Type:** line_too_long
**Description:** Line is 249 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Description**: Develop thorough documentation that includes installation instructions, usage examples, and guidelines for contributing to the codebase. This will facilitate onboarding for new developers and improve overall project maintainability.`

### docs/prioritized_implementation_plan.md:133

**Type:** line_too_long
**Description:** Line is 187 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Description**: Review and optimize the input sanitization process to ensure it only targets necessary inputs, thereby enhancing overall system performance without compromising security.`

### docs/prioritized_implementation_plan.md:156

**Type:** line_too_long
**Description:** Line is 135 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Implement Robust Credential Management                            3            2                 2             1                      1`

### docs/prioritized_implementation_plan.md:157

**Type:** line_too_long
**Description:** Line is 135 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Enhance Error Handling and Logging                                2            3                 2             1                      2`

### docs/prioritized_implementation_plan.md:158

**Type:** line_too_long
**Description:** Line is 135 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Conduct Load Testing and Performance Profiling                    2            3                 2             3                      2`

### docs/prioritized_implementation_plan.md:159

**Type:** line_too_long
**Description:** Line is 135 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Create Comprehensive Documentation                                1            3                 3             2                      2`

### docs/prioritized_implementation_plan.md:160

**Type:** line_too_long
**Description:** Line is 135 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Implement Monitoring and Alerting for CDC Operations              3            3                 2             2                      2`

### docs/prioritized_implementation_plan.md:161

**Type:** line_too_long
**Description:** Line is 135 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Optimize Input Sanitization Process                               2            2                 3             2                      2`

### docs/PR_CREATION_SUMMARY.md:4

**Type:** line_too_long
**Description:** Line is 114 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Successfully created **7 Pull Requests** with proper numbering and comprehensive content for all feature branches.`

### docs/PR_CREATION_SUMMARY.md:227

**Type:** line_too_long
**Description:** Line is 147 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🎯 Mission Accomplished!** All feature branches now have properly numbered Pull Requests with comprehensive content, ready for review and merging.`

### docs/TEST_EXECUTION_SUMMARY.md:67

**Type:** line_too_long
**Description:** Line is 176 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The system ensures that all tool execution follows the intended workflow while providing a smooth developer experience with helpful error messages and easy restoration options.`

### docs/TEST_EXECUTION_SUMMARY.md:85

**Type:** line_too_long
**Description:** Line is 107 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Successfully executed tests across multiple branches and fixed critical issues with test return statements.`

### docs/AST_LEVEL_UP_PLAN.md:4

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Transform from pattern-based syntax fixing to AST-based semantic reconstruction for both Python code and .mdc files.`

### docs/AST_LEVEL_UP_PLAN.md:29

**Type:** line_too_long
**Description:** Line is 110 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **🎯 Semantic Fidelity**: Identical failure patterns prove we captured the **exact same semantic structure**`

### docs/AST_LEVEL_UP_PLAN.md:31

**Type:** line_too_long
**Description:** Line is 129 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `3. **✅ Behavioral Consistency**: Identical failure patterns prove **functional equivalence** more convincingly than passing tests`

### docs/AST_LEVEL_UP_PLAN.md:34

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"Failure equivalence is a stronger indicator of semantic reconstruction quality than success equivalence"**`

### docs/AST_LEVEL_UP_PLAN.md:399

**Type:** line_too_long
**Description:** Line is 206 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This plan represents a fundamental shift from **deterministic grunt work** to **intelligent tool orchestration**, leveraging the strengths of both deterministic tools and LLM heuristics for optimal results.`

### docs/GITHUB_COPILOT_CODE_REVIEW_ANALYSIS.md:5

**Type:** line_too_long
**Description:** Line is 282 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Based on the [GitHub Copilot code review documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review), this feature provides intelligent code analysis and review capabilities that complement our existing GitHub MCP integration.`

### docs/GITHUB_COPILOT_CODE_REVIEW_ANALYSIS.md:160

**Type:** line_too_long
**Description:** Line is 145 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- [GitHub Copilot Code Review Documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review)`

### docs/GITHUB_COPILOT_CODE_REVIEW_ANALYSIS.md:162

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- [Custom Instructions Guide](https://docs.github.com/en/copilot/customize-copilot/custom-instructions-for-github-copilot)`

### docs/GITHUB_COPILOT_CODE_REVIEW_ANALYSIS.md:174

**Type:** line_too_long
**Description:** Line is 199 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Ghostbusters confirms:** 6 delusions detected, including missing code review automation. This integration would address multiple delusions and enhance our security-first, model-driven architecture.`

### docs/PHASE_2_COMPLETION_SUMMARY.md:14

**Type:** line_too_long
**Description:** Line is 107 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **URL**:`<https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-analyze-enhanced%60%60>

### docs/PHASE_2_COMPLETION_SUMMARY.md:26

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **URL**:`<https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-user-analyses%60%60>

### docs/PHASE_2_COMPLETION_SUMMARY.md:57

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `curl -X POST https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-analyze-enhanced \`

### docs/PHASE_2_COMPLETION_SUMMARY.md:71

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `"dashboard_url": "https://ghostbusters-dashboard-1077539189076.us-central1.run.app/dashboard/f23181a3-6119-4b80-9e94-90292a2b83f4",`

### docs/PHASE_2_COMPLETION_SUMMARY.md:78

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `curl -X POST https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-progress \`

### docs/PHASE_2_COMPLETION_SUMMARY.md:98

**Type:** line_too_long
**Description:** Line is 106 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `curl -X POST https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net/ghostbusters-user-analyses \`

### docs/PR_7_diversity_hypothesis_proven.md:17

**Type:** line_too_long
**Description:** Line is 285 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR proves the **"Diversity Hypothesis"** - that multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer. We built a comprehensive system that demonstrates **"diversity is the only free lunch"** in AI-powered code review and analysis.`

### docs/PR_7_diversity_hypothesis_proven.md:36

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Hypothesis**: Multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer.`

### docs/PR_7_diversity_hypothesis_proven.md:195

**Type:** line_too_long
**Description:** Line is 144 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"Diversity is the only free lunch"** - Multiple AI perspectives provide exponentially better blind spot detection than any single AI reviewer.`

### docs/PR_7_diversity_hypothesis_proven.md:492

**Type:** line_too_long
**Description:** Line is 182 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR successfully **proves the Diversity Hypothesis** and demonstrates that **"diversity is the only free lunch"** in AI-powered analysis. We've built a comprehensive system that:`

### docs/PR_7_diversity_hypothesis_proven.md:501

**Type:** line_too_long
**Description:** Line is 138 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The system is **production-ready** and can be immediately deployed for real-time diversity analysis of any technical decision or codebase.`

### docs/PR_2_automated_security_checks.md:5

**Type:** line_too_long
**Description:** Line is 154 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This PR implements **comprehensive automated security checks** and **policy enforcement** to prevent future credential leaks and security vulnerabilities.`

### docs/PR_2_automated_security_checks.md:260

**Type:** line_too_long
**Description:** Line is 129 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🛡️ This PR establishes a robust security foundation that prevents credential leaks and enforces best practices automatically!**`

### docs/PR_17_Completion_Log.md:143

**Type:** line_too_long
**Description:** Line is 126 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `PR #17 successfully addressed the IDE performance issues and enhanced security detection. The comprehensive approach included:`

### docs/CI_CD_PIPELINE.md:5

**Type:** line_too_long
**Description:** Line is 170 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We've successfully set up a comprehensive CI/CD pipeline using Google Cloud Build that automatically builds, tests, and deploys the Ghostbusters API on every code change.`

### docs/CI_CD_PIPELINE.md:44

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `args: ['run', '--rm', 'gcr.io/$PROJECT_ID/ghostbusters-api:latest', 'python', '-c', 'print("Security scan passed")']`

### docs/CI_CD_PIPELINE.md:71

**Type:** line_too_long
**Description:** Line is 211 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `args: ['-X', 'POST', 'https://ghostbusters-api-container-1077539189076.us-central1.run.app/analyze', '-H', 'Content-Type: application/json', '-d', '{"project_path": ".", "agents": ["security", "code_quality"]}']`

### docs/CI_CD_PIPELINE.md:211

**Type:** line_too_long
**Description:** Line is 159 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The CI/CD pipeline is now fully operational and will automatically deploy the Ghostbusters API on every push to the`ghostbusters-gcp-implementation`branch! 🚀`

### docs/PHASE_2_IMPLEMENTATION_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 106 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**✅ Successfully completed Phase 2 of Ghostbusters GCP Cloud Functions migration with advanced features!**`

### docs/PHASE_2_IMPLEMENTATION_SUMMARY.md:165

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `st.markdown('<h1 class="main-header">👻 Ghostbusters Analytics Dashboard</h1>', unsafe_allow_html=True)`

### docs/PHASE_2_IMPLEMENTATION_SUMMARY.md:168

**Type:** line_too_long
**Description:** Line is 126 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `page = st.sidebar.selectbox("Choose a page", ["Overview", "My Analyses", "Analysis Details", "Real-time Updates", "Settings"])`

### docs/PHASE_2_IMPLEMENTATION_SUMMARY.md:321

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `curl -X POST https://us-central1-ghostbusters-project.cloudfunctions.net/ghostbusters-analyze-enhanced \`

### docs/GHOSTBUSTERS_CLOUD_EVALUATION.md:239

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Recommendation: Start with AWS Lambda for cost efficiency, then evaluate Google Cloud for performance if needed.**`

### docs/AST_LEVEL_UP_PROGRESS.md:9

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Capability**: Can interpret syntactically incorrect Python files using tokenization and semantic analysis`

### docs/MODEL_MANAGER_GUIDE.md:5

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `You're absolutely right about the risk of corrupting fragile JSON models! Every time we manually edit JSON files, we risk:`

### docs/MODEL_MANAGER_GUIDE.md:206

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The ModelManager ensures your fragile JSON models stay intact while allowing safe, programmatic manipulation!** 🛡️`

### clewcrew-framework/NEXT_STEPS_SPORE.md:7

**Type:** line_too_long
**Description:** Line is 176 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**clewcrew-framework** is the core framework package for the clewcrew hallucination detection system, providing foundational components for building robust, scalable workflows.`

### clewcrew-framework/NEXT_STEPS_SPORE.md:551

**Type:** line_too_long
**Description:** Line is 136 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This spore contains all the information needed to transform clewcrew-framework from a local package to a thriving open-source project.*`

### clewcrew-framework/README.md:5

**Type:** line_too_long
**Description:** Line is 240 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The clewcrew-framework provides the foundational components for building robust, scalable hallucination detection workflows. It includes workflow orchestration, state management, event handling, plugin systems, and configuration management.`

### clewcrew-framework/README.md:221

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- [clewcrew-recovery](https://github.com/clewcrew/clewcrew-recovery): Recovery engine implementations`

### healthcare-cdc/README.md:5

**Type:** line_too_long
**Description:** Line is 225 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This directory contains the complete Healthcare Change Data Capture (CDC) implementation based on the [Snowflake Healthcare CDC Quickstart](https://quickstarts.snowflake.com/guide/Streamline_Healthcare_CDC_DDB_And_Openflow/).`

### healthcare-cdc/README.md:81

**Type:** line_too_long
**Description:** Line is 136 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Source**: [Snowflake Healthcare CDC Quickstart](https://quickstarts.snowflake.com/guide/Streamline_Healthcare_CDC_DDB_And_Openflow/)`

### healthcare-cdc/docs/HEALTHCARE_CDC_README.md:5

**Type:** line_too_long
**Description:** Line is 373 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This implementation provides a complete **Change Data Capture (CDC) pipeline** for healthcare insurance claims processing, based on the [Snowflake Healthcare CDC Quickstart](https://quickstarts.snowflake.com/guide/Streamline_Healthcare_CDC_DDB_And_Openflow/). The system synchronizes healthcare claims data between Amazon DynamoDB and Snowflake using Openflow in real-time.`

### healthcare-cdc/docs/HEALTHCARE_CDC_README.md:246

**Type:** line_too_long
**Description:** Line is 191 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This implementation is based on the [Snowflake Healthcare CDC Quickstart](https://quickstarts.snowflake.com/guide/Streamline_Healthcare_CDC_DDB_And_Openflow/) with the following enhancements:`

### healthcare-cdc/docs/HEALTHCARE_CDC_README.md:260

**Type:** line_too_long
**Description:** Line is 124 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This software is proprietary and may not be disclosed to third parties without the express written consent of Snowflake Inc.`

### rules/ide_performance_optimization.md:4

**Type:** line_too_long
**Description:** Line is 134 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**When IDE performance issues are reported, immediately apply systematic performance optimization before attempting other solutions.**`

### rules/ide_performance_optimization.md:211

**Type:** line_too_long
**Description:** Line is 139 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Performance optimization is always faster than debugging complex issues. Apply these fixes first, then investigate if problems persist.**`

### clewcrew/README.md:7

**Type:** line_too_long
**Description:** Line is 136 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Not affiliated with any cartoon dogs, paranormal investigators, or 80s movie franchises — just here to keep the LLM output on the level.`

### clewcrew/README.md:13

**Type:** line_too_long
**Description:** Line is 272 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `clewcrew is a comprehensive portfolio of AI development tools designed to eliminate hallucinations, improve code quality, and provide enterprise-grade development capabilities. Each component is a standalone, installable package that can be used independently or together.`

### clewcrew/README.md:201

**Type:** line_too_long
**Description:** Line is 145 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We welcome contributions to any component in the clewcrew portfolio! Each component has its own repository with specific contribution guidelines.`

### clewcrew/PORTFOLIO.md:5

**Type:** line_too_long
**Description:** Line is 325 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `clewcrew is a comprehensive portfolio of AI development tools designed to eliminate hallucinations, improve code quality, and provide enterprise-grade development capabilities. The portfolio consists of 7 independent, installable packages that can be used individually or together to create powerful AI development workflows.`

### clewcrew/PORTFOLIO.md:267

**Type:** line_too_long
**Description:** Line is 281 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The clewcrew portfolio represents a comprehensive solution for AI development challenges, with a total commercial potential of $430M+. Each component is designed to be valuable independently while working seamlessly together to provide enterprise-grade AI development capabilities.`

### clewcrew/PORTFOLIO.md:269

**Type:** line_too_long
**Description:** Line is 178 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The portfolio is positioned to capture significant market share in the rapidly growing AI development tools market, with a focus on quality, security, and developer productivity.`

### clewcrew/PHASE_4_PRODUCTION_SPORE.md:226

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `kubectl set image deployment/clewcrew-core clewcrew-core=louspringer/clewcrew-core:$VERSION -n clewcrew-$ENVIRONMENT`

### clewcrew/PHASE_4_PRODUCTION_SPORE.md:906

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- [Production Deployment Guide](https://github.com/louspringer/clewcrew/blob/main/docs/PRODUCTION.md)`

### clewcrew/PHASE_4_PRODUCTION_SPORE.md:907

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- [Performance Optimization Guide](https://github.com/louspringer/clewcrew/blob/main/docs/PERFORMANCE.md)`

### clewcrew/PHASE_4_PRODUCTION_SPORE.md:930

**Type:** line_too_long
**Description:** Line is 174 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This spore represents the production phase of the clewcrew portfolio development, focusing on deploying to production, launching publicly, and achieving commercial success.*`

### clewcrew/PHASE_3_INTEGRATION_SPORE.md:148

**Type:** line_too_long
**Description:** Line is 138 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `for component in clewcrew-common clewcrew-framework clewcrew-core clewcrew-agents clewcrew-recovery clewcrew-validators clewcrew-tools; do`

### clewcrew/PHASE_3_INTEGRATION_SPORE.md:323

**Type:** line_too_long
**Description:** Line is 138 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `for component in clewcrew-common clewcrew-framework clewcrew-core clewcrew-agents clewcrew-recovery clewcrew-validators clewcrew-tools; do`

### clewcrew/PHASE_3_INTEGRATION_SPORE.md:709

**Type:** line_too_long
**Description:** Line is 138 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `for component in clewcrew-common clewcrew-framework clewcrew-core clewcrew-agents clewcrew-recovery clewcrew-validators clewcrew-tools; do`

### clewcrew/PHASE_3_INTEGRATION_SPORE.md:799

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- [Component Integration Guide](https://github.com/louspringer/clewcrew/blob/main/docs/INTEGRATION.md)`

### clewcrew/PHASE_3_INTEGRATION_SPORE.md:823

**Type:** line_too_long
**Description:** Line is 183 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This spore represents the integration phase of the clewcrew portfolio development, focusing on bringing all components together into a cohesive, tested, and production-ready system.*`

### clewcrew/PHASE_1_FOUNDATION_SPORE.md:433

**Type:** line_too_long
**Description:** Line is 183 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This spore represents the foundation phase of the clewcrew portfolio development, establishing the core infrastructure and shared components that will support all subsequent phases.*`

### clewcrew/PHASE_2_CORE_COMPONENTS_SPORE.md:830

**Type:** line_too_long
**Description:** Line is 193 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This spore represents the core components phase of the clewcrew portfolio development, focusing on building the essential components that provide the core functionality for the entire system.*`

### codeguard-common/README.md:7

**Type:** line_too_long
**Description:** Line is 136 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Not affiliated with any cartoon dogs, paranormal investigators, or 80s movie franchises — just here to keep the LLM output on the level.`

### codeguard-common/README.md:11

**Type:** line_too_long
**Description:** Line is 207 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `clewcrew-common is the foundational package that eliminates duplication across all clewcrew components. It provides standardized utilities for confidence scoring, logging, configuration management, and more.`

### clewcrew-recovery/README.md:5

**Type:** line_too_long
**Description:** Line is 256 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `clewcrew-recovery provides automated recovery engines for fixing various types of code issues including syntax errors, indentation problems, import issues, and type annotations. Each recovery engine specializes in resolving specific types of code problems.`

### clewcrew-recovery/README.md:81

**Type:** line_too_long
**Description:** Line is 106 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- [Recovery Engine Development Guide](https://github.com/louspringer/clewcrew-recovery#engine-development)`

### clewcrew-recovery/README.md:86

**Type:** line_too_long
**Description:** Line is 150 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `We welcome contributions! Please see our [Contributing Guide](https://github.com/louspringer/clewcrew-recovery/blob/main/CONTRIBUTING.md) for details.`

### src/model_driven_projection/COMPONENT_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 272 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The **Model-Driven Projection Component** has been successfully organized as a dedicated component within the OpenFlow Playground project. This component implements the radical vision of pure model-driven development where all artifacts are projected from a central model.`

### src/model_driven_projection/COMPONENT_SUMMARY.md:169

**Type:** line_too_long
**Description:** Line is 182 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The Model-Driven Projection Component has been successfully organized as a dedicated component with perfect functional equivalence, zero duplication, and complete test compatibility.`

### src/model_driven_projection/README.md:5

**Type:** line_too_long
**Description:** Line is 270 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The Model-Driven Projection Component implements the radical vision where **all artifacts are projected from a central model** rather than managed individually. This component achieves perfect functional equivalence with zero duplication and complete test compatibility.`

### src/model_driven_projection/README.md:250

**Type:** line_too_long
**Description:** Line is 259 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The Model-Driven Projection Component successfully implements the radical vision of **pure model-driven development**. All artifacts are now projected from a central model with perfect functional equivalence, zero duplication, and complete test compatibility.`

### src/model_driven_projection/TEST_EQUIVALENCE_REPORT.md:37

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Analysis**: The projected artifacts maintain perfect structural equivalence with the original files.`

### src/model_driven_projection/TEST_EQUIVALENCE_REPORT.md:70

**Type:** line_too_long
**Description:** Line is 175 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- Original: ['SnowflakeConfig', 'OpenFlowConfig', 'DeploymentStatus', 'SecurityManager', 'InputValidator', 'DeploymentManager', 'MonitoringDashboard', 'OpenFlowQuickstartApp']`

### src/model_driven_projection/TEST_EQUIVALENCE_REPORT.md:71

**Type:** line_too_long
**Description:** Line is 176 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- Projected: ['SnowflakeConfig', 'OpenFlowConfig', 'DeploymentStatus', 'SecurityManager', 'InputValidator', 'DeploymentManager', 'MonitoringDashboard', 'OpenFlowQuickstartApp']`

### src/model_driven_projection/TEST_EQUIVALENCE_REPORT.md:167

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `key_classes = ['OpenFlowQuickstartApp', 'SecurityManager', 'DeploymentManager', 'MonitoringDashboard']`

### src/model_driven_projection/TEST_EQUIVALENCE_REPORT.md:224

**Type:** line_too_long
**Description:** Line is 141 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The projected artifacts are functionally equivalent to the original artifacts and pass all the same tests without any modifications required.`

### src/model_driven_projection/projected_artifacts/TEST_SUMMARY.md:144

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**All test files are working correctly and provide comprehensive validation of the projected artifacts.**`

### src/secure_shell_service/README.md:5

**Type:** line_too_long
**Description:** Line is 196 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This service directly addresses the subprocess security vulnerabilities detected by Ghostbusters (197 security issues) by providing a secure, gRPC-based alternative to Python's`subprocess`calls.`

### src/secure_shell_service/README.md:262

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Fixes the exact "pernicious problem" of hanging shell commands and subprocess security vulnerabilities!** 🚀`

### gke-ai-microservices-hackathon/PROJECT_SETUP_TRACKING.md:281

**Type:** line_too_long
**Description:** Line is 126 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This tracking document ensures we're explicit about every API we enable and every cost we track for the 2025 hackathon!** 📝✅`

### gke-ai-microservices-hackathon/GKE_USE_CASE_DIAGRAMS.md:321

**Type:** line_too_long
**Description:** Line is 126 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `| **Multi-Agent Analysis** | Developer, AI Agents, Orchestrator | Pod Autoscaling, Service Discovery | Automated code review |`

### gke-ai-microservices-hackathon/GKE_USE_CASE_DIAGRAMS.md:322

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `| **Agent Orchestration** | Orchestrator, GKE Autoscaler | HPA, Load Balancing | Intelligent scaling |`

### gke-ai-microservices-hackathon/GKE_USE_CASE_DIAGRAMS.md:323

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `| **Quality Gates** | Quality System, GKE Deployment | Deployment Control, Monitoring | Quality enforcement |`

### gke-ai-microservices-hackathon/GKE_USE_CASE_DIAGRAMS.md:324

**Type:** line_too_long
**Description:** Line is 114 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `| **Real-time Monitoring** | Monitoring, Alerting, Team | Cloud Monitoring, Health Checks | Proactive operations |`

### gke-ai-microservices-hackathon/GKE_USE_CASE_DIAGRAMS.md:325

**Type:** line_too_long
**Description:** Line is 101 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `| **Error Recovery** | Error Detection, Recovery System | Pod Restart, Failover | High availability |`

### gke-ai-microservices-hackathon/GKE_USE_CASE_DIAGRAMS.md:326

**Type:** line_too_long
**Description:** Line is 112 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `| **Performance Tuning** | Performance Monitor, Optimization | Resource Scaling, Metrics | Optimal performance |`

### gke-ai-microservices-hackathon/GKE_USE_CASE_DIAGRAMS.md:344

**Type:** line_too_long
**Description:** Line is 201 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**These use case diagrams provide a comprehensive view of how our Ghostbusters AI Agent Microservices Platform will operate on GKE, demonstrating real-world value while showcasing GKE's capabilities.**`

### gke-ai-microservices-hackathon/GKE_NOTIFICATION_OPTIONS.md:5

**Type:** line_too_long
**Description:** Line is 119 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `GKE changes can trigger notifications through multiple channels. Here's a comprehensive guide to all available options:`

### gke-ai-microservices-hackathon/GKE_NOTIFICATION_OPTIONS.md:41

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `"filter": "resource.type=\"k8s_container\" AND resource.labels.cluster_name=\"ghostbusters-hackathon\"",`

### gke-ai-microservices-hackathon/MODEL_VERSION_TRACKING_SOLUTION.md:295

**Type:** line_too_long
**Description:** Line is 110 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**"The model is the authority. Scripts are generated artifacts. Version tracking ensures they stay in sync."**`

### gke-ai-microservices-hackathon/TEARDOWN_IMPLEMENTATION_COMPLETE.md:5

**Type:** line_too_long
**Description:** Line is 128 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Successfully implemented a comprehensive, model-driven teardown script for the Ghostbusters AI Hackathon 2025 GCP project!** 🚀`

### gke-ai-microservices-hackathon/TEARDOWN_IMPLEMENTATION_COMPLETE.md:161

**Type:** line_too_long
**Description:** Line is 155 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The teardown script implementation is complete and provides a robust, safe, and comprehensive way to clean up the hackathon project when it's finished.**`

### gke-ai-microservices-hackathon/TEARDOWN_IMPLEMENTATION_COMPLETE.md:176

**Type:** line_too_long
**Description:** Line is 154 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The Ghostbusters AI Hackathon 2025 now has a complete, professional-grade project management system with automated setup and teardown capabilities!** 🎉🚀`

### gke-ai-microservices-hackathon/README.md:8

**Type:** line_too_long
**Description:** Line is 108 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🌐 Devpost:** [GKE Turns 10 Hackathon](https://gketurns10.devpost.com/) *(Check for specific requirements)*`

### gke-ai-microservices-hackathon/README.md:12

**Type:** line_too_long
**Description:** Line is 154 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This repository contains our submission for the GKE Turns 10 Hackathon, showcasing AI agent microservices built with Kubernetes and Google Cloud Platform.`

### gke-ai-microservices-hackathon/README.md:14

**Type:** line_too_long
**Description:** Line is 114 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🏆 Key Goal:** Demonstrate next-generation microservices architecture with AI agents on Google Kubernetes Engine.`

### gke-ai-microservices-hackathon/README.md:205

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**⚠️ Note: Check the [GKE Devpost page](https://gketurns10.devpost.com/) for complete and up-to-date requirements.**`

### gke-ai-microservices-hackathon/DEPLOYMENT_READY_SUMMARY.md:14

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- ✅ **Namespace Structure** - Organized ghostbusters-ai, ghostbusters-ingress, ghostbusters-monitoring`

### gke-ai-microservices-hackathon/DEPLOYMENT_READY_SUMMARY.md:118

**Type:** line_too_long
**Description:** Line is 163 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `gcloud container clusters create ghostbusters-hackathon --zone=us-central1-a --machine-type=e2-micro --preemptible --enable-autoscaling --min-nodes=1 --max-nodes=3`

### gke-ai-microservices-hackathon/DEPLOYMENT_READY_SUMMARY.md:248

**Type:** line_too_long
**Description:** Line is 128 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**We have successfully created a complete, production-ready GKE infrastructure for the Ghostbusters AI microservices platform!**`

### gke-ai-microservices-hackathon/DEPLOYMENT_READY_SUMMARY.md:283

**Type:** line_too_long
**Description:** Line is 127 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The Ghostbusters AI microservices platform is ready for deployment! Let's build something amazing for the GKE hackathon!** 🏆🚀`

### gke-ai-microservices-hackathon/DEPLOYMENT_READY_SUMMARY.md:285

**Type:** line_too_long
**Description:** Line is 123 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**All design artifacts are complete, cost control is integrated, and we're ready to proceed with the actual deployment!** 💪`

### gke-ai-microservices-hackathon/GKE_COST_CONTROL_STRATEGY.md:426

**Type:** line_too_long
**Description:** Line is 182 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This cost control strategy ensures we can implement our GKE hackathon solution while maintaining strict cost control and integrating with our existing GCP cost monitoring system.**`

### gke-ai-microservices-hackathon/GKE_HACKATHON_ARCHITECTURAL_PLAN.md:70

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Primary Flow:** Load monitoring → Auto-scaling → Pod creation → Service registration → Traffic distribution`

### gke-ai-microservices-hackathon/GKE_HACKATHON_ARCHITECTURAL_PLAN.md:115

**Type:** line_too_long
**Description:** Line is 107 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Orchestrator --> Security[Security Agent<br/>Vulnerability Scanning<br/>HPA: 3-10 pods<br/>256Mi-512Mi RAM]`

### gke-ai-microservices-hackathon/GKE_HACKATHON_ARCHITECTURAL_PLAN.md:116

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Orchestrator --> Quality[Quality Agent<br/>Code Quality Analysis<br/>HPA: 3-10 pods<br/>256Mi-512Mi RAM]`

### gke-ai-microservices-hackathon/GKE_HACKATHON_ARCHITECTURAL_PLAN.md:118

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Orchestrator --> Perf[Performance Agent<br/>Performance Analysis<br/>HPA: 3-10 pods<br/>256Mi-512Mi RAM]`

### gke-ai-microservices-hackathon/GKE_HACKATHON_ARCHITECTURAL_PLAN.md:127

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Storage --> Monitoring[Cloud Monitoring<br/>GKE Metrics<br/>Performance Data<br/>Auto-scaling Triggers]`

### gke-ai-microservices-hackathon/GKE_HACKATHON_ARCHITECTURAL_PLAN.md:131

**Type:** line_too_long
**Description:** Line is 110 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Monitoring --> Dashboard[Quality Dashboard<br/>Results Visualization<br/>Quality Gates<br/>Deployment Control]`

### gke-ai-microservices-hackathon/GKE_HACKATHON_ARCHITECTURAL_PLAN.md:135

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Dashboard --> Production[Production Environment<br/>GKE Deployment<br/>Quality Gate Control<br/>Rollback Capability]`

### gke-ai-microservices-hackathon/GKE_HACKATHON_ARCHITECTURAL_PLAN.md:518

**Type:** line_too_long
**Description:** Line is 113 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Repository:** [nkllon/gke-ai-microservices-hackathon](https://github.com/nkllon/gke-ai-microservices-hackathon)`

### gke-ai-microservices-hackathon/GKE_HACKATHON_ARCHITECTURAL_PLAN.md:523

**Type:** line_too_long
**Description:** Line is 170 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This architectural plan demonstrates our understanding of GKE capabilities while leveraging our existing Ghostbusters framework for a compelling hackathon submission.**`

### gke-ai-microservices-hackathon/GKE_HACKATHON_ARCHITECTURAL_PLAN.md:525

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**We're ready for Google's guidance to ensure our approach is optimal for both the hackathon and showcasing GKE's capabilities!** 🚀`

### gke-ai-microservices-hackathon/GKE_WORKFLOW_MERMAID.md:27

**Type:** line_too_long
**Description:** Line is 107 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Parallel --> Security[Security Agent<br/>Vulnerability Scanning<br/>Security Analysis<br/>Threat Detection]`

### gke-ai-microservices-hackathon/GKE_WORKFLOW_MERMAID.md:28

**Type:** line_too_long
**Description:** Line is 113 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Parallel --> Quality[Quality Agent<br/>Code Style Analysis<br/>Complexity Assessment<br/>Maintainability Metrics]`

### gke-ai-microservices-hackathon/GKE_WORKFLOW_MERMAID.md:29

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Parallel --> Test[Test Agent<br/>Test Coverage Analysis<br/>Pattern Validation<br/>Quality Assessment]`

### gke-ai-microservices-hackathon/GKE_WORKFLOW_MERMAID.md:30

**Type:** line_too_long
**Description:** Line is 109 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Parallel --> Perf[Performance Agent<br/>Performance Analysis<br/>Resource Usage<br/>Optimization Suggestions]`

### gke-ai-microservices-hackathon/GKE_WORKFLOW_MERMAID.md:52

**Type:** line_too_long
**Description:** Line is 127 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Fail --> Report[Generate Quality Report<br/>Security Issues<br/>Quality Problems<br/>Test Coverage Gaps<br/>Performance Issues]`

### gke-ai-microservices-hackathon/DEPLOYMENT_STATE_TRACKING_SOLUTION.md:192

**Type:** line_too_long
**Description:** Line is 123 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `cat project_model_registry.json | jq '.domains.hackathon.hackathon_mapping.gke_turns_10.gcp_project_setup.deployment_state'`

### gke-ai-microservices-hackathon/GKE_ARCHITECTURE_MERMAID.md:23

**Type:** line_too_long
**Description:** Line is 107 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Orchestrator --> Security[Security Agent<br/>Vulnerability Scanning<br/>HPA: 3-10 pods<br/>256Mi-512Mi RAM]`

### gke-ai-microservices-hackathon/GKE_ARCHITECTURE_MERMAID.md:24

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Orchestrator --> Quality[Quality Agent<br/>Code Quality Analysis<br/>HPA: 3-10 pods<br/>256Mi-512Mi RAM]`

### gke-ai-microservices-hackathon/GKE_ARCHITECTURE_MERMAID.md:26

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Orchestrator --> Perf[Performance Agent<br/>Performance Analysis<br/>HPA: 3-10 pods<br/>256Mi-512Mi RAM]`

### gke-ai-microservices-hackathon/GKE_ARCHITECTURE_MERMAID.md:35

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Storage --> Monitoring[Cloud Monitoring<br/>GKE Metrics<br/>Performance Data<br/>Auto-scaling Triggers]`

### gke-ai-microservices-hackathon/GKE_ARCHITECTURE_MERMAID.md:39

**Type:** line_too_long
**Description:** Line is 110 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Monitoring --> Dashboard[Quality Dashboard<br/>Results Visualization<br/>Quality Gates<br/>Deployment Control]`

### gke-ai-microservices-hackathon/GKE_ARCHITECTURE_MERMAID.md:43

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Dashboard --> Production[Production Environment<br/>GKE Deployment<br/>Quality Gate Control<br/>Rollback Capability]`

### gke-ai-microservices-hackathon/IMPLEMENTATION_GUIDE.md:166

**Type:** line_too_long
**Description:** Line is 108 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `kubectl exec -n ghostbusters-ai deployment/ghostbusters-orchestrator -- curl -s http://localhost:8080/health`

### gke-ai-microservices-hackathon/IMPLEMENTATION_GUIDE.md:169

**Type:** line_too_long
**Description:** Line is 110 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `kubectl exec -n ghostbusters-ai deployment/ghostbusters-security-agent -- curl -s http://localhost:8080/health`

### gke-ai-microservices-hackathon/IMPLEMENTATION_GUIDE.md:459

**Type:** line_too_long
**Description:** Line is 170 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This implementation guide provides everything you need to deploy and manage the Ghostbusters AI microservices platform on GKE while maintaining strict cost control!** 🚀`

### gke-ai-microservices-hackathon/GKE_COST_CONTROL_INTEGRATION_SUMMARY.md:270

**Type:** line_too_long
**Description:** Line is 214 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Our GKE cost control system is fully integrated with the existing GCP cost control infrastructure. We can implement the GKE hackathon solution while maintaining strict cost control and staying within budget!** 🚀💰`

### gke-ai-microservices-hackathon/GKE_DEPLOYMENT_DEPENDENCIES.md:5

**Type:** line_too_long
**Description:** Line is 181 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This document outlines all the dependencies, tools, and configuration requirements needed to successfully deploy the Ghostbusters AI microservices to Google Kubernetes Engine (GKE).`

### gke-ai-microservices-hackathon/GKE_DEPLOYMENT_DEPENDENCIES.md:271

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- [Kubectl Troubleshooting](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-cluster/)`

### gke-ai-microservices-hackathon/GKE_DEPLOYMENT_DEPENDENCIES.md:310

**Type:** line_too_long
**Description:** Line is 120 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Once all dependencies are satisfied, you can proceed with the GKE deployment using the provided deployment script!** 🚀`

### gke-ai-microservices-hackathon/GOOGLE_MEETING_AGENDA.md:13

**Type:** line_too_long
**Description:** Line is 121 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Get Google's expert guidance on our GKE hackathon architecture to ensure optimal approach and maximize success potential.`

### gke-ai-microservices-hackathon/GOOGLE_MEETING_AGENDA.md:77

**Type:** line_too_long
**Description:** Line is 107 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Orchestrator --> Security[Security Agent<br/>Vulnerability Scanning<br/>HPA: 3-10 pods<br/>256Mi-512Mi RAM]`

### gke-ai-microservices-hackathon/GOOGLE_MEETING_AGENDA.md:78

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Orchestrator --> Quality[Quality Agent<br/>Code Quality Analysis<br/>HPA: 3-10 pods<br/>256Mi-512Mi RAM]`

### gke-ai-microservices-hackathon/GOOGLE_MEETING_AGENDA.md:80

**Type:** line_too_long
**Description:** Line is 104 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Orchestrator --> Perf[Performance Agent<br/>Performance Analysis<br/>HPA: 3-10 pods<br/>256Mi-512Mi RAM]`

### gke-ai-microservices-hackathon/GOOGLE_MEETING_AGENDA.md:89

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Storage --> Monitoring[Cloud Monitoring<br/>GKE Metrics<br/>Performance Data<br/>Auto-scaling Triggers]`

### gke-ai-microservices-hackathon/GOOGLE_MEETING_AGENDA.md:93

**Type:** line_too_long
**Description:** Line is 110 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Monitoring --> Dashboard[Quality Dashboard<br/>Results Visualization<br/>Quality Gates<br/>Deployment Control]`

### gke-ai-microservices-hackathon/GOOGLE_MEETING_AGENDA.md:97

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Dashboard --> Production[Production Environment<br/>GKE Deployment<br/>Quality Gate Control<br/>Rollback Capability]`

### gke-ai-microservices-hackathon/GOOGLE_MEETING_AGENDA.md:342

**Type:** line_too_long
**Description:** Line is 193 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**This meeting represents a unique opportunity to get Google's expert guidance on our GKE hackathon submission while building a relationship that could extend far beyond the hackathon itself.**`

### gke-ai-microservices-hackathon/GOOGLE_MEETING_AGENDA.md:344

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**We're excited to present our vision and get Google's input to make this the most compelling GKE submission possible!** 🚀`

### gke-ai-microservices-hackathon/PROJECT_SETUP_COMPLETE_SUMMARY.md:195

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The system is ready for execution and will create a clean, cost-controlled GCP environment specifically for the 2025 hackathon!**`

### gke-ai-microservices-hackathon/TEARDOWN_SCRIPT_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 270 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The **`teardown-gcp-project.sh`** script is a comprehensive cleanup tool that completely removes the Ghostbusters AI Hackathon 2025 GCP project and all associated resources. This script is the **inverse operation** of the setup script, ensuring complete project cleanup.`

### gke-ai-microservices-hackathon/TEARDOWN_SCRIPT_SUMMARY.md:253

**Type:** line_too_long
**Description:** Line is 173 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The **`teardown-gcp-project.sh`** script provides a **safe, comprehensive, and automated** way to completely clean up the Ghostbusters AI Hackathon 2025 project. It ensures:`

### gke-ai-microservices-hackathon/TEARDOWN_SCRIPT_SUMMARY.md:261

**Type:** line_too_long
**Description:** Line is 103 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Use this script responsibly and only when you're completely finished with the hackathon project!** 🚨💡`

### gke-ai-microservices-hackathon/MODEL_DRIVEN_SCRIPT_GENERATION_SUMMARY.md:86

**Type:** line_too_long
**Description:** Line is 139 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The template variable substitution is not handling bash array formatting correctly. The newline-separated string approach needs refinement.`

### gke-ai-microservices-hackathon/MODEL_DRIVEN_SCRIPT_GENERATION_SUMMARY.md:157

**Type:** line_too_long
**Description:** Line is 130 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**The model-driven approach is working!** The template processing just needs refinement to handle bash array formatting perfectly.`

### kiro-ai-development-hackathon/README.md:11

**Type:** line_too_long
**Description:** Line is 205 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This repository contains our submission for the Code with Kiro Hackathon, showcasing AI-powered development tools that enable spec-driven development with intelligent code generation and quality assurance.`

### kiro-ai-development-hackathon/README.md:13

**Type:** line_too_long
**Description:** Line is 172 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**⚠️ CRITICAL REQUIREMENT:** The`/.kiro`directory MUST be at the root of this project and MUST NOT be added to`.gitignore`- this is required for submission eligibility.`

### kiro-ai-development-hackathon/README.md:191

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Build tools that save time, reduce friction, or simplify everyday tasks for developers or anyone else.`

### kiro-ai-development-hackathon/README.md:197

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Build something that helps others learn with interactive tutorials and AI-enhanced learning platforms.`

### kiro-ai-development-hackathon/KIRO_HACKATHON_1_MONTH_PLAN.md:25

**Type:** line_too_long
**Description:** Line is 110 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Simple but effective demonstration of AI-powered development tools using Kiro for spec-driven development.**`

### kiro-ai-development-hackathon/KIRO_HACKATHON_1_MONTH_PLAN.md:88

**Type:** line_too_long
**Description:** Line is 117 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `"Hi, I'm showing you Ghostbusters AI Agent Development Framework integrated with Kiro for spec-driven development..."`

### kiro-ai-development-hackathon/KIRO_HACKATHON_1_MONTH_PLAN.md:279

**Type:** line_too_long
**Description:** Line is 102 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Remember: Simple spec-to-code with AI agents is better than complex, broken development platforms!**`

### clewcrew-tools/NEXT_STEPS_SPORE.md:7

**Type:** line_too_long
**Description:** Line is 206 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**clewcrew-tools** is the utility tools package for the clewcrew hallucination detection system, providing a comprehensive set of command-line utilities and tools for development, analysis, and integration.`

### clewcrew-tools/NEXT_STEPS_SPORE.md:711

**Type:** line_too_long
**Description:** Line is 152 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This spore contains all the information needed to transform clewcrew-tools from a local package to a thriving open-source development tools ecosystem.*`

### clewcrew-tools/README.md:5

**Type:** line_too_long
**Description:** Line is 239 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The clewcrew-tools package provides a comprehensive set of command-line utilities and tools for development, analysis, and integration. It includes code analysis, report generation, configuration management, and development workflow tools.`

### elmo-fuzzy-giggle/DEPLOYMENT_SUMMARY.md:5

**Type:** line_too_long
**Description:** Line is 221 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Successfully created the **elmo-fuzzy-giggle** project as a dedicated Ghostbusters deployment environment. This project provides a complete multi-agent delusion detection and recovery system using LangGraph orchestration.`

### elmo-fuzzy-giggle/DEPLOYMENT_SUMMARY.md:135

**Type:** line_too_long
**Description:** Line is 302 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The Ghostbusters deployment project **elmo-fuzzy-giggle** is complete and ready for production use. The system successfully detects delusions, validates findings, plans recovery actions, executes fixes, and validates results - all orchestrated through LangGraph for maximum reliability and scalability.`

### hackathon/README.md:5

**Type:** line_too_long
**Description:** Line is 235 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This directory contains all hackathon-related materials, coordination plans, and submission strategies for the OpenFlow Playground project. We're participating in three major hackathons to showcase our AI-powered development ecosystem.`

### hackathon/README.md:139

**Type:** line_too_long
**Description:** Line is 113 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This hackathon coordination directory is your central hub for all hackathon-related activities and materials.* 🚀`

### hackathon/HACKATHON_STATUS.md:214

**Type:** line_too_long
**Description:** Line is 139 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This status dashboard provides real-time visibility into our hackathon progress and helps coordinate efforts across all three contests.* 📊`

### hackathon/code_with_kiro/KIRO_IDE_EXPLORATION_PLAN.md:5

**Type:** line_too_long
**Description:** Line is 186 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Now that we have **Kiro IDE access**, this document outlines our exploration strategy to understand the platform's capabilities and plan our integration for the Code with Kiro Hackathon.`

### hackathon/code_with_kiro/KIRO_IDE_EXPLORATION_PLAN.md:270

**Type:** line_too_long
**Description:** Line is 173 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `*This exploration plan will guide our understanding of Kiro IDE and enable us to create a compelling hackathon submission showcasing our AI-powered development ecosystem.* 🚀`

### project_management/PROJECT_MANAGEMENT_IMPLEMENTATION_PLAN.md:4

**Type:** line_too_long
**Description:** Line is 236 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This plan outlines the implementation of the new`project_management_design`domain, which provides unified project oversight, systematic design methodologies, and cross-domain workflow orchestration for the OpenFlow Playground project.`

### project_management/README.md:4

**Type:** line_too_long
**Description:** Line is 176 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The Project Management & Design domain provides unified oversight, systematic design methodologies, and cross-domain workflow orchestration for the OpenFlow Playground project.`

### clewcrew-common/README.md:7

**Type:** line_too_long
**Description:** Line is 136 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Not affiliated with any cartoon dogs, paranormal investigators, or 80s movie franchises — just here to keep the LLM output on the level.`

### clewcrew-common/README.md:11

**Type:** line_too_long
**Description:** Line is 207 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `clewcrew-common is the foundational package that eliminates duplication across all clewcrew components. It provides standardized utilities for confidence scoring, logging, configuration management, and more.`

### tidb-agentx-hackathon/TIDB_HACKATHON_1_MONTH_PLAN.md:25

**Type:** line_too_long
**Description:** Line is 107 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**Simple but effective demonstration of multi-step AI agents using TiDB Serverless for real-world impact.**`

### tidb-agentx-hackathon/TIDB_HACKATHON_1_MONTH_PLAN.md:89

**Type:** line_too_long
**Description:** Line is 110 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `"Hi, I'm showing you Ghostbusters Multi-Step AI Agent Platform using TiDB Serverless for real-world impact..."`

### tidb-agentx-hackathon/README.md:12

**Type:** line_too_long
**Description:** Line is 155 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This repository contains our submission for the TiDB AgentX Hackathon 2025, showcasing multi-agent AI workflows with TiDB Serverless for real-world impact.`

### tidb-agentx-hackathon/README.md:14

**Type:** line_too_long
**Description:** Line is 108 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**🏆 Key Goal:** Build multi-step AI agents that demonstrate real-world workflows, not just simple RAG demos.`

### .kiro/specs/ghostbusters-pydantic-fix/design.md:5

**Type:** line_too_long
**Description:** Line is 364 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The Ghostbusters pydantic compatibility issue stems from the transition between pydantic v1 and v2, combined with LangChain's recent migration to pydantic v2 (as of langchain-core 0.3.0). The current implementation uses Python dataclasses for data models, but LangGraph and LangChain expect pydantic BaseModel objects for proper serialization and state management.`

### .kiro/specs/ghostbusters-pydantic-fix/design.md:7

**Type:** line_too_long
**Description:** Line is 162 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The solution involves migrating from dataclasses to pydantic v2 BaseModel classes while ensuring compatibility with LangChain/LangGraph's state management system.`

### .kiro/specs/ghostbusters-pydantic-fix/tasks.md:68

**Type:** line_too_long
**Description:** Line is 118 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- Update SecurityValidator, CodeQualityValidator, TestValidator, BuildValidator, ArchitectureValidator, ModelValidator`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:5

**Type:** line_too_long
**Description:** Line is 484 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `The Ghostbusters multi-agent delusion detection and recovery system currently has pydantic compatibility issues that prevent the full test suite from running. The system uses LangChain/LangGraph for multi-agent orchestration, but there are version conflicts between pydantic v2.0+ (used in the project) and langchain-core dependencies. This creates import errors and prevents proper testing of the Ghostbusters functionality, which is critical for the project's model-driven approach.`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:11

**Type:** line_too_long
**Description:** Line is 194 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**User Story:** As a developer, I want the Ghostbusters test suite to run without pydantic compatibility errors, so that I can validate the multi-agent delusion detection system works correctly.`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:15

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. WHEN running`pytest tests/test_ghostbusters.py`THEN the system SHALL execute all tests without pydantic import errors`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:16

**Type:** line_too_long
**Description:** Line is 154 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `2. WHEN importing Ghostbusters components THEN the system SHALL successfully import all agents, validators, and recovery engines without version conflicts`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:17

**Type:** line_too_long
**Description:** Line is 125 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `3. WHEN running the full test suite THEN the system SHALL achieve >90% success rate for Ghostbusters tests (currently at 50%)`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:21

**Type:** line_too_long
**Description:** Line is 154 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**User Story:** As a developer, I want LangChain/LangGraph integration to work with pydantic v2, so that the multi-agent orchestration functions properly.`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:25

**Type:** line_too_long
**Description:** Line is 131 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. WHEN initializing GhostbustersOrchestrator THEN the system SHALL create LangGraph workflow without pydantic compatibility errors`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:26

**Type:** line_too_long
**Description:** Line is 125 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `2. WHEN running agent detection THEN the system SHALL properly serialize/deserialize DelusionResult objects using pydantic v2`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:27

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `3. WHEN executing the workflow THEN the system SHALL maintain state consistency across all workflow nodes`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:31

**Type:** line_too_long
**Description:** Line is 154 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**User Story:** As a developer, I want proper data models for Ghostbusters components, so that type safety and validation work correctly with pydantic v2.`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:35

**Type:** line_too_long
**Description:** Line is 106 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. WHEN defining DelusionResult models THEN the system SHALL use pydantic v2 BaseModel syntax and features`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:36

**Type:** line_too_long
**Description:** Line is 117 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `2. WHEN validating agent results THEN the system SHALL properly validate data structures using pydantic v2 validators`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:37

**Type:** line_too_long
**Description:** Line is 115 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `3. WHEN serializing workflow state THEN the system SHALL handle GhostbustersState serialization without type errors`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:41

**Type:** line_too_long
**Description:** Line is 123 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**User Story:** As a developer, I want dependency version resolution, so that all packages work together without conflicts.`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:45

**Type:** line_too_long
**Description:** Line is 116 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. WHEN installing dependencies THEN the system SHALL resolve langchain-core and pydantic versions without conflicts`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:46

**Type:** line_too_long
**Description:** Line is 115 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `2. WHEN running UV sync THEN the system SHALL install compatible versions of all multi-agent framework dependencies`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:47

**Type:** line_too_long
**Description:** Line is 122 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `3. WHEN importing both pydantic and langchain THEN the system SHALL use compatible versions that don't cause import errors`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:51

**Type:** line_too_long
**Description:** Line is 136 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `**User Story:** As a developer, I want the disabled test file to be re-enabled, so that comprehensive Ghostbusters testing is available.`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:55

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. WHEN fixing pydantic compatibility THEN the system SHALL re-enable tests/test_ghostbusters.py.disabled`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:56

**Type:** line_too_long
**Description:** Line is 136 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `2. WHEN running comprehensive tests THEN the system SHALL execute both the current simplified tests and the comprehensive disabled tests`

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md:57

**Type:** line_too_long
**Description:** Line is 107 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `3. WHEN validating test coverage THEN the system SHALL achieve full coverage of all Ghostbusters components`

### subprojects/README.md:4

**Type:** line_too_long
**Description:** Line is 184 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This directory manages three separate GitHub projects created for hackathon submissions, each leveraging components from the parent OpenFlow-Playground project as packages or services.`

### subprojects/README.md:16

**Type:** line_too_long
**Description:** Line is 111 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Repository**: [kiro-ai-development-hackathon](https://github.com/louspringer/kiro-ai-development-hackathon)`

### subprojects/README.md:23

**Type:** line_too_long
**Description:** Line is 113 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Repository**: [gke-ai-microservices-hackathon](https://github.com/louspringer/gke-ai-microservices-hackathon)`

### subprojects/kiro-ai-development-hackathon.md:4

**Type:** line_too_long
**Description:** Line is 111 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Repository**: [kiro-ai-development-hackathon](https://github.com/louspringer/kiro-ai-development-hackathon)`

### subprojects/gke-ai-microservices-hackathon.md:4

**Type:** line_too_long
**Description:** Line is 113 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Repository**: [gke-ai-microservices-hackathon](https://github.com/louspringer/gke-ai-microservices-hackathon)`

### subprojects/COMPONENT_DISTRIBUTION_STRATEGY.md:4

**Type:** line_too_long
**Description:** Line is 179 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This document outlines the strategy for distributing components from the parent OpenFlow-Playground project to the three hackathon subprojects as packages, services, or templates.`

### subprojects/tidb-agentx-hackathon/README.md:13

**Type:** line_too_long
**Description:** Line is 256 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `This project demonstrates a comprehensive AI-powered multi-agent testing system integrated with TiDB Serverless for vector search and data management. The system showcases real-world AI agent workflows with automated testing, validation, and orchestration.`

### subprojects/tidb-agentx-hackathon/README.md:258

**Type:** line_too_long
**Description:** Line is 105 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `- **Discussions**: [GitHub Discussions](https://github.com/louspringer/tidb-agentx-hackathon/discussions)`

### prompts/gemini_2_5_preview_pr_review_actual.md:4

**Type:** line_too_long
**Description:** Line is 192 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `You are reviewing PR #9 for the OpenFlow Playground project. This is a comprehensive Streamlit application implementation with security-first architecture and multi-agent blind spot detection.`

### prompts/gemini_2_5_preview_pr_review_actual.md:72

**Type:** line_too_long
**Description:** Line is 118 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **Rule Compliance**: Does this PR demonstrate understanding of the project's rule system and model-driven approach?`

### prompts/gemini_2_5_preview_pr_review_actual.md:116

**Type:** line_too_long
**Description:** Line is 148 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Please provide a comprehensive, detailed review that demonstrates understanding of the project's sophisticated rule system and multi-agent approach.`

### prompts/gemini_2_5_preview_pr_review.md:4

**Type:** line_too_long
**Description:** Line is 192 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `You are reviewing PR #9 for the OpenFlow Playground project. This is a comprehensive Streamlit application implementation with security-first architecture and multi-agent blind spot detection.`

### prompts/gemini_2_5_preview_pr_review.md:72

**Type:** line_too_long
**Description:** Line is 118 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **Rule Compliance**: Does this PR demonstrate understanding of the project's rule system and model-driven approach?`

### prompts/gemini_2_5_preview_pr_review.md:116

**Type:** line_too_long
**Description:** Line is 148 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Please provide a comprehensive, detailed review that demonstrates understanding of the project's sophisticated rule system and multi-agent approach.`

### prompts/gemini_2_5_flash_lite_pr_review.md:4

**Type:** line_too_long
**Description:** Line is 192 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `You are reviewing PR #9 for the OpenFlow Playground project. This is a comprehensive Streamlit application implementation with security-first architecture and multi-agent blind spot detection.`

### prompts/gemini_2_5_flash_lite_pr_review.md:72

**Type:** line_too_long
**Description:** Line is 118 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `1. **Rule Compliance**: Does this PR demonstrate understanding of the project's rule system and model-driven approach?`

### prompts/gemini_2_5_flash_lite_pr_review.md:116

**Type:** line_too_long
**Description:** Line is 148 characters long (max 100)
**Suggestion:** Break long line for better readability
**Context:** `Please provide a comprehensive, detailed review that demonstrates understanding of the project's sophisticated rule system and multi-agent approach.`

## 📁 File-by-File Analysis

### .github/workflows/copilot-validation.yml

- **Type:** yaml
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### .github/workflows/quality-gates.yml

- **Type:** yaml
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### .kiro/specs/ghostbusters-pydantic-fix/design.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### .kiro/specs/ghostbusters-pydantic-fix/requirements.md

- **Type:** markdown
- **Issues:** 21 (Critical: 0, Warnings: 0, Suggestions: 21)
- **One-liner Score:** 0.00%

### .kiro/specs/ghostbusters-pydantic-fix/tasks.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### CLOUDBUILD_GITHUB_FINAL_DIAGNOSTIC.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 1, Suggestions: 4)
- **One-liner Score:** 1.96%

### CLOUDBUILD_GITHUB_LLM_WRAPPER.md

- **Type:** markdown
- **Issues:** 11 (Critical: 0, Warnings: 0, Suggestions: 11)
- **One-liner Score:** 0.61%

### CLOUDBUILD_GITHUB_PROBLEM_SPORE.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### CODE_QUALITY_AUTOMATION_PLAN.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### COMPLETE_QUALITY_SYSTEM_ARCHITECTURE.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### COMPREHENSIVE_ARTIFACT_ANALYSIS_PROGRESS_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### COMPREHENSIVE_ARTIFACT_ANALYSIS_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### COMPREHENSIVE_PROJECT_AUDIT_SUMMARY.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### CURRENT_STATE_SUMMARY.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### DEMO_FOCUSED_ARCHITECTURE_SUMMARY.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### DIVERSITY_HYPOTHESIS_CARD.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### ENHANCED_ROUND_TRIP_SUCCESS.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### EXTRACTION_ACTION_PLAN.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### GHOSTBUSTERS_ANALYSIS_REQUEST.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### GITHUB_CLOUD_BUILD_SETUP.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 1.47%

### HACKATHON_COORDINATION_PLAN.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### HACKATHON_GOOGLE_MEETING_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### LLM_IDENTITY_CRISIS_RESEARCH_MODEL.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### MASTER_PR_LOG.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### MEMORY_MANIFEST.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### NOTES.md

- **Type:** markdown
- **Issues:** 8 (Critical: 0, Warnings: 0, Suggestions: 8)
- **One-liner Score:** 0.00%

### ONE_LINER_LINTER_DOCUMENTATION.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 1, Suggestions: 3)
- **One-liner Score:** 2.61%

### PHASE_3_IMPLEMENTATION_PLAN.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### PHASE_3_INTEGRATION_TESTING_PLAN.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### PHASE_3_READY_TO_START_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### PHASE_4_OPTIMIZATION_SCALING_PLAN.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### PORTFOLIO_REQUIREMENTS_MAP.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### PRE_COMMIT_CLEANUP_SUMMARY.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### PROJECT_MANAGEMENT_DOMAIN_ADDITION_SUMMARY.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### PR_DESCRIPTION.md

- **Type:** markdown
- **Issues:** 7 (Critical: 0, Warnings: 0, Suggestions: 7)
- **One-liner Score:** 0.00%

### PR_LOG.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### QUALITY_SYSTEM_PHASE_1_2_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 1, Suggestions: 1)
- **One-liner Score:** 0.00%

### QUICKSTART.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### README.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### ROUND_TRIP_MODEL_SYSTEM_NOTES.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### SECURITY_AND_QUALITY_IMPROVEMENTS.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### TASK_3_2_CICD_INTEGRATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 7 (Critical: 0, Warnings: 0, Suggestions: 7)
- **One-liner Score:** 0.00%

### TEST_RESULTS_NOTES.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### TEST_RESULTS_SUMMARY.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### VISUALIZATION_SYSTEM_STATUS.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### backup/ghostbusters/ghostbusters/agents.py

- **Type:** python
- **Issues:** 5 (Critical: 0, Warnings: 5, Suggestions: 0)
- **One-liner Score:** 0.00%

### backup/ghostbusters/ghostbusters/agents/code_quality_expert.py

- **Type:** python
- **Issues:** 7 (Critical: 0, Warnings: 7, Suggestions: 0)
- **One-liner Score:** 0.00%

### backup/ghostbusters/ghostbusters/enhanced_learning_timeout_agent.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### backup/ghostbusters/ghostbusters/ghostbusters_orchestrator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### backup/ghostbusters/ghostbusters/web_tool_discovery.py

- **Type:** python
- **Issues:** 5 (Critical: 0, Warnings: 5, Suggestions: 0)
- **One-liner Score:** 0.00%

### call_ghostbusters.py

- **Type:** python
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### clewcrew-agents/README.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### clewcrew-agents/src/clewcrew_agents/code_quality_expert.py

- **Type:** python
- **Issues:** 5 (Critical: 0, Warnings: 5, Suggestions: 0)
- **One-liner Score:** 0.00%

### clewcrew-agents/src/clewcrew_agents/devops_expert.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### clewcrew-agents/src/clewcrew_agents/model_expert.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### clewcrew-agents/src/clewcrew_agents/security_expert.py

- **Type:** python
- **Issues:** 4 (Critical: 0, Warnings: 4, Suggestions: 0)
- **One-liner Score:** 0.00%

### clewcrew-common/README.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### clewcrew-common/src/clewcrew_common/confidence.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### clewcrew-core/README.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### clewcrew-core/src/clewcrew_core/orchestrator.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### clewcrew-framework/NEXT_STEPS_SPORE.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### clewcrew-framework/README.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### clewcrew-framework/src/clewcrew_framework/cli.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### clewcrew-recovery/README.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### clewcrew-recovery/src/clewcrew_recovery/**init**.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### clewcrew-tools/NEXT_STEPS_SPORE.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### clewcrew-tools/README.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### clewcrew-validators/NEXT_STEPS_SPORE.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### clewcrew-validators/README.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### clewcrew-validators/src/clewcrew_validators/**init**.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### clewcrew-validators/src/clewcrew_validators/data_validator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### clewcrew/PHASE_1_FOUNDATION_SPORE.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.35%

### clewcrew/PHASE_2_CORE_COMPONENTS_SPORE.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### clewcrew/PHASE_3_INTEGRATION_SPORE.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### clewcrew/PHASE_4_PRODUCTION_SPORE.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### clewcrew/PORTFOLIO.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### clewcrew/README.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### cloudbuild.yaml

- **Type:** yaml
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### cloudbuild_github_1stgen.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### cloudbuild_github_2ndgen_trigger.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### cloudbuild_github_rest_api.py

- **Type:** python
- **Issues:** 4 (Critical: 0, Warnings: 4, Suggestions: 0)
- **One-liner Score:** 0.00%

### cloudbuild_webhook_trigger.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### codeguard-common/README.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### comprehensive_artifact_analysis.py

- **Type:** python
- **Issues:** 5 (Critical: 0, Warnings: 5, Suggestions: 0)
- **One-liner Score:** 0.00%

### config/Openflow-Playground.yaml

- **Type:** yaml
- **Issues:** 24 (Critical: 13, Warnings: 11, Suggestions: 0)
- **One-liner Score:** 0.00%

### create_notebook.py

- **Type:** python
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### data/cost_analysis.py

- **Type:** python
- **Issues:** 20 (Critical: 1, Warnings: 19, Suggestions: 0)
- **One-liner Score:** 0.00%

### data/diversity_analysis_report.md

- **Type:** markdown
- **Issues:** 74 (Critical: 0, Warnings: 0, Suggestions: 74)
- **One-liner Score:** 0.00%

### docs/ARTIFACTFORGE_ISSUES_LOG.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/AST_LEVEL_UP_PLAN.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### docs/AST_LEVEL_UP_PROGRESS.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### docs/BRANCH_PUSH_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/BRANCH_SEPARATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 1, Suggestions: 4)
- **One-liner Score:** 0.00%

### docs/CALL_MORE_GHOSTBUSTERS_RULE.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### docs/CI_CD_PIPELINE.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### docs/COMPREHENSIVE_TEST_RESULTS.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### docs/CONFLICT_RESOLUTION_SUMMARY.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### docs/DIVERSITY_HYPOTHESIS_ORGANIZATION.md

- **Type:** markdown
- **Issues:** 6 (Critical: 0, Warnings: 0, Suggestions: 6)
- **One-liner Score:** 0.00%

### docs/DIVERSITY_HYPOTHESIS_SUMMARY.md

- **Type:** markdown
- **Issues:** 6 (Critical: 0, Warnings: 0, Suggestions: 6)
- **One-liner Score:** 0.00%

### docs/DOCUMENTATION_INDEX.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### docs/ENHANCED_AST_LEVEL_UP_SUMMARY.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### docs/GCP_VS_AWS_IMPLEMENTATION_COMPARISON.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### docs/GHOSTBUSTERS_ANALYSIS_RESPONSE.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/GHOSTBUSTERS_CLOUD_EVALUATION.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### docs/GHOSTBUSTERS_GCP_IMPLEMENTATION_PLAN.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### docs/GITHUB_COPILOT_CODE_REVIEW_ANALYSIS.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### docs/GITHUB_COPILOT_IMPLEMENTATION_PLAN.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 1, Suggestions: 3)
- **One-liner Score:** 0.30%

### docs/GITHUB_MCP_ANALYSIS.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### docs/GITHUB_MCP_INTEGRATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### docs/GIT_ENHANCED_AST_LEVEL_UP.md

- **Type:** markdown
- **Issues:** 6 (Critical: 0, Warnings: 1, Suggestions: 5)
- **One-liner Score:** 0.00%

### docs/GIT_WORKFLOW_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/HEALTHCARE_CDC_IMPLEMENTATION_PLAN.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/HEURISTIC_VS_DETERMINISTIC_PRINCIPLE.md

- **Type:** markdown
- **Issues:** 9 (Critical: 0, Warnings: 0, Suggestions: 9)
- **One-liner Score:** 0.00%

### docs/IMPLEMENTATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### docs/INTELLIGENT_LINTER_SYSTEM_SUMMARY.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 2, Suggestions: 3)
- **One-liner Score:** 0.00%

### docs/LANGCHAIN_MIGRATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/LEVEL1_IMPLEMENTATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### docs/MAKE_ONLY_ENFORCEMENT_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/MODEL_DRIVEN_CONFIGURATION_ANALYSIS.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### docs/MODEL_DRIVEN_PROJECTION_COMPONENT_COMPLETE.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### docs/MODEL_MANAGER_GUIDE.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/ORGANIZATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### docs/PHASE_1_IMPLEMENTATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### docs/PHASE_2_COMPLETION_SUMMARY.md

- **Type:** markdown
- **Issues:** 6 (Critical: 0, Warnings: 0, Suggestions: 6)
- **One-liner Score:** 0.00%

### docs/PHASE_2_IMPLEMENTATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### docs/PHASE_3_IMPLEMENTATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### docs/PLATFORM_COMPATIBILITY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/PR_10_PYTHON_TEST_FIXES.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### docs/PR_17_Completion_Log.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### docs/PR_1_COMPREHENSIVE_IMPLEMENTATION_PLAN.md

- **Type:** markdown
- **Issues:** 7 (Critical: 0, Warnings: 0, Suggestions: 7)
- **One-liner Score:** 0.00%

### docs/PR_1_security_cleanup.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 1.01%

### docs/PR_2_automated_security_checks.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 1, Suggestions: 2)
- **One-liner Score:** 0.61%

### docs/PR_3_model_driven_orchestration.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/PR_4_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md

- **Type:** markdown
- **Issues:** 9 (Critical: 0, Warnings: 0, Suggestions: 9)
- **One-liner Score:** 0.00%

### docs/PR_4_cursor_rules.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### docs/PR_5_model_persistence.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### docs/PR_6_healthcare_cdc_implementation.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### docs/PR_7_diversity_hypothesis_proven.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### docs/PR_8_diversity_hypothesis_applied_to_pr1.md

- **Type:** markdown
- **Issues:** 8 (Critical: 0, Warnings: 0, Suggestions: 8)
- **One-liner Score:** 0.00%

### docs/PR_9_OPENFLOW_STREAMLIT_APP_IMPLEMENTATION.md

- **Type:** markdown
- **Issues:** 9 (Critical: 0, Warnings: 0, Suggestions: 9)
- **One-liner Score:** 0.00%

### docs/PR_CREATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/README.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### docs/REAL_GHOSTBUSTERS_SUCCESS.md

- **Type:** markdown
- **Issues:** 8 (Critical: 0, Warnings: 0, Suggestions: 8)
- **One-liner Score:** 0.00%

### docs/SECURITY_FIXES.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/SECURITY_SUMMARY.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### docs/SYNTAX_FIX_SUMMARY.md

- **Type:** markdown
- **Issues:** 8 (Critical: 0, Warnings: 0, Suggestions: 8)
- **One-liner Score:** 0.00%

### docs/TEST_ALL_FIX_COMPLETE_SUMMARY.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### docs/TEST_ALL_FIX_SUMMARY.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### docs/TEST_EXECUTION_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/level1_bridge_analysis.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### docs/pr1_diversity_vs_copilot_comparison.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### docs/pr1_healthcare_cdc_context.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### docs/prioritized_implementation_plan.md

- **Type:** markdown
- **Issues:** 13 (Critical: 0, Warnings: 0, Suggestions: 13)
- **One-liner Score:** 0.00%

### elmo-fuzzy-giggle/DEPLOYMENT_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### elmo-fuzzy-giggle/Dockerfile

- **Type:** generic
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 5.00%

### elmo-fuzzy-giggle/cloudbuild.yaml

- **Type:** yaml
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### elmo-fuzzy-giggle/src/code_generator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### elmo-fuzzy-giggle/src/gemini_billing_analyzer.py

- **Type:** python
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### elmo-fuzzy-giggle/src/gemini_billing_analyzer_enhanced.py

- **Type:** python
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### elmo-fuzzy-giggle/src/generate_billing_analyzer.py

- **Type:** python
- **Issues:** 14 (Critical: 0, Warnings: 14, Suggestions: 0)
- **One-liner Score:** 0.00%

### elmo-fuzzy-giggle/src/recursive_code_generator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### fix_remaining_smoke_tests.py

- **Type:** python
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### ghostbusters_diversity_analysis.py

- **Type:** python
- **Issues:** 4 (Critical: 0, Warnings: 4, Suggestions: 0)
- **One-liner Score:** 0.00%

### ghostbusters_diversity_insights.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/DEPLOYMENT_READY_SUMMARY.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/DEPLOYMENT_STATE_TRACKING_SOLUTION.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.51%

### gke-ai-microservices-hackathon/GKE_ARCHITECTURE_MERMAID.md

- **Type:** markdown
- **Issues:** 6 (Critical: 0, Warnings: 0, Suggestions: 6)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/GKE_COST_CONTROL_INTEGRATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.59%

### gke-ai-microservices-hackathon/GKE_COST_CONTROL_STRATEGY.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/GKE_DEPLOYMENT_DEPENDENCIES.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/GKE_HACKATHON_ARCHITECTURAL_PLAN.md

- **Type:** markdown
- **Issues:** 10 (Critical: 0, Warnings: 0, Suggestions: 10)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/GKE_NOTIFICATION_OPTIONS.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/GKE_USE_CASE_DIAGRAMS.md

- **Type:** markdown
- **Issues:** 7 (Critical: 0, Warnings: 0, Suggestions: 7)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/GKE_WORKFLOW_MERMAID.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/GOOGLE_MEETING_AGENDA.md

- **Type:** markdown
- **Issues:** 9 (Critical: 0, Warnings: 0, Suggestions: 9)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/IMPLEMENTATION_GUIDE.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.77%

### gke-ai-microservices-hackathon/MODEL_DRIVEN_SCRIPT_GENERATION_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/MODEL_VERSION_TRACKING_SOLUTION.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/PROJECT_SETUP_COMPLETE_SUMMARY.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/PROJECT_SETUP_TRACKING.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.59%

### gke-ai-microservices-hackathon/README.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/TEARDOWN_IMPLEMENTATION_COMPLETE.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/TEARDOWN_SCRIPT_SUMMARY.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/gke_cost_monitor.py

- **Type:** python
- **Issues:** 10 (Critical: 0, Warnings: 10, Suggestions: 0)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters-generated.sh

- **Type:** shell
- **Issues:** 31 (Critical: 1, Warnings: 30, Suggestions: 0)
- **One-liner Score:** 0.42%

### gke-ai-microservices-hackathon/scripts/deploy-ghostbusters.sh

- **Type:** shell
- **Issues:** 31 (Critical: 1, Warnings: 30, Suggestions: 0)
- **One-liner Score:** 0.42%

### gke-ai-microservices-hackathon/scripts/generate-deploy-script.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/scripts/generate-setup-script.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/scripts/setup-gcp-project-generated.sh

- **Type:** shell
- **Issues:** 37 (Critical: 2, Warnings: 35, Suggestions: 0)
- **One-liner Score:** 1.09%

### gke-ai-microservices-hackathon/scripts/setup-gcp-project.sh

- **Type:** shell
- **Issues:** 37 (Critical: 2, Warnings: 35, Suggestions: 0)
- **One-liner Score:** 1.09%

### gke-ai-microservices-hackathon/scripts/setup-gke-notifications.py

- **Type:** python
- **Issues:** 7 (Critical: 0, Warnings: 7, Suggestions: 0)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/scripts/teardown-gcp-project.sh

- **Type:** shell
- **Issues:** 54 (Critical: 6, Warnings: 48, Suggestions: 0)
- **One-liner Score:** 2.93%

### gke-ai-microservices-hackathon/scripts/test-array-equivalence.sh

- **Type:** shell
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### gke-ai-microservices-hackathon/scripts/update-deployment-state.py

- **Type:** python
- **Issues:** 4 (Critical: 0, Warnings: 4, Suggestions: 0)
- **One-liner Score:** 0.88%

### hackathon/HACKATHON_STATUS.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### hackathon/README.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### hackathon/code_with_kiro/KIRO_IDE_EXPLORATION_PLAN.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### healthcare-cdc/README.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### healthcare-cdc/**init**.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### healthcare-cdc/docs/HEALTHCARE_CDC_README.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### healthcare-cdc/healthcare_cdc_domain_model.py

- **Type:** python
- **Issues:** 4 (Critical: 0, Warnings: 4, Suggestions: 0)
- **One-liner Score:** 0.00%

### healthcare-cdc/models/healthcare-cdc-infrastructure.yaml

- **Type:** yaml
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### kiro-ai-development-hackathon/KIRO_HACKATHON_1_MONTH_PLAN.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### kiro-ai-development-hackathon/README.md

- **Type:** markdown
- **Issues:** 4 (Critical: 0, Warnings: 0, Suggestions: 4)
- **One-liner Score:** 0.00%

### project_management/PROJECT_MANAGEMENT_IMPLEMENTATION_PLAN.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### project_management/README.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### projected_verify_ide_linting_hypothesis.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### prompts/gemini_2_5_flash_lite_pr_review.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### prompts/gemini_2_5_preview_pr_review.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### prompts/gemini_2_5_preview_pr_review_actual.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### recursive_code_generator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### rules/ide_performance_optimization.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### scripts/black_wrapper.sh

- **Type:** shell
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/create_proper_notebook.py

- **Type:** python
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/deploy-container.sh

- **Type:** shell
- **Issues:** 17 (Critical: 0, Warnings: 17, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/deploy-ghostbusters-gcp.sh

- **Type:** shell
- **Issues:** 27 (Critical: 0, Warnings: 27, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/deploy.sh

- **Type:** shell
- **Issues:** 65 (Critical: 0, Warnings: 65, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/enforce_make_only.sh

- **Type:** shell
- **Issues:** 8 (Critical: 0, Warnings: 8, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/enforce_make_only_venv.sh

- **Type:** shell
- **Issues:** 14 (Critical: 0, Warnings: 14, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/flake8_wrapper.sh

- **Type:** shell
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/gcp_billing_daily_reporter.py

- **Type:** python
- **Issues:** 4 (Critical: 0, Warnings: 4, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/gemini_gcp_billing_analyzer.py

- **Type:** python
- **Issues:** 9 (Critical: 0, Warnings: 9, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/model_driven_test_recovery.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/monitor.sh

- **Type:** shell
- **Issues:** 38 (Critical: 0, Warnings: 38, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/mypy_wrapper.sh

- **Type:** shell
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/notebook_model.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/one_liner_linter.py

- **Type:** python
- **Issues:** 13 (Critical: 0, Warnings: 13, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/pytest_wrapper.sh

- **Type:** shell
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/restore_tools_venv.sh

- **Type:** shell
- **Issues:** 14 (Critical: 0, Warnings: 14, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/rule-compliance-check.sh

- **Type:** shell
- **Issues:** 66 (Critical: 0, Warnings: 66, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/run_live_smoke_test.sh

- **Type:** shell
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/run_live_smoke_test_1password.sh

- **Type:** shell
- **Issues:** 4 (Critical: 0, Warnings: 4, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/run_live_smoke_test_1password_flexible.sh

- **Type:** shell
- **Issues:** 8 (Critical: 0, Warnings: 8, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/run_live_smoke_test_direct.sh

- **Type:** shell
- **Issues:** 11 (Critical: 0, Warnings: 11, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/scrub_all_subprojects.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/security-check.sh

- **Type:** shell
- **Issues:** 55 (Critical: 0, Warnings: 55, Suggestions: 0)
- **One-liner Score:** 0.00%

### scripts/setup-cloud-build-trigger.sh

- **Type:** shell
- **Issues:** 13 (Critical: 1, Warnings: 12, Suggestions: 0)
- **One-liner Score:** 3.12%

### scripts/setup-develop-trigger.sh

- **Type:** shell
- **Issues:** 16 (Critical: 1, Warnings: 15, Suggestions: 0)
- **One-liner Score:** 2.86%

### scripts/setup-github-2ndgen.sh

- **Type:** shell
- **Issues:** 32 (Critical: 2, Warnings: 30, Suggestions: 0)
- **One-liner Score:** 2.74%

### scripts/setup-github-connection.sh

- **Type:** shell
- **Issues:** 31 (Critical: 2, Warnings: 29, Suggestions: 0)
- **One-liner Score:** 2.50%

### scripts/setup-github-trigger-direct.sh

- **Type:** shell
- **Issues:** 13 (Critical: 1, Warnings: 12, Suggestions: 0)
- **One-liner Score:** 3.03%

### scripts/trigger-build.sh

- **Type:** shell
- **Issues:** 4 (Critical: 0, Warnings: 4, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/artifact_forge/agents/artifact_correlator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/artifact_forge/agents/artifact_synthesizer.py

- **Type:** python
- **Issues:** 5 (Critical: 0, Warnings: 5, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/code_quality_system/**init**.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/code_quality_system/integrations/ci_cd_integration.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/code_quality_system/multi_agent_integration.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/complete_linting_aware_generator.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/complete_model_generator.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/enhanced_linting_aware_model.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/generate_code_generator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/generate_linting_aware_generator.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/intelligent_model_generator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/linting_aware_model.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/mdc_generator/mdc_model.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/model_driven_projection/COMPONENT_SUMMARY.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### src/model_driven_projection/README.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### src/model_driven_projection/TEST_EQUIVALENCE_REPORT.md

- **Type:** markdown
- **Issues:** 5 (Critical: 0, Warnings: 0, Suggestions: 5)
- **One-liner Score:** 0.00%

### src/model_driven_projection/final_projection_system.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/model_driven_projection/improved_projection_system.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/model_driven_projection/projected_artifacts/TEST_SUMMARY.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### src/model_driven_projection/projected_artifacts/src/security_first/input_validator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/model_driven_projection/projected_artifacts/src/streamlit/openflow_quickstart_app.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/model_driven_projection/test_projected_equivalence.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/model_driven_projection/test_simple_equivalence.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/multi_agent_testing/code_quality_automation_orchestrator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/multi_agent_testing/live_smoke_test_langchain.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/multi_agent_testing/multi_dimensional_smoke_test.py

- **Type:** python
- **Issues:** 20 (Critical: 0, Warnings: 20, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/multi_agent_testing/test_anthropic_simple.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/multi_agent_testing/test_diversity_hypothesis.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/multi_agent_testing/test_model_traceability.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/multi_agent_testing/test_multi_agent_blind_spot_detection.py

- **Type:** python
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/perfect_ast_generator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/perfect_code_generator.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/recursive_code_generator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/scaled_complex_model_generator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/secure_shell_service/README.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### src/secure_shell_service/migration_example.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/secure_shell_service/real_client.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/security_first/https_enforcement.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/security_first/rate_limiting.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/security_first/security_manager.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/security_first/test_streamlit_security_first.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/ultimate_perfect_generator.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/verify_ide_linting_hypothesis.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### src/visualization/comprehensive_dashboard.py

- **Type:** python
- **Issues:** 2 (Critical: 0, Warnings: 2, Suggestions: 0)
- **One-liner Score:** 0.00%

### subprojects/COMPONENT_DISTRIBUTION_STRATEGY.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### subprojects/README.md

- **Type:** markdown
- **Issues:** 3 (Critical: 0, Warnings: 0, Suggestions: 3)
- **One-liner Score:** 0.00%

### subprojects/gke-ai-microservices-hackathon.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### subprojects/kiro-ai-development-hackathon.md

- **Type:** markdown
- **Issues:** 1 (Critical: 0, Warnings: 0, Suggestions: 1)
- **One-liner Score:** 0.00%

### subprojects/tidb-agentx-hackathon/README.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### test_complex_model.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### test_expert_quality_integration.py

- **Type:** python
- **Issues:** 5 (Critical: 0, Warnings: 5, Suggestions: 0)
- **One-liner Score:** 0.00%

### test_orchestrator_quality_integration.py

- **Type:** python
- **Issues:** 3 (Critical: 0, Warnings: 3, Suggestions: 0)
- **One-liner Score:** 0.00%

### tests/test_ghostbusters_gcp.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### tests/test_python_quality_enhanced.py

- **Type:** python
- **Issues:** 1 (Critical: 0, Warnings: 1, Suggestions: 0)
- **One-liner Score:** 0.00%

### tidb-agentx-hackathon/README.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%

### tidb-agentx-hackathon/TIDB_HACKATHON_1_MONTH_PLAN.md

- **Type:** markdown
- **Issues:** 2 (Critical: 0, Warnings: 0, Suggestions: 2)
- **One-liner Score:** 0.00%
