---
title: "Foundation Models and Large Language Models"
---

# Chapter 2: Foundation Models and Large Language Models

## Why it matters

Chapter 1 introduced foundation models and LLMs as the engines of generative AI.
This chapter opens the engine. We compare foundation models with the traditional
machine learning you may already know, walk through the **transformer**
architecture and the **attention** mechanism that made modern LLMs possible, and
end with a clear-eyed look at where these models break down. Understanding the
architecture is not academic: it explains why prompts work the way they do, why
context windows matter, and why some models are better at understanding while
others are better at generating.

## A quick review of traditional ML

Traditional machine learning trains a model on **task-specific data** to do one
job well. The workflow is familiar:

- The model is trained on data curated for a single task.
- Training usually starts from scratch.
- You choose among model families, tree-based models, linear models, neural
  networks, depending on the problem.
- The result is optimized for one task (classification, regression, clustering)
  and is hard to adapt to even a similar task.

Recall the basic vocabulary. In supervised learning you have **features** (the
input columns, such as number of logins or whether a customer watched a video)
and a **label** (the thing you predict, such as whether the customer signed up).
The learning algorithm starts from a random function `f` and refines it until the
features reliably predict the correct label.

```{list-table} A toy supervised dataset
:header-rows: 1
:widths: 25 25 25 25

* - Number of logins
  - Watched video
  - Number of purchases
  - Label: signed up
* - 120
  - Yes
  - 4
  - Yes
* - 1
  - No
  - 0
  - No
* - 219
  - No
  - 12
  - Yes
```

## Foundation models change the workflow

Foundation models break the one-model-per-task pattern. The key difference is
**how** they are trained and adapted.

```{list-table}
:header-rows: 1
:widths: 50 50

* - Traditional ML
  - Foundation models
* - Train on **labeled** data, then deploy.
  - **Pre-train** on huge **unlabeled** data, then **adapt**.
* - One model per task.
  - One model adapted to many tasks (text generation, summarization,
    information extraction, Q&A, chatbot).
* - Needs curated labels for every task.
  - Learns general structure first; little or no task-specific labeling needed
    to adapt.
```

A foundation model is pre-trained once on broad data and then adapted to
downstream tasks, by prompting or light fine-tuning, rather than retrained from
scratch each time. That is why the number and capability of LLMs has grown so
quickly over the past several years: progress on the base model lifts every task
at once.

## The transformer architecture

The breakthrough that made today's LLMs practical is the **transformer**,
introduced in the 2017 paper *Attention Is All You Need*
{cite}`vaswani2017attention`. To see why it mattered, start with the problem it
solved.

### Sequence-to-sequence problems

Many language tasks map an input sequence to an output sequence where both can
vary in length, machine translation ("They are watching" to "Ils regardent"),
or auto-completion. Earlier models processed sequences one token at a time, which
was slow and tended to forget information from earlier in long inputs.

### Encoder-decoder and the context vector

The classic design has two halves. An **encoder** reads the input and compresses
it into a numerical representation, sometimes called a **context vector**. A
**decoder** then reads that representation and produces the output sequence one
token at a time. Transformers were originally built as encoder-decoder models in
exactly this shape.

### Attention is the key idea

The transformer's central innovation is the **attention mechanism**. Attention
lets the model, when processing any given word, look at *all* the other words in
the observable input and weigh how relevant each one is to the current
prediction.

```{admonition} Intuition for attention
:class: tip
In the sentence "The animal didn't cross the street because *it* was too tired,"
what does "it" refer to? Attention lets the model associate "it" strongly with
"animal" rather than "street." It assigns high, medium, and low attention weights
across the sentence so that the most relevant tokens influence the next
prediction the most.
```

Both the encoder and decoder use attention, and they use **multi-headed**
attention, several attention computations in parallel, so the model can capture
different kinds of relationships at once. Two consequences follow that you should
remember:

- **Parallel processing.** Unlike older sequential models, transformers process
  all input tokens in parallel, which makes training on huge datasets feasible.
- **Positional encoding.** Because tokens are processed together rather than in
  order, the model adds **positional information** to each token's embedding so it
  still knows word order.

### Three architectural flavors

Not every model uses both halves of the transformer. Which half a model keeps
determines what it is good at.

