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

## Random, stochastic, aleatoric, and intermittent

People reach for four words when an application does not behave the same way
twice: *random*, *stochastic*, *aleatoric*, and *intermittent*. In everyday
speech they blur together, but each one answers a different question and points
to a different fix. The figure below sets the four side by side, and the table
states the question each word answers.

```{image} ../_static/figures/bk_uncertainty_terms.*
:alt: Four numbered panels. Random shows a die with a flat histogram beside the peaked histogram of two dice summed. Stochastic shows arrows scattered around a target. Aleatoric shows uncertainty falling as data grows, down to a floor that does not move. Intermittent shows a regular and an irregular on and off signal. Each panel ends with an example from a Bedrock application.
:width: 95%
:align: center
:class: anim-fig
```

```{list-table}
:header-rows: 1
:widths: 14 26 30 30

* - Term
  - Question it answers
  - Meaning
  - Example in a Bedrock application
* - Random
  - Is the next outcome known in advance?
  - No. Outcomes follow a probability distribution, which may or may not be
    uniform.
  - The next token the model samples
* - Stochastic
  - Does a probability model describe the outcomes, often over time?
  - Yes. It is the technical word for random, used most for processes.
  - Generating a whole answer one sampled token at a time
* - Aleatoric
  - Could more knowledge remove the uncertainty?
  - No. The variation lives in the question or the data itself. Its
    counterpart, epistemic uncertainty, shrinks with more knowledge.
  - A question with two reasonable readings
* - Intermittent
  - Does it happen all the time?
  - No. It comes and goes, on a regular or an irregular schedule.
  - Throttling errors that appear only when traffic peaks
```

### Random

