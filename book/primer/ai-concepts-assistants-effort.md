---
title: "AI Concepts, Assistants, and Effort Levels"
---

# AI Concepts, Assistants, and Effort Levels

Students meet a flood of overlapping words when they start using AI: machine
learning, deep learning, LLM, frontier model, agent, AGI, superintelligence. They
also meet a crowd of product names, from ChatGPT and Claude to Gemini, Muse,
Vibe and OpenClaw, and a new kind of setting, the **effort level**, that promises
better answers at the price of time and usage limits. This chapter untangles all
three in order:

1. **Part 1** maps the core vocabulary, from the broadest term (AI) to the
   narrowest (frontier models), and explains the terms that sit outside that
   nesting: NLP, agentic AI, AGI and superintelligence.
2. **Part 2** surveys the major assistants and model families as of October
   2026, including which are open weights and which are available on Amazon
   Bedrock, the platform used throughout this book.
3. **Part 3** explains in detail what effort levels such as medium and high
   actually do, and why higher effort means more thorough responses, but takes
   longer and uses your limits faster.

It extends the shorter entries in {doc}`ai-and-tools-reference`, and the two
chapters are meant to be read together.

```{admonition} Learning objectives
:class: tip
After this chapter you should be able to:
- place AI, ML, DL, NLP, generative AI, LLMs, foundation models and frontier
  models on one map, and say which terms describe techniques, problems,
  ways of using models or hypothetical capability levels;
- tell the company, the model family and the app apart for the major AI
  assistants, and explain the difference between open weights and open source;
- explain what an effort level changes inside a model, why it costs time and
  usage, and how to pick a level for a task.
```

## Part 1: The vocabulary of AI, from broadest to narrowest

People use *AI*, *machine learning*, *deep learning*, *LLM* and *agent* as if
they were interchangeable. They are not. Most of these terms **nest inside one
another**, a few **cut across** the others, and a few name **capability levels**
that no one has shown a system to reach. Figure 1 puts them on one map, and the
sections below walk through it from the outside in.

```{figure} ../_static/ai-concepts-map.svg
:alt: Nested boxes from broadest to narrowest. Artificial intelligence contains machine learning, which contains deep learning, which contains generative AI, which contains foundation models and large language models, which contain frontier models. A dashed band labeled NLP cuts across every layer. To the right, agentic AI is shown as a model in a loop with tools, and AGI and superintelligence are shown as hypothetical capability levels.
:width: 100%
:align: center

How the core terms relate. Each box sits inside the broader one around it. The
nesting is a simplification: a few foundation models, such as embedding models,
are not generative, and older generative methods existed before deep learning.
```

### Artificial intelligence (AI)

