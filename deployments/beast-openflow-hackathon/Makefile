SHELL := /bin/bash

.PHONY: bootstrap deploy-openflow deploy-nim deploy-beast seed-data build-embeddings run-demo

bootstrap:
	@echo "[bootstrap] Provision EKS + core addons..."
	# terraform -chdir=infra/eks apply -auto-approve

deploy-openflow:
	@echo "[openflow] Deploy connectors/pipelines (BYOC/SPCS)"
	# kubectl apply -f openflow/

deploy-nim:
	@echo "[nim] Deploy LLM + Retrieval Embedding NIM services"
	cd helm && helm install nim-llm ./nim-llm && helm install nim-embeddings ./nim-embeddings

deploy-beast:
	@echo "[beast] Deploy orchestrator + nodes + wiring"
	cd helm && helm install beast ./beast

seed-data:
	@echo "[data] Seeding example sources..."
	# scripts/seed.sh

build-embeddings:
	@echo "[retrieval] Building embeddings via NIM..."
	# scripts/build_embeddings.sh

run-demo:
	@echo "[demo] ingest→embed→retrieve→reason→act"
	# scripts/run_demo.sh

