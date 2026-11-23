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

## How a model learns: loss, gradients, and overfitting

Every model in this book, from a fraud classifier to a frontier LLM, is trained the same basic way. It is also, in practice, **narrow AI**: it does the tasks it was trained or prompted for, and no system in production today is general intelligence. Models also differ in what they learn. A **discriminative** model learns the boundary between classes so it can label inputs, such as spam or not spam. A **generative** model learns the distribution of its data so it can produce new samples, such as the next token of a sentence.

Training is a loop with four parts.

- **Loss function.** A single number that says how wrong the model's predictions are on the training data. Classifiers and language models use **cross-entropy loss**, which is small when the model gives high probability to the right answer and grows quickly when it is confidently wrong. An LLM's pretraining objective is exactly this: the cross-entropy of predicting each next token.
- **Gradient.** For each weight, the direction and size of change that would increase the loss fastest. Backpropagation computes all of these gradients at once.
- **Gradient descent.** Move every weight a small step against its gradient, then repeat. Each step lowers the loss a little.
- **Learning rate.** The size of each step. Too small and training crawls; too large and the weights overshoot, so the loss bounces or diverges. Most large models use **Adam**, an optimizer that adapts the step for each weight from running averages of its past gradients {cite}`kingma2015adam`.

At the output, a language model produces one raw score, a **logit**, for every token in its vocabulary. The **softmax** function turns those scores into probabilities that sum to 1. Dividing the logits by a **temperature** before the softmax is what the temperature setting described under non-determinism below does: a low temperature sharpens the distribution toward the top token, and a high one flattens it.

The code below trains a two-feature classifier with plain gradient descent at three learning rates, then applies softmax at three temperatures.

```python
import numpy as np

rng = np.random.default_rng(0)
# Toy task: predict sign-up (1) from two scaled features
X = rng.normal(size=(200, 2))
y = (X[:, 0] + 0.5 * X[:, 1] + rng.normal(scale=0.5, size=200) > 0).astype(float)

def softmax(logits, temperature=1.0):
    z = np.asarray(logits, dtype=float) / temperature
    z = z - z.max()                       # for numerical stability
    e = np.exp(z)
    return e / e.sum()

def cross_entropy(p, y):                  # p = predicted probability of class 1
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

def train(lr, steps=100):
    w, b = np.zeros(2), 0.0
    for _ in range(steps):
        p = sigmoid(X @ w + b)               # forward pass
        grad_w = X.T @ (p - y) / len(y)      # gradient of the loss
        grad_b = float(np.mean(p - y))
        w -= lr * grad_w                     # gradient descent step
        b -= lr * grad_b
    return cross_entropy(sigmoid(X @ w + b), y)

print(f"starting loss = {cross_entropy(np.full(200, 0.5), y):.3f}")
for lr in (0.01, 0.5, 500.0):
    print(f"learning rate {lr:>5}: loss after 100 steps = {train(lr):.3f}")

logits = [2.0, 1.0, 0.1]
for t in (0.5, 1.0, 2.0):
    print(f"softmax at temperature {t}: {np.round(softmax(logits, t), 3)}")
```

```text
starting loss = 0.693
learning rate  0.01: loss after 100 steps = 0.584
learning rate   0.5: loss after 100 steps = 0.293
learning rate 500.0: loss after 100 steps = 2.701
softmax at temperature 0.5: [0.864 0.117 0.019]
softmax at temperature 1.0: [0.659 0.242 0.099]
softmax at temperature 2.0: [0.502 0.304 0.194]
```

A loss of 0.693 is what a model that always says 50 percent would score. A learning rate of 0.01 is too timid to get far in 100 steps, 0.5 reaches a good fit, and 500 overshoots so badly that the loss ends far worse than where it started. At temperature 0.5 the top logit takes 86 percent of the probability; at temperature 2.0 it takes only half.

**Overfitting** is the main way training goes wrong. A model with enough capacity can memorize its training data, noise included, so training loss keeps falling while performance on new data gets worse. That is why data is split into a **training set** to learn from, a **validation set** to tune settings and decide when to stop, and a **test set** that is touched only once, for the final score. Early stopping, regularization, more data, and smaller models all reduce overfitting. The opposite, **underfitting**, means the model is too simple or trained too little to capture the pattern.

**Transfer learning** reuses a model trained on one task as the starting point for another, so the new task needs far less data and compute. Foundation models are transfer learning at a very large scale: pretraining learns general patterns once, and prompting, retrieval, or fine-tuning adapts them to your task, as the next section describes.

