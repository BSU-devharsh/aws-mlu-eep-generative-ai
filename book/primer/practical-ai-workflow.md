---
title: "A Practical AI Workflow"
---

# A Practical AI Workflow: Making AI Do the Heavy Lifting

The chapters in this book teach the mechanics of generative AI. This chapter is
about *habit*, a repeatable personal workflow for getting consistent,
high-quality output from everyday AI assistants. It is adapted, with credit, from
a widely shared LinkedIn post by **Dan Martell** describing how his team pushed AI
to handle the bulk of their routine work.

```{admonition} Credit and framing
:class: note
This workflow is adapted from a public LinkedIn post by Dan Martell (founder,
author of *Buy Back Your Time*). The original frames the goal as having AI do
"92% of the work." Treat that figure as motivational shorthand, not a measured
benchmark; no peer-reviewed evidence supports a specific percentage. The steps
below are summarized and connected to the concepts in this
book; the commentary is original. Always keep sensitive data out of consumer AI
tools (see {doc}`ai-literacy`).
```

## The idea in one line

Stop treating AI as a chatbot you re-explain yourself to every time. Instead, build
reusable **context** and **instructions** once, then reuse them so the AI works
like a trained team member. The split the post proposes is useful: let AI handle
research, drafts, analysis, and options; keep **vision, taste, final decisions, and
emotional intelligence** human.

## The seven steps

### 1. Get a capable assistant

Start with a capable, paid-tier assistant (the post uses ChatGPT Plus/Pro; Claude
and Gemini have equivalents). Capability and larger context windows matter for this
workflow. Remember the privacy guidance in {doc}`ai-literacy`: use an
appropriate tier and keep regulated data out.

### 2. Create a master prompt (your context)

A **master prompt** captures who you are so the AI starts every task already
informed. The post's method: ask the AI, *"I'm [role] at [company type]. Create a
master prompt for me. Ask me every question you need to give the most context
possible,"* spend 30-45 minutes answering, save the result, and paste it into new
chats. In this book's terms, this is the **context** component of a prompt
({doc}`../module-1/03-prompt-engineering`), captured once and reused.

### 3. Build system prompts (your formula)

If a master prompt tells AI *who you are*, a **system prompt** tells it *how to
work*. The post's trick is reverse-engineering: get the AI to produce a great
output through 3-6 iterations, then ask, *"Write the system prompt that would have
generated this output,"* and save it. You now have a reusable formula for that
quality, an applied form of prompt engineering and instruction design.

### 4. Use project folders (persistent context)

Group related work into **projects** (or "folders"), each loaded with the master
prompt and relevant documents, so every conversation builds on the same context
and can be shared with a team. Conceptually this is **memory** and **retrieval**
applied to your own knowledge, the same idea formalized as RAG in
{doc}`../module-3/03-retrieval-augmented-generation`.

### 5. Set custom instructions (your defaults)

Use the assistant's **custom instructions / personalization** settings to fix your
communication style once, short, bulleted, no fluff, preferred tone, and to ban
filler words like "delve" and "moreover." This stops you repeating formatting
requests and is the personal-settings analogue of a standing system prompt.

### 6. Turn workflows into custom assistants

Package your best system prompts into reusable **custom GPTs / assistants**, one
per repeatable task (email, content, financial analysis, hiring, strategy). Update
the assistant once and everyone who uses it benefits. This is a no-code version of
the **agent and tool** patterns in {doc}`../module-3/04-agents`: a specialized,
reusable worker for a specific job.

### 7. Use AI to improve your AI

Ask the assistant to help build the workflow itself, to draft your master prompt,
write system prompts, suggest custom instructions, and improve your prompts. This
is the iterative, "prompting is a loop" mindset from
{doc}`../module-1/03-prompt-engineering`, turned on the workflow itself.

## What "AI does the work" looks like in practice

```{list-table}
:header-rows: 1
:widths: 20 50 30

* - Area
  - AI does
  - You do
* - **Content**
  - Research, outlines, first drafts.
  - Edit and add your voice.
* - **Operations**
  - Draft SOPs, analyze processes, suggest improvements.
  - Decide.
* - **Finance**
  - Analyze reports, build models, surface insights.
  - Make the decisions.
* - **Strategy**
  - Process information, lay out options.
  - Choose the direction.
```

The consistent pattern: **AI drafts and analyzes; humans judge and decide.** The
human 8%, vision, taste, final decisions, and emotional intelligence, is exactly
the part that responsible-AI practice (Module 2) says should stay human.

## How this maps to the rest of the book

