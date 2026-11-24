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

```{image} ../_static/figures/bk_finetune_vs_rag.*
:alt: Fine-tuning trains a base model on 100 to 1,000 examples into a new specialized model, while RAG feeds current data into the prompt of the same unchanged model
:width: 95%
:align: center
:class: anim-fig
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

```{image} ../_static/figures/bk_rag.*
:alt: RAG in two parts, indexing documents into chunks, embeddings, and a vector database, then answering a question by a cleaned query, similarity search, rerank, augment, and generate
:width: 95%
:align: center
:class: anim-fig
```

```{admonition} Worked example: a return-policy bot
:class: note
A user asks "What is the company's return policy?" The system generates a
retrieval query ("Amazon's return policy in the USA"), embeds it, retrieves the
matching passage ("Return policy: 15 days after purchase..."), augments the prompt
with that passage, and the LLM composes a grounded answer, citing real policy
text rather than guessing.
```

### Knowledge graphs and GraphRAG

Similarity search finds passages that sound like the question. It struggles when the answer depends on relationships spread across many documents, such as which suppliers of a failed part also serve another plant. **GraphRAG** adds a **knowledge graph**, a store of entities and the relationships between them, to retrieval. Amazon Bedrock Knowledge Bases has offered GraphRAG since March 2025: during ingestion a foundation model extracts entities and relationships from your documents, and the service stores the graph alongside the embeddings in Amazon Neptune Analytics ([AWS](https://aws.amazon.com/about-aws/whats-new/2025/03/amazon-bedrock-knowledge-bases-graphrag-generally-available)). At query time it runs a vector search for the relevant chunks, then follows graph links to related entities and passages, which gives the model connected context and makes the answer easier to trace. The current limits include Amazon S3 as the only data source and no options to customize how the graph is built ([AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-build-graphs.html)). The {doc}`../primer/ai-concepts-assistants-effort` places knowledge graphs in the wider family of symbolic and semantic AI.

```{admonition} Security view
:class: warning
Everything retrieval returns enters the prompt, so a document can carry instructions as well as facts. A poisoned page in the knowledge base can tell the model to ignore its rules or to send data somewhere, which is **indirect prompt injection**. Treat retrieved text as data: filter retrieval by the user's own permissions so the model never sees documents the user may not read, keep write access to the knowledge base as tight as write access to code, and check the output before it leaves. The companion textbook covers these controls ([The Output Channel as an Exfiltration Path](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#the-output-channel-as-an-exfiltration-path)) and when to use RAG instead of fine-tuning from a security point of view ([Choosing Between RAG and Fine-Tuning](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#choosing-between-rag-and-fine-tuning-knowledge-versus-behavior)).
```

## Keeping retrieval healthy: golden queries, retrieval shift, and embedding drift

A RAG system can fail without any error message. A document is replaced, an index rebuild drops a shard, or users start asking about a topic the knowledge base never covered, and the answers quietly get worse. Three cheap checks catch most of this.

- **Golden queries** are test queries whose correct source document you know. Run them after every index rebuild or restore and track recall@k, the share whose correct document appears in the top k results.
- **Retrieval shift** compares which documents come back for your most common queries today with a saved baseline. A sudden change for a handful of popular queries, with nothing changed in the source collection, is a sign that someone has planted documents tuned to those queries, one of the poisoning risks described in Module 2.
- **Embedding drift** compares the distribution of incoming query embeddings with a baseline window. A large shift means users are asking about something new, which may need new content rather than a new model.

The code below runs all three on random vectors that stand in for real embeddings. One document is silently replaced, an attacker plants three documents tuned to each of six popular queries, and in a later week users shift toward a new topic.

```python
import numpy as np

rng = np.random.default_rng(3)
docs = rng.normal(size=(200, 16))
docs /= np.linalg.norm(docs, axis=1, keepdims=True)

def top_k(index, q, k=5):
    return list(np.argsort(index @ q)[::-1][:k])

# 1. Golden queries: queries whose correct document is known
golden = {i: docs[i] + rng.normal(scale=0.15, size=16) for i in range(0, 200, 20)}
def golden_recall(index):
    return np.mean([doc_id in top_k(index, q) for doc_id, q in golden.items()])

print(f"golden-query recall@5, clean index:    {golden_recall(docs):.2f}")
poisoned = docs.copy()
poisoned[40] = rng.normal(size=16)            # one document silently replaced
poisoned[40] /= np.linalg.norm(poisoned[40])
print(f"golden-query recall@5, tampered index: {golden_recall(poisoned):.2f}")

# 2. Retrieval shift: overlap of top-5 results for common queries, before and after
common = [rng.normal(size=16) for _ in range(30)]
injected = poisoned.copy()
for q in common[:6]:                           # attacker plants 3 documents tuned to each of 6 popular queries
    q = q / np.linalg.norm(q)
    for _ in range(3):
        d = q + rng.normal(scale=0.05, size=16)
        injected = np.vstack([injected, d / np.linalg.norm(d)])
overlap = [len(set(top_k(docs, q)) & set(top_k(injected, q))) / 5 for q in common]
print(f"mean top-5 overlap across 30 common queries: {np.mean(overlap):.2f}")
print(f"queries whose results changed by 40% or more: {sum(o <= 0.6 for o in overlap)}")

# 3. Embedding drift: distance between this week's and the baseline's mean query embedding
topic, new_topic = rng.normal(size=16), rng.normal(size=16)
baseline = topic + rng.normal(scale=1.0, size=(500, 16))
this_week = topic + rng.normal(scale=1.0, size=(500, 16))
shifted = 0.6 * topic + 0.4 * new_topic + rng.normal(scale=1.0, size=(500, 16))  # users start asking about a new topic
def drift(a, b):
    ma, mb = a.mean(0), b.mean(0)
    return 1 - ma @ mb / (np.linalg.norm(ma) * np.linalg.norm(mb))
print(f"drift (cosine distance of means), normal week:  {drift(baseline, this_week):.2f}")
print(f"drift (cosine distance of means), shifted week: {drift(baseline, shifted):.2f}")
```

```text
golden-query recall@5, clean index:    1.00
golden-query recall@5, tampered index: 0.90
mean top-5 overlap across 30 common queries: 0.87
queries whose results changed by 40% or more: 6
drift (cosine distance of means), normal week:  0.00
drift (cosine distance of means), shifted week: 0.34
```

Golden-query recall fell from 1.00 to 0.90 because the one replaced document was a golden query's answer. The planted documents left the average overlap high, 0.87, which is why the per-query count matters: exactly the six targeted queries changed by 40 percent or more. Drift between two normal weeks is essentially zero, while the shifted week moves to 0.34. On Amazon Bedrock, the RAG evaluation jobs described in Module 2 can score retrieval relevance and coverage with an LLM judge; these checks are the cheap, continuous complement you run between those jobs. The cybersecurity textbook's section on [monitoring and responding to AI incidents](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#monitoring-and-responding-to-ai-incidents) covers what to do when one of them fires.

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
- **GraphRAG** adds a knowledge graph of entities and relationships to vector
  search. Retrieved text is untrusted input: filter it by the user's permissions
  and guard against indirect prompt injection.

Next, we let models act, not just retrieve, with agents.
