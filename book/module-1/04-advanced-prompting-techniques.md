---
title: "Advanced Prompting Techniques"
---

# Chapter 4: Advanced Prompting Techniques

## Why it matters

Standard prompt engineering, clear instructions and a few examples, handles most
everyday tasks. But difficult questions require an LLM to follow complex
instructions and reason over several steps, and there standard techniques fall
short. Few-shot examples eat up the limited context window; a single chain of
reasoning can just as easily be wrong as right; and models can be nudged into
unsafe outputs. This chapter introduces three techniques that push reasoning
further: **chain-of-thought**, **self-consistency**, and **tree-of-thought**.
Each builds on the last, and together they form a ladder from a single guess to a
deliberate search over possibilities.

## A quick review

Before adding new tools, recall the good practices from Chapter 3: write clear,
specific, positive instructions; highlight what matters; separate instruction,
content, and output directions; use examples (in-context learning); and iterate.
The advanced techniques here do not replace those habits; they sit on top of
them.

## Chain-of-thought prompting

**Chain-of-thought (CoT)** prompting breaks a complex task into intermediate
reasoning steps, encouraging the model to *explain its reasoning* rather than
jump to an answer {cite}`wei2022chain`. Decomposing the problem into a series of
steps tends to produce more accurate final answers, and it is the foundation the
other two techniques build on.

There are two common ways to trigger it.

### Zero-shot CoT

Simply append an instruction like **"Let's think step by step"** to the prompt.
This alone elicits a sequential reasoning chain {cite}`kojima2022large`.

```{admonition} Worked example: the juggler problem
:class: note
**Standard (zero-shot):**

    Q: A juggler can juggle 16 balls. Half of the balls are golf balls and half
       of the golf balls are blue. How many blue golf balls are there?
    A: The answer (in numerals) is
    -> Output: 8   (incorrect)

**Zero-shot CoT:**

    Q: A juggler can juggle 16 balls. Half of the balls are golf balls and half
       of the golf balls are blue. How many blue golf balls are there?
    A: Let's think step by step.
    -> Output: There are 16 balls in total. Half are golf balls, so there are 8
       golf balls. Half of the golf balls are blue, so there are 4 blue golf
       balls.   (correct)

The only change is the four-word cue, yet it turns a wrong answer into a right
one by forcing the intermediate arithmetic into the open.
```

### Few-shot CoT

Show the model worked examples that include the reasoning, not just the answer.
Seeing the *explanation* of how each example was solved leads the model to
produce its own reasoned answer, often improving accuracy further.

### Benefits and limitations

CoT helps because LLMs benefit from detailed, logical steps. You can facilitate it
by adding small logical steps to the prompt, by giving demonstrations that pair a
question with a reasoning chain and answer, or with cues like "Let's think step
by step." It particularly improves arithmetic, common-sense, and symbolic
reasoning, with the largest gains appearing in models around 100 billion
parameters {cite}`wei2022chain`.

It is not free, though:

- CoT prompts, especially few-shot ones, are **specific to a problem type**.
- **Smaller models** may produce fluent but illogical chains, hurting
  performance.
- Generating the extra reasoning **increases cost**.

```{admonition} Choosing a technique
:class: tip
A rough guide:

- **Zero-shot** when the model can do the task from pre-training alone.
- **One-shot** when the output must follow a structure shown by one example.
- **Few-shot** when a structure is best demonstrated by several examples.
- **Chain-of-thought** when the task requires reasoning before answering.
```

## How decoding produces text

To understand the next two techniques, it helps to know how a model turns
probabilities into words. Decoder-only models generate text one word at a time.
At each step the model computes **logits**, scores assigned to every token in its
vocabulary, forming a probability distribution. **Decoding** is the process of
turning those logits into actual text. There are two broad styles:

```{list-table}
:header-rows: 1
:widths: 50 50

* - Greedy decoding
  - Stochastic decoding
* - Deterministic: always pick the highest-probability token.
  - Non-deterministic: sample the next token from the probability distribution.
* - Fast; no need to track multiple sequences.
  - The sampled token is not guaranteed to be the single most likely one.
* - Can get stuck in repetitive loops; output is not "creative."
  - Allows greater diversity in output.
* - Equivalent to sampling with `T = 0`.
  - Controlled by temperature, top-p, and top-k.
```

