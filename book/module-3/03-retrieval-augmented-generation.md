---
title: "Retrieval-Augmented Generation"
---

# Chapter 3: Retrieval-Augmented Generation

## Why it matters

Chapter 2 ended with a problem: you cannot fit all your knowledge into a prompt,
and even if you could, the model's training data is frozen and may be wrong.
**Retrieval-Augmented Generation (RAG)** is the dominant solution. It grounds a
model in external, up-to-date data by retrieving the relevant pieces and feeding
them into the prompt, no training required. This chapter covers grounding, the
RAG workflow and architecture, the vector databases and chunking that make it
work, and how RAG extends to images through multimodal embeddings.

## Grounding a model

**Grounding** is a set of techniques that make an LLM's output consistent with
established facts (mitigating hallucinations), common-sense reasoning, real-world
context, and user intent. It can be achieved through prompt engineering
(in-context learning), fine-tuning, RAG, and tools (with agents).

### Fine-tuning vs. RAG

Both adapt a model to a domain, but differently. **Fine-tuning** continues
pre-training on high-quality data, changing the model's weights to create a new,
specialized model. It needs relatively few but very high-quality examples
(~100-1,000), suits data that changes about annually, and on Bedrock requires no
code (upload CSVs to S3 and configure). Its weaknesses: poor fit for fast-changing
data (stock prices), inability to fix fundamental limitations like math, a
maintenance burden, and possible erosion of responsible-AI mitigations, requiring
re-evaluation for drift.

```{list-table}
:header-rows: 1
:widths: 22 39 39

* - Aspect
  - Fine-tuning
  - RAG
* - **Rationale**
  - Create a task-specific LLM.
  - Provide the LLM with task-specific context.
* - **How**
  - Adapt weights via gradient updates (training).
  - Retrieve relevant data from external sources while prompting.
* - **Unique value**
  - Retain knowledge *within* the model.
  - Retrieve current or fluctuating data.
* - **Example**
  - Fine-tune on academic content to build a virtual tutor.
  - Ask "Is it a good time to buy a company's stock?"
```

## Retrieval-Augmented Generation

RAG is an **in-context learning** technique that gives an LLM knowledge beyond its
training, with no training or fine-tuning. It has three steps:

1. **Retrieve** data from an external source.
2. **Augment** the prompt's context with the retrieved data.
3. **Generate** a response with the LLM, based on the prompt plus retrieved data.

The data can come from internal documents, logs, company policies, and more.

## The RAG workflow

### Document chunking

Long documents are split into **chunks** that fit the LLM's context window;
vectorized representations of those chunks are stored in a vector database. When
chunking, mind three knobs: **overlap** (for continuity between chunks), **chunk
size** (too small loses context, too large overflows the window), and
**separators**. LangChain offers text splitters such as `CharacterTextSplitter`,
`MarkdownHeaderTextSplitter`, and `RecursiveCharacterTextSplitter`.

### Vector database and similarity search

Retrieval requires fast fetching of relevant content. You store **embeddings** of
all chunks in a **vector database**, then convert the user's query to a vector and
perform a **similarity search** to find the closest chunks. (Embeddings and vector
databases were introduced in the {doc}`../primer/ai-and-tools-reference`.)

### Rerankers and recall

**Recall** is the LLM's ability to find the right information from everything
retrieved. One way to improve it is to retrieve *more* documents, but not all are
equally relevant. **Rerankers** are specialized models that score the relevance of
each document to the query, much more accurate than embedding models but slower.
This motivates **two-stage retrieval**: first retrieve candidates with embeddings,
then re-rank them for relevance.

### RAG architecture end to end

Putting it together, a query flows through five stages:

1. **Generate a query for retrieval** (a clean query, stripped of verbose prompt
   scaffolding like role-setting and output instructions).
2. **Convert the query to an embedding** using a common embedding model.
3. **Retrieve relevant info** from the vector database via similarity search.
4. **Augment** the prompt with the retrieved results.
5. **Generate** the final response with the LLM.

```{admonition} Worked example: a return-policy bot
:class: note
A user asks "What is the company's return policy?" The system generates a
retrieval query ("Amazon's return policy in the USA"), embeds it, retrieves the
matching passage ("Return policy: 15 days after purchase..."), augments the prompt
with that passage, and the LLM composes a grounded answer, citing real policy
text rather than guessing.
```

## Multimodal embeddings and multimodal RAG

RAG extends beyond text. Multimodal models face three classic challenges:
**representation** (efficiently encoding different modalities without redundancy),
**alignment** (relating elements across modalities, an image and its caption), and
**translation** (mapping one modality to another, where relationships are often
open-ended). **Multimodal embeddings** solve this by placing different modalities
in one **joint embedding space**, where similar objects, whether text or image,
sit close together and the model preserves semantic similarity within and across
modalities.

This enables **cross-modal retrieval**. Rather than describing every image in text
and doing lexical search (which fails when similar content lacks similar words),
**multimodal RAG** uses the same embedding model for both the vector database and
the query, so images can be used for retrieval, for prompting, or both.

```{admonition} AWS in practice
:class: note
Amazon Bedrock Knowledge Bases provides managed RAG: you connect a data source,
Bedrock handles chunking, embedding (with Titan or other embedding models), vector
storage, and retrieval, and returns answers with **citations** (the explainability
feature from Module 2). Titan multimodal embeddings power the cross-modal
retrieval above.
```

## In the news

RAG has become the default pattern for grounding enterprise LLMs, and the frontier
has moved to **agentic RAG**, systems that decide *when* and *what* to retrieve,
and **rerankers** and hybrid (keyword plus vector) search to boost precision.
Long-context models complement rather than replace RAG: retrieval keeps cost down
and provides the citations that make answers auditable.

## Hands-on labs

Implement RAG and multimodal RAG on Amazon Bedrock in
{doc}`labs/Lab-3/lab3a-retrieval_augmented_generation` and
{doc}`labs/Lab-3/lab3b-multimodal_rag`.

## Key takeaways

- **Grounding** aligns outputs with fact and context; **RAG** does it by retrieving
  external data into the prompt, with no training.
- RAG is **retrieve, augment, generate**, built on **chunking**, a **vector
  database**, **similarity search**, and optionally **rerankers**.
- **Fine-tuning** bakes knowledge into weights (slow-changing data); **RAG** fetches
  current data at query time.
- **Multimodal embeddings** put text and images in one space, enabling **multimodal
  RAG**.

Next, we let models act, not just retrieve, with agents.
