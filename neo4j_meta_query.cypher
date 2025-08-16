
// Meta-Model Discovery Query
// This query discovers all dimensions and relationships in the project model

// 1. Discover all node types
MATCH (n)
RETURN DISTINCT labels(n) as node_types, count(n) as count
ORDER BY count DESC;

// 2. Discover all relationship types
MATCH ()-[r]->()
RETURN DISTINCT type(r) as relationship_types, count(r) as count
ORDER BY count DESC;

// 3. Discover domain structure
MATCH (d:Domain)
RETURN d.name as domain_name,
       d.description as description,
       d.status as status,
       d.priority as priority,
       size([(d)-[:CONTAINS]->(r:Rule) | r]) as rule_count;

// 4. Discover rule patterns
MATCH (r:Rule)
RETURN r.type as rule_type,
       r.emoji as emoji,
       count(r) as count
ORDER BY count DESC;

// 5. Discover package potential
MATCH (d:Domain)
WHERE d.package_potential IS NOT NULL
RETURN d.name as domain_name,
       d.package_potential.score as score,
       d.package_potential.pypi_ready as pypi_ready,
       d.package_potential.package_name as package_name
ORDER BY d.package_potential.score DESC;

// 6. Discover model completeness
MATCH (d:Domain)
RETURN d.status as status, count(d) as count
ORDER BY count DESC;

// 7. Discover cross-domain relationships
MATCH (d1:Domain)-[:RELATES_TO]->(d2:Domain)
RETURN d1.name as source_domain, d2.name as target_domain, type(RELATES_TO) as relationship_type;

// 8. Discover model metadata
MATCH (m:Meta)
RETURN m.model_type as model_type,
       m.model_completeness as completeness,
       m.domain_coverage as coverage,
       m.test_coverage as test_coverage;
