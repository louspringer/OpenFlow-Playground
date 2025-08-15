
CREATE (cursor_rules:Domain {name: 'cursor_rules', description: 'Cursor rules for AI assistance and code quality enforcement', status: 'completed', rule_firing_identification: true}) RETURN cursor_rules;

CREATE (model_first_enforcement:Rule {name: 'model_first_enforcement', emoji: '🧠', description: 'Rule: model_first_enforcement', type: 'cursor_rule'}) RETURN model_first_enforcement;

CREATE (security:Rule {name: 'security', emoji: '🔒', description: 'Rule: security', type: 'cursor_rule'}) RETURN security;

CREATE (tool_integration_patterns:Rule {name: 'tool_integration_patterns', emoji: '🛠️', description: 'Rule: tool_integration_patterns', type: 'cursor_rule'}) RETURN tool_integration_patterns;

CREATE (ghostbusters:Rule {name: 'ghostbusters', emoji: '👻', description: 'Rule: ghostbusters', type: 'cursor_rule'}) RETURN ghostbusters;

CREATE (deterministic_editing:Rule {name: 'deterministic_editing', emoji: '⚙️', description: 'Rule: deterministic_editing', type: 'cursor_rule'}) RETURN deterministic_editing;

CREATE (python_quality_enforcement:Rule {name: 'python_quality_enforcement', emoji: '🐍', description: 'Rule: python_quality_enforcement', type: 'cursor_rule'}) RETURN python_quality_enforcement;

CREATE (package_management_uv:Rule {name: 'package_management_uv', emoji: '📦', description: 'Rule: package_management_uv', type: 'cursor_rule'}) RETURN package_management_uv;

CREATE (make_first_enforcement:Rule {name: 'make_first_enforcement', emoji: '🎯', description: 'Rule: make_first_enforcement', type: 'cursor_rule'}) RETURN make_first_enforcement;

CREATE (pr_procedure_enforcement:Rule {name: 'pr_procedure_enforcement', emoji: '📋', description: 'Rule: pr_procedure_enforcement', type: 'cursor_rule'}) RETURN pr_procedure_enforcement;

CREATE (cleanup_before_next_thing:Rule {name: 'cleanup_before_next_thing', emoji: '🧹', description: 'Rule: cleanup_before_next_thing', type: 'cursor_rule'}) RETURN cleanup_before_next_thing;

CREATE (intelligent_policy:Rule {name: 'intelligent_policy', emoji: '🧭', description: 'Rule: intelligent_policy', type: 'cursor_rule'}) RETURN intelligent_policy;

CREATE (investigation_analysis:Rule {name: 'investigation_analysis', emoji: '🔍', description: 'Rule: investigation_analysis', type: 'cursor_rule'}) RETURN investigation_analysis;

CREATE (llm_architect:Rule {name: 'llm_architect', emoji: '🏗️', description: 'Rule: llm_architect', type: 'cursor_rule'}) RETURN llm_architect;

CREATE (model_driven_enforcement:Rule {name: 'model_driven_enforcement', emoji: '📊', description: 'Rule: model_driven_enforcement', type: 'cursor_rule'}) RETURN model_driven_enforcement;

CREATE (model_driven_orchestration:Rule {name: 'model_driven_orchestration', emoji: '🎼', description: 'Rule: model_driven_orchestration', type: 'cursor_rule'}) RETURN model_driven_orchestration;

CREATE (call_more_ghostbusters:Rule {name: 'call_more_ghostbusters', emoji: '🚨', description: 'Rule: call_more_ghostbusters', type: 'cursor_rule'}) RETURN call_more_ghostbusters;

CREATE (cloudformation_linting:Rule {name: 'cloudformation_linting', emoji: '☁️', description: 'Rule: cloudformation_linting', type: 'cursor_rule'}) RETURN cloudformation_linting;

CREATE (dont_break_the_fixer:Rule {name: 'dont_break_the_fixer', emoji: '🔧', description: 'Rule: dont_break_the_fixer', type: 'cursor_rule'}) RETURN dont_break_the_fixer;

CREATE (intelligent_linter_prevention:Rule {name: 'intelligent_linter_prevention', emoji: '🧹', description: 'Rule: intelligent_linter_prevention', type: 'cursor_rule'}) RETURN intelligent_linter_prevention;

CREATE (dynamic_prevention_rules:Rule {name: 'dynamic_prevention_rules', emoji: '⚡', description: 'Rule: dynamic_prevention_rules', type: 'cursor_rule'}) RETURN dynamic_prevention_rules;

CREATE (yaml_type_specific:Rule {name: 'yaml_type_specific', emoji: '📄', description: 'Rule: yaml_type_specific', type: 'cursor_rule'}) RETURN yaml_type_specific;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'model_first_enforcement'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'security'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'tool_integration_patterns'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'ghostbusters'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'deterministic_editing'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'python_quality_enforcement'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'package_management_uv'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'make_first_enforcement'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'pr_procedure_enforcement'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'cleanup_before_next_thing'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'intelligent_policy'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'investigation_analysis'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'llm_architect'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'model_driven_enforcement'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'model_driven_orchestration'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'call_more_ghostbusters'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'cloudformation_linting'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'dont_break_the_fixer'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'intelligent_linter_prevention'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'dynamic_prevention_rules'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'}) MATCH (r:Rule {name: 'yaml_type_specific'}) CREATE (d)-[:CONTAINS]->(r) RETURN d, r;

MATCH (d:Domain {name: 'cursor_rules'})-[:CONTAINS]->(r:Rule) RETURN d.name as domain, r.name as rule, r.emoji as emoji ORDER BY r.name;

MATCH (r:Rule) WHERE r.emoji CONTAINS '🔒' OR r.emoji CONTAINS '🔧' RETURN r.name as rule, r.emoji as emoji, r.description as description;

MATCH (d:Domain)-[:CONTAINS]->(r:Rule) RETURN d.name as domain, count(r) as rule_count ORDER BY rule_count DESC;

