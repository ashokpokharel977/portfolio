---
title: "Re-Architecting a High-Volume SMS Platform for Scale & Cost"
client: "A high-volume messaging (SMS) platform"
industry: "Communications / FinTech"
duration: "3 months"
role: "Cloud / DevOps Architect"
challenge: "The application and every worker process ran together on a single host, and a sudden CPU spike forced a costly vertical bump from a t3.2xlarge to an m5.4xlarge just to stay online. The platform needed true horizontal auto-scaling and a handle on cost, without downtime for a service sending and receiving multiple messages per second."
solution:
  - "Split the application and worker processes onto separate auto-scaling node groups sitting behind a single shared load balancer"
  - "Designed a VPC with public/private subnet separation, keeping the load balancer, database, and compute in private subnets and routing egress through a NAT gateway"
  - "Moved to immutable AMI deployments built with Packer, promoted by updating the Auto Scaling launch configuration to the new image"
  - "Centralized logging and monitoring with the CloudWatch agent, custom queue-depth metrics per worker type, alarms, and dashboards"
  - "Encrypted configuration with AWS KMS, decrypted at boot via an instance IAM role, and enabled CloudTrail for audit"
  - "Applied FinOps cost optimization: EC2 Spot for low-priority workers, plus Savings Plans and Reserved Instances for the stable baseline"
outcomes:
  - { metric: "Up to 72%", description: "Projected EC2 savings from Savings Plans vs on-demand pricing on the committed baseline" }
  - { metric: "Single-host", description: "Bottleneck eliminated by separating application and worker tiers onto independent node groups" }
  - { metric: "Horizontal", description: "Auto-scaling replaces reactive vertical instance bumps under load" }
  - { metric: "Zero-downtime", description: "Deploys via immutable AMIs rolled through Auto Scaling, with centralized observability" }
technologies: ["EC2 Auto Scaling", "AWS", "Packer", "Spot Instances", "Savings Plans", "FinOps", "CloudWatch", "AWS KMS", "RabbitMQ", "Celery"]
heroImage: "/images/case-studies/sms-platform-autoscaling-cost.webp"
category: "devops-transformation"
pubDate: 2024-11-01
featured: false
---

## Project Overview

The platform is a high-volume SMS service that sends and receives multiple messages per second across several channels. It had grown up on a single AWS host, with the application server and every background worker packed onto the same instance. That worked until it didn't. My engagement was a re-architecture: take a design that had already hit its ceiling and redraw it around horizontal auto-scaling, centralized observability, and disciplined cost control, all without interrupting live traffic.

This was a design and cost-optimization effort. The numbers below are the targets the architecture was built to hit, not post-launch measurements, and I've framed them that way throughout.

## The Challenge: Single-Host Bottleneck

Almost every service in the platform is stateless, which is good news for scaling, but the deployment topology didn't take advantage of it. The application server and all of the worker processes ran together inside one host. Workers were managed by Supervisor and fed by a RabbitMQ broker, with several worker classes competing for the same CPU: a high-throughput delivery worker, a push-notification worker, a priority queue, and a couple of general workers.

The failure mode was predictable. A spike in CPU usage saturated the box, and the only lever available was to make the box bigger. The instance had already been bumped from a `t3.2xlarge` to an `m5.4xlarge` to absorb one such spike. That's vertical scaling as a reflex, and it's both expensive and finite. There was no way to add capacity to just the part of the system that was under pressure, and no isolation between the application handling inbound and outbound messages and the workers grinding through queues.

The objectives were clear:

- Make the platform genuinely auto-scalable
- Serve both messaging channels through a single load balancer
- Separate worker nodes from the application (management) nodes
- Encrypt configuration with KMS
- Centralize logging and monitoring on CloudWatch

## Solution: Distributed, Auto-Scaling Architecture

### Network Layer

I laid the platform out across a VPC with public and private subnets. The private subnet holds the load balancer targets, the database, the application node, and the worker nodes, so nothing that processes messages is directly exposed. The public subnet carries a NAT gateway, which lets instances in the private subnet reach the internet for outbound calls and updates without accepting inbound connections. A single load balancer fronts the whole thing and routes to the right node group, which satisfied the requirement to serve both messaging channels without standing up duplicate infrastructure.