The fact that stochastic decoding produces *different* reasoning paths on each run
is exactly what the next technique exploits.

## Self-consistency

**Self-consistency** builds directly on chain-of-thought {cite}`wang2022self`.
The idea: instead of trusting one chain of reasoning, generate **multiple, diverse
reasoning paths** through few-shot CoT, then take a **majority vote** over their
final answers. By exploring several possibilities and keeping the most common
answer, the model becomes more reliable on arithmetic and common-sense reasoning.

```{admonition} Intuition: model ensembling
:class: tip
Self-consistency is reminiscent of **ensembling** in classical machine learning,
where you average many models to reduce error. Here you "ensemble" many reasoning
paths from a single model and let them vote. It works best on tasks that have a
single correct answer, such as quantitative business questions.
```

Its limitations mirror its strengths:

- It costs **more compute** than plain CoT. In practice you generate a small
  number of paths (say 5-10); performance usually saturates quickly.
- If **most** reasoning paths are wrong, the majority vote is wrong too, so it
  cannot rescue a model that fundamentally misunderstands the task.
- A practical refinement: use self-consistency to generate higher-quality
  training data, fine-tune on it, then get improved accuracy from a single
  inference run.

## Tree-of-thought

**Tree-of-thought (ToT)** generalizes chain-of-thought one step further
{cite}`yao2023tree`. Rather than following a single line of reasoning (CoT) or
several independent lines (self-consistency), ToT guides the model to
**generate, evaluate, expand on, and choose among** multiple candidate solutions,
much as a person weighs options before committing.

ToT builds a **tree** in which each "thought" is a coherent chunk of language
representing an intermediate step toward a solution. The model:

- generates thoughts (via CoT prompting),
- adds tree-branching with breadth-first and depth-first search,
- and thereby explores systematically, with **look-ahead** and **back-tracking**.

This makes ToT well suited to problems with important early decisions and a need
to explore alternatives, creative writing such as ad-copy generation,
mathematical reasoning, and puzzles like crosswords.

```{admonition} The progression at a glance
:class: note
- **Input-Output:** ask, get one answer.
- **Chain-of-thought:** ask, get one reasoned answer.
- **Self-consistency:** generate several reasoned answers, take the majority vote.
- **Tree-of-thought:** branch into many thoughts, evaluate and search among them,
  back-tracking when a branch looks unpromising.

Each step trades more computation for more reliable reasoning.
```

### Benefits and limitations of ToT

ToT shines on tasks that hinge on initial decisions, planning for the future, and
exploring multiple solutions. But deliberate search is **not always necessary**:
for tasks that strong models already handle easily, it adds cost without benefit.
ToT also requires **more resources** than sampling methods, though the
flexibility of how you build the tree lets you tune the cost-performance
trade-off.

## A note on safety

Advanced reasoning prompts make models more capable, but capability cuts both
ways. The same flexibility that lets you elicit step-by-step reasoning can be
abused to coax models past their safeguards if protections are not in place. This
is the bridge to Module 2, where evaluating, securing, and responsibly deploying
LLMs takes center stage.

## In the news

Reasoning has become the frontier of model development. A wave of **reasoning
models** now performs extended, structured "thinking" internally before
answering, effectively building chain-of-thought and search into the model rather
than relying solely on the prompt. The techniques in this chapter are the
conceptual ancestors of that work: chain-of-thought, self-consistency voting, and
tree-style search reappear, now partly automated inside the models themselves.
Understanding them by hand is the best way to understand what those systems do.

## Hands-on labs

Implement these techniques on Amazon Bedrock in
{doc}`labs/Lab-4/lab4a-Self-consistency`, which generates multiple reasoning paths
and votes on the answer, and {doc}`labs/Lab-4/lab4b-Tree-of-Thought`, which builds
and searches a tree of thoughts.

## Key takeaways

- **Chain-of-thought** elicits step-by-step reasoning ("Let's think step by
  step") and improves accuracy on reasoning tasks, especially in large models.
- **Self-consistency** samples several diverse CoT paths and takes a **majority
  vote**, like ensembling, at the cost of extra compute.
- **Tree-of-thought** branches into many thoughts and **searches** among them with
  look-ahead and back-tracking, best for problems needing exploration.
- Greater reasoning capability raises safety stakes, motivating responsible AI in
  Module 2.

The final chapter of this module extends prompting beyond text into images and
other modalities.
