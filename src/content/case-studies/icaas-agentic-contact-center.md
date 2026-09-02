---
title: "ICAAS: Agentic Contact Center on Amazon Connect"
client: "A multi-strategy hedge fund"
industry: "Financial Services / Asset Management"
duration: "4 months"
role: "AI Solution Architect"
challenge: "Customer service scaled linearly with headcount, and a lean investor-relations and operations team was drowning in repetitive, high-touch inquiries — account lookups, balance checks, KYC and document requests. Manual handling created compliance exposure, and clients across time zones had no after-hours coverage."
solution:
  - "Stood up an Amazon Connect contact flow with an embedded chat widget as the customer entry point, wiring both self-service and agent-assist AI agents on session creation"
  - "Routed every inbound message through Amazon Lex V2 (QInConnectIntent) into an orchestration AI agent that drives autonomous, multi-turn conversation"
  - "Built self-service and agent-assist experiences on Amazon Q in Connect, backed by Bedrock Claude for reasoning and natural-language dialogue"
  - "Exposed 16 domain MCP tools through a Bedrock AgentCore Gateway — CRM lookup, portfolio API, trade blotter, persist-conversation, and a human-in-the-loop relay"
  - "Embedded domain-specific compliance guardrails so the agent never leaks cross-customer data, with every turn persisted to Aurora Serverless v2 (PostgreSQL)"
  - "Added human-in-the-loop supervisor steering and seamless escalation that hands off the full conversation with zero context loss, surfaced in an embedded agent workspace app"
  - "Packaged the entire ~120-resource stack — Connect, Lex, Q, AgentCore, Aurora, workspace app — behind a single AWS CDK deploy command"
outcomes:
  - { metric: "<10s", description: "End-to-end response time for autonomous inquiries, from customer message to answer" }
  - { metric: "24/7", description: "Autonomous coverage — routine inquiries resolved end-to-end with no human in the loop and no after-hours gap" }
  - { metric: "~120", description: "AWS resources provisioned and configured from a single AWS CDK deploy command" }
  - { metric: "Zero", description: "Context loss on escalation — the human agent inherits the full transcript, tool calls, and AI findings" }
technologies: ["Amazon Connect", "Amazon Bedrock", "Bedrock AgentCore", "Amazon Lex", "Amazon Q", "Claude", "MCP", "GenAI", "AWS CDK", "Aurora Serverless", "PostgreSQL"]
heroImage: "/images/case-studies/ai-automation.svg"
category: "ai-automation"
pubDate: 2025-10-01
featured: true
---

## Overview

The client is a multi-strategy hedge fund managing multi-billion-dollar AUM, with a small investor-relations and operations team serving both institutional and individual limited partners. That team was the bottleneck: every account lookup, balance check, and document request landed on the same handful of people, and there was no coverage once the office closed.

I worked as the AI Solution Architect to design and deliver ICAAS — an agentic contact center built on Amazon Connect that handles routine investor inquiries autonomously. Bedrock Claude drives the conversation, real-time data flows through MCP tools, compliance guardrails keep customer data isolated, and anything the AI can't finish escalates cleanly to a human with the full context intact. The whole stack deploys into the client's own AWS account from a single command.

## The Problem: Customer Service That Doesn't Scale

Growing businesses hit the same wall: customer inquiries scale linearly with headcount. For this fund, the symptoms were specific and expensive:

- **Repetitive high-touch work** — Account lookups, balance checks, document requests, and status updates were the same workflows repeated hundreds of times a month.
- **Specialized people as bottlenecks** — Domain experts spent the majority of their time on routine questions, so strategic work got sidelined.
- **Compliance risk in manual processes** — Manual tracking leaves gaps, and in a regulated environment those gaps are exactly what audits find.
- **No after-hours coverage** — LPs in different time zones simply waited until the next business day.

The goal was not to replace the team but to take the operational load off it — resolve the routine inquiries autonomously, and hand the genuinely hard ones to a human who arrives already caught up.

## How It Works

The path from customer to resolution follows a consistent flow:

1. **The customer connects via a chat widget.** Amazon Connect creates a contact. The inbound flow spins up a Q in Connect session and wires both the self-service and agent-assist AI agents.
2. **Lex routes to the orchestrator.** Amazon Lex V2, using a `QInConnectIntent`, routes every message to the orchestration AI agent, which runs the multi-turn conversation autonomously.
3. **The orchestrator calls MCP tools.** It reaches real-time data through the Bedrock AgentCore Gateway — CRM lookup, portfolio API, trade blotter, persist-conversation, and the HITL relay — 16 tools in total.
4. **The session escalates or completes.** Return-to-Control tools hand back to the contact flow: escalation sets a queue and transfers with full context; completion closes the session cleanly.
5. **A human picks up in the agent workspace.** On escalation, the human agent receives the contact with Connect's AI assist panel and the embedded ICAAS workspace app showing the entire transcript.

## Architecture

### Contact Flow

