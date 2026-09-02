---
title: "Lasius: Enterprise AI Platform on Kubernetes"
client: "Lasius (enterprise AI platform)"
industry: "AI SaaS / Platform"
duration: "6+ months (ongoing)"
role: "AI Platform & DevOps Architect"
challenge: "A financial-services firm was drowning in ungoverned 'Shadow AI' — unmanaged tools and API keys leaking sensitive data and breaking compliance. They needed every employee on a secure, governed path to AI. Delivering that meant both a governed AI product and the reproducible, multi-environment cloud-native platform to run it on."
solution:
  - "Built Lasius as a centralized AI governance hub — SSO, RBAC, approval workflows, content filtering, PII detection, encryption, and immutable audit logging, so every AI request is authenticated, policy-checked, logged, and costed"
  - "Assembled an AI services layer behind a single governed API — foundation models with a model router, an agent framework, a RAG engine with vector store, and version-controlled prompt management"
  - "Pre-configured financial-services compliance (SOX, FINRA/SEC, BSA/AML, GLBA, fair-lending) with bias testing, explainable AI, and model-risk governance"
  - "Ran the whole platform on a single multi-tenant Amazon EKS cluster (K8s 1.36) with namespace-isolated dev/stage/prod and per-environment quotas — one control plane, three tenants"
  - "Adopted Cilium (eBPF, kube-proxy replacement, Hubble) as CNI, Traefik on the Kubernetes Gateway API, and cert-manager + Let's Encrypt DNS-01 for automated wildcard TLS"
  - "Codified everything in Terraform across two isolated states, with EKS Pod Identity for workload IAM and External Secrets Operator syncing AWS Secrets Manager"
  - "Delivered through Argo CD GitOps — an ApplicationSet with PR-driven dev→stage→prod promotion — and a self-hosted LGTM observability stack (Loki/Grafana/Tempo/Mimir) + Grafana Alloy"
  - "Treated AI plumbing as first-class infra: per-env Amazon Bedrock Knowledge Bases (S3 + Aurora PostgreSQL/pgvector) for RAG, a Milvus vector DB, and Temporal for durable agent workflows"
outcomes:
  - { metric: "70%", description: "Lower cost than a custom build — roughly $1.5-2M down to $150-300K" }
  - { metric: "300%", description: "First-year ROI — about $2M Year-1 value on a $500K investment" }
  - { metric: "GitOps", description: "Every change flows through Git + Argo CD on one multi-tenant EKS cluster serving 3 isolated environments" }
  - { metric: "100%", description: "Shadow AI eliminated with zero compliance violations across the rollout" }
technologies: ["Amazon EKS", "Kubernetes", "Cilium", "Argo CD", "GitOps", "Terraform", "SRE", "Grafana", "Amazon Bedrock", "RAG", "GenAI", "AI Governance", "Responsible AI", "Security", "Compliance", "cert-manager", "External Secrets", "Aurora", "pgvector", "Temporal"]
heroImage: "/images/case-studies/devops-platform.svg"
category: "devops-transformation"
pubDate: 2026-08-11
featured: true
---

## Project Overview

Lasius is an enterprise AI platform — it runs agents, orchestrates long-running workflows, and serves RAG knowledge bases, all behind a governance boundary that makes it safe to hand to an entire firm. This case study covers both halves of the work I led: **architecting the governed AI product**, and **engineering the cloud-native platform it runs on**.

The catalyst was a financial-services firm operating in a heavily regulated environment where a single mishandled data point can trigger a regulatory event. Like most enterprises, they didn't have too little AI — they had too much of it, ungoverned. Employees had reached for whatever tools helped them move faster, producing a sprawl of unauthorized services, unmanaged API keys, and locally installed models operating entirely outside the firm's security perimeter. My mandate: eliminate Shadow AI by making the *governed* path the *fast* path — and build the platform underneath that could deliver it reproducibly across dev, stage, and prod.

## The Challenge

"Shadow AI" is the AI equivalent of shadow IT — unauthorized services reached through unmanaged keys, browser tools that bypass network controls, and locally installed models. In financial services it's not a productivity footnote; it's a data-exfiltration and compliance liability:

