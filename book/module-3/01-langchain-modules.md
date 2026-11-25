---
title: "LangChain Modules"
---

# Chapter 1: LangChain Modules

This chapter introduces LangChain, the framework the Module 3 labs use to build applications from models. It covers the core modules, prompt templates, output parsers, and chains, and the memory that lets an application remember earlier turns.

## Why it matters

A single prompt is rarely a whole application. Real systems combine prompts,
models, output parsing, external data, memory, and control flow. **LangChain** is
one of the most popular frameworks for stitching these pieces together. This
chapter introduces LangChain, explains why it exists, and walks through its core
modules, prompt templates, output parsers, chains, and memory, which the rest of
Module 3 builds on.

## What is LangChain?

LangChain is a framework for developing applications powered by language models.
Its appeal rests on modular components, flexibility and scalability, and a long
list of third-party integrations. People use it for text generation,
summarization, conversational chatbots, code understanding, retrieval augmented
generation (RAG), and reasoning agents.

Four motivations explain why it caught on:

- **Prompt, don't train.** Capable existing LLMs can be adapted with prompts and
  scripts, which is cheaper and faster than training or fine-tuning, and
  compatible with existing APIs.
- **Standard interface.** Common interfaces let you switch between a growing set
  of models and providers without rewriting your application.
- **Orchestration.** As applications grow complex, LangChain connects components
  into controlled flows, looping until a goal is met, persisting data across
  stages, and including humans in the loop.
- **Observability and evaluation.** Tracing lets you observe outputs at every
  stage, test parts of an application without running the whole workflow, and
  measure latency, performance, and cost.

## Core modules

Three modules do most of the work in a LangChain application: a prompt template builds the input, the model generates, and an output parser shapes the result. Chains connect them.

### Prompt templates

A **prompt template** is a parameterized, reusable recipe for an LLM, a
pre-defined string with slots for instructions, context, and examples. It is
model-agnostic and reusable:

```python
# "Plan a three-day itinerary for a trip to {city}." with city = "Paris"
```

### Output parsers

Output parsers convert an LLM's raw text into structured formats, for example
`StrOutputParser`, `JsonOutputParser`, `XMLOutputParser`, and
`BooleanOutputParser`. They are essential when downstream code needs the output in
a specific shape.

### Chains and LCEL

Chains build complex applications by composing modules into a sequence of
calls to an LLM, a tool, and so on. The recommended way to write them is the
**LangChain Expression Language (LCEL)**, which composes components with a simple
pipe syntax and provides streaming, parallel execution, retries and fallbacks,
access to intermediate steps, and input/output schemas.

```python
# A simple LLM chain: prompt template -> model -> output parser
prompt_template = PromptTemplate.from_template("Tell me a {content_type} about {topic}.")
chain = prompt_template | llm | StrOutputParser()
chain.invoke({"content_type": "bedtime story", "topic": "a cat"})
# >> Once upon a time, there was a little black cat named Midnight...
```

You can connect multiple chains into a workflow, for instance a screenwriter chain
feeding a movie-critic chain feeding a social-media-manager chain, by matching
each chain's output variables to the next chain's inputs.

## Memory

LLMs are **stateless**: without a component to persist context, the model is
unaware of prior interactions. Ask it your name in a second prompt and it cannot
answer. **Memory** fixes this by maintaining information the LLM can refer to,
remembering past interactions and persisting context, roles, and rules. An
application with memory **retrieves** prior context, adds it to the prompt, gets a
response, and **writes** the new exchange back to memory.

The simplest form is **conversational (buffer) memory**, which stores every
interaction for perfect recall:

```python
memory = ConversationBufferMemory()
memory.save_context({"input": "Hi"}, {"output": "What's up?"})
memory.load_memory_variables({})
# >> {'history': 'Human: Hi\nAI: What's up?'}
```

Storing *everything* eventually overflows the context window, the problem Chapter
2 solves with smarter memory strategies.

The figure below shows a chain and its memory working together on one call.

```{image} ../_static/figures/bk_langchain_chain.*
:alt: An LCEL chain in which input variables fill a prompt template, a chat model on Amazon Bedrock generates a reply, and an output parser returns a string, while memory retrieves the conversation history into the prompt before the call and writes the new exchange back after it
:width: 95%
:align: center
:class: anim-fig
```

```{admonition} AWS in practice
:class: note
LangChain integrates with Amazon Bedrock through `langchain-aws`, so the chains and
memory above run on Bedrock models (Titan, Nova, Claude, Llama, and others) behind
LangChain's standard interface. Switching models is a one-line change, exactly the
"standard interface" benefit.
```

## In the news

LangChain has expanded from a library into an ecosystem, adding **LangGraph** for
building stateful, multi-step agent workflows as graphs and **LangSmith** for
tracing and evaluation, the "orchestration" and "observability" themes above made
into products. The broader trend is that composing LLM applications from reusable,
observable components has become standard engineering practice rather than an
experiment.

## Key takeaways

The points below summarize the LangChain building blocks used in the rest of this module.

- **LangChain** composes LLM applications from modular, swappable components and
  emphasizes prompting over training.
- Core modules are **prompt templates**, **output parsers**, **chains** (best
  written in **LCEL**), and **memory**.
- LLMs are **stateless**; memory persists context so applications can hold a
  conversation.
- LangChain runs on Amazon Bedrock models through a standard interface.

Next, we use these modules to build conversational applications.
