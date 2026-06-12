---
title: "Multimodal Applications"
---

# Chapter 5: Multimodal Applications

## Why it matters

This final chapter brings the whole book together. You have models (Module 1),
responsible practices (Module 2), and application patterns, chains, chatbots, RAG,
and agents (Module 3). Now we combine them with the multimodal capability from
Module 1 to build applications that see, read, and act across text, images, and
video. This is where generative AI delivers its most visible business value.

## Why multimodal applications add value

Multimodal applications help businesses in four ways:

- **Improved accuracy and robustness**, from richer representations across
  multiple modalities.
- **Ease of development**, complex models but simpler applications.
- **Interactive, intuitive solutions**, interaction through natural media: text,
  speech, gestures.
- **Easy access to performant models**, you pay to use, not to pre-train, with a
  wide range of open-source and commercial choices by size, cost, and performance.

## Examples of multimodal applications

### Personalization

Multimodal models can automatically generate or update content for a target
audience, matching technical depth, providing relevant examples, setting document
or video length, using inclusive and accessible language, and generating
multilingual content. They also personalize *consumption*: users can interact with
documents, presentations, and videos through Q&A for summaries, explanations,
translations, and scene descriptions, enabling personalized, self-paced learning.

A concrete case is **scene description**, generating descriptions of visual
elements, **alt-text** for accessibility, and multilingual descriptions from
images, documents, and videos. Another is **personalized presentations**:
generating transcripts and notes tailored to each student or group, with examples
that appeal to the audience and minimal human supervision (proofing still
required).

### Video analysis

Multimodal models can **navigate** videos (jump to when a topic was introduced,
find all mentions of a concept, skip to the next topic), **summarize** them (whole
videos, per-concept, or within a time range), **personalize** consumption (detailed
or short explanations, supporting examples, multilingual Q&A for accessibility),
and **extract step-by-step instructions** from walkthrough videos to assist with
setup. Ultimately you can **chat directly with a video**, retrieving information
from the video itself, though extracting every detail with high recall is
challenging for some models.

### Customer service

Customers can describe an issue with text, images, or video, while a vector
database holds relevant resolution documents (user manuals, FAQs, troubleshooting
guides), a multimodal RAG application. Multimodal customer service can identify and
resolve complaints from textual feedback and from uploaded images or video, power
automated call support that gauges urgency and frustration from audio to decide on
escalation, and provide guided assistance over video calls.

### E-commerce and healthcare

In **e-commerce**: multimodal search engines, finding similar products by image,
text, or video, generating product listings from images or video, extracting
product information from labels, and generating images of products in different
scenes. In **healthcare** (with appropriate oversight and compliance, see the
{doc}`../primer/ai-literacy`): generating preliminary reports from scans against
patient records, assisting with triage, virtual diagnosis of minor ailments, and
generating personalized patient reports.

## Multimodal agents

The capstone pattern combines this chapter with the previous one: a **multimodal
agent** is an agent (Chapter 4) whose tools and reasoning span modalities. It can
accept an image or video as part of the request, retrieve across modalities
(multimodal RAG from Chapter 3), reason with the ReAct pattern, and call tools to
act, for instance, a customer-service agent that looks at a photo of a broken
device, retrieves the right manual page, and walks the user through a fix.

```{admonition} AWS in practice
:class: note
Everything here runs on Amazon Bedrock: multimodal models (Amazon Nova, Anthropic
Claude, and others) for understanding images and video, Titan multimodal
embeddings for cross-modal retrieval, Bedrock Knowledge Bases for multimodal RAG,
and Bedrock Agents for orchestration. The personalization, troubleshooting, and
multimodal-agent labs put these together.
```

## In the news

Multimodal applications are expanding fastest in **video understanding** and
**real-time, voice-driven assistants**, and multimodal agents that can perceive a
screen or camera and act are an active frontier. The business cases in this
chapter, accessibility, customer service, e-commerce, and education, are precisely
where early deployments are concentrating, because they turn the technical
capability of multimodality into measurable value.

## Hands-on labs

The Module 3 capstone labs implement personalization, troubleshooting, and
multimodal agents on Amazon Bedrock: see {doc}`labs/Lab-5/lab5a-personalization`,
{doc}`labs/Lab-5/lab5b-troubleshooting`, and
{doc}`labs/Lab-5/lab5c-multimodal_agents`.

## Key takeaways

- Multimodal applications add accuracy, ease of development, intuitive interaction,
  and access to performant models.
- Major patterns: **personalization** (scene description, tailored content),
  **video analysis**, **customer service**, **e-commerce**, and **healthcare**.
- A **multimodal agent** unites agents, multimodal RAG, and the ReAct loop across
  modalities.
- Amazon Bedrock provides the models, embeddings, knowledge bases, and agent
  orchestration to build all of these.

This completes the book. From the fundamentals of foundation models, through their
responsible use, to building real applications, you now have an end-to-end,
practical foundation in generative AI with Amazon Bedrock.