**Artificial intelligence** is the broadest term. It was coined in a 1955
proposal by John McCarthy, Marvin Minsky, Nathaniel Rochester and Claude Shannon
for a summer study at Dartmouth College in 1956. The proposal rested on the
conjecture that every feature of intelligence can in principle be described so
precisely that a machine can be made to simulate it, and its goals already
included getting machines to use language {cite}`mccarthy1955proposal`. McCarthy
later defined AI simply as the science and engineering of making intelligent
machines ([McCarthy, What is AI?](http://jmc.stanford.edu/articles/whatisai/whatisai.pdf)).

Laws and standards now use a more operational wording. The OECD revised its
definition of an **AI system** in November 2023 to cover generative AI, and the
European Union's AI Act adopted almost the same text: a machine-based system
that operates with some autonomy and **infers from the input it receives how to
generate outputs** such as predictions, content, recommendations or decisions
([OECD.AI](https://oecd.ai/en/wonk/ai-system-definition-update);
[EU AI Act, Article 3](https://artificialintelligenceact.eu/article/3/)).

AI is wider than learning from data. A chess engine that searches millions of
positions, a route planner, or a **rule-based expert system** written by hand
are all AI, even though none of them learned anything from examples.

### Machine learning (ML)

**Machine learning** is the part of AI in which a system **learns patterns from
data instead of following rules a person wrote**. Arthur Samuel used the term in
1959 for a checkers program that learned to play better than its own programmer,
and he argued that learning from experience would remove much of the detailed
programming otherwise needed {cite}`samuel1959some`. The main kinds of machine
learning differ in what signal the model learns from:

```{list-table}
:header-rows: 1
:widths: 22 40 38

* - Kind
  - What the model learns from
  - Everyday example
* - **Supervised learning**
  - Examples paired with the right answer (labels)
  - A spam filter trained on emails marked spam or not spam
* - **Unsupervised learning**
  - Data with no labels; the model finds structure on its own
  - Grouping customers into segments by purchase history
* - **Reinforcement learning**
  - Rewards and penalties for actions taken in an environment
  - A model race car learning to drive a track, as in AWS DeepRacer (now the
    open-source DeepRacer on AWS solution)
* - **Self-supervised learning**
  - Labels created from the data itself, such as hiding the next word and
    asking the model to predict it
  - Pretraining a large language model on web text
```

LeCun, Bengio and Hinton describe supervised learning as the most common form of
machine learning {cite}`lecun2015deep`, while self-supervised learning at very
large scale is what made foundation models possible {cite}`bommasani2021opportunities`.
{doc}`../appendix-traditional-ml` covers classic machine learning in depth.

### Deep learning (DL)

**Deep learning** is machine learning with **neural networks that have many
layers**. Each layer turns its input into a slightly more abstract
representation, and the network learns these layers of features from data
instead of relying on features a person designed by hand. LeCun, Bengio and
Hinton define it as models composed of multiple processing layers that learn
representations of data with multiple levels of abstraction, trained with the
backpropagation algorithm {cite}`lecun2015deep`. Deep learning drove the jumps in
image recognition, speech recognition and translation in the 2010s, and every
modern large language model is a deep-learning model.

### Natural language processing (NLP)

**Natural language processing** is the field concerned with getting computers to
understand, interpret and generate human language: translation, summarization,
sentiment analysis, question answering, speech assistants and chatbots. The
standard textbook by Jurafsky and Martin describes it as the field, also called
computational linguistics, aimed at getting computers to perform useful tasks
involving human language, and calls it the new heart of modern AI
([Jurafsky and Martin, Speech and Language Processing, 3rd edition draft](https://web.stanford.edu/~jurafsky/slp3/1.pdf)).
NLP is drawn as a dashed band in Figure 1 because it is defined by the **problem**
(language), not by a technique. Over the decades it has been tackled with
hand-written rules (ELIZA, a 1966 program that imitated a psychotherapist by
pattern matching, is a famous early example), with statistical machine learning,
with deep learning, and now mostly with large language models. A spam filter built on word
counts and a modern chatbot are both NLP.

### Generative AI

**Generative AI** refers to models that **create new content**, such as text,
images, audio, video or code, that resembles the data they learned from. The US
National Institute of Standards and Technology (NIST) notes that not all
generative AI is derived from foundation models, although for the purposes of
its generative AI risk profile the term generally refers to generative
foundation models
([NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)).
{doc}`../module-1/01-introduction-to-generative-ai` introduces the topic for this
book.

### Large language models (LLMs)

A **large language model** is a deep-learning model, almost always a
**Transformer** {cite}`vaswani2017attention`, trained on very large amounts of
text to work with language. Jurafsky and Martin describe four training stages
that turn raw text into the assistants you use
([Speech and Language Processing, chapter 1](https://web.stanford.edu/~jurafsky/slp3/1.pdf)):

1. **Pretraining.** The model reads trillions of tokens and learns to **predict
   the next token**. This self-supervised objective teaches grammar, facts and
   patterns of reasoning, but on its own it produces a text-completer, not a
   helpful assistant.
2. **Instruction tuning.** The model is fine-tuned on examples of instructions
   paired with good responses.
3. **Preference alignment.** People rank alternative answers, a reward model
   learns their preferences, and reinforcement learning nudges the model toward
   answers people prefer. This is **reinforcement learning from human feedback
   (RLHF)**. In the InstructGPT study, outputs from a 1.3 billion parameter model
   trained this way were preferred to those of the 175 billion parameter GPT-3,
   which shows how much these later stages matter {cite}`ouyang2022training`.
4. **Reinforcement learning with verifiable rewards.** For math, code and other
   tasks whose answers can be checked automatically, the model is rewarded for
   reaching correct answers, which trains the step-by-step reasoning described
   under reasoning models below.

Because LLMs generate the most likely continuation rather than look facts up,
they can state false things fluently. NIST calls this **confabulation**, the
behavior popularly called hallucination
([NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)). A
related risk is **sycophancy**, the tendency to agree with whatever the user says
they believe. A 2026 study of AI-assisted forensic opinion found that the models
it tested mostly did not defer to an examiner's stated view, but that they
checked conclusions without auditing the reasons behind them
{cite}`trivedi2026tool`.
Tokens are explained in {doc}`tokens-and-embeddings`, and
{doc}`../module-1/02-foundation-models-and-llms` covers LLMs in more depth.

### Foundation models

A **foundation model** is any model trained on broad data, generally with
self-supervision at scale, that can be **adapted to a wide range of downstream
tasks**. The term was coined by a Stanford group in 2021, whose examples were
BERT, GPT-3 and CLIP; they chose the word *foundation* to stress that such models
are central yet incomplete on their own {cite}`bommasani2021opportunities`. Most
LLMs are foundation models, but so are image, audio and multimodal models.

The EU AI Act calls the same idea a **general-purpose AI model**. Its recitals
suggest, as a rule of thumb, that models with at least a billion parameters
trained this way should count, and Commission guidelines published in July 2025
use a training-compute indicator of more than 10<sup>23</sup> operations for
models that generate language, images or video
([EUR-Lex, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689);
[European Commission](https://digital-strategy.ec.europa.eu/en/news/commission-publishes-guidelines-providers-general-purpose-ai-models)).

### Frontier models

A **frontier model** is a foundation model at the **leading edge of capability**
at a given moment. Industry and some governments define it **relative to the
state of the art**, so the set of frontier models changes every few months. The
Frontier Model Forum, launched by Anthropic, Google, Microsoft and OpenAI in July
2023, and the UK government's 2023 paper on frontier AI both use capability-based
definitions with no fixed number
([OpenAI, Frontier Model Forum](https://openai.com/blog/frontier-model-forum);
[UK DSIT](https://www.gov.uk/government/publications/frontier-ai-capabilities-and-risks-discussion-paper/frontier-ai-capabilities-and-risks-discussion-paper)).

Laws need a line they can enforce, so they use **training compute**, counted as
the total number of arithmetic operations used to train the model. For scale,
10<sup>26</sup> operations is a hundred trillion trillion operations.

```{list-table} Compute thresholds in law and policy (as of October 2026)
:header-rows: 1
:widths: 30 22 48

* - Rule
  - Threshold
  - What it means
* - EU AI Act, Article 51
  - More than 10<sup>25</sup> operations
  - A general-purpose AI model is **presumed** to have high-impact capabilities
    and systemic risk; obligations apply from 2 August 2025, and the threshold
    can be amended ([Article 51](https://artificialintelligenceact.eu/article/51/)).
    The Commission's enforcement powers over these models, including fines,
    apply from 2 August 2026
    ([Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2026/07/eu-ai-act-news-digital-omnibus-on-ai-new-guidance-on-risk-classification-gpai-and-transparency-obligations)).
* - California SB 53, Transparency in Frontier AI Act
  - More than 10<sup>26</sup> operations
  - Defines a **frontier model**, counting the original training run plus later
    fine-tuning, reinforcement learning or other material modifications; extra
    duties fall on large frontier developers with more than 500 million dollars
    in annual revenue; in effect since January 1, 2026
    ([SB 53 bill text](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260SB53);
    [Governor of California](https://www.gov.ca.gov/2025/09/29/governor-newsom-signs-sb-53-advancing-californias-world-leading-artificial-intelligence-industry/)).
* - New York RAISE Act, as amended in March 2026
  - More than 10<sup>26</sup> operations
  - Brought much closer to California's law, with differences such as a
    72-hour incident-reporting deadline; takes effect January 1, 2027
    ([Wiley](https://www.wiley.law/alert-New-York-Finalizes-RAISE-Act-for-Frontier-AI-Models-Law-Takes-Effect-January-1-2027)).
* - US Executive Order 14110 (2023)
  - More than 10<sup>26</sup> operations
  - A reporting threshold that **no longer applies**: the order was revoked on
    January 20, 2025 by Executive Order 14148
    ([Federal Register](https://govinfo.gov/content/pkg/FR-2025-01-28/html/2025-01901.htm)).
```

These thresholds are no longer far away. The International AI Safety Report
2026 notes that the largest training runs have now likely exceeded
10<sup>26</sup> operations ([International AI Safety Report 2026](https://arxiv.org/abs/2602.21012)).
In the United States a federal discussion draft released in June 2026, the Great
American AI Act, would use the same 10<sup>26</sup> threshold and override
state laws on model development for three years, but it is a draft, not law
([Global Policy Watch](https://www.globalpolicywatch.com/2026/07/backlash-to-bipartisan-ai-omnibus-illustrates-preemption-impasse/)).

The existing comparison of foundation and frontier models in
{doc}`ai-and-tools-reference` still holds: **all frontier models are foundation
models, but not all foundation models are on the frontier.**

### Reasoning models

A **reasoning model** is an LLM trained to **think before it answers**: it
generates a hidden or summarized chain of reasoning, checks itself, and only then
writes the visible reply. This built-in thinking is an automated cousin of the
chain-of-thought prompting in {doc}`../module-1/04-advanced-prompting-techniques`
{cite}`wei2022chain`. OpenAI introduced o1 in September 2024 as a model
trained with reinforcement learning to produce a long internal chain of thought
before answering, and reported that it improved both with more training and with
more time spent thinking
([OpenAI, Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/)).
In January 2025 DeepSeek-R1 showed that reinforcement learning, without
human-written examples of reasoning, can teach a model to reason this way, with
self-checking behavior emerging on its own {cite}`guo2025deepseek`. Most current
frontier models have this ability built in, and the **effort level** in Part 3
controls how much of it they use.

### Agentic AI

**Agentic AI** describes systems in which a model does not just answer once but
**works in a loop**: it plans, calls tools such as web search, code execution,
files or apps, looks at the results, and decides what to do next until a goal is
met. Anthropic distinguishes **workflows**, where code follows a predefined path
and calls a model at fixed steps, from **agents**, where the model dynamically
directs its own process and tool use; both count as agentic systems
([Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)).

NIST's Center for AI Standards and Innovation describes an AI agent system as at
least one generative AI model plus scaffolding software that gives it tools to
take discretionary, autonomous actions. Its January 2026 request for information
explicitly sets aside chatbots and retrieval-augmented generation systems that
are not orchestrated to act autonomously
([Federal Register, January 8, 2026](https://www.govinfo.gov/content/pkg/FR-2026-01-08/html/2026-00206.htm)).
NIST launched an AI Agent Standards Initiative in February 2026
([NIST](https://nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure)).
Agentic AI is therefore **a way of using models**, not a new layer in Figure 1.
{doc}`../module-3/04-agents` shows how to build one.

### Artificial general intelligence (AGI)

**AGI** names a **capability level**, not a technique, and there is **no single
agreed definition**. Three widely cited ones show the range:

- **Economic.** The OpenAI Charter (2018) defines AGI as highly autonomous
  systems that outperform humans at most economically valuable work
  ([OpenAI Charter](https://openai.com/charter/)).
- **Levels.** Researchers at Google DeepMind propose levels from Emerging to
  Superhuman, crossed with narrow versus general scope. They place 2023 chatbots
  such as ChatGPT at **Emerging AGI** and say the **Competent AGI** level, at
  least as good as the median skilled adult on a wide range of non-physical
  tasks, had not been reached {cite}`morris2024levels`.
- **Cognitive test.** A 2025 proposal by Dan Hendrycks, Yoshua Bengio and
  coauthors defines AGI as matching or exceeding the cognitive versatility and
  proficiency of a well-educated adult, scored across ten areas of human
  cognition. Under their scoring GPT-4 reached 27 percent and GPT-5 57 percent
  {cite}`hendrycks2025definition`.

Because the definitions disagree, a claim that AGI has arrived is contested by
design. When Microsoft and OpenAI restructured their partnership in October 2025,
they agreed that any OpenAI declaration of AGI would be **verified by an
independent expert panel**
([OpenAI](https://openai.com/index/next-chapter-of-microsoft-openai-partnership/)).

### Superintelligence (ASI)

**Superintelligence**, or artificial superintelligence (ASI), means an intellect
that **greatly exceeds** the best humans in practically every field. The
philosopher Nick Bostrom gave the classic definition in 1998 and refined it in
his 2014 book: any intellect that greatly exceeds the cognitive performance of
humans in virtually all domains of interest {cite}`bostrom2014superintelligence`.
In the DeepMind levels, it is Level 5 general AI, outperforming all humans, and
it has not been achieved; some **narrow** systems, such as AlphaFold for protein
structures, are already superhuman at a single task {cite}`morris2024levels`.

The word has recently moved from philosophy into company names and public
debate:

- In June 2025 Meta created **Meta Superintelligence Labs**
  ([TechCrunch](https://techcrunch.com/2025/06/30/meta-restructures-its-ai-unit-under-superintelligence-labs/)),
  and in July 2025 Mark Zuckerberg described Meta's goal as personal
  superintelligence for everyone ([Meta](https://www.meta.com/superintelligence/)). Its first models,
  the Muse series, appear in Part 2.
- In November 2025 Microsoft AI formed the MAI Superintelligence Team under
  Mustafa Suleyman, who described the goal as **humanist superintelligence**:
  advanced AI that always works for and in service of people and humanity
  ([Microsoft AI, Towards Humanist Superintelligence](https://microsoft.ai/news/towards-humanist-superintelligence/)).
- In October 2025 the Future of Life Institute released a **Statement on
  Superintelligence** calling for a prohibition on developing superintelligence
  until there is broad scientific consensus that it can be done safely and
  strong public buy-in. Signers include Geoffrey Hinton, Yoshua Bengio and
  Stuart Russell, and the statement listed more than 77,000 signatures in
  October 2026 ([superintelligence-statement.org](https://superintelligence-statement.org/)).

When a company says it is building superintelligence, it is describing a goal,
not a product you can use today.

### Open weights and open source

Two phrases describe how freely a model is shared. A model has **open weights**
when anyone can download its trained parameters and run it on their own
hardware. **Open source** is a stricter idea. The Open Source Initiative's Open Source AI
Definition 1.0 (October 2024) requires the freedoms to use, study, modify and
share the system, plus what is needed to modify it: detailed information about
the training data, the complete training and inference code, and the weights
([OSI](https://opensource.org/ai/open-source-ai-definition)). The OSI notes that
weights alone fall short of this because they omit the code and data needed to
reproduce training ([OSI, Open Weights](https://opensource.org/ai/open-weights)).

By that standard, most downloadable models are **open weights, not open
source**. Models that did pass the OSI's validation include EleutherAI's Pythia,
AI2's OLMo and Google's T5 ([OSI FAQ](https://opensource.org/ai/faq)). Their licenses also differ. OpenAI's gpt-oss models and Google's
Gemma 4 use the permissive Apache 2.0 license, while Meta's Llama 4 uses Meta's
own community license, which requires companies with more than 700 million
monthly active users to obtain a separate license and binds all users to an
acceptable use policy
([Llama 4 license](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)).
Part 2 notes the license for each model family.

### The terms at a glance

```{list-table}
:header-rows: 1
:widths: 24 46 30

* - Term
  - One-line meaning
  - What kind of term
* - AI
  - Machines doing tasks that need human-like intelligence
  - Field (broadest)
* - Machine learning
  - Learning patterns from data instead of hand-written rules
  - Approach within AI
* - Deep learning
  - Machine learning with many-layered neural networks
  - Approach within ML
* - NLP
  - Computers working with human language
  - Problem area that cuts across approaches
* - Generative AI
  - Models that create new content
  - Kind of model
* - LLM
  - Deep-learning model trained on huge text corpora to predict and generate text
  - Kind of model
* - Foundation model
  - Broadly pretrained model adapted to many tasks
  - Kind of model
* - Frontier model
  - The most capable foundation models of the moment
  - Moving tier, sometimes a legal category
* - Reasoning model
  - LLM trained to think before answering
  - Kind of model
* - Agentic AI
  - Model in a loop with tools, pursuing a goal over many steps
  - Way of using models
* - AGI
  - Human-level ability across most intellectual tasks
  - Hypothetical capability level
* - Superintelligence
  - Far beyond the best humans in nearly every field
  - Hypothetical capability level
```

## Part 2: The major AI assistants and model families

When people name an AI tool, they may mean any of three different things:

- the **company** that builds it (OpenAI, Anthropic, Google, Meta, Mistral AI);
- the **model family**, the trained network itself (GPT, Claude, Gemini, Muse,
  Llama);
- the **app or agent** you actually use (ChatGPT, the Claude app, the Gemini
  app, Meta AI, Mistral Vibe), which wraps one or more models with a chat
  interface, tools, memory and plans.

Keeping the layers apart explains a lot of confusion. The same model can sit
behind several apps, an app can switch models without changing its name, and a
company can sell its models to developers through cloud platforms such as Amazon
Bedrock while also running its own consumer app.

```{admonition} A snapshot, not a ranking
:class: warning
This part describes the landscape as of mid-October 2026. AI products are
renamed, merged, repriced and retired every few months, and several items below
changed during 2026 alone. Vendor claims about benchmarks are the vendors' own.
Check each provider's current documentation before relying on a detail here.
```

```{list-table} Major assistants and model families (mid-October 2026)
:header-rows: 1
:widths: 13 19 26 24 18

* - Company
  - Assistant or agent
  - Main models
  - Weights
  - On Amazon Bedrock
* - OpenAI
  - ChatGPT, Codex
  - GPT-6 Astra, GPT-6.1 Sol, GPT-6 Luna
  - Flagships closed; gpt-oss open weights (Apache 2.0)
  - Yes, including GPT-6 Astra and gpt-oss
* - Anthropic
  - Claude app, Claude Code
  - Claude Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5
  - Closed
  - Yes
* - Google
  - Gemini app
  - Gemini 4 Argon, Gemini 3.8 Flash
  - Gemini closed; Gemma 4 open weights (Apache 2.0)
  - Gemma only
* - Meta
  - Meta AI, Muse agent, Muse Code
  - Muse Wonder, Muse Spark
  - Mixed: Muse Spark Open, Muse Glimmer and Llama 4 downloadable
  - Llama only
* - Mistral AI
  - Vibe (formerly Le Chat)
  - Mistral Medium 3.5, Mistral Large 4 (preview)
  - Mostly open weights
  - Yes, Mistral 3 family and Devstral 2
* - Amazon
  - Amazon Quick, Kiro
  - Amazon Nova 2 models, plus models from other providers
  - Closed
  - Yes (Nova)
* - DeepSeek
  - DeepSeek app
  - DeepSeek V4 family
  - Open weights (MIT)
  - Earlier models (V3.x, R1)
* - Alibaba
  - Qwen app
  - Qwen3.8
  - Open weights, licenses vary
  - Earlier Qwen3 models
* - xAI (now part of SpaceX)
  - Grok
  - Grok 4.7
  - Flagship closed
  - Yes
* - Microsoft
  - Copilot
  - Models from OpenAI and Anthropic, among others
  - Not applicable
  - Not applicable
* - Perplexity
  - Perplexity, Comet browser
  - Sonar plus third-party models
  - Not applicable
  - Not applicable
* - OpenClaw Foundation
  - OpenClaw
  - Any model you connect
  - Software is open source (MIT)
  - Can use Bedrock models
```

Sources for the table are given in the sections below; the Bedrock column is
based on the Amazon Bedrock model catalog
([AWS, Bedrock model cards](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html)).

### OpenAI: ChatGPT, Codex and GPT models

**ChatGPT** is OpenAI's assistant. Its launch on November 30, 2022 brought
conversational generative AI to a mass audience
([OpenAI, Introducing ChatGPT](https://openai.com/index/chatgpt/)). In
October 2026 OpenAI's lineup centers on the GPT-6 generation: **GPT-6 Astra**,
which OpenAI calls its most intelligent model and rolled out first to a limited
set of organizations in early September 2026 before opening it to ChatGPT
Plus, Pro, Business and Enterprise users, and the cheaper **GPT-6 Sol** (since updated to **GPT-6.1 Sol**) and
**GPT-6 Luna** for everyday work
([OpenAI, GPT-6 Astra](https://openai.com/index/gpt-6-astra/);
[OpenAI, GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna/)).
ChatGPT's plans run from Free and Go through Plus, Pro, Business and Enterprise,
and the models you get depend on the plan
([ChatGPT pricing](https://chatgpt.com/pricing)). **Codex** is OpenAI's coding
agent, available in the ChatGPT apps, a command-line tool, an IDE extension and
the cloud ([OpenAI, Codex docs](https://learn.chatgpt.com/docs)).

The two GPT-6 models you will see compared most often are:

- **GPT-6 Astra**, OpenAI's most capable model, aimed at complex reasoning,
  coding, computer use and research. It costs 10 dollars per million input
  tokens and 50 dollars per million output tokens. OpenAI says it meets the
  Critical threshold for cybersecurity under its Preparedness Framework, so for
  now it refuses some advanced security tasks
  ([OpenAI, GPT-6 Astra](https://openai.com/index/gpt-6-astra/)).
- **GPT-6.1 Sol**, introduced on September 29, 2026, the cheaper model for
  everyday professional work, at 2 dollars per million input tokens and 10
  dollars per million output tokens. OpenAI reports that it matches Astra on one
  coding test and approaches it on a document test at roughly one fifth of the
  cost ([OpenAI, Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/)).

Both have a context window of 1,050,000 tokens, of which up to 922,000 can be
input, can write up to 128,000 tokens in one response, have a knowledge cutoff of
April 30, 2026, and offer reasoning effort from low to max. Prompts longer than
272,000 input tokens cost more: twice the input rate and one and a half times
the output rate for the whole request
([OpenAI, GPT-6 Astra model page](https://developers.openai.com/api/docs/models/gpt-6-astra);
[OpenAI, GPT-6.1 Sol model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol)).

OpenAI's flagship models are closed (you cannot download the weights), but in
August 2025 it released **gpt-oss-120b** and **gpt-oss-20b**, open-weight
reasoning models under the Apache 2.0 license; the smaller one runs within 16 GB
of memory ([OpenAI, gpt-oss](https://openai.com/index/introducing-gpt-oss/)).
Since September 8, 2026, GPT-6 Astra has also been generally available on
**Amazon Bedrock**, and the Bedrock catalog lists GPT-6.1 Sol, GPT-6 Sol and
GPT-6 Luna as well
([AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/09/openai-gpt-6-astra-on-amazon-bedrock/);
[AWS, Bedrock model cards](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html)).

### Anthropic: Claude

**Claude** is Anthropic's assistant and model family, available in the Claude
apps for web, desktop and mobile, through the Claude API, and on Amazon Bedrock,
Google Cloud and Microsoft's cloud. In October 2026 Anthropic's documentation
lists four current models
([Claude models overview](https://platform.claude.com/docs/en/models/overview)):

- **Claude Fable 5.1** (September 2026), which Anthropic calls its most capable
  generally available model ([Anthropic, Claude Fable](https://www.anthropic.com/claude/fable));
- **Claude Opus 5.5** (September 2026), which Anthropic says performs at the
  level of Fable 5.1 on most work at a lower price
  ([Anthropic, Claude Opus 5.5](https://www.anthropic.com/news/claude-opus-5-5));
- **Claude Sonnet 5.5** (September 2026), a faster and cheaper complement to
  Opus ([Anthropic, Claude Sonnet 5.5](https://www.anthropic.com/news/claude-sonnet-5-5));
- **Claude Haiku 5.5** (October 2026), the small, low-cost model for
  high-volume work such as summarization, classification and subagents
  ([Anthropic, Claude Haiku 5.5](https://www.anthropic.com/news/claude-haiku-5-5)).

A separate model, **Claude Mythos 5.1**, shares Fable 5.1's underlying model but
is restricted to vetted cybersecurity defenders and life scientists; Fable 5.1
is the generally available version with added safeguards in those areas
([Anthropic, Mythos](https://www.anthropic.com/claude/mythos)). Claude models
are closed. **Claude Code** is Anthropic's agentic coding tool, which runs in a
terminal, IDE extensions, a desktop app and the web, and can also use Claude
through Amazon Bedrock ([Claude Code overview](https://code.claude.com/docs/en/overview);
[Claude Code on Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock)).
All current Claude models appear in the Amazon Bedrock model catalog
([AWS, Anthropic on Bedrock](https://aws.amazon.com/bedrock/anthropic/)), which
is why the labs in this book can use them.

### Google: Gemini and Gemma

**Gemini** is both Google's assistant app and its model family. Its flagship is
**Gemini 4 Argon**, the first model of the Gemini 4 generation. Google first
offered it to select cybersecurity partners on September 30, 2026 and made it
generally available on October 13, 2026, to developers through the
Gemini API and AI Studio and to Google AI Pro and Ultra subscribers in the Gemini
app and AI Mode in Search
([Google, Gemini 4 Argon](https://blog.google/intl/en-in/products/introducing-gemini-4-argon/);
[Reuters via Khaleej Times](https://www.khaleejtimes.com/business/google-announces-gemini-4-flagship-ai-model-after-months-of-delays-2)).
The essentials:

- **Context.** One combined limit of 1 million tokens covers input and output
  together ([Google, Gemini 4 Argon model card](https://deepmind.google/models/model-cards/gemini-4-argon/)).
- **Thinking.** Argon reasons before it answers, and developers choose how much
  with a thinking level that defaults to medium, the Gemini version of the
  effort settings in Part 3
  ([Gemini thinking](https://ai.google.dev/gemini-api/docs/thinking)).
- **Price.** Through November 30, 2026 the API charges 2 dollars per million
  input tokens and 10 dollars per million output tokens, thinking included. From
  December 1, 2026 both prices double, to 4 and 20 dollars
  ([Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)).
- **What Google emphasizes.** Google highlights knowledge work, agentic coding,
  very long documents, 3D and visual coding, and safety behavior such
  as pausing for human confirmation before irreversible steps. These are the
  vendor's own claims; the head-to-head comparison at the end of this part shows
  how independent tests see it.
- **Where it is not.** Gemini models are not offered on Amazon Bedrock, so the
  Bedrock labs in this book cannot call Argon
  ([AWS, Bedrock model cards](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html)).

**Gemini 3.8 Flash** (September 2026) is Google's most intelligent Flash model
for everyday work, and smaller Flash-Lite models serve low-cost uses
([Google, Gemini 3.8 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/);
[Gemini API models](https://ai.google.dev/gemini-api/docs/models)). The Gemini
app has a free tier and paid Google AI Plus, Pro and Ultra plans
([Gemini subscriptions](https://gemini.google/subscriptions/)).

Gemini models are closed, but Google also publishes **Gemma**, a family of
open-weight models. **Gemma 4** (April 2026) comes in sizes from about 2 billion
to 31 billion parameters under the Apache 2.0 license and is built from the same
research as Gemini 3
([Google Open Source Blog](https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html);
[9to5Google](https://9to5google.com/2026/04/02/google-gemma-4/)).

### Meta: Meta AI, Muse and Llama

Meta's assistant, **Meta AI**, lives in WhatsApp, Instagram, Facebook,
Messenger and Ray-Ban Meta glasses. Meta's model strategy changed sharply in
2026:

- **Llama** was Meta's family of downloadable models. The last major release was
  **Llama 4** (Scout and Maverick) in April 2025, under the Llama 4 Community
  License, which has use restrictions and is not an open source license in the
  OSI sense ([Llama 4 license](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)).
- **Muse** is the new model series from Meta Superintelligence Labs. **Muse
  Spark** (April 8, 2026) is a small, fast multimodal model with Instant and
  Thinking modes that now powers Meta AI; it was not released as open weights
  ([Meta, Muse Spark](https://about.fb.com/news/2026/04/introducing-muse-spark-meta-superintelligence-labs/)).
  Commentators described the move as a pivot away from Meta's open-weights Llama
  strategy ([The Batch](https://charonhub.deeplearning.ai/with-muse-spark-meta-pivots-away-from-its-open-weights-llama-strategy/)).
- **Muse**, the agent, launched in the US on September 8, 2026 as a personal AI
  agent that runs on a dedicated cloud machine, browses the web, fills out forms
  and can pay for things, checking with the user before sensitive actions such
  as sending email or making purchases
  ([Meta, Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse)).
- **Muse Wonder** (October 12, 2026), which Meta calls its most capable model to
  date, is aimed at agentic tasks and offered through the Meta Model API and the Muse Code
  coding agent ([Meta, Muse Wonder](https://about.fb.com/news/2026/10/introducing-muse-wonder-models/)).
- Meta has also returned to downloadable models: **Muse Glimmer** (August 2026),
  a roughly 30 billion parameter model under Apache 2.0
  ([Meta, Muse Glimmer](https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model)),
  and **Muse Spark Open** (October 15, 2026), a large mixture-of-experts model
  under Meta's own Muse Model License, which requires attribution and limits some
  commercial hosting
  ([Meta, Muse Spark Open](https://research.meta.ai/blog/muse-spark-open);
  [Hugging Face model card](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B)).

### Mistral AI: Mistral Vibe

**Mistral AI** is a French company. On May 28, 2026 it renamed its **Le Chat**
assistant to **Vibe**: one agent and one subscription for both work and code,
with a Work Mode for multi-step tasks across connected apps, a Code Mode that
runs coding sessions in the cloud and opens pull requests, the **Vibe CLI** for
the terminal and a VS Code extension
([Mistral AI, Vibe](https://mistral.ai/news/vibe-agent/)). Mistral is known for
releasing many of its models as open weights. **Mistral Medium 3.5** (spring
2026), a 128 billion parameter model that powers Vibe, is open weights under a
modified MIT license
([Mistral AI, Medium 3.5](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5)),
and the **Mistral 3** family (December 2025), including Mistral Large 3, uses
Apache 2.0 and is available on Amazon Bedrock
([Mistral AI, Mistral 3](https://mistral.ai/news/mistral-3)). On October 6, 2026
Mistral previewed **Mistral Large 4**, a one trillion parameter
mixture-of-experts model, and said it would release the weights by the end of
October ([Mistral AI, Large 4](https://mistral.ai/news/mistral-large-4)).

### Amazon: Quick, Kiro and Nova

Amazon's AI products for people (as opposed to developers' building blocks such
as Bedrock) were reorganized in 2025 and 2026:

- **Amazon Quick**, launched in October 2025 as **Amazon Quick Suite** and now
  simply called Amazon Quick, is Amazon's AI assistant for work. AWS describes it
  as a set of agentic teammates for chat, research, business insights and
  automation, with a desktop app that works with local files and free and paid
  plans that do not require an AWS account
  ([AWS, Amazon Quick](https://aws.amazon.com/quick/);
  [AWS, Free and Plus plans](https://aws.amazon.com/about-aws/whats-new/2026/04/amazon-quick-free-plus/);
  [AWS, launch announcement](https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-quick-suite-agentic-ai-powered-workspace)).
- **Amazon Q** is being phased out. Amazon Q Business no longer accepts new
  customers, and AWS recommends moving to Amazon Quick
  ([AWS docs](https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/qbusiness-availability-change.html)).
  Amazon Q Developer's IDE plugins and paid subscriptions reach end of support on
  April 30, 2027, with **Kiro** as the recommended successor
  ([AWS DevOps Blog](https://aws.amazon.com/blogs/devops/amazon-q-developer-end-of-support-announcement/)).
- **Kiro** is AWS's agentic coding tool, built around spec-driven development:
  it turns a prompt into requirements, a design and a task list before writing
  code, and lets you choose among models from Anthropic, OpenAI and open-weight
  providers ([Kiro](https://kiro.dev/)). Through the Kiro Students program, eligible
  students at participating universities get a year of Kiro with monthly credits
  ([AWS Weekly Roundup, September 14, 2026](https://aws.amazon.com/blogs/aws/aws-weekly-roundup-openai-gpt-6-astra-on-amazon-bedrock-amazon-quick-desktop-ga-kiro-for-students-and-more-september-14-2026/)).
- **Amazon Nova** is Amazon's own model family on Bedrock. The Nova 2 models
  arrived in December 2025. In mid-2026 Amazon was reported to be scaling back
  several Nova models to focus on a new frontier model; Nova Canvas and Nova
  Reel reached end of life on Bedrock in several Regions on September 30, 2026,
  while Nova 2 Lite, Nova 2 Sonic, Nova Forge and Nova Act continue
  ([Amazon](https://www.aboutamazon.com/news/aws/aws-agentic-ai-amazon-bedrock-nova-models);
  [eWeek](https://www.eweek.com/news/amazon-nova-ai-overhaul/);
  [AWS, Bedrock model lifecycle](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle-legacy.html)).

### DeepSeek and Qwen: open-weight models from China

**DeepSeek** is a Chinese AI lab whose models drew worldwide attention in early
2025. Its technical report for **DeepSeek-V3** (December 2024) described a
mixture-of-experts model with 671 billion parameters, of which 37 billion are
active for each token, trained in 2.788 million GPU hours; that figure is the
source of widely quoted low training cost claims, and it excludes earlier
research and experiments ([DeepSeek-V3 technical report](https://arxiv.org/abs/2412.19437)).
**DeepSeek-R1**, released on January 20, 2025 with weights under the MIT
license, was a reasoning model that DeepSeek said performed on par with OpenAI's
o1 ([DeepSeek](https://api-docs.deepseek.com/news/news250120)); its training
method is described in Part 1 and Part 3. The **DeepSeek V4** generation followed
in 2026, again as open weights under the MIT license, with a one million token
context window ([DeepSeek, V4 preview](https://api-docs.deepseek.com/news/news260424);
[Hugging Face, DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)).

Several governments have restricted DeepSeek's hosted app and services, citing
security risks and the transfer of users' personal data to China. Australia banned DeepSeek products from
government devices in February 2025, Italy blocked the app over its handling of
personal data, and in June 2025 a German data protection commissioner asked Apple
and Google to remove it from their German app stores
([Reuters via Ada Derana](https://adaderana.lk/news/105560/australia-bans-deepseek-on-government-devices-citing-security-concerns);
[Berlin Commissioner for Data Protection](https://www.datenschutz-berlin.de/fileadmin/user_upload/pdf/pressemitteilungen/2025/20250627-BlnBDI-Press-Release_DeepSeek.pdf)).
Those concerns apply to the hosted service. Open weights can also be run on
other infrastructure; for example, Amazon Bedrock offers several DeepSeek models
([Bedrock model cards](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html)).
Check your organization's policy before using any model with sensitive data.

**Qwen** is Alibaba's model family and app. In August 2026 Alibaba released
**Qwen3.8**, including a very large mixture-of-experts model under a custom
license that requires larger commercial providers to obtain a separate license,
and a 27 billion parameter model under Apache 2.0
([eWeek](https://www.eweek.com/news/alibaba-qwen3-8-27b-license-apac-china/)).
Amazon Bedrock offers several earlier Qwen3 models
([Bedrock model cards](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html)).

### OpenClaw: an open-source agent you run yourself

**OpenClaw**, introduced in {doc}`ai-and-tools-reference`, is different from
everything above: it is **not a model** but an open-source (MIT-licensed)
personal agent that runs on your own computer and that you talk to through chat
apps such as WhatsApp, Telegram, Slack, Discord or iMessage. You connect it to a
model of your choice, from a cloud provider such as Anthropic, OpenAI, Google,
DeepSeek, Mistral or Amazon Bedrock, or a local runtime such as Ollama, and
extend it with skills and plugins ([OpenClaw on GitHub](https://github.com/openclaw/openclaw);
[OpenClaw docs, providers](https://docs.openclaw.ai/providers)).
Created by Peter Steinberger in November 2025, it was briefly called Clawdbot
and then Moltbot before taking the name OpenClaw on January 30, 2026
([OpenClaw docs](https://docs.openclaw.ai/start/lore)). Since July 2026 it has
been stewarded by the **OpenClaw Foundation**, a US non-profit whose partners
include OpenAI, NVIDIA, Microsoft and the University of Michigan
([OpenClaw Foundation](https://openclaw.ai/blog/introducing-openclaw-foundation)).

OpenClaw is also a case study in **agent security**. An agent that can read your
messages and files and run commands is a powerful target:

- A high-severity vulnerability, CVE-2026-25253, let a single malicious link
  steal an access token from versions before 2026.1.29
  ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-25253)).
- Researchers found 341 malicious skills among 2,857 in the ClawHub skill
  registry, most of them using fake setup steps to install information-stealing
  malware on Macs ([The Hacker News](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)).
- In March 2026 China's government reportedly warned state-run firms and public
  bodies against installing OpenClaw on office computers
  ([Tom's Hardware](https://tomshardware.com/tech-industry/artificial-intelligence/china-bans-openclaw-from-government-computers-and-issues-security-guidelines-amid-adoption-frenzy)).

The lesson applies to every agent in this chapter: give an agent only the
permissions it needs, install skills only from sources you trust, keep it
updated, and rely on limits you can check from outside rather than on the
agent's own reports about what it did {cite}`trivedi2026verifiable`.

### Other assistants you will meet

- **Microsoft Copilot** is Microsoft's assistant across Windows and Microsoft
  365, already introduced in {doc}`ai-and-tools-reference`. In August 2026
  Microsoft began merging the consumer Copilot app and the Microsoft 365 Copilot
  app into a single app
  ([Windows Central](https://www.windowscentral.com/artificial-intelligence/microsoft-copilot/microsoft-begins-unified-copilot-app-rollout-reveals-major-plan-to-merge-copilot-and-microsoft-365-copilot-across-all-platforms-along-with-updated-branding)),
  and in many features of Microsoft 365 Copilot users can choose between
  OpenAI and Anthropic models where their organization allows it
  ([Microsoft Learn](https://learn.microsoft.com/microsoft-365/copilot/connect-to-ai-subprocessor)).
  Microsoft builds the assistant; the underlying models come largely
  from other companies.
- **Grok** is the assistant from **xAI**, which SpaceX acquired in February 2026
  and which has since been rebranded under the SpaceX name
  ([Yahoo Finance](https://finance.yahoo.com/news/elon-musks-spacex-merges-xai-153111324.html)).
  Its newest model, **Grok 4.7** (September 2026), is aimed at coding and
  knowledge work, has no downloadable weights, and is available through the
  Grok API and on Amazon Bedrock ([Grok 4.7 announcement](https://x.ai/news/grok-4-7);
  [AWS, Grok 4.7 on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/grok-4-7-is-now-available-on-amazon-bedrock/)). In January 2026 California's
  attorney general opened an investigation into whether Grok had been used to
  create sexualized images of real people without their consent, and regulators
  in France, the United Kingdom and the EU opened similar inquiries
  ([California Attorney General](https://www.oag.ca.gov/news/press-releases/attorney-general-bonta-launches-investigation-xai-grok-over-undressed-sexual-ai);
  [Insurance Journal](https://amp.insurancejournal.com/news/west/2026/01/15/854280.htm)),
  a reminder of the responsible-AI issues covered in Module 2.
- **Perplexity** is an AI answer engine that searches the web and cites its
  sources; paid users can choose among third-party models or Perplexity's own
  Sonar model, and the company also makes the **Comet** AI browser
  ([Perplexity Help Center](https://www.perplexity.ai/help-center/en/articles/10352901-what-is-perplexity-pro);
  [Perplexity, Comet](https://www.perplexity.ai/comet)).
  In March 2026 a federal judge granted Amazon a preliminary injunction blocking
  Comet's agent from shopping in password-protected parts of Amazon's site for
  its users, an early legal test of agents acting on people's behalf
  ([GeekWire](https://www.geekwire.com/2026/judge-blocks-perplexitys-ai-bot-from-shopping-on-amazon-in-early-test-of-agentic-commerce/)).

### Head to head: four flagships in October 2026

Four models dominate comparisons this fall: Anthropic's **Claude Opus 5.5**,
OpenAI's **GPT-6 Astra** and **GPT-6.1 Sol**, and Google's **Gemini 4 Argon**.
They arrived within a few weeks of each other, and comparing them is also a
lesson in reading benchmarks, because the answer depends on who ran the test,
how, and at which effort setting.

**Specifications and price.** These come from each company's own documentation.

```{list-table} Four flagship models compared: specifications (mid-October 2026)
:header-rows: 1
:widths: 20 20 20 20 20

* - Measure
  - Claude Opus 5.5
  - GPT-6 Astra
  - GPT-6.1 Sol
  - Gemini 4 Argon
* - Released
  - September 22, 2026
  - September 3, 2026, first to a limited set of organizations
  - September 29, 2026
  - September 30, 2026 for select partners; generally available October 13
* - Context window
  - 1M tokens
  - 1,050,000 tokens (up to 922,000 input)
  - 1,050,000 tokens (up to 922,000 input)
  - 1,048,576 tokens, shared by input and output
* - Longest single response
  - 128,000 tokens
  - 128,000 tokens
  - 128,000 tokens
  - 65,536 tokens by default; up to about 1M with long decode
* - API price per million input and output tokens
  - 4 and 20 dollars
  - 10 and 50 dollars
  - 2 and 10 dollars
  - 2 and 10 dollars through November 30, 2026; 4 and 20 dollars from
    December 1
* - Effort or thinking settings
  - Low to max; default medium
  - Low to max
  - Low to max; default medium
  - Low, medium or high; default medium
* - On Amazon Bedrock
  - Yes
  - Yes
  - Yes
  - No
```

Sources:
[Claude models overview](https://platform.claude.com/docs/en/models/overview);
[Anthropic, Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5);
[Anthropic, Effort](https://platform.claude.com/docs/en/build-with-claude/effort);
[OpenAI, GPT-6 Astra model page](https://developers.openai.com/api/docs/models/gpt-6-astra);
[OpenAI, GPT-6.1 Sol model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol);
[OpenAI, GPT-6 Astra](https://openai.com/index/gpt-6-astra/);
[Google, Gemini 4 Argon model page](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon);
[Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing);
[AWS, Bedrock model cards](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html).
OpenAI charges more for prompts longer than 272,000 input tokens, as described
above.

**Independent results.** Artificial Analysis runs the same tests on every model
itself. Each model below was tested at its highest setting: max effort for the
Anthropic and OpenAI models and high thinking for Argon.

```{list-table} Four flagship models compared: independent results from Artificial Analysis
:header-rows: 1
:widths: 28 18 18 18 18

* - Measure
  - Claude Opus 5.5
  - GPT-6 Astra
  - GPT-6.1 Sol
  - Gemini 4 Argon
* - Intelligence Index v4.3.2 (higher is better)
  - **58**
  - 53
  - 52
  - 53
* - Cost per Intelligence Index task
  - 5.98 dollars
  - 3.26 dollars
  - **0.72 dollars**
  - 1.99 dollars at the introductory price (3.98 dollars at the full price)
* - Hallucination rate on AA-Omniscience (lower is better)
  - Not given in the published summary
  - 51%
  - 54%
  - **15%**
* - Output speed
  - **About 97 tokens per second**
  - About 57 tokens per second
  - About 66 tokens per second
  - Not yet reported
* - Time to first answer token, including thinking (lower is better)
  - About 728 seconds
  - **About 269 seconds**
  - About 324 seconds
  - Not yet reported
```

Sources:
[Artificial Analysis, Claude Opus 5.5](https://artificialanalysis.ai/models/claude-opus-5-5);
[Artificial Analysis, GPT-6 Astra](https://artificialanalysis.ai/models/gpt-6-astra);
[Artificial Analysis, GPT-6.1 Sol and Claude Opus 5.5](https://artificialanalysis.ai/models/releases/comparisons/gpt-6-1-sol-vs-claude-opus-5-5);
[Artificial Analysis, Gemini 4 Argon and Claude Opus 5.5](https://artificialanalysis.ai/models/comparisons/gemini-4-argon-vs-claude-opus-5-5);
[Artificial Analysis, Gemini 4 Argon article](https://artificialanalysis.ai/articles/gemini-4-argon-google-top-three-labs).
Bold marks the best figure in each row. Artificial Analysis updates its
measurements, so figures on its pages can change over time; at the time of
writing it had not yet published speed figures for Argon.

In the same independent testing, Opus 5.5 led GPT-6.1 Sol on Humanity's Last
Exam (61.4 percent against 52.9) and Terminal-Bench 4.0 (59.6 against 56.1),
while Sol scored higher on GDP.pdf, which OpenAI describes as a test of
answering questions about professional PDF documents (31.0 against 26.2)
([Artificial Analysis](https://artificialanalysis.ai/models/releases/comparisons/gpt-6-1-sol-vs-claude-opus-5-5);
[OpenAI, Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/)).

**Results reported by a vendor.** Google's model card for Argon reports scores
for Argon, Astra and Opus 5.5 side by side; GPT-6.1 Sol is not included.

```{list-table} Selected results from Google's Gemini 4 Argon model card (vendor-reported, October 2026)
:header-rows: 1
:widths: 34 22 22 22

* - Benchmark (what it tests)
  - Claude Opus 5.5
  - GPT-6 Astra
  - Gemini 4 Argon
* - Terminal-bench 4.0 (work in a command-line terminal)
  - **66.4%**
  - 58.2%
  - 57.4%
* - FrontierSWE v2 (large software engineering projects)
  - 62.3%
  - **65.5%**
  - 55.0%
* - DeepSWE v1.1 (agentic coding)
  - 74.2%
  - 74.1%
  - **77.9%**
* - OSWorld-2.0, offline subset (operating a computer)
  - Not reported
  - **72.6%**
  - 69.2%
* - Vals Index (professional knowledge work)
  - 67.0%
  - 63.1%
  - **68.9%**
* - GraphWalks, 256K to 1M tokens (long-context reasoning, F1)
  - 66.8%
  - 71.8%
  - **84.2%**
```

Source: [Google, Gemini 4 Argon model card](https://deepmind.google/models/model-cards/gemini-4-argon/).
Bold marks the best figure in each row.

Five lessons come out of these tables:

1. **Who ran the test matters.** On Terminal-Bench 4.0, Opus 5.5 scored 66.4
   percent in Anthropic's own run at its xhigh effort setting, the figure
   Google's card also lists, but about 60 percent when Artificial Analysis ran
   the test itself.
2. **Versions of a benchmark differ.** OpenAI's announcement of Astra quotes a
   score of 61.2 on an earlier version (4.1) of the Artificial Analysis
   Intelligence Index, while the current version 4.3.2 gives Astra 53. Both are
   correct for their version, and they cannot be compared with each other
   ([OpenAI, GPT-6 Astra](https://openai.com/index/gpt-6-astra/)).
3. **Effort changes the gap.** At low effort, Opus 5.5 and GPT-6.1 Sol both
   score 42 on the Artificial Analysis index, at 0.55 and 0.13 dollars per task.
   At max effort, Opus 5.5 pulls ahead, 58 to 52, but its cost per task rises to
   5.98 dollars against 0.72 for Sol, and its time to first answer token grows
   from under 7 seconds to more than 12 minutes
   ([Artificial Analysis](https://artificialanalysis.ai/models/releases/comparisons/gpt-6-1-sol-vs-claude-opus-5-5)).
   That is Part 3 in action.
4. **Price per token is not price per task.** Argon and Sol charge the same
   per token until November 30, 2026, yet Argon cost about 1.99 dollars per
   index task against 0.72 for Sol, because it produced about 62,000 output
   tokens per task. Astra has the highest price per token of the four but costs
   less per task than Opus 5.5 at max effort.
5. **A hallucination rate is not an accuracy score.** Artificial Analysis
   defines the hallucination rate on its AA-Omniscience knowledge test as how
   often a model guesses when it lacks the required knowledge, instead of
   admitting it does not know
   ([Artificial Analysis, AA-Omniscience](https://artificialanalysis.ai/articles/aa-omniscience-knowledge-hallucination-benchmark)).
   Argon guessed far less often (15 percent against 51 for Astra), but Astra
   answered more questions correctly (63 percent against 50 for Argon). One
   model knows more; the other is better at knowing what it does not know.

**Which should you choose?** There is no single winner, so match the model to
the work:

- **Claude Opus 5.5** led the independent intelligence index, and it led
  terminal-based coding against the models tested in both vendor and
  independent runs. It is the most expensive per task
  at max effort and, of the three models with measured times, the slowest to
  start answering at that setting.
- **GPT-6 Astra** posted the best reported results in the tables above for
  operating a computer and for large software projects. It has the highest price
  per token and guessed often on the AA-Omniscience test.
- **GPT-6.1 Sol** was by far the cheapest per task and matched Opus 5.5 at low
  effort, which makes it a strong default for high-volume and budget-sensitive
  work.
- **Gemini 4 Argon** guessed least in independent testing, led long-context
  reasoning and professional knowledge work in Google's tests, and can write very
  long single responses with long decode. Its
  price doubles on December 1, 2026.
- **In this book's labs**, Opus 5.5, Astra and Sol are all available on Amazon
  Bedrock; Argon is not.
- **Whatever you pick**, run a small evaluation on your own tasks before you
  commit, as {doc}`../module-2/01-evaluating-llms` recommends; a lead of a few
  points on someone else's benchmark rarely predicts which model will do better
  on your work.

## Part 3: Effort levels, explained in detail

The model menu in Anthropic's Claude apps offers an effort setting with options
from Low to Max, and above the options it shows this description:

> Higher effort means more thorough responses, but takes longer and uses your
> limits faster.

Anthropic's Help Center says the same thing in its own words: higher effort is
more thorough but slower, and it uses more tokens, so you reach your usage limits
faster ([Claude Help Center, model, effort and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)).
ChatGPT and Gemini have similar controls under different names. The sentence
makes three claims, and each one has a concrete technical reason behind it.

```{figure} ../_static/effort-levels.svg
:alt: Three rows show the same model answering the same prompt at low, medium and high or maximum effort. At low effort there is one short thinking step before the answer. At medium effort there are a few thinking steps and one tool call. At high or maximum effort there are many thinking steps, several tool calls and a self-check before a longer answer. An arrow shows that waiting time, tokens used and checking all grow with effort.
:width: 100%
:align: center

What changes when you raise the effort level. The model and the prompt stay the
same; what grows is the work done before and during the answer.
```

### What effort is, and what it is not

An **effort level** tells a model **how much work to put into this particular
request**: how much to think before answering, how many tools to call, and how
much to check its own work. It is easiest to understand by what it does **not**
change:

- **It does not change what the model knows.** Anthropic's tutorials put it
  plainly: effort sets how hard the model works, not how much it knows, and
  changing effort changes cost while keeping the model's core capabilities
  intact, unlike switching to a different model
  ([Anthropic Academy, Claude Code](https://academy.claude.com/tutorials/choosing-the-right-effort-level-in-claude-code);
  [Anthropic Academy, Chat](https://academy.claude.com/tutorials/how-to-select-the-right-effort-setting-for-claude-cowork-and-chat)).
- **It is not a fixed token budget.** Anthropic's API documentation calls effort
  a **behavioral signal, not a strict token budget**. The hard ceiling on how
  much a model may generate is a separate setting, the maximum output tokens
  ([Anthropic, Effort](https://platform.claude.com/docs/en/build-with-claude/effort)).
- **It is not only about thinking.** In Claude, effort affects **all** output
  tokens: the visible text, tool calls and thinking. That is why it still works
  when thinking is turned off. Lower effort tends to combine operations into
  fewer tool calls with terse confirmations; higher effort may make more tool
  calls, explain its plan and give fuller summaries ([Anthropic, Effort](https://platform.claude.com/docs/en/build-with-claude/effort)).
- **The same name is not the same amount everywhere.** Anthropic notes that a
  level such as high does not represent the same underlying value on different
  models, and each model's default is tuned separately
  ([Claude Code, model configuration](https://code.claude.com/docs/en/model-config)).

In the Claude app, effort and the **thinking** toggle are separate settings:
effort controls how thorough Claude is in every response, while the thinking
toggle controls whether Claude reasons in an expandable section before replying.
On the newest models thinking is always on and cannot be switched off
([Claude Help Center](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)).

### Under the hood: thinking tokens and test-time compute

An LLM writes **one token at a time**, and each token requires a full pass
through the network. A reasoning model can spend tokens on **thinking**, a
private scratchpad where it breaks the problem down, tries approaches and checks
intermediate results, before it writes the visible answer. Every thinking token
costs the same computation as an answer token. Raising effort lets the model
spend more of this **test-time compute**, meaning computation used while
answering rather than during training.

Research explains why this works and where it stops working:

- **Writing out steps helps.** Chain-of-thought prompting showed in 2022 that
  asking a large model to write intermediate reasoning steps improves its
  accuracy on multi-step problems {cite}`wei2022chain`. Reasoning models
  generate such steps on their own.
- **Spending compute wisely can beat a bigger model.** Snell and colleagues found
  that adapting test-time compute to the difficulty of each prompt was more than
  four times as efficient as a simple best-of-N approach, and that on problems a
  smaller model could already sometimes solve, extra test-time compute let it
  outperform a model 14 times larger. On the hardest questions, however, extra
  test-time compute helped very little {cite}`snell2025scaling`.
- **Models can learn to think longer, and only when needed.** During the
  reinforcement-learning training of DeepSeek-R1-Zero, responses grew longer as
  the model learned to use more thinking time, and its average score on the AIME
  2024 math competition rose from 15.6 percent to 77.9 percent. The final
  DeepSeek-R1 used fewer than 7,000 thinking tokens on simpler competition
  problems, more than 18,000 on the hardest ones, and under 100 tokens for a
  question like 1 + 1 {cite}`guo2025deepseek`.
- **More thinking helps, then flattens.** The s1 study controlled thinking length
  directly, cutting the model off early or appending the word *Wait* to make it
  keep going. Longer thinking raised accuracy on AIME 2024 from 50 percent to 57
  percent, but the gains eventually flattened out and were capped by the context
  window {cite}`muennighoff2025s1`.

An effort setting is a product-level knob for this same trade-off: it lets you
decide how much test-time compute a request deserves.

Three practical details follow from this design:

- **Adaptive thinking.** Current Claude models decide for themselves whether and
  how much to think. Effort shifts that decision: at low effort Claude minimizes
  thinking and skips it for simple tasks, at medium it thinks moderately, at high
  it thinks on most requests that benefit, at xhigh it thinks more readily and
  more deeply, and at max it thinks the most, with no constraint on length. **No
  level guarantees** that a thinking step will happen
  ([Anthropic, Steering thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)). OpenAI's reasoning models also adapt within a
  level ([OpenAI, reasoning guide](https://developers.openai.com/api/docs/guides/reasoning)),
  and Gemini models think dynamically by default
  ([Google, Gemini thinking](https://ai.google.dev/gemini-api/docs/thinking)).
- **You usually cannot read the raw thinking.** Claude never returns its raw
  chain of thought; the app or API shows a summary or nothing at all
  ([Anthropic, Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)). OpenAI does not expose raw reasoning tokens but
  offers an optional summary, and Gemini can return thought summaries when you
  turn them on.
- **You pay for the full thinking anyway.** Anthropic, OpenAI and Google all bill
  thinking or reasoning tokens **as output tokens**, based on the full reasoning
  generated, not the shorter summary you see. Thinking also counts against the
  maximum output setting and occupies space in the context window
  ([Anthropic, Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking);
  [OpenAI](https://developers.openai.com/api/docs/guides/reasoning);
  [Google](https://ai.google.dev/gemini-api/docs/thinking)).

### Why higher effort uses your limits faster

Paid Claude plans have a **session limit that resets every five hours** plus
**weekly limits**, and every Claude surface (web, desktop, mobile and Claude
Code) draws on the same allowance. How fast you use it depends on the length and
complexity of the conversation, the features used, the model, and **the effort
level** ([Claude Help Center, usage limits](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work)).
Anthropic's Academy explains why: in chat, the limit is measured in **tokens**,
and everything Claude does, including thinking and tool use, draws from it.
Higher effort means more thinking, more tool calls and more self-checking, so
each task consumes more tokens
([Anthropic Academy](https://academy.claude.com/tutorials/how-to-select-the-right-effort-setting-for-claude-cowork-and-chat)).

A worked example makes the arithmetic concrete. **The token counts below are
invented for illustration**; real counts vary by model, prompt and level.

```{list-table} One question at two effort levels (hypothetical numbers)
:header-rows: 1
:widths: 34 22 22 22

* - Item
  - Low effort
  - High effort
  - Ratio
* - Thinking tokens
  - 0
  - 4,000
  -
* - Visible answer tokens
  - 400
  - 800
  -
* - **Total output tokens**
  - **400**
  - **4,800**
  - **12 times**
* - API cost at 20 dollars per million output tokens
  - 0.008 dollars
  - 0.096 dollars
  - 12 times
* - Generation time at an assumed 100 tokens per second
  - about 4 seconds
  - about 48 seconds
  - 12 times
```

The calculation is simple multiplication: 4,800 tokens times 20 dollars divided
by 1,000,000 tokens is 0.096 dollars, and 4,800 tokens divided by 100 tokens per
second is 48 seconds. Twenty dollars per million output tokens is the listed
API price of Claude Opus 5.5 in October 2026
([Claude models overview](https://platform.claude.com/docs/en/models/overview)),
while 100 tokens per second is a round number chosen for the example, not a
measured speed. Tool calls add still more, because each tool result is fed back
into the model as input on the next step. On a subscription you do not see a
bill, but the same tokens are counted against your session and weekly limits,
which is exactly what the app sentence means by **uses your limits faster**.

### The settings each major provider offers

```{list-table} Effort and thinking controls as of October 2026
:header-rows: 1
:widths: 16 34 50

* - Provider
  - Setting and values
  - Defaults and notes
* - **Anthropic** (Claude API)
  - `effort`: low, medium, high, xhigh, max
  - Most models default to high; Claude Opus 5.5 and Claude Haiku 5.5 default
    to medium. Not every model supports every level ([Anthropic, Effort](https://platform.claude.com/docs/en/build-with-claude/effort)).
* - **Anthropic** (Claude app and Claude Code)
  - Low, Medium, High, Extra high (xhigh), Max
  - Each model marks a recommended default. In Claude Code the default is medium
    on Opus 5.5, Sonnet 5.5 and Haiku 5.5, and typing *ultrathink* in a prompt
    asks for deeper reasoning on that one turn without changing the setting
    ([model configuration](https://code.claude.com/docs/en/model-config)).
* - **OpenAI** (API)
  - `reasoning.effort`: none, minimal, low, medium, high, xhigh, max, depending
    on the model
  - Medium is the default for most current models. A separate `reasoning.mode`
    (standard or pro) does more work at the same effort
    ([OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning)).
* - **OpenAI** (ChatGPT)
  - Thinking options: Instant, Medium, High, Extra High, Pro
  - Availability depends on your plan; asking ChatGPT to think harder in the
    prompt does not switch the level
    ([OpenAI Help Center](https://help.openai.com/en/articles/11909943-gpt-55-in-chatgpt)).
* - **Google** (Gemini API, Gemini 3 and later)
  - `thinking_level`: minimal, low, medium, high, depending on the model
  - Gemini 4 Argon and Gemini 3.8 Flash default to medium. The older numeric
    `thinking_budget` is a legacy setting on Gemini 3 and deprecated on Gemini 4,
    where the Gemini API maps it to the nearest level with a warning and Google
    Cloud rejects it
    ([Gemini thinking](https://ai.google.dev/gemini-api/docs/generate-content/thinking);
    [Google Cloud, thinking](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/thinking)).
```

Two older designs explain where numeric token figures come from. Claude's
earlier **extended thinking** mode asked developers for a `budget_tokens` value,
with a minimum of 1,024 and a suggestion of 16,000 or more for complex tasks;
it is deprecated on Claude 4.6 models and rejected on Claude 4.7 and later, in
favor of adaptive thinking controlled by effort ([Anthropic, Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)).
Gemini 2.5 models still take a numeric `thinking_budget`, for example 128 to
32,768 tokens on Gemini 2.5 Pro
([Google Cloud, thinking](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/thinking)).

### More effort is not always better

Extra thinking helps most on problems that genuinely need several steps, and the
gains shrink as the budget grows. Providers say so directly:

- In its guidance for Claude Opus 4.7, Anthropic notes that max can add
  significant cost for relatively small quality
  gains on most workloads and can lead to **overthinking** on some tasks
  ([Anthropic, Effort](https://platform.claude.com/docs/en/build-with-claude/effort)).
- Anthropic's tutorials list three symptoms of too much effort: responses that
  get wordier without getting better, work that expands beyond what you asked,
  and a model that checks a correct answer and **talks itself out of it**
  ([Anthropic Academy](https://academy.claude.com/tutorials/how-to-select-the-right-effort-setting-for-claude-cowork-and-chat)).
- OpenAI advises treating reasoning effort as a tuning knob rather than the main
  way to recover quality, and using xhigh only when evaluations show a clear
  benefit ([OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning)).

Research agrees. Chen and colleagues found that long reasoning models of the o1
type used about 20 times as many tokens as conventional models to answer the
question what is 2 plus 3, and that across math test sets their first round of
solutions was already correct in more than 80 percent of cases
{cite}`chen2025do`. Gema and colleagues
went further and built tasks on which longer reasoning made accuracy **worse**
across Claude, OpenAI and open models, an effect they call inverse scaling in
test-time compute {cite}`gema2025inverse`.

### A note on the token ranges you may see online

Blog posts and summaries often attach token ranges to each level, for example
roughly 0 to 2,000 thinking tokens for low, 2,000 to 4,000 for medium, 5,000 to
16,000 for high, and 10,000 to 32,000 or more for extra high and max. **No
primary source from Anthropic, OpenAI or Google publishes fixed ranges like
these.** Some widely shared secondary posts, such as several MindStudio
articles on Claude effort levels, do list per-level ranges, but they disagree
with one another (one gives medium as 2,000 to 5,000 tokens, another as 4,000 to
8,000) and cite no primary source
([MindStudio, Opus 4.8 effort levels](https://www.mindstudio.ai/blog/claude-opus-4-8-effort-levels-explained);
[MindStudio, Fable 5 effort levels](https://www.mindstudio.ai/blog/claude-fable-5-effort-levels-explained)).
Numbers of this size most likely come from older numeric
thinking budgets, such as Claude's 1,024 minimum and 16,000 suggestion or Gemini
2.5's 32,768 cap, or from third-party gateways such as OpenRouter, which turn an
effort word into a fixed fraction of the maximum output length (for example 80
percent for high and 50 percent for medium)
([OpenRouter, reasoning tokens](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens)).
Anthropic's own guidance points the other way: it describes xhigh as suited to
long-running agentic and coding tasks with token budgets in the millions
([Anthropic, Effort](https://platform.claude.com/docs/en/build-with-claude/effort)), far beyond any of the ranges above.

The official documentation instead says that effort is a behavioral signal and
not a token budget, that the same level means different amounts of work on
different models, and that the model may skip thinking entirely on an easy
question even at a high setting. The only official numbers come from the older
designs described above (Claude's `budget_tokens`, Gemini 2.5's
`thinking_budget`) and from general guidance, such as OpenAI's note that a
request can use anywhere from a few hundred to tens of thousands of reasoning
tokens and its advice to reserve at least 25,000 tokens for reasoning and output
when starting out ([OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning)).
Treat any per-level token range as a rough anecdote about one model at one
time, not a specification. The one claim in those summaries that the primary
sources do confirm is the most useful one: **effort changes how hard the model
works, not what it knows.**

### Choosing an effort level

```{list-table}
:header-rows: 1
:widths: 18 48 34

* - Level
  - Good fit
  - Watch out for
* - **Low**
  - Quick lookups, rewording, formatting, classification, short factual
    answers, high-volume or background subtasks
  - Shallow answers on anything with several steps
* - **Medium**
  - Everyday writing, summarizing, explaining, routine code; the default on
    several current models
  - Occasional missed edge cases on hard problems
* - **High**
  - Multi-step analysis, debugging, careful code changes, research that needs
    checking
  - Slower replies and faster use of limits
* - **Extra high / Max**
  - The hardest problems and long agentic tasks where a wrong answer is costly
    and you can wait
  - Diminishing returns, overthinking, and the fastest use of limits
```

A few habits help:

1. **Start at the default** the app recommends for the model you picked; it is
   tuned for that model.
2. **Raise effort when you see reasoning errors**, such as a wrong step in math,
   a bug the model missed or an unchecked claim, not just because a task feels
   important.
3. **Lower effort for simple or repetitive work** to save time and limits.
4. **Ask for length directly.** On some models effort controls the amount of
   thinking more than the length of the visible answer, so if you want a short
   or long reply, say so in the prompt ([Anthropic, Effort](https://platform.claude.com/docs/en/build-with-claude/effort)).
5. **Switch models when effort is not enough.** Effort cannot add knowledge or
   ability the model does not have; a more capable model can. Some systems
   automate this by routing each request to a cheaper or stronger model. The
   ProofLayer policy-screening system, for example, includes a cost-aware layer
   that routes between models, and its paper is careful to call the resulting
   saving a projection from token prices rather than measured spending
   {cite}`trivedi2026prooflayer`.

## Knowledge check

Test your understanding. Each answer is hidden; click to reveal it.

```{admonition} Q1. Is every machine learning system an example of AI? Is every AI system an example of machine learning?
:class: dropdown
Every machine learning system is AI, because machine learning is one way of
building AI. The reverse is false: a chess engine that searches positions or a
hand-written rule-based expert system is AI without learning anything from data.
```

```{admonition} Q2. Why is NLP drawn as a band that cuts across the nested boxes instead of as one more box?
:class: dropdown
NLP is defined by the problem it addresses, human language, not by a technique.
Language tasks have been solved with hand-written rules, classic machine learning,
deep learning and LLMs, so NLP overlaps every layer of the map.
```

```{admonition} Q3. A model was trained with $3 \times 10^{25}$ operations. Under which of the rules in Part 1 does it count as frontier or high-impact?
:class: dropdown
It exceeds the EU AI Act presumption of more than $10^{25}$ operations, so it is
presumed to have high-impact capabilities and systemic risk in the EU. It does not
reach the $10^{26}$ threshold used by California SB 53 and the New York RAISE Act,
so it is not a frontier model under those laws. The revoked US Executive Order
14110 threshold no longer applies at all.
```

```{admonition} Q4. Is agentic AI a new kind of model? What makes a system agentic?
:class: dropdown
No. Agentic AI is a way of using models: a model placed in a loop where it plans,
calls tools such as search, code or apps, looks at the results and decides the
next step until a goal is met. NIST excludes ordinary chatbots and
retrieval-augmented generation systems that are not set up to act on their own.
```

```{admonition} Q5. A company releases a model's weights under the Apache 2.0 license but not its training code or data. Is it open source?
:class: dropdown
It is open weights with a permissive license. Under the OSI Open Source AI
Definition 1.0 it is not fully open source, because that definition also requires
detailed information about the training data and the complete training and
inference code.
```

```{admonition} Q6. You switch from medium to high effort on the same model. Does the model know more? What does change?
:class: dropdown
It does not know more: effort changes how hard the model works, not what it
knows. At higher effort it tends to think longer, make more tool calls and check
its work more, so it uses more tokens, takes longer and draws down usage limits
faster. To get knowledge or ability the model lacks, you need a different model
or a tool such as web search.
```

```{admonition} Q7. In the worked example in Part 3, the high-effort reply used 4,800 output tokens. What would 10,000 such replies cost at 20 dollars per million output tokens?
:class: dropdown
$4{,}800 \times 10{,}000 = 48{,}000{,}000$ tokens. At 20 dollars per million tokens
that is $48 \times 20 = 960$ dollars, compared with 4,000,000 tokens and 80 dollars at the
low-effort size of 400 tokens per reply.
```

```{admonition} Q8. A friend says high effort always uses between 5,000 and 16,000 thinking tokens. How would you respond?
:class: dropdown
No primary source states fixed ranges like that. Anthropic calls effort a
behavioral signal rather than a token budget, the same level means different
amounts of work on different models, and with adaptive thinking a model may skip
thinking entirely on an easy question even at high effort. Such numbers are at
best rough anecdotes from one model and one prompt.
```

```{admonition} Q9. When can raising the effort level make an answer worse?
:class: dropdown
On simple tasks, extra thinking can make answers wordier without making them
better, expand the scope beyond what was asked, or lead the model to second-guess
a correct answer. Research has documented overthinking on easy problems and
tasks where longer reasoning lowers accuracy.
```

```{admonition} Q10. Claude Opus 5.5 scores 66.4 percent on Terminal-Bench 4.0 in one table and 60 percent in another. Which number is wrong?
:class: dropdown
Probably neither. The 66.4 percent comes from Anthropic's own run at the xhigh
effort setting, and the 60 percent from Artificial Analysis running the test
independently with its own setup. Benchmark scores depend on who runs them, the
effort or thinking setting, the test harness and timeouts, so always note the
source and conditions before comparing models.
```

```{admonition} Q11. GPT-6.1 Sol and Gemini 4 Argon both cost 2 dollars per million input tokens and 10 dollars per million output tokens, yet one cost about 0.72 dollars per task and the other about 1.99. How can that be?
:class: dropdown
The price per token was the same, but the number of tokens each model used per
task was not. Argon produced about 62,000 output tokens per task in Artificial
Analysis's testing, much of it thinking, so each task cost more. Cost per task
depends on price per token times tokens used, and the tokens used depend on the
model and the effort setting.
```

## Key takeaways

- **AI contains ML, which contains deep learning**; generative AI, foundation
  models, LLMs and frontier models are progressively narrower groups inside deep
  learning. **NLP** is a problem area that cuts across all of them.
- **Frontier** is a moving, capability-based label. Laws use training-compute
  thresholds instead: 10<sup>26</sup> operations for frontier models in
  California and New York, and 10<sup>25</sup> for the EU's presumption of
  systemic risk.
- **Agentic AI** is a way of using models in a loop with tools. **AGI** and
  **superintelligence** are hypothetical capability levels with competing
  definitions and no agreed test.
- Separate the **company**, the **model** and the **app**. Most flagship models
  are closed; open-weight models vary widely in license, and open weights are
  not the same as open source.
- The October 2026 flagships, **Claude Opus 5.5**, **GPT-6 Astra**,
  **GPT-6.1 Sol** and **Gemini 4 Argon**, trade leads depending on the test, the
  tester, the benchmark version and the effort setting; compare cost per task,
  not just price per token, and evaluate on your own tasks.
- An **effort level** sets how much work a model does on a request, mostly
  thinking, tool calls and self-checking. It is a **behavioral signal, not a
  token budget**, and it does not change what the model knows.
- Thinking tokens are billed and counted like output even when hidden, so
  higher effort means **longer waits, higher cost and faster use of limits**,
  with diminishing returns at the top. Start at the default and raise effort
  only when you see reasoning errors.

```{admonition} About this chapter
:class: seealso
Written by Devharsh Trivedi, Ph.D., CISSP, Department of Mathematics,
Engineering and Computer Science, LaGuardia Community College, The City
University of New York (CUNY). ORCID: <https://orcid.org/0000-0001-6374-7249>.
Prepared
with research and drafting assistance from Claude (Anthropic). Product details
were checked against vendor documentation and announcements available on
October 16, 2026, and research claims against the cited papers. Because this
field changes quickly, confirm current details in each provider's documentation.
```
