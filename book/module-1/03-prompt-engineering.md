---
title: "Prompt Engineering"
---

# Chapter 3: Prompt Engineering

This chapter covers the craft of writing input that gets good output from a model. It names the parts of a prompt, explains the inference parameters that shape generation, lists best practices, and shows how examples in a prompt let a model learn a task on the spot.

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

The figure below labels the four parts of the example prompt and adds the inference parameters that the next section describes.

```{image} ../_static/figures/bk_prompt_anatomy.*
:alt: A prompt built from four labeled parts, context, instruction, input, and output format, flows into an LLM whose temperature, top-p, and maximum-token settings shape a bulleted response
:width: 95%
:align: center
:class: anim-fig
```

```{admonition} Definition
:class: tip
**Prompt engineering** is the systematic design and optimization of prompts to
guide an LLM's response so that outputs are accurate, relevant, and coherent.
```

Four things are worth internalizing about prompt engineering as a discipline:

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
  - Controls randomness. Near `T = 0` the model almost always picks the most
    likely token; higher temperatures produce more varied text. Even `T = 0` is
    not perfectly repeatable on a shared service (see below).
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
Ask a model to *Write a tagline for a coffee shop.* At `T = 0` you will get
nearly the same safe tagline every time, useful when you need consistency, such
as classification. At `T = 0.9` you will get varied, surprising taglines on each
run, useful for brainstorming. Choosing temperature is therefore a task decision,
and the sections below show how to make it with evidence.
```

### How temperature works

At every step the model gives each token in its vocabulary a score, a **logit**
$z_i$. Temperature $T$ divides every logit before the softmax turns the scores
into probabilities:

$$p_i = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}}$$

- $T = 1$ leaves the model's own distribution unchanged.
- $T < 1$ sharpens the distribution toward the top token. As $T$ approaches 0,
  sampling becomes **greedy decoding**: always take the top token.
- $T > 1$ flattens the distribution and gives unlikely tokens more chances.

Temperature never changes the order of the tokens, only the gaps between them.
The name comes from statistical physics, where the same formula, the Boltzmann
distribution, describes how heat spreads particles across energy states.

The code below applies five temperatures to one made-up next-token distribution
for the prompt *The capital of France is*, measures how spread out each
distribution is (its entropy, in bits), and draws 10,000 samples at each
setting. It then applies three truncation filters, explained in the next
section, at temperature 1.5.

```python
# Temperature, top-k, top-p, and min-p on one next-token distribution (no API calls)
import numpy as np

tokens = ["Paris", "Lyon", "France", "the", "a", "Marseille", "Berlin", "banana"]
logits = np.array([6.0, 3.5, 3.0, 2.0, 1.5, 1.0, 0.0, -2.0])   # model scores for the next token

def softmax(z, temperature=1.0):
    z = np.asarray(z, dtype=float) / temperature
    e = np.exp(z - z.max())                    # subtract the max for numerical stability
    return e / e.sum()

def entropy_bits(p):
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())

rng = np.random.default_rng(42)
print("temperature  P(Paris)  entropy(bits)  in 10,000 samples: distinct tokens, times banana")
for t in [0.2, 0.7, 1.0, 1.5, 2.0]:
    p = softmax(logits, t)
    draws = rng.choice(len(tokens), size=10_000, p=p)
    print(f"{t:>11}  {p[0]:8.3f}  {entropy_bits(p):13.2f}  {len(set(draws)):>20}  {int((draws == 7).sum()):>11}")
print("top token at every temperature:", {t: tokens[int(np.argmax(softmax(logits, t)))] for t in [0.2, 1.0, 2.0]})

# Truncation filters, applied after temperature 1.5
p = softmax(logits, 1.5)
order = np.argsort(p)[::-1]
top_k = set(order[:3])                                           # keep the 3 most likely
cum = np.cumsum(p[order])
top_p = set(order[: int(np.searchsorted(cum, 0.90)) + 1])       # smallest set reaching 90 percent
min_p = {i for i in range(len(p)) if p[i] >= 0.10 * p.max()}     # keep tokens at least 10 percent as likely as the top one
for name, kept in [("top-k (k=3)", top_k), ("top-p (p=0.9)", top_p), ("min-p (0.1)", min_p)]:
    print(f"{name:14} keeps {[tokens[i] for i in sorted(kept, key=lambda i: -p[i])]}")
```

```text
temperature  P(Paris)  entropy(bits)  in 10,000 samples: distinct tokens, times banana
        0.2     1.000           0.00                     1            0
        0.7     0.954           0.34                     7            0
        1.0     0.854           0.88                     8            4
        1.5     0.666           1.68                     8           29
        2.0     0.526           2.16                     8           89