- **Sensitive data leaving the perimeter** — proprietary and customer data sent to external services, retained in training sets with no recall.
- **Unmanaged keys and auth gaps** — tools wired in with no permission model, widening the attack surface per integration.
- **Security blind spots and regulatory exposure** — existing frameworks were never designed for AI workloads, leaving gaps in data-access controls, audit trails, and recordkeeping obligations.
- **No leadership visibility** — risk couldn't be measured, let alone managed.

Solving it structurally meant a second, deeper challenge: an AI platform is not a stateless web app. It carries vector stores, durable workflows, a query engine, and AWS-native retrieval plumbing. Standing that up once is hard; standing it up as **three isolated environments that never drift — without three clusters' worth of overhead** — is the real platform problem.

## The Lasius Platform

I designed Lasius as a centralized hub that sits between employees and AI, layered deliberately so governance is the boundary every request passes through — not a bolt-on.

### Governance & Security Layer

The enforcement boundary. **SSO** ties every session to a real identity and **RBAC** decides what each role can do. **Approval workflows** gate higher-risk models, so a research analyst and a compliance officer operate under different rules by design. Every interaction runs through **content filtering** and **PII detection**, **encryption** protects data in transit and at rest, and **immutable audit logging** captures a tamper-evident trail of who did what — the exact artifact regulators and internal audit want.

### AI Services Layer

Behind the boundary sits the intelligence, exposed through a single governed API so teams never touch raw model endpoints. **Foundation models** are served through a **model router** that picks the right model per request on cost and capability. An **agent framework** lets teams build agents with custom tools, a **RAG engine** backed by a vector store grounds responses in the firm's own data, and **prompt management** version-controls prompts so quality and compliance travel with every use case.

### No-Code Workflows & Compliance Controls

Governance only sticks if the sanctioned path is also easier. A **no-code, drag-and-drop workflow builder** lets business teams compose multi-step AI automations visually, inside the guardrails. And the controls that make Lasius viable in this industry ship **pre-configured**: SOX (audit trails, change management), FINRA/SEC (recordkeeping, supervision), BSA/AML (transaction monitoring), GLBA (safeguarding customer data), and fair-lending ECOA/FCRA (bias testing, explainable AI) — paired with model-risk governance.

## Cloud-Native Platform Engineering

The product is only as good as the platform it ships on. The foundation is Infrastructure as Code end to end, delivered through GitOps, observable from day one.

### Cluster & Networking (EKS + Cilium)

The platform runs on a single Amazon EKS cluster (Kubernetes 1.36) in `us-east-1`, fronted by one Network Load Balancer. Rather than a cluster per environment, dev, stage, and prod are namespace-isolated on the same cluster with per-environment quotas — one control plane, one node fleet, three tenants. Networking runs on **Cilium** for its eBPF dataplane: it replaces kube-proxy outright, uses cluster-pool IPAM with tunnel/VXLAN routing, and ships **Hubble** for flow-level observability — being able to reason about pod-to-pod traffic across namespaces is a security asset on a shared cluster, not a nice-to-have. A general-workload group runs on-demand `t3.large` nodes, with `c7i.2xlarge` and **spot** groups defined for cost efficiency and a Cluster Autoscaler balancing them.

### Ingress, TLS & Infrastructure as Code

Ingress is built on the **Kubernetes Gateway API** with Traefik, which cleanly separates the platform team that owns the `Gateway` from the app teams that attach `HTTPRoute`s — exactly the boundary you want on a shared cluster. **cert-manager** drives a Let's Encrypt DNS-01 issuer so a single wildcard certificate auto-renews across every subdomain. The entire platform is **Terraform**, split into two independent S3/DynamoDB-locked states — an infrastructure root (VPC, EKS, NLB, IAM, EFS, Bedrock KB prerequisites) and an in-cluster addons state (Cilium, CSI drivers, EKS addons) that reads root outputs remotely. Splitting them keeps blast radius small: an addon change can never touch the VPC. Workload IAM runs on **EKS Pod Identity** cluster-wide rather than IRSA/OIDC.

### GitOps Delivery (Argo CD)

Application delivery is GitOps through **Argo CD**. An **ApplicationSet** generates one `Application` per app per environment, so adding an app or environment is a config change, not a bespoke pipeline. The cluster bootstraps through an explicit five-stage pipeline (`base` → `00-core` → `01-app-baseline` → `02-cicd` → `03-app-common`). GitHub Actions build and push images to ECR via OIDC, then bump the image tag in the GitOps repo for Argo CD to re-sync. Promotion is deliberate: **dev auto-syncs on merge; stage and prod are PR-driven**, copying the exact tested image tag forward, with prod gated by a manual sync. Rollback is simply reverting the bump PR.