```{list-table}
:header-rows: 1
:widths: 22 30 48

* - Architecture
  - Examples
  - Best for
* - **Encoder-only**
  - BERT, ELECTRA
  - Natural language *understanding*: classification, named entity recognition,
    text extraction. Uses **bi-directional** attention (sees the whole input).
* - **Decoder-only**
  - GPT, Llama, Claude
  - Text *generation*. **Auto-regressive**: each token can only see tokens that
    came before it, and the model generates the next token from that history.
* - **Encoder-decoder**
  - Original transformer, T5
  - Sequence-to-sequence tasks such as translation and summarization.
```

The decoder-only family is the one behind most chat and generation systems on
Bedrock, and it is the architecture we lean on for the rest of the book.

### Why transformers won

Pulling the threads together, the transformer is the state-of-the-art deep
learning architecture for generative AI because it:

- processes input in parallel rather than sequentially,
- uses self-attention to capture relationships between all words regardless of
  position,
- typically learns through **self-supervised learning**, generating labels
  automatically from unlabeled text, so there is no need to hand-curate labels,
  and
- generalizes beyond language to computer vision, audio, reinforcement learning,
  and multimodal applications.

```{admonition} AWS in practice
:class: note
You rarely implement a transformer yourself when working with Bedrock; the
provider has already trained it. But the architecture explains the knobs you do
control. The **context window** (how much text the model can attend to at once)
is a direct consequence of attention. The difference between an *embedding* model
like Titan Embeddings (encoder-style, understanding) and a *generative* model
like Titan Text (decoder-style, generation) maps onto the flavors above.
```

## Challenges and limitations of LLMs

Powerful as they are, LLMs have real limits. Designing responsibly, the focus of
Module 2, starts with knowing them.

**Reliability and bias.** A model's knowledge is limited to its training data. It
cannot reliably tell truth from falsehood and can reproduce biases present in
that data.

**Context window.** The model's attention is bounded by its context window.
Anything beyond that length is invisible to the model. For example, an early
Titan Premier model had a 30,000-token limit at release. Inputs longer than the
window must be truncated, chunked, or retrieved selectively, which is one
motivation for retrieval augmented generation in Module 3.

**Copyright and intellectual property.** Training data may include sensitive or
copyrighted material, and a model can generate content resembling someone's
creative or intellectual property, raising ethical and legal questions.

**Misinformation and privacy.** Models can generate sensitive or personal data
and can create or amplify misinformation about people, groups, or organizations.

**System cost.** Training large models demands enormous compute, specialized
talent, and power. Models with more than 100 billion parameters can carry total
project costs over 100 million dollars.

**Environmental impact.** That compute has a carbon footprint. By one cited
estimate, the CO2 emissions from training a five-billion-parameter model on GPUs
are roughly equivalent to a trans-American flight.

```{admonition} A useful unit: the token
:class: tip
LLMs read and write **tokens**, not characters or words. A rough rule of thumb is
that one token is about four characters of English, so roughly 100 tokens equals
about 75 words. Tokens are the unit you are billed in and the unit the context
window is measured in, so the concept reappears throughout the book.
```

## In the news

Two architecture-driven trends dominate recent headlines. First, **context
windows have expanded dramatically**, from a few thousand tokens to hundreds of
thousands and beyond in leading models, easing (though not eliminating) the
context-window limitation above. Second, the **cost and efficiency conversation
has matured**: techniques such as quantization and smaller, well-trained models
now deliver strong performance at a fraction of the compute, and providers
increasingly publish model cards documenting capabilities and limitations. Both
trends trace directly back to the transformer's attention mechanism and the
economics of scale described in this chapter.

## Hands-on labs

With the architecture in hand, the Module 1 labs become much easier to read.
{doc}`labs/Lab-2/lab2a-introduction-to-amazon-bedrock` shows how to invoke
different Bedrock foundation models with Boto3, and
{doc}`labs/Lab-2/lab2b-chat_amazon_bedrock` builds a simple conversational
application on top of a decoder-only model.

## Key takeaways

- Traditional ML trains one model per task; foundation models pre-train once and
  adapt to many tasks.
- The **transformer** uses **attention** to relate every token to every other
  token, processes input in parallel, and learns through self-supervision.
- **Encoder-only** models excel at understanding, **decoder-only** at generation,
  and **encoder-decoder** at sequence-to-sequence tasks.
- LLMs are limited by reliability, bias, the context window, IP and privacy
  risks, cost, and environmental impact, all of which motivate later modules.

Next, we turn from how models work to how you direct them: prompt engineering.
