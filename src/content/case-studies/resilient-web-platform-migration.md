---
title: "Resilient Cloud Migration for a Content & Community Platform"
client: "A content & community web platform"
industry: "Media / Web"
duration: "4 months"
role: "Cloud / DevOps Engineer"
challenge: "The platform ran on a single Ubuntu VM with a self-managed MySQL database and SFTP-based releases, capping it at roughly 2,000 concurrent users and causing frequent overloads and downtime during traffic spikes. Deployments took 2-3 hours and there was no automated backup or disaster recovery."
solution:
  - "Re-architected the WordPress workload onto AWS Elastic Beanstalk with EC2 Auto Scaling behind an Application Load Balancer for managed, elastic compute"
  - "Migrated the self-managed MySQL database to Amazon RDS Multi-AZ with automated failover and backups, and moved media assets to shared Amazon EFS"
  - "Built an automated CI/CD pipeline with AWS CodePipeline and CodeBuild, gated by SonarQube static analysis and manual approvals between environments"
  - "Ran an AWS Resilience Hub assessment and formalized RTO/RPO targets, with AWS Backup covering RDS and EFS across regions"
  - "Authored disaster-recovery runbooks and playbooks, and validated failover and recovery through DR testing before handover"
  - "Established observability with CloudWatch and CloudTrail, X-Ray tracing, and Slack alerting, with WAF and Security Hub for continuous security posture"
outcomes:
  - { metric: "5x", description: "Concurrent user capacity, from ~2,000 to 10,000+" }
  - { metric: "99%", description: "Uptime sustained through peak traffic on Multi-AZ infrastructure" }
  - { metric: "~15 min", description: "Deployments, down from 2-3 hours via automated CI/CD" }
  - { metric: "RTO 6h / RPO 1h", description: "Recovery objectives validated against AWS-defined standards" }
technologies: ["AWS Elastic Beanstalk", "RDS", "AWS Resilience Hub", "CI/CD", "SRE", "CloudWatch", "Route 53", "EFS", "CodePipeline", "Terraform", "WordPress"]
heroImage: "/images/case-studies/cloud-migration.svg"
category: "cloud-migration"
pubDate: 2025-08-20
featured: false
---

## Project Overview

The client operates a content and community platform in the entertainment and lifestyle space, serving a large, spike-prone audience following influencers, celebrities, and fitness and sports content. Traffic was unpredictable and event-driven, but the hosting underneath it was not built for that reality.

The entire application ran on a single self-managed virtual machine with a database the team backed up by hand and released to over SFTP. My job was to move the platform onto AWS without losing data or history, and to leave it materially more resilient, scalable, and faster to ship than it was before.

## The Challenge

The starting state made every busy day a risk:

- **Hard capacity ceiling** — a single Ubuntu VM (2 vCPU, 4 GB RAM) topped out around 2,000 concurrent users, and popular content routinely pushed past that.
- **Fragile data management** — self-hosted MySQL 5.7 with manual, ad-hoc backups and no tested recovery path.
- **Slow, error-prone releases** — SFTP-based deployments took 2-3 hours per release, with no rollback story.
- **Frequent downtime** — traffic overloads caused outages exactly when the audience was largest.

There was no meaningful disaster recovery. If the box or the database failed, recovery would have been slow and manual, with real risk of data loss.

## Solution / Architecture

I re-architected the platform onto managed AWS services, favouring PaaS where it removed undifferentiated operational work, and treated resilience as a first-class requirement rather than an afterthought. The design followed AWS Well-Architected Framework principles throughout.

### Compute and Application Management

WordPress moved onto **AWS Elastic Beanstalk** running a managed PHP environment with **EC2 Auto Scaling** behind an **Application Load Balancer**. Beanstalk handled provisioning, health checks, and rolling deployments; Auto Scaling absorbed traffic spikes that used to take the old VM down. This alone lifted the concurrent-user ceiling roughly fivefold.

### Data and Storage

