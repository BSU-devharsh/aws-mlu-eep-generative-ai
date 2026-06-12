---
title: "Introduction to Generative AI"
---

# Chapter 1: Introduction to Generative AI

> "Generative models are a key enabler of machine creativity, allowing machines
> to go beyond what they've seen before and create something new."
> — Ian Goodfellow

## Why it matters

Most machine learning you have likely met before is **discriminative**: it takes
an input and predicts a label, such as "spam or not spam" or "cat or dog."
**Generative** AI does something qualitatively different. It produces new
content, text, images, audio, code, that resembles its training data but did not
exist before. This shift from *predicting* to *creating* is what makes the
technology feel new, and it is why a single model can now draft an email,
summarize a contract, answer a question, and write code.

This chapter sets up the whole book. It introduces the two ideas that everything
else rests on, foundation models and large language models, surveys what people
actually use these models for, and shows how Amazon Bedrock turns them into
something you can call from an application with a few lines of code.

## Foundation models

A **foundation model** is a large machine learning model that is pre-trained on
vast amounts of data and can then be adapted to many more specialized tasks. The
word "foundation" is deliberate: the model is a base you build on rather than a
finished solution for one narrow problem.

Two properties make foundation models distinctive:

- **They are pre-trained on huge, broad datasets.** Rather than learning one task
  from a small curated dataset, they absorb general structure from data at web
  scale.
- **They can be trained on any kind of data.** Text, images, video, and audio can
  all serve as training signal, which is why the same family of techniques powers
  chatbots, image generators, and speech systems.

```{admonition} Definition
:class: tip
A **foundation model** is a large model pre-trained on broad data that can be
adapted (through prompting or fine-tuning) to a wide range of downstream tasks.
```

## Large language models

A **large language model (LLM)** is a foundation model trained on text. At its
core, an LLM is a very large statistical model that learns the probabilities of
words appearing in particular contexts. Its training task is deceptively simple:
predict a missing or next word in a sequence.

Consider the sentence:

> "The weather has been cloudy for the last two days. Most likely it will be
> ____ tomorrow."

To fill the blank well (*cloudy? sunny? foggy?*), the model must pick up grammar,
facts, and a little common-sense reasoning, all from the single objective of
predicting text. Scaled up over enormous datasets, this next-word objective is
enough to produce models that write fluently, answer questions, and follow
instructions.

### How big are these models?

State-of-the-art models are genuinely enormous. To make the scale concrete, the
largest models are comparable in size to:

- a 474-million-page document,
- 35 hours of 4K video, or
- a codebase with 80 billion lines of code.

That scale has a cost. Training a frontier model can require hundreds of people
and exceed 100 million dollars in compute. We return to these costs, and their
environmental impact, in {doc}`02-foundation-models-and-llms`.

## What LLMs are used for

LLMs are not a single product; they are a general capability that shows up across
many domains, education, healthcare, customer service, marketing, finance, and
law among them. The most common application patterns are worth naming because
the rest of the book keeps coming back to them.

**Conversational chatbots.** Interactive applications that hold human-like,
context-aware dialogue, remember earlier turns, and answer follow-up questions.
These power virtual assistants and support agents.

**Interactive training and education.** Rapid generation of personalized,
multilingual learning content, slides, exercises, quizzes, and tailored
explanations for a specific audience.

**Creative assistants.** Prompt-based generation of written content, art, and
music, where the user steers the output with natural-language instructions and
sometimes images or audio.

**Productivity tools.** Automating routine work: drafting and summarizing
documents, generating and commenting code, writing test cases, and drafting or
auto-completing email.

**Data analytics.** Surfacing hidden patterns in data (sentiment, topics,
personally identifiable information), interpreting charts, generating reports,
and creating synthetic data for testing.

```{admonition} Worked example: from task to pattern
:class: note
Suppose a retailer wants to (a) answer customer questions, (b) summarize product
reviews, and (c) write product descriptions. Rather than building three separate
ML systems, all three map onto one LLM through different prompts: a *chatbot*
prompt, a *summarization* prompt, and a *text-generation* prompt. Recognizing
which pattern a business problem fits is the first design skill in generative AI.
```

