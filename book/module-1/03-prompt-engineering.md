---
title: "Prompt Engineering"
---

# Chapter 3: Prompt Engineering

## Why it matters

You now know what LLMs are and how transformers make them work. But a foundation
model on its own is inert; it does whatever your input tells it to. **Prompt
engineering** is the craft of writing that input well. Because the same model can
summarize, classify, translate, or chat depending only on the prompt, prompting
is the highest-leverage skill in applied generative AI: it is fast, requires no
training, and often makes the difference between an unusable answer and a great
one. This chapter covers the anatomy of a prompt, the **inference parameters**
that shape a model's output, best practices, and **in-context learning** with
zero-, one-, and few-shot examples.

## What is a prompt?

A **prompt** is the input you give a model to get a response, usually a
natural-language query. A good prompt does more than ask a question: it can
explain the task, set constraints, show examples, and specify the output format.
In short, the prompt carries your *intent* so the model can generate the response
you actually want.

### The components of a prompt

It helps to think of a prompt as having up to four parts. Consider this example:

> The following is a customer email received last week. Summarize the main points
> of the email in a bulleted list.
>
> To whom it may concern: Following up on our last meeting, we want to propose a
> few suggestions for faster production and delivery of our ordered products...
> Looking forward to hearing from you.

The parts are:

```{list-table}
:header-rows: 1
:widths: 22 78

* - Component
  - Role in the prompt above
* - **Instruction**
  - The task: "Summarize the main points... in a bulleted list."
* - **Context**
  - Background that guides the response: "The following is a customer email
    received last week."
* - **Input**
  - The data to act on: the body of the customer email.
* - **Output indicator / format**
  - The requested shape of the answer: a bulleted list.
```

Not every prompt needs all four, but naming them gives you a checklist. When an
answer disappoints, it is usually because one component is missing or ambiguous.

```{admonition} Definition
:class: tip
**Prompt engineering** is the systematic design and optimization of prompts to
guide an LLM's response so that outputs are accurate, relevant, and coherent.
```

Three things are worth internalizing about prompt engineering as a discipline:

- It is **iterative**. Finding the optimal prompt often takes several attempts.
- Prompt **quality and structure** significantly influence performance.
- Well-constructed prompts can **counteract hallucinations**.
- It is a **fast-moving field**, spanning everything from settled best practices
  to emerging research techniques (several of which appear in Chapter 4).

## Inference parameters

Beyond the words of the prompt, you control a set of **inference parameters**.
These shape how the model turns its internal probabilities into text. Crucially,
they do **not** change the model's architecture or weights; they only affect
generation at inference time. They control properties such as creativity and
diversity, the confidence of generation, response length, and when generation
stops.

```{list-table}
:header-rows: 1
:widths: 24 76

* - Parameter
  - What it does
* - **Temperature**
  - Controls randomness. `T = 0` makes the output deterministic (always the most
    likely token). Higher temperatures produce more diverse, creative text.
* - **Top-p (nucleus sampling)**
  - Selects the next word from the smallest set of tokens whose probabilities sum
    to *p*.
* - **Top-k**
  - Picks the next token from the top *k* tokens sorted by probability.
* - **Maximum tokens**
  - Caps the length of the generated response. Set too low, it can cut answers
    off mid-sentence.
* - **Stop sequences**
  - Strings that, when generated, halt further output.
```

```{admonition} Worked example: temperature in practice
:class: note
Ask a model to "Write a tagline for a coffee shop." At `T = 0` you will get the
same safe tagline every time, useful when you need consistency, such as
classification. At `T = 0.9` you will get varied, surprising taglines on each
run, useful for brainstorming. Choosing temperature is therefore a task decision:
low for deterministic, factual work; higher for creative work.
```

## Best practices in prompt engineering

A handful of practices reliably improve results across models and tasks:

- Write **clear and specific** instructions, unambiguous and precise.
- **Highlight or specify** the part of the prompt the model should focus on.
- Add **relevant details or restrictions**.
- **Separate** the instruction, content, question, and output directions (often
  with delimiters or line breaks).
- Prefer **positive instructions** ("respond in two sentences") over negative
  ones ("don't be verbose").
- Expect to **iterate**; the best prompt usually emerges over a few attempts.

### Instruction-tuned and model-specific prompts

LLMs are pre-trained on raw text, but most chat-capable models are additionally
**instruction-tuned**, fine-tuned to follow textual instructions, so they align
their output with user intent. Even so, **different models expect different prompt
formats**, and you should consult each model's card or documentation:

