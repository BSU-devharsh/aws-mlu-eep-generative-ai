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

## Quantization

A **quantized model** stores its numerical parameters, its weights and sometimes its activations, at lower precision than it was trained in: 8-bit or 4-bit integers, or 8-bit floating-point numbers, instead of 32-bit or 16-bit floating-point numbers. Each group of weights keeps a **scale factor**, and every weight is divided by the scale, rounded to the nearest integer the format allows, and stored as that integer. At inference time the integers are multiplied back by the scale. The model loses a little numerical precision and gains a smaller memory footprint, faster inference, and lower energy use, which is what lets large models run on a laptop, a phone, or fewer GPUs.

There are two ways to get there. **Post-training quantization (PTQ)** compresses a model that is already trained, often using a small set of **calibration data** to keep the error low; it is fast and needs no retraining. **Quantization-aware training (QAT)** simulates low-precision arithmetic during training or fine-tuning, so the model learns to tolerate it and keeps more of its accuracy; Jacob and colleagues introduced the integer-only training and inference scheme that made it practical on mobile hardware {cite}`jacob2018quantization`. Several PTQ methods give their names to the quantized models people share:

- **GPTQ** uses approximate second-order information to correct the error of each weight as it quantizes the next. It quantized models with 175 billion parameters to 3 or 4 bits per weight in about four GPU hours with negligible loss of accuracy {cite}`frantar2023gptq`.
- **AWQ**, activation-aware weight quantization, observes that a small fraction of weights matter most and finds them by looking at the activations rather than the weights; scaling those channels before quantizing protects them {cite}`lin2024awq`.
- **LLM.int8()** and the 4-bit **NF4** format of QLoRA keep large language models usable at 8 and 4 bits {cite}`dettmers2022llmint8,dettmers2023qlora`.
- **GGUF** is a file format rather than a method: a single file holding the tensors and metadata for inference with GGML and llama.cpp, with many quantization types such as Q8_0, Q4_K, and Q6_K {cite}`hfgguf`. Ollama and other local runtimes use it.

The code below quantizes one row of weights that, like real language-model layers, contains two large outliers. It compares one scale for the whole row with one scale per block of 32 weights, the layout of GGUF's Q8_0 and Q4_0 types, and then works out the memory that weights alone need.

```python
import numpy as np

rng = np.random.default_rng(0)
w = rng.normal(0, 0.02, size=4096).astype(np.float32)    # one row of a weight matrix
w[[100, 2000]] = [0.6, -0.5]                             # two outliers, as real LLM layers have

def absmax(x, bits):
    """Symmetric quantization: one scale maps the largest magnitude to the top integer."""
    qmax = 2 ** (bits - 1) - 1                            # 127 for 8 bits, 7 for 4 bits
    scale = np.abs(x).max() / qmax
    return np.clip(np.round(x / scale), -qmax, qmax) * scale

def blockwise(x, bits, block=32):
    """One scale per block of 32 weights, as in GGUF's Q8_0 and Q4_0 types."""
    return np.concatenate([absmax(b, bits) for b in x.reshape(-1, block)])

def rel_err(x_hat):
    return np.linalg.norm(x_hat - w) / np.linalg.norm(w)

print(f"{'scheme':<30}{'bits per weight':>16}{'relative error':>16}")
for name, x_hat, bpw in [("int8, one scale per row", absmax(w, 8), 8 + 16 / 4096),
                         ("int4, one scale per row", absmax(w, 4), 4 + 16 / 4096),
                         ("int8, scale per 32 weights", blockwise(w, 8), 8 + 16 / 32),
                         ("int4, scale per 32 weights", blockwise(w, 4), 4 + 16 / 32)]:
    print(f"{name:<30}{bpw:>16.2f}{rel_err(x_hat):>16.1%}")

print("\nWeights alone, in GB:")
for params in (7e9, 70e9):
    sizes = {fmt: params * bits / 8 / 1e9 for fmt, bits in [("FP32", 32), ("FP16", 16), ("INT8", 8), ("INT4", 4)]}
    print(f"  {params / 1e9:.0f}B parameters: " + ", ".join(f"{k} {v:.1f}" for k, v in sizes.items()))
```

