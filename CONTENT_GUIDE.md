# Content Management Guide

This guide explains how to add and manage blog posts, case studies, tags, categories, and images for your portfolio site.

## Table of Contents

- [Blog Posts](#blog-posts)
- [Case Studies](#case-studies)
- [Categories](#categories)
- [Tags](#tags)
- [Images](#images)
- [Search](#search)

---

## Blog Posts

Blog posts are stored in `src/content/blog/` as Markdown files.

### Creating a New Blog Post

1. Create a new `.md` file in `src/content/blog/`
2. Name it using kebab-case (e.g., `my-new-post.md`)
3. Add the required frontmatter at the top

### Blog Post Template

```markdown
---
title: "Your Blog Post Title"
description: "A brief description of your post (appears in cards and SEO)"
pubDate: 2024-01-27
updatedDate: 2024-01-28  # Optional - only if you update the post
heroImage: "/images/blog/my-post/hero.jpg"  # Optional
category: "devops"  # Required - see categories below
tags: ["kubernetes", "docker", "automation"]  # Optional array
draft: false  # Set to true to hide from production
---

Your blog content goes here in Markdown format.

## Subheading

Regular paragraph text with **bold** and *italic* formatting.

- Bullet points
- Another point

### Code Examples

\`\`\`typescript
const example = "code block";
\`\`\`

> Blockquotes look like this

[Links](https://example.com) work as expected.
```

### Blog Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `title` | Yes | string | Post title |
| `description` | Yes | string | Brief description for SEO and cards |
| `pubDate` | Yes | date | Publication date (YYYY-MM-DD) |
| `updatedDate` | No | date | Last update date |
| `heroImage` | No | string | Path to hero image |
| `category` | Yes | enum | One of the valid categories |
| `tags` | No | string[] | Array of tag strings |
| `draft` | No | boolean | Hide from production if true |

---

## Case Studies

Case studies are stored in `src/content/case-studies/` as Markdown files.

### Creating a New Case Study

1. Create a new `.md` file in `src/content/case-studies/`
2. Name it using kebab-case (e.g., `company-project.md`)
3. Add the required frontmatter

### Case Study Template

```markdown
---
title: "Project Title - What You Accomplished"
client: "Company Name"
industry: "Finance / Healthcare / Technology / etc."
duration: "6 months"
role: "Lead DevOps Engineer"
challenge: "A brief description of the main challenge or problem"
solution:
  - "First key solution or approach"
  - "Second key solution"
  - "Third key solution"
outcomes:
  - metric: "99.9%"
    description: "System uptime achieved"
  - metric: "60%"
    description: "Reduction in deployment time"
  - metric: "$500K"
    description: "Annual cost savings"
technologies:
  - "Kubernetes"
  - "Terraform"
  - "AWS"
  - "Python"
heroImage: "/images/case-studies/project-name/hero.jpg"  # Optional
category: "cloud-migration"  # Required - see categories below
pubDate: 2024-01-15
featured: true  # Optional - highlights on homepage
---

## Overview

Detailed description of the project, context, and background.

## The Challenge

Expand on the specific challenges faced...

## Our Approach

Detailed explanation of the solution...

## Results

More details about the outcomes and impact...

## Key Learnings

What was learned from this project...
```

### Case Study Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `title` | Yes | string | Project title |
| `client` | Yes | string | Client/company name |
| `industry` | Yes | string | Industry sector |
| `duration` | Yes | string | Project duration |
| `role` | Yes | string | Your role on the project |
| `challenge` | Yes | string | Brief challenge description |
| `solution` | Yes | string[] | Array of solution points |
| `outcomes` | Yes | object[] | Array of {metric, description} |
| `technologies` | Yes | string[] | Technologies used |
| `heroImage` | No | string | Path to hero image |
| `category` | Yes | enum | One of the valid categories |
| `pubDate` | Yes | date | Publication date |
| `featured` | No | boolean | Feature on homepage |

---

## Categories

Categories are predefined and must match exactly.

### Blog Categories

| Value | Display Name | Description |
|-------|--------------|-------------|
| `devops` | DevOps | CI/CD, automation, tooling |
| `cloud` | Cloud | AWS, Azure, GCP, cloud architecture |
| `security` | Security | DevSecOps, compliance, security practices |
| `ai` | AI & ML | AI, machine learning, GenAI |
| `leadership` | Leadership | Team management, strategy |
| `automation` | Automation | Scripts, workflows, efficiency |

### Case Study Categories

| Value | Display Name | Description |
|-------|--------------|-------------|
| `cloud-migration` | Cloud Migration | Moving to cloud infrastructure |
| `devops-transformation` | DevOps Transformation | CI/CD and DevOps adoption |
| `ai-automation` | AI Automation | AI-powered solutions |
| `security` | Security | Security implementations |

### Adding New Categories

To add a new category, edit `src/content/config.ts`:

```typescript
// For blog categories
const blogCategories = ['devops', 'cloud', 'security', 'ai', 'leadership', 'automation', 'new-category'] as const;

// For case study categories
const caseStudyCategories = ['cloud-migration', 'devops-transformation', 'ai-automation', 'security', 'new-category'] as const;
```

Then update the display labels in:
- `src/components/CategoryNav.astro`
- `src/components/BlogCard.astro`
- `src/pages/blog/category/[category].astro`

---

## Tags

Tags are free-form strings - you can use any tag you want.

### Best Practices for Tags

1. **Use lowercase** - `kubernetes` not `Kubernetes`
2. **Use hyphens for multi-word tags** - `ci-cd` not `CI/CD`
3. **Be consistent** - Always use `aws` not sometimes `AWS`
4. **Keep them specific** - `terraform` is better than `iac`
5. **Limit to 3-5 tags per post** - More focused is better

### Common Tags

```
# Cloud Providers
aws, azure, gcp, digitalocean

# Containers & Orchestration
kubernetes, docker, helm, k8s

# Infrastructure
terraform, ansible, pulumi, cloudformation

# CI/CD
github-actions, jenkins, gitlab-ci, argocd

# Languages
python, go, typescript, bash

# Practices
devops, devsecops, gitops, sre

# AI/ML
genai, llm, machine-learning, rag
```

### How Tags Work

- Tags are displayed on blog cards and post pages
- Clicking a tag goes to `/blog/tag/[tag-name]`
- Tags are shown in the filter section on the blog index
- Tags are indexed by Pagefind for search

---

## Images

Images should be stored in the `public/images/` directory.

### Directory Structure

```
public/
  images/
    blog/
      my-post-slug/
        hero.jpg
        diagram-1.png
        screenshot.png
    case-studies/
      project-slug/
        hero.jpg
        architecture.png
        results-chart.png
    certs/
      aws-devops.png
      gcp-architect.png
    companies/
      company-name.svg
```

### Image Guidelines

| Type | Recommended Size | Aspect Ratio | Format | Notes |
|------|-----------------|--------------|--------|-------|
| Blog Hero | 1200x675px | 16:9 | JPG/WebP | Matches card aspect ratio |
| Case Study Hero | 1200x675px | 16:9 | JPG/WebP | Matches card aspect ratio |
| OG/Social Share | 1200x630px | ~1.91:1 | JPG | For social media previews |
| In-content images | Max 1200px wide | Variable | PNG/JPG | Optimize for web |
| Diagrams | Variable | Variable | PNG/SVG | SVG preferred for diagrams |
| Logos | 200x200px | 1:1 | SVG/PNG | SVG preferred |

### Referencing Images

In frontmatter:
```yaml
heroImage: "/images/blog/my-post/hero.jpg"
```

In Markdown content:
```markdown
![Alt text description](/images/blog/my-post/diagram.png)
```

### Image Optimization Tips

1. **Compress images** before adding - use tools like:
   - [Squoosh](https://squoosh.app/)
   - [TinyPNG](https://tinypng.com/)

2. **Use WebP format** when possible for smaller file sizes

3. **Provide alt text** for accessibility

4. **Keep file sizes under 200KB** for hero images

---

## Search

The site uses [Pagefind](https://pagefind.app/) for static search.

### How Search Works

1. Search indexes are built during `npm run build`
2. Only content marked with `data-pagefind-body` is indexed
3. Blog posts and case studies are automatically indexed

### Building Search Index

```bash
# Build the site and generate search index
npm run build

# The search index is created in dist/pagefind/
```

### Search Page

The search page is at `/search` and includes:
- Full-text search across all content
- Results show title, excerpt, and link
- Search tips and browse sections

---

## Quick Reference

### Adding a Blog Post

```bash
# 1. Create the file
touch src/content/blog/my-new-post.md

# 2. Add frontmatter and content (see template above)

# 3. Add images (optional)
mkdir -p public/images/blog/my-new-post
# Add your images to this folder

# 4. Preview
npm run dev
# Visit http://localhost:4321/blog/my-new-post

# 5. Build and verify search
npm run build
npm run preview
```

### Adding a Case Study

```bash
# 1. Create the file
touch src/content/case-studies/project-name.md

# 2. Add frontmatter and content (see template above)

# 3. Add images (optional)
mkdir -p public/images/case-studies/project-name
# Add your images to this folder

# 4. Preview
npm run dev
# Visit http://localhost:4321/case-studies/project-name

# 5. Build and verify
npm run build
npm run preview
```

### File Naming Convention

- Use **kebab-case** for all file names
- The filename becomes the URL slug
- Examples:
  - `kubernetes-best-practices.md` → `/blog/kubernetes-best-practices`
  - `acme-cloud-migration.md` → `/case-studies/acme-cloud-migration`

---

## Troubleshooting

### Post Not Showing Up

1. Check `draft: false` in frontmatter
2. Verify the category is valid
3. Check for frontmatter syntax errors
4. Restart the dev server

### Images Not Loading

1. Verify the path starts with `/images/`
2. Check file exists in `public/images/`
3. Verify file extension matches exactly (case-sensitive)

### Search Not Finding Content

1. Run `npm run build` to regenerate index
2. Verify `data-pagefind-body` is on the content container
3. Check that the page isn't marked as draft

### Category/Tag Page 404

1. For categories: verify it's in the `blogCategories` or `caseStudyCategories` array
2. For tags: tags are auto-generated, just use them in posts
3. Run `npm run build` to generate all static pages