- Anthropic's Claude models were trained on alternating **Human / Assistant**
  dialogue, and prompts should replicate that turn structure.
- Some open models use special tokens (for example
  `<|prompter|>` and `<|assistant|>`) to mark parts of the prompt.

```{admonition} AWS in practice
:class: note
On Amazon Bedrock you call several model families through one API, but each still
has its own preferred prompt format. The Bedrock documentation and per-model
**model cards** specify these formats and the valid ranges for temperature,
top-p, top-k, and max tokens. When a Bedrock response looks off, check the model
card before rewriting your prompt: you may simply be using the wrong format or an
out-of-range parameter.
```

### Cost-effective prompting

API usage is billed by tokens, the length of the prompt plus the length of the
response, so prompt design is also cost design. Practical levers:

- **Control response length** with `max_new_tokens` and with instructions like
  "be concise" or "answer in less than 50 words."
- **Shorten or combine** prompts where possible.
- **Test cheaper models**; a smaller LLM is often good enough for simple tasks.
- Remember the rule of thumb: ~1 token per 4 characters, ~100 tokens per 75 words.

Two further inference strategies reduce cost and latency:

- **Quantization** loads model weights in a lower-precision data type, cutting
  memory and compute and speeding inference, usually with minimal performance
  loss.
- **Batch predictions** process many inputs together rather than one at a time,
  which is faster, especially on GPUs.

## In-context learning

The most important idea in this chapter is **in-context learning**: you adapt the
model's behavior *without updating its weights*, purely by what you put in the
prompt. You can supply instructions and, optionally, correct examples of the
task. There are three canonical settings, distinguished by how many examples you
provide.

### Zero-shot learning

Give only an instruction, no examples, and rely on the model's generalized
understanding from pre-training. This works for tasks the model was never
explicitly trained to do, such as translation or arithmetic reasoning, an
**emergent ability** of large models.

```text
Prompt:   Translate from English to Spanish
          cat =>
Output:   "gato"
```

### One-shot learning

Provide a single example alongside the instruction to show the model the desired
pattern.

```text
Prompt:   Complete the last sentence based on the example below
          sentence: cat is an animal
          sentence: table is
Output:   "a piece of furniture"
```

### Few-shot learning

Provide several examples so the model can identify the pattern and apply it.

```text
Prompt:   Complete the last sentence based on the examples below:
          sentence: cat is not a piece of furniture
          sentence: table is not an animal
          sentence: car is
Output:   "not a living thing"
```

```{admonition} Worked example: sentiment analysis, zero-shot with format control
:class: note
A common production pattern combines a clear instruction, an input, and an
explicit output format:

    Classify the following customer review as Positive or Negative.
    text: Best purchase ever! This kitchen robot is great!
    Format your response as a JSON object with text and class keys.

Output:

    {
      "text": "Best purchase ever! This kitchen robot is great!",
      "class": "Positive"
    }

Requesting JSON makes the output machine-parseable, the single most useful trick
for wiring an LLM into an application.
```

The same zero-shot recipe extends to summarization ("Summarize the following text
in one sentence"), personalized explanation ("Explain in-context learning to a
high-school student in 2-3 sentences"), code generation ("Write Python to read a
CSV file"), information extraction, and simple question answering.

## In the news

Prompt engineering has become a recognized professional skill, with model
providers, including AWS, publishing prompt-engineering guides and structured
prompt templates. At the same time, **structured output** has matured from a
prompting trick into a first-class feature: many models and APIs now support
returning validated JSON or tool-call arguments directly, building on the
JSON-formatting idea above. The throughline is that getting reliable, parseable
answers, which once depended entirely on clever wording, is increasingly
supported by the platform.

## Hands-on labs

Put these ideas to work in {doc}`labs/Lab-3/lab3-prompt-engineering`, which walks
through standard prompt-engineering techniques on Amazon Bedrock, varying
instructions, formats, and inference parameters, and observing how the output
changes.

## Key takeaways

- A prompt can contain an **instruction**, **context**, **input**, and **output
  format**; naming these helps you debug weak responses.
- **Inference parameters** (temperature, top-p, top-k, max tokens, stop
  sequences) shape generation without changing the model.
- Follow best practices: be clear, specific, positive, and structured, and expect
  to iterate. Respect each model's required prompt format.
- **In-context learning**, zero-, one-, and few-shot, adapts the model purely
  through the prompt, with no retraining.

Standard prompting takes you a long way, but hard, multi-step problems need more.
The next chapter introduces advanced prompting techniques for reasoning.