### Application & Worker Separation

The core of the re-architecture was splitting one host into two roles:

- **Application node** — runs the application core components and serves traffic behind the load balancer.
- **Worker nodes** — all worker classes (the delivery worker, push-notification worker, priority queue, and general workers) grouped and deployed onto their own node group.

Because the workers now live on separate, independently scalable nodes, a queue backlog scales the worker tier without touching the application tier, and a traffic surge scales the application tier without starving the workers. The single-host contention that forced the `m5.4xlarge` bump simply stops being a single point of pressure. For compute, the design targets compute-optimized C5 instances for the application and worker tiers, with a general-purpose T-family instance for the lighter management node.

### Immutable AMI Deployments

Deployments are immutable. On each change, Packer bakes a new AMI containing the code and all dependencies, and a lifecycle rule prunes older images so they don't accumulate. Promotion is a matter of pointing the Auto Scaling launch configuration at the new image ID and rolling the group. There's no in-place mutation of running hosts, which is what makes zero-downtime deploys realistic: new instances come up on the new image and old ones drain out behind the load balancer. An S3 bucket holds build artifacts and logs.

### Logging & Monitoring

Every host runs the CloudWatch agent, shipping custom log files and metrics into CloudWatch Logs. The piece that matters most for a queue-driven system is queue visibility: I pushed custom per-worker queue metrics into CloudWatch (one per worker class) so scaling decisions and alarms react to actual backlog rather than just CPU. On top of that sit the alarms and dashboards, a mix of standard-resolution and a few high-resolution alarms for the metrics that need faster reaction, plus dashboards for at-a-glance health.

### Security

Configuration is encrypted with AWS KMS and decrypted at OS boot using the instance's IAM role, so secrets never sit in plaintext in the image or the repo. CloudTrail records API and user activity across the account for audit. Keeping compute in private subnets, as described in the network layer, rounds out the posture.

### Cost Optimization / FinOps

Cost was a first-class design constraint, not an afterthought. Three levers, applied deliberately:

- **Spot for low-priority workers** — the workers that can tolerate interruption run on EC2 Spot. Interruptions are handled gracefully by watching the Spot interruption event and having Auto Scaling replace the instance ahead of reclamation, so business operations stay smooth while capturing Spot's discount.
- **Savings Plans on the baseline** — committing usage in dollars-per-hour on the stable baseline is projected to cut EC2 cost by up to 72% versus on-demand, sized against the current EC2 bills.
- **Reserved Instances later** — RIs are the right move once the workload is proven stable and predictable. The recommendation was to ship the design, measure real efficiency, then commit RIs where the usage pattern justifies it.

## Outcomes

Because this was a re-architecture and cost design, these are the targets the platform was built to achieve:

- **Up to 72% EC2 savings** on the committed baseline through Savings Plans versus on-demand, with Spot layered on for interruptible workers.
- **Single-host bottleneck eliminated** by separating the application and worker tiers onto independent auto-scaling node groups.
- **Horizontal auto-scaling** in place of reactive vertical instance upgrades, so capacity follows load per tier.
- **Zero-downtime deploys and centralized observability** via immutable Packer AMIs rolled through Auto Scaling, with per-worker queue metrics, alarms, and dashboards in CloudWatch.

## Key Learnings

1. **Vertical scaling is a warning light, not a fix.** Bumping the instance size buys time and hides the real problem, which is that unrelated workloads share one failure domain. Separating tiers is what actually solves it.
2. **Scale on the metric that matters.** For a queue-driven system, CPU is a lagging signal. Custom queue-depth metrics let the worker tier scale on backlog, which is the thing customers actually feel.
3. **Design cost in from the start.** Spot, Savings Plans, and Reserved Instances each fit a different part of the workload. Matching the commitment model to the predictability of each tier is where the real savings live, and it's a decision that belongs in the architecture, not a cleanup pass afterward.
4. **Immutable infrastructure makes zero-downtime deploys boring.** Baking an AMI and rolling the Auto Scaling group turns a deploy into a capacity swap behind the load balancer, which is exactly what you want it to be.
