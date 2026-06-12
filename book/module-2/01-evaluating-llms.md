---
title: "Evaluating LLMs"
---

# Chapter 1: Evaluating LLMs

## Why it matters

Before you can use a model responsibly, you have to know how good it is, and that
turns out to be surprisingly hard. An LLM is versatile, its outputs are
subjective, and there is no single universal test. This chapter explains why
evaluation matters more than ever, surveys the spectrum of evaluation approaches
from objective metrics to human judgment, and shows how Amazon Bedrock supports
both automated and human evaluation.

## Why evaluating LLMs matters

Five forces make evaluation essential:

1. **An increasing number of core abilities.** Modern LLMs do question
   answering, content generation, logical and arithmetic reasoning, common-sense
   reasoning, code generation, and multi-hop reasoning. Each ability needs its
   own assessment.
2. **Knowledge of diverse topics.** LLMs are trained across finance, education,
   software, medicine, and more, but their knowledge can be shallow. Does the
   model's behavior align with *your* company's data, policies, and brand?
3. **Increasing visibility and influence.** As LLMs mediate how people access
   information, safety, security, and ethical implications grow, making
   responsible AI central.
4. **Going beyond content generation.** Agentic applications let LLMs execute
   actions, write and run code, query databases, call APIs, even control systems.
   Actions carry real risk and must be evaluated against security policies.
5. **LLMs acting as experts for other systems.** Models increasingly annotate
   data and even evaluate other LLMs, so their reliability compounds.

## Why evaluation is hard

Evaluating language is subjective, and an LLM is so versatile that comprehensive
evaluation is difficult. There is no universal framework, high-quality evaluation
data is scarce, and running large models for evaluation is computationally
expensive. It helps to know where LLMs typically fail: complex arithmetic and
analytical reasoning, serving as a reliable knowledge source on niche topics,
understanding and mitigating bias, avoiding **hallucinations** (false, misleading,
or fabricated content), analyzing structured data such as databases and
spreadsheets, and complying with every rule and protocol.

## The spectrum of evaluation approaches

Evaluation runs from objective to subjective.

### Metric-based evaluation

Objective metrics score performance numerically. They are easy to compute but do
not extend well to complex traits such as reasoning. Common metrics:

```{list-table}
:header-rows: 1
:widths: 22 78

* - Metric
  - What it measures
* - **Accuracy**
  - Proportion of correct predictions.
* - **Perplexity**
  - How well the model predicts the given text (lower is better).
* - **BLEU**
  - Precision-based comparison of generated text against references.
* - **ROUGE**
  - Recall-oriented overlap of generated text with references.
```

### Evaluation datasets (benchmarks)

High-quality benchmark datasets test complex traits using objective metrics.
Widely used examples:

- **MMLU** (Massive Multitask Language Understanding): general knowledge across 57
  subjects from STEM to social science.
- **HellaSwag**: natural-language inference requiring attention to intricate
  detail.
- **GSM8K**: 8,500 grade-school math problems needing multi-step arithmetic.
- **AGIEval**: standardized human exams (GRE, GMAT, SAT, LSAT, civil service).
- **Responsible AI (RAI)** frameworks: safety of chat-optimized models in
  conversation.

### Feedback-based and human evaluation

For subjective qualities, you use **A/B testing**, **LLM evaluators** (one model
judging another), and **manual human evaluation**. The practical rule: never ship
an AI-generated solution you have not evaluated. Focus on the metrics and
benchmarks that matter for *your* use case, expect to collect your own annotated
benchmark dataset, and engage human evaluators when automated metrics are not
enough.

## Evaluation on Amazon Bedrock

Amazon Bedrock provides built-in model evaluation in two flavors.

**Programmatic (automatic) evaluation** is a four-step flow: (1) choose a
foundation model, (2) select the task type (text generation, classification, Q&A,
and so on), (3) choose metrics (accuracy, robustness, toxicity), and (4) select a
built-in dataset or upload your own prompt dataset.

**Manual (human) evaluation** lets human reviewers compare responses from up to
two models. You can **bring your own team** or use an **AWS-managed work team**.
The workflow: choose one or two models, choose the task type, use recommended
metrics or define your own, upload a dataset, add people to the work team, run
inference, collect human evaluations, and view results. The evaluation report
tracks your team's ratings, visualizes score distributions, and explains metrics
simply.

```{admonition} Worked example: choosing what to measure
:class: note
Suppose you are deploying a customer-support assistant. Pure accuracy is the wrong
headline metric. You would likely combine an automated **toxicity** and
**robustness** check on Bedrock with a **human** evaluation of helpfulness and
tone on a few hundred real support prompts you annotate yourself, because "good
support" is exactly the kind of subjective quality metrics alone cannot capture.
```

## In the news

Evaluation has become a field of its own. Public leaderboards and human-preference
arenas now rank models head to head, and the conversation has shifted toward
evaluating **agents** and **reasoning**, not just single answers. A recurring
theme is **benchmark contamination** (models trained on test data) and
**saturation** (models maxing out older benchmarks), which keeps pushing the
community toward harder, fresher, task-specific evaluations, exactly the
"collect your own benchmark" advice above.

## Key takeaways

- Evaluation matters because LLMs have many abilities, broad but shallow
  knowledge, growing influence, agentic reach, and roles judging other systems.
- It is hard because language is subjective and there is no universal test.
- Approaches span **metrics** (accuracy, perplexity, BLEU, ROUGE), **benchmarks**
  (MMLU, HellaSwag, GSM8K, AGIEval), and **human/feedback** evaluation.
- **Amazon Bedrock** supports both **programmatic** and **human** evaluation;
  never deploy an unevaluated solution.

Next we step back from measurement to the principles that make AI responsible.
