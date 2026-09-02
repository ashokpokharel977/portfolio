---
title: "Cloud Foundation for an AI-Driven Fitness Platform"
client: "An AI-driven fitness & wellness platform"
industry: "Health & Fitness"
duration: "6 months"
role: "Cloud / AI Solutions Architect"
challenge: "The platform's generic, one-size-fits-all programs left members disengaged, with roughly 65% of new subscribers dropping off within three months. There was no personalized guidance, no consistent coaching, and no real-time feedback — and no cloud foundation capable of supporting AI personalization at scale."
solution:
  - "Designed a multi-account AWS structure following the Well-Architected Framework, separating workloads by environment and function"
  - "Executed a phased lift-and-shift migration of existing workloads to AWS with minimal disruption"
  - "Provisioned all infrastructure as code with Terraform for repeatable, auditable environments"
  - "Built automated CI/CD pipelines to standardize builds, testing, and deployments"
  - "Integrated centralized security, guardrails, and monitoring across all accounts"
  - "Delivered GenAI-driven personalized workout and diet plans with wearable data and smart equipment tracking"
outcomes:
  - { metric: "~65% churn", description: "Targeted the pre-existing three-month dropout rate with personalized, adaptive guidance" }
  - { metric: "Higher retention", description: "Real-time feedback and AI coaching improved engagement and adherence" }
  - { metric: "Responsible AI", description: "Safety guardrails and privacy compliance built into every AI interaction with health data" }
  - { metric: "Scalable foundation", description: "Well-Architected, IaC-provisioned environment supports thousands of users with dynamic plan adjustments" }
technologies: ["AWS", "Terraform", "CI/CD", "GenAI", "Well-Architected", "Amazon Bedrock", "ECS Fargate", "RAG", "LLaMA 3", "PostgreSQL"]
heroImage: "/images/case-studies/ai-fitness-wellness-platform.webp"
category: "cloud-migration"
pubDate: 2026-02-11
featured: false
---

## Project Overview

The client operates an AI-driven fitness and wellness platform aiming to transform how members train and eat. But their traditional, generic programs weren't holding attention — nearly two-thirds of new members were cancelling within three months. The problems were clear enough: no personalized guidance, inconsistent trainer support, and no real-time feedback loop.

Fixing the experience meant fixing the foundation first. Before any AI could personalize a workout or adapt a diet plan, the platform needed a cloud environment that was secure, repeatable, and built to scale. My mandate was to design and stand up that foundation on AWS, then layer GenAI personalization on top of it — adopting AI responsibly, with safety and privacy treated as first-class requirements in a health context.

## Customer Challenges

The engagement started from a candid assessment of where the platform stood:

- **High churn** — roughly 65% of new subscribers left within three months of signing up
- **No personalization** — every member received largely the same plan regardless of goals, history, or wearable data
- **Inconsistent coaching** — trainer support varied and didn't scale with the member base
- **No real-time feedback** — members had no adaptive loop reacting to their actual activity and progress
- **No scalable foundation** — the existing setup couldn't support AI workloads or grow with demand

## Solution

I approached this in two connected halves: build a Well-Architected cloud foundation, then deliver GenAI personalization on top of it.

### Well-Architected Foundation

I designed a multi-account AWS structure aligned to the Well-Architected Framework, so the platform started from a defensible baseline rather than retrofitting governance later:

- Separate accounts by environment and function to isolate blast radius
- Centralized identity, logging, and billing across the organization
- Guardrails and baseline controls applied consistently from day one
- Design decisions traced back to the framework's pillars — operational excellence, security, reliability, performance efficiency, and cost optimization

### Migration Strategy

Rather than a risky big-bang cutover, I ran a phased lift-and-shift migration:

1. **Assess & prioritize** — inventory existing workloads and sequence them by risk and dependency
2. **Migrate in waves** — move workloads incrementally so each phase could be validated before the next
3. **Stabilize** — verify parity and performance after each wave before proceeding
4. **Optimize** — refine sizing and configuration once workloads were running on AWS

Phasing kept disruption low and gave the team confidence at every step rather than betting everything on a single migration event.

### CI/CD & Automation

To make the environment repeatable and safe to change, everything was codified:

- **Terraform** provisioned all infrastructure as code — environments could be rebuilt identically and reviewed like any other code
- **Automated CI/CD pipelines** standardized builds, testing, and deployments, removing manual steps and the errors that come with them
- Consistent promotion paths across environments so changes flowed predictably from development to production

### GenAI Personalization

With the foundation in place, the platform delivered the personalized experience members were missing. Specialized AI agents — running on ECS Fargate — handled workout generation, diet generation, and motivational coaching:

- **Data ingestion** pulled together wearable device data, user profiles, and workout history to feed the agents
- **Retrieval-Augmented Generation (RAG)** grounded responses in each member's prior guidance and metrics, retrieved from a vector database
- **Prompt engineering & orchestration** routed queries to the right agent and updated plans dynamically based on real-time data
- **Workout and diet agents** produced tailored plans, with **LLaMA 3** generating the personalized responses and an AI coach delivering real-time, adaptive feedback
- **Smart equipment and wearable tracking** kept plans responsive to what members actually did, not just what they said

### Security & Monitoring

In a health and wellness context, responsible AI isn't optional — it's the product:

- **Guardrails** checked every plan for safety and health compliance before it reached a member, and respected dietary restrictions and privacy
- **Centralized monitoring** provided visibility across accounts and workloads
- **Security and compliance controls** protected sensitive health data throughout the pipeline
- Fine-tuning via Amazon Bedrock kept coaching supportive and contextually appropriate

## Key Outcomes

The source data for this engagement is qualitative on most fronts, and I'll keep it honest rather than invent precision:

- **Targeted the ~65% churn** — the personalized, adaptive experience directly addressed the dropout that generic plans had been driving
- **Improved engagement and retention** — real-time feedback and AI coaching gave members a reason to stay
- **Responsible AI adoption** — safety guardrails and privacy compliance were built into every interaction with health data
- **A scalable foundation** — a Well-Architected, Terraform-provisioned environment now supports thousands of users with dynamic, wearable-driven plan adjustments

A one-year TCO analysis confirmed the pay-as-you-go, managed-services approach kept costs closely tied to actual usage — leaning on managed AI inference instead of dedicated hardware avoided overprovisioning and reduced operational overhead.

## Key Learnings

1. **Foundation before features** — AI personalization is only as reliable as the cloud environment underneath it. Getting the Well-Architected structure and IaC right first made everything after it faster and safer.
2. **Phased migration builds trust** — moving in waves let the team validate each step and avoided the risk of a single large cutover.
3. **Responsible AI is non-negotiable in health** — guardrails, privacy compliance, and safety checks aren't a finishing touch; in a wellness product they're core to the design.
4. **Real-time data is what makes personalization work** — combining GenAI with live wearable data is what turned generic plans into an experience members actually stuck with.
