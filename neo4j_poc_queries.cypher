-- Neo4j Proof of Concept Queries
-- Generated from project model

-- Query 1
CREATE (cursor_rules:Domain {
            name: 'cursor_rules',
            description: 'Cursor rules for AI assistance and code quality enforcement',
            status: 'completed',
            rule_firing_identification: true
        })

-- Query 2
CREATE (model_first_enforcement:Rule {
                name: 'model_first_enforcement',
                emoji: '🧠',
                description: 'Rule for model_first_enforcement',
                type: 'cursor_rule'
            })

-- Query 3
CREATE (security:Rule {
                name: 'security',
                emoji: '🔒',
                description: 'Rule for security',
                type: 'cursor_rule'
            })

-- Query 4
CREATE (tool_integration_patterns:Rule {
                name: 'tool_integration_patterns',
                emoji: '🛠️',
                description: 'Rule for tool_integration_patterns',
                type: 'cursor_rule'
            })

-- Query 5
CREATE (ghostbusters:Rule {
                name: 'ghostbusters',
                emoji: '👻',
                description: 'Rule for ghostbusters',
                type: 'cursor_rule'
            })

-- Query 6
CREATE (deterministic_editing:Rule {
                name: 'deterministic_editing',
                emoji: '⚙️',
                description: 'Rule for deterministic_editing',
                type: 'cursor_rule'
            })

-- Query 7
CREATE (python_quality_enforcement:Rule {
                name: 'python_quality_enforcement',
                emoji: '🐍',
                description: 'Rule for python_quality_enforcement',
                type: 'cursor_rule'
            })

-- Query 8
CREATE (package_management_uv:Rule {
                name: 'package_management_uv',
                emoji: '📦',
                description: 'Rule for package_management_uv',
                type: 'cursor_rule'
            })

-- Query 9
CREATE (make_first_enforcement:Rule {
                name: 'make_first_enforcement',
                emoji: '🎯',
                description: 'Rule for make_first_enforcement',
                type: 'cursor_rule'
            })

-- Query 10
CREATE (pr_procedure_enforcement:Rule {
                name: 'pr_procedure_enforcement',
                emoji: '📋',
                description: 'Rule for pr_procedure_enforcement',
                type: 'cursor_rule'
            })

-- Query 11
CREATE (cleanup_before_next_thing:Rule {
                name: 'cleanup_before_next_thing',
                emoji: '🧹',
                description: 'Rule for cleanup_before_next_thing',
                type: 'cursor_rule'
            })

-- Query 12
CREATE (intelligent_policy:Rule {
                name: 'intelligent_policy',
                emoji: '🧭',
                description: 'Rule for intelligent_policy',
                type: 'cursor_rule'
            })

-- Query 13
CREATE (investigation_analysis:Rule {
                name: 'investigation_analysis',
                emoji: '🔍',
                description: 'Rule for investigation_analysis',
                type: 'cursor_rule'
            })

-- Query 14
CREATE (llm_architect:Rule {
                name: 'llm_architect',
                emoji: '🏗️',
                description: 'Rule for llm_architect',
                type: 'cursor_rule'
            })

-- Query 15
CREATE (model_driven_enforcement:Rule {
                name: 'model_driven_enforcement',
                emoji: '📊',
                description: 'Rule for model_driven_enforcement',
                type: 'cursor_rule'
            })

-- Query 16
CREATE (model_driven_orchestration:Rule {
                name: 'model_driven_orchestration',
                emoji: '🎼',
                description: 'Rule for model_driven_orchestration',
                type: 'cursor_rule'
            })

-- Query 17
CREATE (call_more_ghostbusters:Rule {
                name: 'call_more_ghostbusters',
                emoji: '🚨',
                description: 'Rule for call_more_ghostbusters',
                type: 'cursor_rule'
            })

-- Query 18
CREATE (cloudformation_linting:Rule {
                name: 'cloudformation_linting',
                emoji: '☁️',
                description: 'Rule for cloudformation_linting',
                type: 'cursor_rule'
            })

-- Query 19
CREATE (dont_break_the_fixer:Rule {
                name: 'dont_break_the_fixer',
                emoji: '🔧',
                description: 'Rule for dont_break_the_fixer',
                type: 'cursor_rule'
            })

-- Query 20
CREATE (intelligent_linter_prevention:Rule {
                name: 'intelligent_linter_prevention',
                emoji: '🧹',
                description: 'Rule for intelligent_linter_prevention',
                type: 'cursor_rule'
            })

-- Query 21
CREATE (dynamic_prevention_rules:Rule {
                name: 'dynamic_prevention_rules',
                emoji: '⚡',
                description: 'Rule for dynamic_prevention_rules',
                type: 'cursor_rule'
            })

-- Query 22
CREATE (yaml_type_specific:Rule {
                name: 'yaml_type_specific',
                emoji: '📄',
                description: 'Rule for yaml_type_specific',
                type: 'cursor_rule'
            })

-- Query 23
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'model_first_enforcement'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 24
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'security'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 25
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'tool_integration_patterns'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 26
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'ghostbusters'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 27
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'deterministic_editing'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 28
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'python_quality_enforcement'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 29
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'package_management_uv'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 30
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'make_first_enforcement'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 31
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'pr_procedure_enforcement'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 32
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'cleanup_before_next_thing'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 33
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'intelligent_policy'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 34
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'investigation_analysis'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 35
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'llm_architect'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 36
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'model_driven_enforcement'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 37
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'model_driven_orchestration'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 38
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'call_more_ghostbusters'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 39
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'cloudformation_linting'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 40
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'dont_break_the_fixer'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 41
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'intelligent_linter_prevention'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 42
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'dynamic_prevention_rules'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 43
MATCH (d:Domain {name: 'cursor_rules'})
            MATCH (r:Rule {name: 'yaml_type_specific'})
            CREATE (d)-[:CONTAINS]->(r)

-- Query 44
// Query 1: Find all rules in cursor_rules domain
        MATCH (d:Domain {name: 'cursor_rules'})-[:CONTAINS]->(r:Rule)
        RETURN d.name as domain, r.name as rule, r.emoji as emoji
        ORDER BY r.name

-- Query 45
// Query 2: Count rules by domain
        MATCH (d:Domain)-[:CONTAINS]->(r:Rule)
        RETURN d.name as domain, count(r) as rule_count
        ORDER BY rule_count DESC

-- Query 46
// Query 3: Find rules by emoji
        MATCH (r:Rule)
        WHERE r.emoji CONTAINS '🔒'
        RETURN r.name as rule, r.emoji as emoji, r.description as description

