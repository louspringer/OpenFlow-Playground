# Beast + Openflow + Hackathon Deployment

Thin-slice, production-credible demo inside **OpenFlow-Playground** integrating:
- **Snowflake Openflow/NiFi** for unified ingestion & transformation
- **NVIDIA NIM** (LLM + Retrieval Embedding) on **AWS/EKS**
- **Beast cluster** for agentic orchestration
- **Public Observability** via https://observatory.nkllon.com (plus local Grafana/Loki/Tempo)

## Quick start (demo profile)
```bash
cd helm/
make bootstrap          # EKS + base addons
make deploy-openflow    # Openflow connectors/pipelines (BYOC or SPCS notes)
make deploy-nim         # LLM + Retrieval Embedding NIM services
make deploy-beast       # Orchestrator + nodes + wiring
make seed-data          # Example sources to ingest
make build-embeddings   # Generate embeddings via NIM
make run-demo           # End-to-end task (ingest→embed→retrieve→reason→act)
```

Artifacts:
- `ontology/beast-openflow.ttl` — RDF/Turtle semantic model
- `docs/requirements.md` — Requirements, risks, constraints, stakeholder views
- `helm/` — Production-ready Helm charts for all services

> Scope: optimized for hackathon timebox & ~$100 credits; see `docs/requirements.md`.

