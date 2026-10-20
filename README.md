# production-ai-agent

Production-ready AI agent: FastAPI + Postgres, LangGraph, pgvector RAG, observability, and LLM evals

An end-to-end production AI system built in 4 layers — not a demo. A deterministic
backend service first, then an LLM agent on top of it, then grounded retrieval,
then evals that gate changes in CI.

## Roadmap

- **Week 1 — Backend service:** Postgres + FastAPI service with
  `fetch_order_status` / `process_refund`, OpenTelemetry +
  Prometheus/Grafana, K8s/Helm
- **Week 2 — Agent:** LangGraph agent + Redis memory, using the Week 1 APIs
  as LLM tools
- **Week 3 — RAG:** pgvector RAG over policies/FAQs, prompts loaded from
  Langfuse/LangSmith at runtime
- **Week 4 — Evals:** 50–100 golden prompts + LLM-as-Judge evals,
  GitHub Actions on PRs

## Structure

```
app/                  Week 1 — FastAPI service
  api/                Routes: fetch_order_status, process_refund
  db/                 Postgres models / queries
  core/               Config, observability setup
agent/                Week 2 — LangGraph agent + Redis memory
rag/                  Week 3 — pgvector retrieval, policy/FAQ documents
evals/                Week 4 — Golden prompts, LLM-as-Judge evals
infra/
  k8s/                Kubernetes manifests
  helm/               Helm chart
  observability/      Prometheus / Grafana config
tests/                Tests (per week, as each layer lands)
.github/workflows/    CI — evals on PRs (Week 4)
docker-compose.yml    Local Postgres (pgvector) + Redis
```

## Getting started (Week 1, Task 1)

1. Copy `.env.example` to `.env` and fill in local values only.
2. Start local infra: `docker compose up -d`
3. Next task — and only this task for now: get Postgres running and
   confirm you can connect to it. No FastAPI code yet.

## Stack

Python · FastAPI · Postgres + pgvector · Redis · LangGraph ·
OpenTelemetry · Prometheus/Grafana · Kubernetes/Helm ·
Langfuse/LangSmith · GitHub Actions