```{admonition} Security view
:class: note
The same gradients that train a model also attack it. An attacker who can compute or estimate gradients can nudge an input in the direction that most increases the loss, which is how adversarial examples are made. Overfitting is a privacy risk too: a model that memorized its training records leaks them through membership inference and extraction. The companion textbook covers both ([Adversarial Machine Learning](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#adversarial-machine-learning) and [Attacks on Models](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#attacks-on-models-inversion-extraction-membership-inference-and-poisoning)).
```

## The hardware underneath: GPUs, accelerators, and memory

Training and running neural networks is mostly multiplying large matrices, so the hardware that matters is the hardware that does many multiplications in parallel. **GPUs** do this with thousands of simple cores and became the default for both training and inference. Cloud providers also build their own accelerators: Google's **TPUs**, and AWS's **Trainium** for training and **Inferentia** for inference. Phones and laptops include a low-power **NPU** (neural processing unit) for running small models on the device, which keeps data local and saves battery.

Memory is usually the limit before arithmetic is. Each parameter stored in 16-bit precision takes 2 bytes, so the weights of a 70-billion-parameter model alone take about 140 GB, well beyond the 80 GB of an NVIDIA H100, so the model must be split across GPUs or compressed; serving also needs room for the **KV cache**, which grows with the context length and the number of users served at once. Two techniques stretch memory. **Quantization** stores weights in 8 or 4 bits instead of 16, trading a little accuracy for a smaller footprint. A **mixture-of-experts** (MoE) model splits its layers into many expert networks and routes each token to only a few of them. Its **active parameters**, the ones used for a given token, set the compute cost, but memory must still hold every expert. DeepSeek-V3, for example, has 671 billion parameters, of which 37 billion are active for each token ([DeepSeek-V3 technical report](https://arxiv.org/abs/2412.19437)).

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
motivation for retrieval-augmented generation in Module 3.

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
are roughly equivalent to a trans-American flight. At the scale of the whole industry, the International Energy Agency estimated that data centers used about 415 terawatt-hours of electricity in 2024, about 1.5 percent of global demand, and projects that use to roughly double by 2030 ([IEA](https://www.iea.org/reports/energy-and-ai/executive-summary)). Data center operators report efficiency as **power usage effectiveness (PUE)**: total facility energy divided by the energy delivered to computing equipment, where 1.0 would mean no overhead for cooling and power conversion. Choosing the smallest model that does the job is the most direct way to cut this cost.

**Non-determinism.** The same prompt can return different answers. At each step the model computes a probability for every possible next token, and **decoding** settings decide how one is picked. **Temperature** scales those probabilities: near zero the model almost always takes the most likely token, and higher values spread the choice across less likely ones. **Top-p** (nucleus sampling) samples only from the smallest set of tokens whose probabilities add up to p, and **top-k** samples only from the k most likely tokens. In the Converse API, `temperature`, `topP`, and `maxTokens` go in `inferenceConfig`. Even temperature zero does not guarantee identical output on a shared service. In September 2025, Thinking Machines Lab sent one prompt 1,000 times at temperature zero and got 80 different completions; the main cause was that the server batches each request with others, and the batch size changes the order of floating-point additions inside the model ([Thinking Machines](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)). Design tests and audits that expect some variation.

**Catastrophic forgetting.** A neural network trained on a new task tends to lose what it learned before, because the same weights store both {cite}`kirkpatrick2017overcoming`. Fine-tuning an LLM on a narrow dataset can therefore weaken skills it never practiced in that data. Safety behavior is one of those skills: researchers showed that fine-tuning an aligned model, even on harmless data, can weaken its refusals {cite}`qi2024finetuning`. Parameter-efficient methods that change few weights, mixing general and safety data into the fine-tuning set, and re-running safety evaluations after every fine-tune all reduce the risk.

**Model collapse.** Models trained on text generated by earlier models lose the rare cases first, and over generations their output narrows toward the common ones. A 2024 study in *Nature* showed this happening across repeated rounds of training on generated data {cite}`shumailov2024collapse`. As more of the web is written by models, the provenance of training data matters: keep a share of human-written data and record where each dataset came from.

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
- Models learn by gradient descent on a **loss**; the **learning rate** sets the
  step size, **softmax** with a temperature turns logits into probabilities, and
  **overfitting** is why data is split into training, validation, and test sets.
- Memory, not arithmetic, usually limits model size: 16-bit weights take 2 bytes
  per parameter, and a mixture-of-experts model computes with its **active
  parameters** but must store them all.
- Outputs vary run to run, even at temperature zero; fine-tuning can erase old
  skills, including safety behavior (**catastrophic forgetting**); and training
  on model-generated data narrows what models know (**model collapse**).

Next, we turn from how models work to how you direct them: prompt engineering.
