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

## Case studies: testing AI tools before people rely on them

Two peer-reviewed studies published in 2026 by the author of this book, both in
the *Journal of Cybersecurity, Digital Forensics and Jurisprudence*, apply the
ideas above to settings where a wrong answer has legal or public consequences.
The first asks whether a chatbot simply tells an expert what the expert already
believes; the second asks whether a policy-screening score measures what it
appears to measure.

### Does the model just agree with the expert? LLM sycophancy in forensic work

**Sycophancy** is a model's tendency to shape its answer to match what the user
says they believe. In forensic practice the prompt usually carries the
examiner's working hypothesis, so a sycophantic model could hand that hypothesis
back in the voice of an independent instrument and create the appearance of
corroboration where none exists. The concern is practical: in *Matter of Weber*
(2024), a surrogate's court put its own Microsoft Copilot query to three of its
computers and got three different figures, and the expert whose calculation
prompted the exercise could not recall what prompt he had used
{cite}`trivedi2026tool`.

The study tested the hypothesis directly {cite}`trivedi2026tool`:

- **Design.** Six dated model snapshots answered five forensic interpretation
  items under three framings that differed only in what the examiner asserted.
  Each combination was sampled 30 times, for 2,700 trials in total.
- **Scoring.** A model judge classified the replies. Before trusting it, the
  judge was validated against hand coding of 77 replies, with an agreement
  statistic (Gwet's AC1) of 0.855.
- **Main result.** The hypothesis was not supported. Across the 2,160 trials
  analyzed, models asserted the incorrect proposition in 36.1 percent of trials
  when asked neutrally and in 19.6 percent when an examiner asserted it. In 13
  of 24 model and item combinations the answers moved away from the examiner,
  in 10 they did not move, and the single combination that moved toward the
  examiner already had a baseline error rate of 93.3 percent.
- **The sharper finding.** On an item whose conclusion rested on an
  unsupported premise, one of the six models contested the premise in 80
  percent of trials and the other five never did, in any of 150 trials. The
  models checked conclusions without auditing the reasons behind them.
- **Law.** Comparing reliability rules for expert evidence across six legal
  systems, the study found that the jurisdictions with the strictest
  reliability screening had no rule on experts' use of generative AI, while
  Australia, which does not use such a screen, had the only binding rules. It
  also argued that US Federal Rule of Evidence 702(d) is a sharper test than the
  error-rate factor from *Daubert*, because a prompt-dependent error rate is not
  a property of a method.

### Does the score measure what you think? ProofLayer and policy screening

**ProofLayer** is a two-stage system for screening government cybersecurity
policies against a control catalog: a keyword stage maps policy text to 22
controls crosswalked to NIST SP 800-53 Revision 5, and a language-model stage is
meant to resolve the cases keyword matching cannot, with an orchestration layer
that routes requests between models to save cost {cite}`trivedi2026prooflayer`.
The paper evaluates the first stage on ten Maryland state and local government
policy documents and is careful to separate what was measured from what was only
described:

- **Measurement choices move the result.** Reading every document in full gave
  a mean control coverage of 62.8 percent (standard deviation 24.1). An earlier
  analysis that stopped reading at page 15 reported 49.1 percent. Seven of the
  ten documents were longer than 15 pages, and the two longest gained 36 and 41
  points when read in full.
- **Look for confounds.** Document length alone explained 48 percent of the
  variance in coverage, so longer documents scored higher partly because they
  contained more words to match.
- **Inspect the matches.** Of 138 covered document and control pairs, 18.1
  percent had a negation word near the match and 44.2 percent rested on a single
  keyword. A footnote URL was scored as transport encryption, and a real
  incident-reporting requirement was scored as absent because the keyword list
  lacked the word notifying.
- **Do not grade with the model you are testing.** The language-model stage is
  described but not evaluated, because judging it needs expert-annotated ground
  truth that does not yet exist, and the paper declines to use model-generated
  labels as a substitute. Its cost saving is likewise a projection from token
  prices, not measured spending.
- **Name what the number means.** The paper reports policy-vocabulary coverage,
  not compliance, and releases all 220 document and control pairs so others can
  check the work.

```{admonition} Lessons for your own evaluations
:class: tip
- Treat the prompt and the input pipeline as part of the experiment: vary the
  framing, and report how much of each input the system actually read.
- Sample repeatedly, because the same prompt can give different answers.
- Validate any LLM judge against human labels before trusting its scores, and
  never use the system under test to create its own ground truth.
- Check the reasons as well as the conclusion, and look for simple confounds
  such as document length.
- Report negative and partial results honestly; a hypothesis that is not
  supported is still a finding.
```

## Hallucinations, grounding, and knowing when not to answer

A **hallucination** is fluent output that is not supported by the facts. When the model was given source material, as in summarization or retrieval-augmented generation, researchers distinguish two kinds {cite}`ji2023survey`. An **intrinsic** hallucination contradicts the source: the document says the fee is 2 percent and the answer says 3. An **extrinsic** hallucination adds claims the source cannot support: the answer cites a fee waiver the document never mentions. Extrinsic content is sometimes true, but it is unverifiable from the source, so a grounded application should treat it as an error.

**Faithfulness**, also called **groundedness**, measures how much of an answer is supported by its source. Amazon Bedrock Guardrails can check it at run time: its contextual grounding check takes the grounding source, the user's query, and the model's response, scores the response for grounding and for relevance, and blocks it when either score falls below a threshold you set between 0 and 0.99 ([AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html)).

The safest answer is sometimes no answer. **Abstention** means the system declines, says it does not know, or hands off to a person when it lacks reliable information. Deciding when to abstain depends on the kind of uncertainty {cite}`kendall2017uncertainties`. **Aleatoric uncertainty** comes from noise or ambiguity in the data itself, such as a question with two reasonable readings; more data does not remove it, but a clarifying question can. **Epistemic uncertainty** comes from gaps in what the model knows, such as an event after its training cutoff; better data, retrieval, or a tool call can remove it. Evaluate abstention like any other behavior: a system that never abstains will hallucinate on hard questions, and one that abstains too often is useless.

```{admonition} Security view
:class: warning
Hallucinations can be weaponized. Code assistants sometimes suggest packages that do not exist. A USENIX Security 2025 study generated 576,000 code samples with 16 LLMs and found that 19.7 percent of the packages they recommended were hallucinated, with 205,474 unique made-up names {cite}`spracklen2025package`. An attacker who registers one of those names on a public registry, a technique now called **slopsquatting**, gets malware installed by every developer who trusts the suggestion. Check that a suggested package exists, is the one you expect, and comes from an approved source before installing it. The companion textbook covers this with the other supply chain attacks ([Supply Chain Attacks](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#supply-chain-attacks)).
```

## Measuring a classifier when one class is rare

Many evaluation tasks are classification: is this message toxic, is this transaction fraud, does this answer cite a real source. When one class is rare, **accuracy** misleads. Picture 100,000 transactions of which 517 are fraud. A model that calls every transaction legitimate is 99.48 percent accurate and catches no fraud at all. Use the **confusion matrix** instead, which counts true positives, false positives, false negatives, and true negatives, and the measures built on it:

- **Precision**: of the items the model flagged, the share that were truly positive.
- **Recall**: of the truly positive items, the share the model flagged.
- **F1 score**: the harmonic mean of precision and recall, high only when both are.
- **PR-AUC**: the area under the precision-recall curve across all thresholds. A random model scores about the share of positives, 0.005 here, so on rare classes it separates good models from weak ones more clearly than accuracy or ROC-AUC.

Then choose the decision threshold from what each mistake costs. If a missed fraud costs 100 times what a false alarm costs, the best threshold on calibrated probabilities is the false-alarm cost divided by the sum of both costs, about 0.01, far below the default of 0.5. The companion textbook works through this example with code ([Evaluating Models Under Class Imbalance](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#evaluating-models-under-class-imbalance-beyond-accuracy)).

## More metrics you will meet

A few more measures appear across model cards, papers, and security reports.

- **ROC curve and ROC-AUC.** The receiver operating characteristic curve plots the true-positive rate against the false-positive rate as the decision threshold moves. The area under it runs from 0.5, chance, to 1.0, perfect ranking. On rare classes it can look strong while precision is poor, which is why the PR curve above is the better guide there.
- **pass@k.** For code generation, the probability that at least one of k generated samples passes the unit tests. It was introduced with the HumanEval benchmark, along with an unbiased way to estimate it from n samples of which c pass: one minus the number of ways to choose k samples from the n minus c failing ones, divided by the number of ways to choose k from n {cite}`chen2021evaluating`. A high pass@10 with a low pass@1 means a person or a test suite must pick the good answer out of many.
- **Attack success rate (ASR).** In safety and security testing, the share of adversarial attempts that achieve their goal, such as jailbreak prompts that get a disallowed answer. Report it with the attack set, the number of tries, and the model settings, because the same model can score very differently against a different set.
- **Goodhart's law.** Often stated as: when a measure becomes a target, it ceases to be a good measure. A team that tunes a model to a benchmark, or a judge model to one rubric, can raise the score without improving the behavior the score was meant to reflect. Keep some evaluations out of the tuning loop, and rotate in new ones.

## Drift: when yesterday's evaluation stops being true

An evaluation describes a model on the data you tested. Production data moves. **Data drift** is a change in the inputs: users ask about a new product, write in another language, or paste longer documents. **Concept drift** is a change in the right answer for the same input: a policy, a price, or a law changes, so a response that was correct last month is wrong today. **Label drift**, also called prior shift, is a change in the mix of outcomes, such as a fraud rate that doubles, which changes precision even when neither the inputs nor the model change. Evaluations also go stale when **benchmark contamination** leaks test questions into training data, so a score measures memory rather than skill.

Treat evaluation as continuous. Keep a fixed **golden test set** of representative and adversarial cases and re-run it after every change to catch regressions, sample live traffic for fresh review, watch input statistics and user feedback for shifts, and re-run the full evaluation whenever the model, the prompt, the retrieved data, or the world it describes changes.

## Evaluation on Amazon Bedrock

Amazon Bedrock Evaluations offers four kinds of evaluation job. The first two are the classic ones.

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

**LLM-as-a-judge evaluation** uses a judge model that you pick from those on
Bedrock to score another model's answers against your prompt dataset. Built-in
metrics include correctness, completeness, faithfulness (hallucination
detection), helpfulness, professional style and tone, and responsible AI metrics
such as harmfulness and answer refusal, and you can define custom metrics with
your own rubric. **RAG evaluation** applies the same judge to a retrieval system,
either Amazon Bedrock Knowledge Bases or your own pipeline: retrieve-only jobs
score context relevance and coverage, and retrieve-and-generate jobs add
correctness, faithfulness, and citation precision and coverage. Both became
generally available on March 20, 2025 {cite}`awsllmjudge2025`. With **bring your
own inference responses**, you supply the answers in the dataset, so a model or
RAG system hosted outside Bedrock can be scored the same way. A judge is a model
with its own biases. Zheng and colleagues found that judges favor the answer
shown first (position bias), longer answers (verbosity bias), and answers
written by themselves (self-enhancement bias), although a strong judge still
agreed with human raters over 80 percent of the time {cite}`zheng2023judging`.
Swap answer order between runs, use a judge from a different model family than
the models under test, and validate its scores against a sample of human ratings
before you rely on them, as the case study above did.

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
- Two 2026 case studies show evaluation in practice: test whether a model just
  agrees with the user (**sycophancy**), validate any LLM judge against human
  labels, and check that a score measures what you think before relying on it.
- Separate **intrinsic** from **extrinsic** hallucinations, measure **faithfulness**,
  and let the system **abstain** when it lacks reliable information.
- When one class is rare, report **precision, recall, F1, and PR-AUC**, not
  accuracy, and set thresholds from the cost of each error. Re-evaluate as
  **data drift** and **concept drift** change what correct looks like.

Next we step back from measurement to the principles that make AI responsible.
