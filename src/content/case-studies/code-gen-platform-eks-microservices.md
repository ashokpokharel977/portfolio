---
title: "Kubernetes Platform for a Code-Generation SaaS"
client: "A code-generation developer platform"
industry: "Developer Tools / SaaS"
duration: "6 months"
role: "Tech Lead — Cloud & DevOps"
challenge: "A code-generation SaaS was running on self-managed EC2 instances that couldn't scale to meet demand, ran up high operational costs, and offered weak observability with no multi-AZ high availability. Sudden traffic spikes led to bottlenecks and service disruptions."
solution:
  - "Migrated the platform to Amazon EKS with managed, auto-scaling node groups for container orchestration"
  - "Stored static frontend assets in S3 and used Velero for automated cluster and application backups to S3"
  - "Built GitHub Actions CI/CD pipelines with Terraform for consistent, repeatable infrastructure provisioning"
  - "Instrumented full observability with CloudWatch, AWS X-Ray, and ADOT/OpenTelemetry for metrics, traces, and Prometheus-based ingress metrics"
  - "Delivered HA/DR with RDS Multi-AZ failover, AWS Backup, and multi-AZ/multi-region deployment"
  - "Hardened security with IAM access controls and KMS encryption at rest and in transit, plus dynamic auto-scaling for cost optimization"
outcomes:
  - { metric: "-70%", description: "Reduction in log search time through centralized logging and analytics" }
  - { metric: "<5 min", description: "From commit to production deployment, at 10-20 deploys per week" }
  - { metric: "-45%", description: "Reduction in mean time to recover (MTTR)" }
  - { metric: "200ms → 40ms", description: "Content delivery latency improvement" }
technologies: ["Amazon EKS", "Kubernetes", "Terraform", "GitHub Actions", "CloudWatch", "AWS X-Ray", "Velero", "Amazon RDS", "SRE", "FinOps"]
heroImage: "/images/case-studies/devops-platform.svg"
category: "devops-transformation"
pubDate: 2025-04-04
featured: true
---

## Project Overview

The client runs a code-generation developer platform serving a fast-growing base of engineers. When I came in, the entire product was running on self-managed EC2 instances. The setup was expensive, hard to operate, and — most damaging — unable to absorb the traffic spikes that came with growth.

I led the transition from that EC2-based footprint to a containerized architecture on Amazon EKS, designed around scalability, high availability, cost efficiency, and observability. The goal was simple: make the platform hold up under peak demand while cutting the operational drag the team was carrying.

## Key Challenges

The starting state had four structural problems:

- **No scalability** — the infrastructure couldn't handle sudden spikes in demand, causing bottlenecks and outages
- **High operational cost** — self-managed EC2 meant paying for instance provisioning, data transfer, storage, and constant management overhead
- **Weak observability** — no real log analytics, search optimization, or visualization, so the team couldn't derive insight or troubleshoot quickly
- **Limited high availability** — a single-AZ footprint left the platform exposed to hardware and network failures

## Solution / AWS Architecture

I designed the target architecture around AWS managed services so the team could stop babysitting infrastructure and focus on the product.

### Storage

Static frontend assets — images, stylesheets, and JavaScript — moved into dedicated S3 buckets for fast, highly available content delivery. S3 also became the primary backup target: Velero manages regular, automated backups of application data and cluster resources so critical state can be restored after a failure.

### EKS Orchestration

Amazon EKS runs the containerized workloads. Managed, auto-scaling node groups size the cluster to actual load, which optimizes both resource usage and cost instead of paying for idle capacity around the clock.

### DevOps Automation

GitHub Actions drives CI/CD, taking a commit to production automatically. Terraform provisions every AWS resource as code, so environments are consistent and reproducible rather than hand-built. SonarQube runs in the pipeline for security and quality scanning before anything ships.

### Observability

I instrumented three layers of visibility:

- **CloudWatch** for real-time application performance and utilization metrics
- **AWS X-Ray** for distributed tracing, integrated with OpenTelemetry
- **ADOT** for Prometheus-based metrics on ingress requests

Together these gave the team centralized logging, real-time analytics, and the tracing they'd been missing.

### High Availability and Disaster Recovery

RDS Multi-AZ provides fault tolerance with automatic failover. AWS Backup handles automated backups for fast recovery, and Velero backs up in-cluster resources — deployments, persistent volumes, and more. The deployment spans multiple availability zones and regions to keep the service running through localized failures.

### Security

IAM enforces least-privilege access controls. KMS encrypts data at rest and in transit. Pod-level security controls protect workloads inside the cluster.

### Cost

Auto-scaling ties spend to actual demand — the cluster scales up under load and back down when it's idle, eliminating the standing waste of always-on EC2.

## Results

The migration delivered measurable gains across reliability, speed, and experience:

- **Log search time down 70%** through centralized logging and analytics
- **Downtime reduced 50%** via real-time log analytics and proactive issue detection
- **Deployments in under 5 minutes** from commit, sustaining 10-20 production releases per week
- **MTBF up 25%** for greater system stability
- **MTTR down 45%** for faster recovery from incidents
- **Latency from 200ms to 40ms** on content delivery

## Key Learnings

1. **Managed services buy back focus** — moving to EKS with managed node groups let the team stop operating servers and start shipping features
2. **Observability is the foundation, not an add-on** — centralized logging and tracing cut troubleshooting time more than any single infra change
3. **Automate the whole path** — Terraform plus GitHub Actions turned deployment from a risk into a routine, unlocking 10-20 releases a week
4. **Scale with demand, not fear** — auto-scaling handled the spikes that used to cause outages while cutting the cost of idle capacity