```text
scheme                         bits per weight  relative error
int8, one scale per row                   8.00            5.9%
int4, one scale per row                   4.00           81.5%
int8, scale per 32 weights                8.50            0.8%
int4, scale per 32 weights                4.50           13.2%

Weights alone, in GB:
  7B parameters: FP32 28.0, FP16 14.0, INT8 7.0, INT4 3.5
  70B parameters: FP32 280.0, FP16 140.0, INT8 70.0, INT4 35.0
```

Two lessons show in the numbers. With one scale per row, the outliers set the scale, so at 4 bits almost every ordinary weight rounds to zero and the error is 81.5 percent; one scale per block confines each outlier's damage to its own 32 weights, at a cost of half a bit per weight for the extra scales. That is why practical formats quantize in small groups, and why methods such as AWQ treat important weights specially. The memory table matches the rule of thumb: a 70-billion-parameter model needs about 140 GB for its weights at 16 bits, 70 GB at 8 bits, and 35 GB at 4 bits, before the KV cache and other working memory.

On Amazon Bedrock you rarely quantize anything yourself, because AWS serves the hosted models. Quantization matters when you bring your own model. Custom Model Import accepts weights in safetensors format at FP32, FP16, or BF16 precision, converts FP32 models to BF16 internally, and does not support importing quantized models ([AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html)). A quantized copy is for hardware you run yourself, such as an edge device or a self-hosted server.

### Trusting a quantized model

Quantized copies of popular open models are easy to find on model hubs, usually made by someone other than the lab that released the original. The cybersecurity textbook asks what a security team should do with one: the lab signed the original, but its signature does not cover the quantized files. The best answer is to quantize the verified original in your own pipeline and sign the result, because a clean malware scan cannot reveal behavior hidden in the weights and popularity is not evidence ([trusting derived models](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#trusting-derived-models-quantized-converted-and-fine-tuned-copies)). Research supports the caution: Egashira and colleagues built models that look benign in full precision but behave maliciously once quantized, including in GGUF formats {cite}`egashira2024exploiting,egashira2025mind`.

On AWS the pipeline looks like this:

1. Download the lab's original into a build environment and verify its signature. The OpenSSF `model_signing` tool checks a Sigstore signature against the identity the lab publishes, for example `model_signing verify <model_dir> --signature model.sig --identity <lab identity> --identity-provider <OIDC provider>`; flag spellings have changed between releases, so check `model_signing verify --help` for your version.
2. Record the hash of every file and store the verified files in an Amazon S3 bucket with versioning turned on, writable only by the build role.
3. For Bedrock, import the verified full-precision files directly, since Custom Model Import does not take quantized models. For your own hardware, quantize in the same isolated build with a pinned tool version and settings, and write a provenance record that links the input hashes, the tool and settings, and the output hashes.
4. Evaluate the result against the original, including security behavior, sign it with your organization's identity, and let deployment accept only signed artifacts.

The import itself takes the S3 location of the verified files:

```python
import boto3

bedrock = boto3.client("bedrock")
job = bedrock.create_model_import_job(
    jobName="lab-model-v1-verified",
    importedModelName="lab-model-v1",
    roleArn="arn:aws:iam::111122223333:role/MyImportModelRole",
    modelDataSource={"s3DataSource": {"s3Uri": "s3://verified-models/lab-model-v1/"}},
)
print(job["jobArn"])
```

Give the import role read access only to the verified bucket, so that nobody can import a model that skipped the checks.

```{image} ../_static/figures/bk_quantized_pipeline.*
:alt: Verify the lab signed original, store it in a versioned S3 bucket, then import full precision to Bedrock or quantize in-house, evaluate, sign, and deploy only signed artifacts; an unverified hub quantization is rejected
:width: 95%
:align: center
:class: anim-fig
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
- **Quantization** stores weights at 8 or 4 bits with a scale per group of
  weights; PTQ compresses a trained model, QAT trains for low precision, and
  small groups keep outliers from ruining accuracy. Derive quantized copies
  from a verified original in your own pipeline and sign them.
- Outputs vary run to run, even at temperature zero; fine-tuning can erase old
  skills, including safety behavior (**catastrophic forgetting**); and training
  on model-generated data narrows what models know (**model collapse**).

Next, we turn from how models work to how you direct them: prompt engineering.