top token at every temperature: {0.2: 'Paris', 1.0: 'Paris', 2.0: 'Paris'}
top-k (k=3)    keeps ['Paris', 'Lyon', 'France']
top-p (p=0.9)  keeps ['Paris', 'Lyon', 'France', 'the']
min-p (0.1)    keeps ['Paris', 'Lyon', 'France']
```

At 0.2 the model is effectively greedy: Paris every time and zero entropy. At
1.0, the model's own distribution, seven alternatives appear and the absurd
*banana* is drawn 4 times in 10,000; at 2.0 it is drawn 89 times. Higher
temperature buys variety at the cost of more poor picks, and in a long answer one
poor token can derail everything after it. Paris stays the top token at every
temperature, which explains the most common misconception below: lowering the
temperature cannot fix a model whose most likely answer is wrong.

### Top-k, top-p, and min-p

Truncation filters remove the unlikely tail before sampling, so that a higher
temperature can add variety without adding nonsense.

- **Top-k** keeps the *k* most likely tokens {cite}`fan2018hierarchical`. A fixed
  *k* is too generous when the model is confident and too strict when many tokens
  are plausible.
- **Top-p**, or **nucleus sampling**, keeps the smallest set of tokens whose
  probabilities add up to *p* {cite}`holtzman2020curious`. Holtzman and colleagues
  introduced it after showing that sampling from the full distribution produces
  incoherent text, while always taking the most likely tokens produces bland,
  repetitive text.
- **Min-p** keeps every token that is at least a set fraction as likely as the
  top token, so the cutoff tightens when the model is confident and loosens when
  it is not {cite}`nguyen2025minp`. It was an oral paper at ICLR 2025 and is
  built into open-source libraries such as Hugging Face Transformers and vLLM.
  Managed APIs, including Bedrock, generally expose temperature, top-p, and
  sometimes top-k, but not min-p.

In the lab, top-k with *k* = 3 and min-p of 0.1 keep Paris, Lyon, and France,
while top-p of 0.9 also keeps *the*. Because temperature and top-p both reshape
the same distribution, most providers recommend adjusting one of them, not both.

### Ranges and defaults

Ranges and defaults differ by provider and model, and the newest reasoning models
increasingly fix them. The values below come from each provider's documentation
as of November 2026. Check the model card before you rely on them.

```{list-table}
:header-rows: 1
:widths: 26 24 50

* - Model or API
  - Temperature
  - Notes
* - Amazon Bedrock Converse API (`inferenceConfig`)
  - 0 to 1; the default is each model's own
  - `topP` is 0 to 1. Model-specific settings such as top-k go in
    `additionalModelRequestFields`
    ([AWS](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InferenceConfiguration.html)).
* - Anthropic Claude on Bedrock
  - 0 to 1, default 1
  - `top_p` defaults to 0.999 and `top_k` is off by default, up to 500. Claude
    Sonnet 4.5 and Haiku 4.5 accept `temperature` or `top_p`, not both
    ([AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages-request-response.html)).