In everyday speech, *random* means lacking a definite plan, purpose, or pattern.
Statistics uses a narrower sense: an event is random when it has a definite
probability of occurrence, and a random sample is one in which every element has
the same chance of being chosen
([Merriam-Webster](https://www.merriam-webster.com/dictionary/random)). The first
statistical sense does not require equal chances. A fair die is uniform, because
each face comes up one time in six. The sum of two dice is random too, yet 7
comes up six times in 36 while 2 and 12 come up once each. A model's next token
is random in the same way. The model gives every token in its vocabulary a
probability, and the distribution is far from uniform: in the temperature example
above, *Paris* has probability 0.854 at temperature 1.0.

The shape of a distribution decides how well a guesser does. The best single
guess is the most likely outcome, and it is right with exactly that outcome's
probability. Greedy decoding makes this guess at every step. Entropy, used in the
temperature example, measures the average spread of a distribution.
**Min-entropy**, the negative base-2 logarithm of the largest probability,
measures the worst case: how easy the single best guess is
([NIST glossary](https://csrc.nist.gov/glossary/term/min_entropy)). A
distribution that is not uniform is still random; it is only easier to guess.
For the same reason, text sampled from a model should never serve as a password
or a key. Each token carries little min-entropy when the distribution is peaked,
and an attacker with access to the same model can try the likely outputs first.
Cryptographic keys come from uniform random bit generators instead, which the
cybersecurity textbook's section on
[true, pseudo, and cryptographically secure randomness](https://book.com.puter.tips/chapters/02_cryptography/chapter02.html#randomness-true-pseudo-and-cryptographically-secure)
covers.

Temperature changes the peak by the same rule that governs every distribution.
The probabilities always add up to 1, so a narrower distribution must have a
taller peak. Lowering the temperature from 1.0 to 0.7 raises *Paris* from 0.854
to 0.954, and raising it to 2.0 lowers the peak to 0.526, as the earlier table
shows. A next-token probability can never exceed 1. A continuous quantity, such
as a latency or a similarity score, has a density instead, and its peak can
rise above 1 when the values are packed into a range narrower than one unit,
because only the area under the curve must equal 1. The cybersecurity
textbook's section on
[peak density](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#peak-density-how-high-a-distribution-rises)
works through the normal, uniform, exponential, and count distributions.

### Stochastic

*Stochastic* means random, specifically involving a random variable, and more
broadly involving chance or probability
([Merriam-Webster](https://www.merriam-webster.com/dictionary/stochastic)). It
comes from the Greek *stochastikos*, skillful in aiming, from a verb meaning to
aim at or to guess. The image fits. An archer aims at a target, and the arrows
land around it in a spread that a distribution describes, yet no one can say
where the next arrow will land. In mathematics, random and stochastic mean the
same thing. The difference is register and focus: stochastic is the technical
word, and a **stochastic process** is a sequence of random outcomes that unfolds
over time.

Text generation is a stochastic process. Each token is drawn from a distribution
that depends on every token before it, so one early draw can send the rest of the
answer down a different path. That is why the next chapter calls sampling
*stochastic decoding*, and why self-consistency can sample several reasoning
paths and keep the majority answer. Setting the temperature to zero removes the
sampling step, but it does not make a hosted model fully repeatable. As the
non-determinism discussion in {doc}`02-foundation-models-and-llms` shows, one
prompt sent 1,000 times at temperature zero returned 80 different completions
([Thinking Machines](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)).
That variation does not come from sampling. It comes from the server: the batch
your request joins changes the order of floating-point additions inside the
model.

### Aleatoric and epistemic uncertainty

*Aleatoric* comes from the Latin *alea*, a die or a game of dice, by way of
*aleator*, a gambler
([Dictionary.com](https://www.dictionary.com/browse/aleatory)). Law uses the
older form: an aleatory contract, such as an insurance policy, pays out only if
an uncertain event occurs. In modeling, **aleatoric uncertainty** is variation
built into the process, which more knowledge would not remove. Its counterpart,
**epistemic uncertainty**, comes from a lack of knowledge, and more data or a
better model can reduce it {cite}`hullermeier2021aleatoric`.

The line between the two depends on the model. Der Kiureghian and Ditlevsen
propose a practical test: an uncertainty is epistemic if the modeler sees a way
to reduce it by gathering more data or refining the model, and aleatoric
otherwise {cite}`derkiureghian2009aleatory`. A coin toss shows why the test is
practical rather than absolute. A toss follows physics, and a 2025 study of
350,757 flips found that a coin lands on the side it started on about 50.8
percent of the time {cite}`bartos2025coin`. Most analyses still treat the toss as
aleatoric, because no one measures the launch precisely enough to predict it.

The two kinds call for different fixes in an LLM application
{cite}`kendall2017uncertainties`. A question with two reasonable readings, such
as *What is the fee?* when two products have fees, is aleatoric from the model's
side: retrieval and more training data cannot settle it, but a clarifying
question to the user can. A question about an event after the model's training
cutoff is epistemic: retrieval, a tool call, or fine-tuning on newer data can
remove it. Lowering the temperature removes neither; it only makes the model
give its most likely answer every time. The section on abstention in Module 2's
{doc}`../module-2/01-evaluating-llms` shows how to decide when a system should
ask, retrieve, or decline to answer.

### Intermittent

*Intermittent* means coming and going at intervals, not continuous
([Merriam-Webster](https://www.merriam-webster.com/dictionary/intermittent)). It
comes from the Latin *intermittere*, built from *inter-*, between, and *mittere*,
to send. Unlike the other three words, it describes a pattern in time, not a
probability. A job that runs every hour on the hour is intermittent and fully
predictable; a fault that appears only under heavy load is intermittent and hard
to predict.

The intermittent failures you will meet most often on Amazon Bedrock are
capacity errors. The troubleshooting guide lists a `ThrottlingException` (HTTP
429) when a request exceeds your account quotas, and a 503 error when the
service is temporarily short of capacity. For both, it recommends retries with
exponential backoff and random jitter {cite}`aws2026bedrockerrors`. These errors
come and go with traffic, so a request that fails now often succeeds a moment
later.

Retries handle intermittent failures, and randomness makes the retries work.
**Exponential backoff** doubles the wait after each failed attempt, up to a cap.
Backoff alone leaves a problem: clients that failed together retry together, so
the load still arrives in spikes. **Jitter** breaks up the spikes by drawing each
wait at random. Marc Brooker's analysis for AWS found that backoff without
jitter took more calls and more time than the jittered versions
{cite}`brooker2015backoff`. The retry behavior that the AWS SDKs document uses **full jitter**, which waits
a random time between zero and the capped backoff {cite}`aws2026sdkretry`.

The code below makes both ideas concrete with no API calls. The first part
computes how often the best guess wins, and the min-entropy, for a fair die, for
the next-token distribution from the temperature example at three temperatures,
and for a uniform 128-bit key. The second part throttles 100 clients at the same
moment, lets every retry fail, and counts the calls that land in the busiest
100-millisecond window, with and without full jitter.

```python
# Best guess, min-entropy, and retry jitter (no API calls)
import numpy as np

logits = np.array([6.0, 3.5, 3.0, 2.0, 1.5, 1.0, 0.0, -2.0])   # from the temperature example

def softmax(z, temperature):
    z = np.asarray(z, dtype=float) / temperature
    e = np.exp(z - z.max())
    return e / e.sum()

# 1. The best single guess is the most likely outcome; it wins with that outcome's probability.
print("distribution            best guess wins   min-entropy (bits)")
for name, top in [("fair die", 1 / 6),
                  ("next token, T = 0.7", softmax(logits, 0.7).max()),
                  ("next token, T = 1.0", softmax(logits, 1.0).max()),
                  ("next token, T = 2.0", softmax(logits, 2.0).max()),
                  ("uniform 128-bit key", 2.0 ** -128)]:
    print(f"{name:22} {top:16.3g}   {-np.log2(top):18.2f}")

# 2. 100 clients are throttled at the same moment and every retry fails (the worst case).
#    Each waits base * 2^attempt seconds, capped at 20, with or without full jitter.
rng = np.random.default_rng(7)
base, cap, clients, retries = 1.0, 20.0, 100, 4

def retry_times(jitter):
    times = []
    for _ in range(clients):
        t = 0.0
        for attempt in range(retries):
            delay = min(cap, base * 2 ** attempt)
            t += rng.uniform(0, delay) if jitter else delay
            times.append(t)
    return np.array(times)

print()
for label, jitter in [("no jitter", False), ("full jitter", True)]:
    t = retry_times(jitter)
    busiest = np.bincount((t * 10).astype(int)).max()        # calls in the busiest 100 ms window
    print(f"{label:12} {len(t)} retries over {t.max():5.1f} s   busiest 100 ms window: {busiest:3d} calls")
```

```text
distribution            best guess wins   min-entropy (bits)
fair die                          0.167                 2.58
next token, T = 0.7               0.954                 0.07
next token, T = 1.0               0.854                 0.23
next token, T = 2.0               0.526                 0.93
uniform 128-bit key            2.94e-39               128.00

no jitter    400 retries over  15.0 s   busiest 100 ms window: 100 calls
full jitter  400 retries over  13.0 s   busiest 100 ms window:  23 calls
```

The first block applies the guessing rule from the Random subsection. The best
guess on a fair die wins one time in six. At temperature 0.7 the next token is
almost as predictable as a constant, with 0.07 bits of min-entropy, and even at
temperature 2.0 it carries less than one bit. A uniform 128-bit key carries the
full 128 bits, so its best guess is no better than any other and almost never
right.

The second block shows why jitter matters. Without jitter, the 100 clients retry
in lockstep: all 100 calls land in the same 100-millisecond window, four times
over, and each spike can trigger the next round of throttling. With full jitter,
the same 400 retries spread out, and the busiest window holds 23 calls. The last
retry also comes sooner, because a random wait averages half the full backoff.

In practice the SDK runs this loop for you. Set the retry mode and the attempt
limit explicitly when you create the client, because the defaults depend on the
SDK and its version. The AWS SDKs and Tools Reference Guide notes, for example,
that its updated 2026 retry behavior applies only when you set
`AWS_NEW_RETRIES_2026=true`, until that behavior becomes the default
{cite}`aws2026sdkretry`. In Boto3, `total_max_attempts` counts the first request,
while `max_attempts` in a `Config` object counts only the retries
{cite}`aws2026boto3retries`.

```python
import boto3
from botocore.config import Config

# Standard mode retries throttling and transient errors with exponential backoff and jitter.
# total_max_attempts=5 means the first request plus up to four retries.
config = Config(retries={"mode": "standard", "total_max_attempts": 5})
client = boto3.client("bedrock-runtime", config=config)
```

Retry only calls that are safe to repeat. A model call that only reads is safe;
an agent's tool call that sends a payment is not, and Module 3's
{doc}`../module-3/04-agents` shows how an idempotency key lets a downstream service ignore a duplicate.

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
- **Random** means the next outcome is unknown, under any distribution, and
  **stochastic** is its technical synonym for processes such as generation.
  **Aleatoric** uncertainty is built into the question and needs a clarifying
  question; **epistemic** uncertainty yields to retrieval or tools.
  **Intermittent** failures such as throttling come and go, and retries with
  exponential backoff and jitter handle them.
- Follow best practices: be clear, specific, positive, and structured, and expect
  to iterate. Respect each model's required prompt format.
- **In-context learning**, zero-, one-, and few-shot, adapts the model purely
  through the prompt, with no retraining.

Standard prompting takes you a long way, but hard, multi-step problems need more.
The next chapter introduces advanced prompting techniques for reasoning.
