# Beastmaster Ontology v0.1 (portable)

This bundle contains:

- `ontology/beastmaster.ttl` — RDF/Turtle ontology
- `ontology/beastmaster.shacl.ttl` — SHACL integrity shapes
- `spores/schema/spore.schema.json` — minimal spore schema
- `examples/example.spore.ttl` — compact example spore

## Quick start

Use any RDF tool (Jena, rdflib) to load `beastmaster.ttl` and validate instances with `beastmaster.shacl.ttl`.

## Core ideas

- Requirements-as-solution; everything is a DAG with traceability.
- Metrics are first-class edges; PDCA and RCA live in-graph.
- Diversity (multi-LLM, multi-impl) is tracked, not suppressed.
- DDD isolates vendor terms via adapters/UL mapping.
