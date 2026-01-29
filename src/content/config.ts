import { defineCollection, z } from 'astro:content';

// Define category enums
const blogCategories = ['devops', 'cloud', 'security', 'ai', 'leadership', 'automation'] as const;
const caseStudyCategories = ['cloud-migration', 'devops-transformation', 'ai-automation', 'security'] as const;

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    category: z.enum(blogCategories),
    draft: z.boolean().default(false),
  }),
});

const caseStudiesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    client: z.string(),
    industry: z.string(),
    duration: z.string(),
    role: z.string(),
    challenge: z.string(),
    solution: z.array(z.string()),
    outcomes: z.array(z.object({
      metric: z.string(),
      description: z.string(),
    })),
    technologies: z.array(z.string()),
    heroImage: z.string().optional(),
    category: z.enum(caseStudyCategories),
    pubDate: z.date(),
    featured: z.boolean().default(false),
  }),
});

export const collections = {
  blog: blogCollection,
  'case-studies': caseStudiesCollection,
};

// Export types for use in components
export type BlogCategory = typeof blogCategories[number];
export type CaseStudyCategory = typeof caseStudyCategories[number];
export const BLOG_CATEGORIES = blogCategories;
export const CASE_STUDY_CATEGORIES = caseStudyCategories;