* - Claude 4.7 and later models
  - Fixed
  - Non-default `temperature`, `top_p`, or `top_k` values return an error;
    Anthropic recommends steering the model through the prompt instead
    ([Anthropic](https://platform.claude.com/docs/about-claude/model-deprecations)).
* - Amazon Nova
  - 0.00001 to 1, default 0.7
  - `topP` defaults to 0.9 and `topK` (0 to 128) is off by default. Change
    `temperature` or `topP`, not both
    ([AWS](https://docs.aws.amazon.com/nova/latest/userguide/complete-request-schema.html)).
* - OpenAI Chat Completions
  - 0 to 2, default 1
  - OpenAI recommends changing `temperature` or `top_p`, not both, and notes that
    parameter support differs for reasoning models
    ([OpenAI](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)).
* - Google Gemini
  - 0 to 2, default 1.0
  - Google strongly recommends keeping Gemini 3 models at the default of 1.0
    ([Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)).
```

The same number does not mean the same thing across these rows. A temperature
of 0.7 is the Nova default but a mild setting on a scale that runs to 2, and
each model's logits are scaled differently, so tune per model rather than
copying a value from one to another.

### Choosing a temperature

The usual advice is a low temperature, 0 to 0.3, for extraction,
classification, code, and translation, and a higher one, 0.7 and up, for
brainstorming and creative writing. The evidence is more mixed than that advice
suggests.

- Renze tested nine models with five prompting techniques on multiple-choice
  problem solving and found that changing temperature from 0.0 to 1.0 had no
  statistically significant effect on accuracy {cite}`renze2024effect`.
- Peeperkorn and colleagues found that in story writing, temperature was only
  weakly correlated with novelty and moderately correlated with incoherence,
  far from the creativity dial it is often described as
  {cite}`peeperkorn2024temperature`.
- Li and colleagues tested temperatures from 0.1 to 1.9 on 12 open models.
  Instruction following held steady up to about 1.0 and then dropped sharply,
  translation did best near 0, and medium and large models did best near 1.3 on
  causal reasoning and creative tasks. Larger models were less sensitive to
  temperature overall {cite}`li2025hotcold`.

A practical rule follows. Start from the provider's default, or from a low value
for tasks with one right answer. Then measure a few settings on your own
evaluation set, as Module 2 describes, and keep the one that wins. Techniques
that depend on variety need a temperature above zero: **self-consistency**,
covered in the next chapter, samples several reasoning paths and takes the
majority answer, which only works if the paths differ.

### Common misconceptions

A few beliefs about inference parameters are widespread and wrong, and each one can lead to a bad design choice.

- **Temperature zero is deterministic.** It is greedy in principle, but hosted
  services batch your request with others and floating-point arithmetic depends
  on the order of operations, so the output can still vary, as the
  non-determinism discussion in the previous chapter shows. If you need
  repeatable results, store the outputs instead of regenerating them.
- **A lower temperature prevents hallucination.** It removes random detours, but
  if the model's most likely answer is wrong, temperature zero returns that wrong
  answer every time, fluently. Grounding with retrieval, guardrails, and
  evaluation address hallucination; temperature does not.
- **Temperature is the creativity setting.** It adds randomness, and randomness
  is not the same as originality, as the studies above show.
- **Change temperature and top-p together for fine control.** Providers advise
  changing one, and some newer models reject requests that set both.

### Setting temperature on Amazon Bedrock

With the Converse API, `temperature`, `topP`, `maxTokens`, and `stopSequences`
go in `inferenceConfig`, and model-specific settings go in
`additionalModelRequestFields`. The example below asks Amazon Nova 2 Lite to
classify a support ticket, a task with one right answer, so it sets a low
temperature and a small token limit.

```python
import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")
response = client.converse(
    modelId="us.amazon.nova-2-lite-v1:0",
    messages=[{"role": "user", "content": [{"text":
        "Classify this ticket as billing, technical, or account. "
        "Reply with one word. Ticket: I was charged twice this month."}]}],
    inferenceConfig={"temperature": 0.2, "maxTokens": 10},
)
print(response["output"]["message"]["content"][0]["text"])
```

For a model from Claude 4.7 onward, leave `temperature` out entirely and put
any instruction about style in the prompt.

### Temperature elsewhere in machine learning

The same division of logits by a temperature appears in two other places you
will meet.

- **Knowledge distillation** trains a small student model on a large teacher's
  outputs. Raising the teacher's softmax temperature produces softer targets
  that show which wrong answers the teacher found nearly right, and those soft
  targets carry more information for the student {cite}`hinton2015distilling`.
- **Temperature scaling** fits a single temperature on validation data so that a
  classifier's confidence scores match how often it is actually right. Guo and
  colleagues found it the most effective simple fix for overconfident modern
  networks, and it never changes which class the model predicts
  {cite}`guo2017calibration`.

Decoding settings are also a security concern: on self-hosted open models,
simply changing temperature, top-p, or top-k can undo safety training. The
cybersecurity textbook's section on
[sampling temperature and decoding](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#sampling-temperature-and-decoding-a-security-view)
covers that attack and how to control these settings in production.

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
- Remember the rule of thumb: ~1 token per 4 characters of English text, ~100 tokens per 75 words.

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

The points below are the core habits of good prompting.

- A prompt can contain an **instruction**, **context**, **input**, and **output
  format**; naming these helps you debug weak responses.
- **Inference parameters** (temperature, top-p, top-k, max tokens, stop
  sequences) shape generation without changing the model.
- **Temperature** divides the logits before the softmax: low values sharpen the
  distribution toward the top token, high values flatten it, and the ranking of
  tokens never changes. Top-k, top-p, and min-p trim the unlikely tail.
- Ranges and defaults differ by model, and the newest reasoning models fix them.
  Tune temperature on your own evaluation set, and do not count on temperature
  zero for repeatability or for preventing hallucination.
- Follow best practices: be clear, specific, positive, and structured, and expect
  to iterate. Respect each model's required prompt format.
- **In-context learning**, zero-, one-, and few-shot, adapts the model purely
  through the prompt, with no retraining.

Standard prompting takes you a long way, but hard, multi-step problems need more.
The next chapter introduces advanced prompting techniques for reasoning.