The self-managed database migrated to **Amazon RDS Multi-AZ for MySQL**, which brought automated backups and synchronous failover to a standby in a second Availability Zone. Media and shared assets moved to **Amazon EFS**, mounted across instances so the fleet could scale horizontally without losing shared state. **CloudFront** was added in front for edge caching and lower latency across regions.

### CI/CD and Infrastructure as Code

I replaced the SFTP release process with an automated pipeline. Infrastructure was provisioned through **Terraform** for repeatable, reviewable environments. Application delivery ran through **AWS CodePipeline** and **CodeBuild**:

- A credential-less **CodeStar** connection triggered the pipeline on pushes to environment branches (dev, stage, main).
- CodeBuild built the deployable artifact (PHP, WP-CLI, Composer) in an isolated environment.
- **SonarQube** static analysis enforced quality gates — failing code halted the deployment automatically.
- Cross-account IAM role assumption kept dev, stage, and prod isolated under least privilege, with manual approval gates between stages.
- Elastic Beanstalk's rolling updates and automatic versioning gave zero-downtime deploys and one-click rollback.

This cut release time from 2-3 hours to roughly 15 minutes.

### Resilience & Disaster Recovery

This was the differentiator on the engagement. Rather than assume the new architecture was resilient, I measured it.

- I ran an **AWS Resilience Hub** assessment against the workload to surface single points of failure and validate the design against defined resilience policies.
- We set explicit recovery objectives — **RTO of 6 hours and RPO of 1 hour** — aligned to AWS-defined standards, and confirmed the architecture could actually meet them.
- **AWS Backup** centralized and automated protection for both RDS and EFS, with multi-region copies for recovery assurance. Backup runtime dropped from 2-3 hours of manual work to roughly 20 minutes, automated.
- I wrote **disaster-recovery runbooks and playbooks** covering failover, restore, and rollback, then validated them through DR testing before go-live rather than trusting them on paper.
- A multi-account structure isolated environments and blast radius.

The result was that recovery stopped being a hope and became a tested, time-bounded procedure.

### Monitoring & Security

Observability ran on **CloudWatch** and **CloudTrail** for metrics, logs, and audit, with **X-Ray** tracing WordPress REST API performance and **Slack** integration for real-time ops alerts. Security was built in from day one with **AWS WAF**, **Security Hub**, and Prowler checks against CIS and AWS FSBP benchmarks.

## Results

The migration delivered measurable improvements across capacity, reliability, and delivery speed:

- **5x concurrent-user capacity** — from ~2,000 to 10,000+ users, stable through peak traffic.
- **~99% uptime**, holding steady during the traffic spikes that used to cause outages.
- **~90% faster deployments** — from 2-3 hours down to ~15 minutes.
- **Validated DR** — RTO 6h / RPO 1h confirmed against AWS standards, with backup time cut ~85%.
- **Faster recovery** — mean time to recovery under 15 minutes, enabled by monitoring and automatic rollback.

The move to AWS raised raw infrastructure cost by roughly 20-30% versus the previous local vendor, but eliminated vendor lock-in, removed hidden scaling and support costs, and — through pay-as-you-go pricing and savings plans — put cost under the team's control. Against the gains in performance, resilience, and operational efficiency, it was a clear net win, and it freed the client to focus on content and growth instead of firefighting infrastructure.

## Key Learnings

1. **Adopt IaC early** — Terraform gave us consistent, reproducible environments and made every change reviewable from the start.
2. **CI/CD pays for itself fast** — automated pipelines with quality gates removed the human error and hours that the old SFTP process baked in.
3. **Resilience has to be measured, not assumed** — running a Resilience Hub assessment and testing the runbooks turned "we think we can recover" into defined, validated RTO/RPO numbers.
4. **Managed services buy focus** — leaning on Beanstalk, RDS, and EFS removed operational toil so the team could concentrate on the product.
5. **Security from day one is cheaper than retrofitting** — baking WAF, Security Hub, and least-privilege IAM into the design avoided a costly hardening pass later.
