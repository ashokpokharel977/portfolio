---
title: "Agentic AI Helpdesk Automation (Lasius Lite)"
client: "Nova Corp"
industry: "Enterprise IT / Cybersecurity"
duration: "30-day pilot to production"
role: "AI / Platform Architect"
challenge: "Skilled engineers were spending 60%+ of their time on repetitive L1 work — password resets, access requests, and alert triage — while support costs scaled linearly with every new client. SLA breaches surfaced only after they happened, and every new environment meant rebuilding onboarding, ticketing, and knowledge transfer from scratch."
solution:
  - "Designed 8 specialized AI agents — Ticket Classifier, Auto-Resolver, Access Provisioner, Alert Validator, SLA Intelligence, Onboarding Orchestrator, Smart Router, and Supervisor — each with a dedicated role, trigger, and model, running on Claude Sonnet for reasoning and Claude Haiku for high-throughput routing"
  - "Built graph-based agent orchestration on LangGraph with explicit state machines, tool calling, and human-in-the-loop checkpoints so any action can pause for approval"
  - "Ran every multi-step workflow on Inngest as durable step functions with event-driven triggers, retries, and SLA pause/resume — ITIL-compliant state transitions that survive failures"
  - "Implemented a hybrid RAG pipeline with LlamaIndex — Vector RAG via pgvector embeddings and Graph RAG via pgRouting entity traversal, merged and cross-encoder re-ranked, all on PostgreSQL"
  - "Added ML-based false-positive alert filtering that correlates alerts against deployment and maintenance windows, plus predictive SLA breach detection that escalates 2 hours in advance"
  - "Connected to the client's existing stack — Jira, ServiceNow, Slack, Active Directory, Okta, AWS, Datadog, and PagerDuty — with no rip-and-replace, and instrumented the whole pipeline with OpenTelemetry traces, metrics, and logs"
  - "Shipped a Next.js application with live SSE-streamed metrics and an audit trail, deployed entirely inside the client's own cloud"
outcomes:
  - { metric: "78%", description: "L1 tickets auto-resolved end-to-end without human intervention" }
  - { metric: "<5 min", description: "Average resolution time, down from 30+ minutes of manual work" }
  - { metric: "91%", description: "Ticket classification accuracy from NLP intent extraction" }
  - { metric: "94%", description: "Knowledge-base match rate in the top-3 hybrid RAG results" }
technologies: ["GenAI", "LangGraph", "LlamaIndex", "RAG", "Claude", "PostgreSQL", "pgvector", "MLOps", "Inngest", "OpenTelemetry", "Next.js"]
heroImage: "/images/case-studies/lasius-ai-helpdesk-automation.webp"
category: "devops-transformation"
pubDate: 2026-01-15
featured: false
---

## Project Overview

Nova Corp is an enterprise IT and Zero-Trust security firm — roughly 350 employees, one of the more demanding operational environments I've worked in. Their engineers were good. That was part of the problem: some of the sharpest people on the team were spending most of their day resetting passwords and clearing alert queues.

I came in as the AI / Platform Architect to build **Lasius Lite**, an agentic helpdesk automation platform that classifies, resolves, and routes IT support tickets on its own. We went from a scoped pilot to running in production on real tickets in 30 days. The platform runs entirely inside Nova Corp's own cloud, plugs into the tools they already had, and handles the operational load their engineers used to carry by hand.

## The Challenge: The Hidden Cost of Keeping the Lights On

IT teams get stretched thin as they grow, and the costs compound quietly. Four things were hurting Nova Corp:

- **Skilled engineers on repetitive work.** Password resets, access requests, routine alerts — their best people spent 60%+ of their time on tasks that didn't need their expertise.
- **Costs that scaled linearly.** Every new client and every new system pushed ticket volume up. There was no leverage in the model — more work meant more headcount, full stop.
- **SLA breaches nobody saw coming.** By the time anyone noticed, the SLA was already gone. Alerts flooded the queue, and a lot of them were false positives that ate triage time.
- **Starting from zero every time.** New client, same onboarding, same ticketing setup, same knowledge transfer — rebuilt from scratch on each engagement.

None of these are exotic problems. They're the tax you pay to keep the lights on. The goal was to automate that tax away without ripping out the systems the team already trusted.

## Solution: Agentic Architecture

I built Lasius Lite as a layered system — connectors at the edge, agents making decisions, durable workflows executing them, and a hybrid RAG layer feeding everything with the right context. The design principle throughout: LLM-driven agents make the judgment calls, deterministic workflows execute the steps, and a human can step in at any checkpoint.

### The 8 Specialized Agents

Each agent has a single job, a clear trigger, and a model matched to its workload — Claude Sonnet where reasoning matters, Claude Haiku where speed and cost matter:

1. **Ticket Classifier** (Claude Sonnet) — Uses NLP to extract intent, urgency, category, and affected system from every incoming ticket.
2. **Auto-Resolver** (Sonnet + RAG) — Matches tickets against the knowledge base and executes the resolution end-to-end.
3. **Access Provisioner** (Rule Engine + API) — Handles RBAC validation and provisioning across LDAP, AD, and IAM.
4. **Alert Validator** (ML Model) — Filters false-positive alerts by correlating them against deployment and maintenance windows.
5. **SLA Intelligence** (ML + Rules) — Predicts breaches 2 hours in advance and triggers proactive escalation.
6. **Onboarding Orchestrator** (Sonnet + Workflow) — Runs end-to-end new-hire workflows that used to take 30+ days.
7. **Smart Router** (Haiku + Scoring) — Routes anything unresolved to the best-fit engineer by score.
8. **Supervisor** (Claude Sonnet) — Coordinates the other agents and monitors pipeline health.