### Secrets & Observability

**AWS Secrets Manager** is the single source of truth; the **External Secrets Operator** syncs secrets in via a `ClusterSecretStore` authenticated by Pod Identity, with per-namespace `ExternalSecret`s refreshing every 15 minutes — no long-lived credentials in Git. Observability is self-hosted on the full **LGTM** stack — Loki (logs), Grafana (dashboards), Tempo (traces), Mimir (metrics) — with **Grafana Alloy** collecting logs, traces, and Cilium/Hubble-aware metrics. Datasources are cross-linked so you can pivot from a log line to a trace to a metric without leaving Grafana, and nine alerting rules span ingress 5xx, node pressure, and workload health.

### AI Platform Services

The AI plumbing is first-class infrastructure. Each environment gets a scoped **Amazon Bedrock Knowledge Base** backed by S3 and **Aurora PostgreSQL/pgvector** for RAG, alongside a self-hosted **Milvus** vector database, **Temporal** as a durable workflow engine for long-running agent execution, **Trino** for queries, and PostgreSQL/Redis for state — all provisioned per environment through the same IaC and GitOps discipline.

## Rollout: A 4-Phase Transformation

Rather than a big-bang launch, the governance rollout ran in four phases — **Identify** (map the real Shadow AI footprint via traffic analysis, expense review, and surveys, scored on a risk-value matrix), **Ideate** (design the governance framework and platform blueprint, select high-impact pilots), **Inspect** (deploy, integrate identity, run penetration and user-acceptance testing), and **Scale** (phased enterprise rollout, Shadow AI sunset, and an **AI Center of Excellence** to own governance after the engagement ends).

## Engineering Decisions

- **One multi-tenant cluster, not three** — namespace isolation with quotas gives real separation while collapsing three control planes into one; the tradeoff is logical rather than physical isolation, which is why quotas, RBAC, and Hubble-visible traffic matter.
- **Cilium overlay + hostNetwork webhooks** — tunnel routing means pod IPs aren't reachable from the control plane, so cert-manager's webhook runs on `hostNetwork`. A deliberate, documented constraint rather than a surprise.
- **Two Terraform states over one** — a little extra wiring for a much smaller blast radius.
- **Spot + on-demand FinOps** — baseline on-demand, elastic workloads on spot, balanced by the autoscaler.

## Results

- **70% lower cost than a custom build** — ~$1.5-2M delivered for ~$150-300K, configured by 1-2 people rather than a 3-5 engineer team.
- **4-6 weeks to deployment** vs the 9-12 months a ground-up build would have taken, largely because compliance shipped pre-built.
- **300% first-year ROI** — ~$2M Year-1 value on a $500K investment across efficiency, fraud prevention, and risk reduction, on infrastructure holding 99.9% availability.
- **100% Shadow AI eliminated, zero compliance violations** — full visibility, complete audit trails, 90% employee adoption.
- **GitOps-driven, reproducible platform** — every change flows through Git and Argo CD; the whole platform lives in Terraform; one multi-tenant EKS cluster serves three isolated environments with unified, cross-linked observability and automated TLS and secret rotation.

## Key Learnings

1. **Make the governed path the fast path.** Adoption hit 90% because Lasius was easier than the rogue tools it replaced. Enablement beats enforcement.
2. **Ship compliance pre-built, not per-project.** Pre-configuring SOX, FINRA/SEC, and the rest is what turned a 9-12 month effort into a 4-6 week one — in regulated industries, the compliance layer *is* the differentiator.
3. **Multi-tenancy is a discipline, not a default.** One cluster for three environments only works because isolation is enforced deliberately — quotas, RBAC, Gateway/route separation, and network observability. Take those away and "multi-tenant" quietly becomes "shared blast radius."
4. **Make promotion boring.** Auto-sync to dev, PR-promotion of a tested tag to stage and prod, and a manual prod gate turn releases into a predictable, auditable flow — and rollback into a single revert.
5. **Treat AI services as platform, not app.** Bedrock knowledge bases, the vector DB, and the durable workflow engine are as load-bearing as the databases. Provisioning them through the same IaC and GitOps discipline is what keeps an AI platform reproducible instead of hand-assembled.