Amazon Connect is the front door. The chat widget creates a contact, and the inbound flow creates the Q in Connect (Wisdom) session, wires agent-assist, and hands control to Lex V2. Lex's `QInConnectIntent` forwards each turn to the orchestrator; Return-to-Control tools bring the conversation back to the flow to either escalate — setting the queue and transferring with context — or complete.

### Q in Connect AI Agents

Two AI agents run on Amazon Q in Connect: a **self-service orchestrator** that carries the autonomous customer conversation, and an **agent-assist agent** that supports the human once a contact escalates. Both are driven by Bedrock Claude behind carefully scoped orchestration prompts, so the agent reasons over live data rather than reciting canned responses.

### AgentCore Gateway & MCP Tools

The orchestrator's connection to the business lives behind a Bedrock AgentCore Gateway that exposes 16 MCP tools, backed by Lambda targets and grouped by capability — CRM lookup, portfolio API, and trade blotter for reads, plus `persist_conversation` and the HITL relay for state and supervision. Structuring the integration as MCP tools means the same pattern re-skins to any vertical: swap the toolset, keep the orchestration.

### Data Plane & Human-in-the-Loop

Every turn of every conversation is persisted to Aurora Serverless v2 (PostgreSQL) through `persist_conversation`. That persistent record is what makes supervision possible: a supervisor watches active sessions live, and `check_supervisor_instructions` lets the orchestrator pull in injected guidance mid-conversation and weave it into the dialogue. Human oversight becomes a steering wheel, not just a kill switch.

### Agent Workspace

Human agents work from a unified desktop. The Connect CCP handles voice and chat, the Connect assistant panel provides MCP-powered AI answers to natural-language questions, and the ICAAS workspace app — embedded in Agent Workspace via SDK and scoped per contact — shows the full AI transcript with every tool call expandable to its input and output. A supervisor dashboard sits alongside it for live monitoring across sessions.

### Infrastructure & CDK

The entire platform is defined as AWS CDK. One deploy command provisions roughly 120 resources and configures them end to end: the Connect instance, contact flow, and Lex bot; the Q in Connect assistant with its two AI agents and prompts; the AgentCore Gateway with its Lambda targets and 16 MCP tools; Aurora Serverless v2 with auto-migration and seed data; the agent desktop on S3 and CloudFront with the workspace app; security profiles and MCP tool permissions; and gateway and identity observability. The stack runs in a private VPC with KMS, Secrets Manager, and CloudWatch. The client owns all of it — infrastructure, data, and agents.

## What ICAAS Adds Beyond Native Connect

Native Connect gives you the contact center; ICAAS makes the AI layer transparent and governable.

- **Customer ↔ AI is no longer a black box.** Native Connect surfaces nothing about the AI conversation until escalation. ICAAS persists every turn to PostgreSQL as it happens.
- **Supervisors get a live view.** Instead of waiting for a handoff, a supervisor sees the running transcript, the tool calls, and sentiment in real time.
- **Human-in-the-loop steering is possible.** A supervisor can inject guidance mid-conversation and the AI incorporates it — something native Connect can't do at all.
- **Escalation carries real context.** Rather than a one-line summary, the human inherits the full picture: who the customer is, what they asked, what the AI found, and where it got stuck.
- **The agent workspace is richer.** Beyond a basic screen pop, the embedded workspace app gives the agent the entire conversation panel scoped to the contact.

## Results

- **Sub-10-second end-to-end responses** on autonomous inquiries — fast enough that the AI conversation feels like a well-briefed human, not a bot.
- **24/7 autonomous coverage** — routine inquiries are resolved end to end, day or night, with no human in the loop and no after-hours gap.
- **~120 AWS resources from one command** — the full stack deploys reproducibly into the client's own account, so there's no bespoke, hand-assembled environment to maintain.
- **Zero-context-loss escalation** — when a conversation does reach a human, they arrive already caught up, which is what makes the handoff feel seamless to the customer.

## Key Learnings

1. **Persistence is the foundation, not a feature.** Writing every turn to Aurora up front is what unlocked live supervision, HITL steering, and rich escalation. The transparency layer only exists because the data was captured from the first message.
2. **Model the integration as MCP tools.** Exposing the business through 16 MCP tools behind an AgentCore Gateway kept the orchestrator clean and made the platform re-skinnable per vertical — swap the toolset, keep the orchestration.
3. **Guardrails are non-negotiable in regulated domains.** Compliance rules that keep customer data isolated had to be built into the agent's behavior, not bolted on. In a hedge fund, a cross-customer data leak isn't a bug — it's an incident.
4. **Autonomy and human oversight aren't opposites.** The system resolves the routine load on its own, but the supervisor's ability to watch, steer, and take over is exactly what made it safe to run autonomously in the first place.
5. **One-command deployment changes the sales conversation.** Because the whole stack stands up from a single CDK command into the client's own account, ICAAS is something a client owns outright — infrastructure, data, and AI agents — rather than a service they rent.