This workflow is the everyday, no-code expression of ideas you will see formalized
later:

- Master prompt and custom instructions = **prompt context and standing
  instructions** ({doc}`../module-1/03-prompt-engineering`).
- Reverse-engineered system prompts = **prompt engineering as an iterative
  formula** ({doc}`../module-1/04-advanced-prompting-techniques`).
- Project folders = **memory and retrieval / RAG**
  ({doc}`../module-3/03-retrieval-augmented-generation`).
- Custom GPTs = **specialized agents/tools** ({doc}`../module-3/04-agents`).
- Keeping decisions human = **responsible AI**
  ({doc}`../module-2/02-foundations-of-responsible-ai`).

## Building a reusable prompt template library

The workflow above produces reusable prompts; the next skill is organizing them
into a **template library** so you never start from scratch. The following
eight-step system is adapted, with credit, from a LinkedIn post by **Ronnie
Parsons** (Mighty AI Lab).

```{admonition} Credit
:class: note
Adapted from a public LinkedIn post by Ronnie Parsons
(<https://www.linkedin.com/in/ronnieparsons>). The steps are summarized; the
commentary and example are original to this book.
```

1. **Identify high-value AI tasks.** Track which prompts you write repeatedly
   (client research, content creation), note how often you use each, and estimate
   the time spent rewriting similar prompts.
2. **Analyze prompt structure.** Review 3-5 prompts that worked well, highlight the
   parts that stay **consistent**, and circle the information that **changes** each
   time.
3. **Create clear variables.** Replace the changing elements with descriptive
   variables in `[BRACKETS]`, using `ALL_CAPS` names (for example `[CLIENT_NAME]`)
   that clearly indicate what goes there.
4. **Build a template framework.** Start with the AI role/context, give clear
   output instructions, structure the body with numbered sections, and end with
   specific formatting instructions, the prompt components from
   {doc}`../module-1/03-prompt-engineering`, made reusable.
5. **Test with multiple inputs.** Run the template with three different sets of
   variable data, compare outputs for consistency and quality, and refine the
   wording to remove inconsistencies, the iterative loop of prompt engineering.
6. **Organize the template library.** Keep templates in a dedicated document,
   grouped by business function (marketing, operations), with usage notes for each.
7. **Develop template workflows.** Identify templates that work together and create
   "connectors" where one template's output feeds the next, an informal version of
   the chains in {doc}`../module-3/01-langchain-modules`.
8. **Improve continuously.** Schedule weekly reviews, track time saved and quality,
   and refine templates from feedback, the LLMOps mindset from
   {doc}`../module-2/01-evaluating-llms`.

```{admonition} Pro tip: variable defaults
:class: tip
Include a default example inside each variable, `[VARIABLE_NAME="Example value"]`.
This shows what kind of input works best and lets you leave the default in place
for values you use often, reducing decision fatigue. For example:

    [TONE="Professional and authoritative, but approachable"]
```

A template, in practice, looks like this, and is trivial to fill programmatically:

```python
TEMPLATE = """You are a [ROLE="senior market analyst"].
Task: Research [COMPANY_NAME] and summarize in [SECTIONS="3"] numbered sections.
Tone: [TONE="Professional and authoritative, but approachable"].
Format: bullet points, no preamble."""

def fill(template, **values):
    import re
    # Replace [NAME] or [NAME="default"] with the provided value or the default.
    def repl(m):
        name = m.group(1)
        default = m.group(2)
        return values.get(name, default if default is not None else f"[{name}]")
    return re.sub(r'\[([A-Z_]+)(?:="([^"]*)")?\]', repl, template)

print(fill(TEMPLATE, COMPANY_NAME="Acme Corp"))   # uses defaults for the rest
```

Together, the master-prompt workflow and this template library turn ad-hoc
prompting into a maintainable system, the practical foundation that the prompt
engineering, chains, and evaluation chapters formalize.

## Key takeaways

- Build **reusable context** (master prompt), **reusable formulas** (system
  prompts), and **reusable workers** (custom assistants), then stop re-explaining
  yourself.
- Use **project folders** and **custom instructions** so context and style persist.
- Let AI **draft and analyze**; keep **judgment, taste, and final decisions**
  human.
- These habits are the practical, no-code front end to the prompting, retrieval,
  and agent concepts taught throughout this book.

```{admonition} Source
:class: seealso
Adapted with credit from a public LinkedIn post by Dan Martell
(<https://www.linkedin.com/in/dmartell>). The original text is the author's;
the summary, commentary, and cross-references here are original to this book.
```