Because the agents are LLM-driven rather than scripted, they handle novel variations of known issues instead of falling over on anything that doesn't match a rigid template.

### Orchestration: LangGraph + Inngest

Two engines run underneath the agents, and separating them was one of the more important design decisions.

**LangGraph** handles agent orchestration as a graph — explicit state machines, tool calling, and human-in-the-loop checkpoints. This is where the adaptive, decision-making behavior lives.

**Inngest** handles execution as durable step functions with event-driven triggers, retry and error handling, and SLA pause/resume. This is where reliability lives: ITIL-compliant state transitions that survive a crash mid-workflow, with approval gates at any stage.

A password reset flows straight through — ticket in, classify, RAG match, AD API reset, closed. A new-hire onboarding runs as a multi-step durable workflow with an approval checkpoint before provisioning. An escalation with a vendor hold pauses the SLA timer, waits, and resumes cleanly. The agents decide; the workflow engine guarantees the decision actually executes, once, in order, even when something upstream fails.

### Hybrid RAG Pipeline: Vector + Graph

Resolution quality depends entirely on retrieval quality, so the RAG layer got the most attention. I built it on **LlamaIndex** over PostgreSQL, pulling from resolved Jira tickets, the Confluence knowledge base (SOPs, runbooks, playbooks), resolution notes, and an entity graph linking tickets, docs, systems, and RBAC.

The pipeline parses, chunks, embeds, and dual-indexes every source, then retrieves along two paths:

- **Vector RAG** — semantic similarity via cosine distance against 90 days of ticket history and KB docs, using **pgvector**.
- **Graph RAG** — entity-relationship traversal with multi-hop reasoning via **pgRouting**, so the system can follow *this user → this system → this access policy* rather than just matching text.

Both paths merge into a single candidate set, then a **cross-encoder re-ranks** them. Anything scoring above 85% auto-resolves; below that, it smart-routes to a human. Keeping vector, graph, and re-ranking all on PostgreSQL meant one data layer to operate instead of a separate vector store, graph database, and search cluster.

### SLA Intelligence & False-Positive Filtering

Two ML-driven pieces attack the parts of the queue that were pure waste.

The **Alert Validator** correlates incoming alerts against deployment and maintenance windows — an alert that fires during a known deploy is almost always noise, and the model learns to auto-close it instead of paging someone.

The **SLA Intelligence** agent flips SLA management from reactive to predictive. Instead of noticing a breach after the fact, it forecasts breaches 2 hours out and escalates at a 75% threshold, before the timer runs down. That alone changed how the on-call team spent their attention.

### Integrations

Lasius Lite plugs into the stack Nova Corp already ran — no rip and replace:

- **Ticket sources:** Jira SM, ServiceNow, Email, Slack, web forms (REST API + webhooks)
- **Identity & access:** Active Directory, Azure AD, Okta SSO, LDAP (SCIM, Graph API)
- **Cloud platforms:** AWS IAM, Google Workspace, Exchange Online, Azure
- **Monitoring:** CloudWatch, Datadog, PagerDuty
- **Knowledge & collaboration:** Confluence, Slack, GitHub

The whole pipeline is wired with **OpenTelemetry** — traces, metrics, and logs — so resolution rates, agent performance, SLA compliance, and cost-per-resolution are all observable rather than guessed at.

## Results (Nova Corp)

Deployed on real tickets in one of Nova Corp's demanding Zero-Trust environments, the platform delivered:

- **78% of L1 tickets auto-resolved** end-to-end, with no human in the loop
- **Under 5 minutes average resolution time**, down from 30+ minutes of manual handling
- **91% classification accuracy** on intent extraction from incoming tickets
- **94% knowledge-base match rate** in the top-3 hybrid RAG results

The knock-on effects mattered as much as the headline numbers: incidents dropped roughly 25%, 60-70% of ticket volume ran through automation, and the L1 team's effective capacity went from needing 3 engineers to 1, freeing the other two for work that actually used their expertise. Onboarding collapsed from a 30+ day manual process to under a day. And because the framework is configured rather than custom-built per client, the same engine redeploys to the next environment without a rebuild.

## Key Learnings

1. **Separate the decision from the execution.** Letting LangGraph handle agent reasoning and Inngest handle durable execution kept the system both adaptive and reliable. Trying to do both in one layer would have made it either brittle or slow.
2. **Retrieval quality is the ceiling on resolution quality.** The hybrid vector-plus-graph approach with cross-encoder re-ranking is what pushed KB match into the 90s. A single retrieval path wasn't enough for a Zero-Trust environment where access relationships matter as much as text similarity.
3. **Predictive beats reactive on SLAs.** Forecasting breaches 2 hours out changed the team's whole posture — they stopped firefighting breaches and started preventing them.
4. **Human-in-the-loop is a feature, not a fallback.** Checkpoints and approval gates were what made the client comfortable letting agents touch production access. Autonomy earned trust because a human could always intervene.
5. **Configure, don't rebuild.** Designing for a repeatable framework instead of a bespoke build per client is what turned a single deployment into something that scales to the next one in hours.