## Amazon Bedrock

Knowing what LLMs can do raises a practical question: how do you actually use one
without standing up a cluster of GPUs? This is the gap **Amazon Bedrock** fills.

Amazon Bedrock is a fully managed service that makes foundation models available
through a single API. Instead of hosting models yourself, you call an endpoint
and pay for what you use. Bedrock offers models from several providers behind a
consistent interface, including:

```{list-table}
:header-rows: 1
:widths: 30 70

* - Provider
  - Example model family
* - Amazon
  - Titan
* - AI21 Labs
  - Jurassic-2
* - Anthropic
  - Claude
* - Cohere
  - Command
* - Meta
  - Llama
```

What makes Bedrock attractive for real applications is not just convenience but
governance:

- You can **privately customize** foundation models with your own data.
- You can **integrate models into applications** using familiar AWS tools without
  provisioning or managing infrastructure.
- Your **prompts and responses are not shared** with AWS or third-party model
  providers.
- Bedrock adds **security capabilities** such as encryption, identity and access
  management (IAM), and a range of compliance designations.

### Amazon Titan models

Amazon's own family on Bedrock is **Titan**. Titan is positioned around
responsible, high-performing models and comes in two flavors that you will use
repeatedly:

- **Titan Text** is a generative model for summarization, text generation (for
  example, drafting a blog post), classification, open-ended question answering,
  and information extraction.
- **Titan Embeddings** translates text into numerical vectors, *embeddings*, that
  capture the semantic meaning of the text. Embeddings are the backbone of search
  and personalization, and they reappear in {doc}`05-multimodal-prompting` and in
  Module 3's chapter on retrieval augmented generation.

### Common Bedrock use cases

The service documentation groups Bedrock use cases into a handful of recurring
shapes, which line up neatly with the LLM applications above:

- **Text generation:** create original content such as stories, posts, and pages.
- **Chatbots:** build conversational assistants.
- **Search:** find and synthesize answers from a large corpus.
- **Text summarization:** condense articles, books, and documents.
- **Image generation:** create images from language prompts.
- **Personalization:** deliver more relevant, contextual recommendations than
  simple word matching.

## In the news

Generative AI moved from research demos to mainstream tooling remarkably fast.
Amazon Bedrock became generally available in 2023 and has steadily expanded the
catalog of models it offers, adding newer Anthropic Claude versions, Meta Llama
models, and Amazon's own Titan and later Nova models. Two broader trends frame
this chapter:

- **Managed access is the norm.** The industry has converged on consuming
  foundation models as managed API services rather than self-hosting, which is
  exactly the pattern Bedrock embodies.
- **Capability is generalizing.** The same underlying models increasingly handle
  text, images, and code together, foreshadowing the multimodal chapter at the
  end of this module.

Because this field changes monthly, always check the
[Amazon Bedrock documentation](https://docs.aws.amazon.com/bedrock/) for the
current list of available models and features.

## Hands-on labs

The labs for Module 1 begin with Amazon Bedrock. In the console-based Lab 1 (see
the source repository) you make predictions with foundation models directly, and
in {doc}`labs/Lab-2/lab2a-introduction-to-amazon-bedrock` you call Bedrock
programmatically with Boto3. Read this chapter first, then open the labs from
{doc}`labs-overview`.

## Key takeaways

- Generative AI *creates* new content rather than only classifying inputs.
- A **foundation model** is pre-trained on broad data and adapted to many tasks;
  an **LLM** is a foundation model trained on text whose core skill is predicting
  the next word.
- Frontier models are enormous and expensive to train, which is why most teams
  consume them as a service.
- **Amazon Bedrock** provides foundation models from multiple providers through
  one secure, managed API, with **Amazon Titan** as Amazon's own text and
  embedding models.

In the next chapter we open up the model itself: what foundation models are made
of, how the transformer architecture works, and where LLMs fall short.
