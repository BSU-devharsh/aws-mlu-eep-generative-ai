---
title: "Ten AI Skills for 2025"
---

# Ten AI Skills for 2025

The generative-AI job market rewards a specific cluster of skills. This chapter
explains ten of the most in-demand ones, what each is, when to use it, the tools
associated with it, and a short Python example, and connects each to the deeper
treatment elsewhere in this book. Think of it as a practical map from "skills
employers list" to "chapters that teach them."

```{admonition} About the tools named
:class: note
Each skill lists representative tools. Tool ecosystems change quickly and naming a
tool is not an endorsement; confirm current capabilities and pricing before
adopting one. The Python snippets are illustrative and are not executed during the
book build.
```

## Overview

```{list-table}
:header-rows: 1
:widths: 4 26 40 30

* - #
  - Skill
  - What it is
  - Representative tools
* - 1
  - **Prompt Engineering**
  - The difference between average output and answers you can act on.
  - ChatGPT, Claude, Gemini, Perplexity
* - 2
  - **AI Agents**
  - AI that does not just reply but completes tasks end to end.
  - OpenAI Agents, CrewAI, LangGraph, LangChain
* - 3
  - **Workflow Automation**
  - Plugging your tools together so routine work happens without you.
  - Make, Zapier, n8n, Bardeen
* - 4
  - **Agentic AI**
  - AI that plans, adapts, and self-corrects instead of following a fixed script.
  - OpenAI o1, Claude, Reflexion, DSPy
* - 5
  - **Multimodal AI**
  - AI that works across text, images, audio, and code in one flow.
  - Gemini, Claude 3.5 Sonnet, OpenAI Vision, Stable Audio
* - 6
  - **RAG**
  - Teaching AI to pull from your data instead of making things up.
  - Pinecone, LlamaIndex, Haystack, Elastic
* - 7
  - **AEO / GEO**
  - Optimising so your brand shows up in AI-generated answers.
  - Searchable, Trakkr.ai, Screaming Frog
* - 8
  - **AI Tool Stacking**
  - Combining tools so they run as one system.
  - Notion AI, ClickUp AI, Airtable AI, Zapier AI
* - 9
  - **AI Content Generation**
  - Producing content at scale without a large team.
  - Descript, Saywhat, OpusClip, ElevenLabs
* - 10
  - **LLM Management**
  - Controlling cost, accuracy, and performance across the AI you use.
  - Arize AI, TruLens, Helicone, Weights & Biases
```

A useful way to see how these relate: skills build from controlling a single model
up to operating a whole AI system.

```{list-table} From single prompt to managed system
:header-rows: 1
:widths: 30 70

* - Layer
  - Skills
* - **Direct a model**
  - Prompt Engineering (1), Multimodal AI (5)
* - **Ground and extend it**
  - RAG (6), AI Content Generation (9)
* - **Let it act**
  - AI Agents (2), Agentic AI (4)
* - **Connect and scale**
  - Workflow Automation (3), AI Tool Stacking (8)
* - **Reach and operate**
  - AEO/GEO (7), LLM Management (10)
```

## 1. Prompt Engineering

**What it is:** the craft of writing inputs that turn a capable model into useful,
actionable output. **When to use it:** any time you need AI to think like a
strategist or operator, not a chatbot. **Tools:** ChatGPT, Claude, Gemini,
Perplexity. This is the foundation; see {doc}`../module-1/03-prompt-engineering`
and {doc}`../module-1/04-advanced-prompting-techniques`.

```python
# A structured prompt: instruction + context + input + explicit output format.
prompt = """You are a financial analyst. Summarize the report below.
Return JSON with keys: summary (string), risk_level (low|medium|high).

Report:
{report_text}
"""
# On Amazon Bedrock via LangChain:
from langchain_aws import ChatBedrock
llm = ChatBedrock(model_id="amazon.nova-pro-v1:0")
response = llm.invoke(prompt.format(report_text="Q3 revenue fell 8% ..."))
```

## 2. AI Agents

**What it is:** AI that completes tasks end to end rather than just answering.
**When to use it:** automating jobs you would hand to an intern, lead generation,
research, scheduling. **Tools:** OpenAI Agents, CrewAI, LangGraph, LangChain.
Covered in {doc}`../module-3/04-agents`.

```python
# A minimal LangChain agent with tools (calculator + search).
from langchain.agents import load_tools, initialize_agent, AgentType
tools = load_tools(["llm-math", "wikipedia"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
agent.invoke("How old is the current US president in days?")
```

## 3. Workflow Automation

**What it is:** connecting your tools so routine work happens without you. **When
to use it:** any repeatable task, reporting, onboarding, data entry. **Tools:**
Make, Zapier, n8n, Bardeen. These are mostly no-code platforms; the same logic can
be scripted in Python, which is what makes the skill transferable.

```python
# Example: a scheduled job that summarizes new files and posts the summary.
def automate(new_files):
    for f in new_files:
        text = open(f).read()
        summary = llm.invoke(f"Summarize in 3 bullets:\n{text}")
        notify_channel(summary)   # e.g. webhook to Slack/Teams
# Trigger this on a schedule (cron) or on a file-created event.
```

## 4. Agentic AI

**What it is:** AI that plans, adapts, and self-corrects instead of following a
fixed script. **When to use it:** complex, multi-step tasks like research, ops, or
QA where flexibility beats rigid workflows. **Tools:** OpenAI o1, Claude,
Reflexion, DSPy. This builds on agents (skill 2) with reasoning and self-critique;
see the reasoning techniques in {doc}`../module-1/04-advanced-prompting-techniques`
and effort/extended-thinking in {doc}`ai-and-tools-reference`.

```python
# Self-correction loop: act, evaluate, retry (the idea behind Reflexion).
def agentic_solve(task, max_iters=3):
    answer = llm.invoke(task)
    for _ in range(max_iters):
        critique = llm.invoke(f"Critique this answer for errors:\n{answer}")
        if "no issues" in critique.lower():
            break
        answer = llm.invoke(f"Improve the answer given this critique:\n{critique}")
    return answer
```

## 5. Multimodal AI

**What it is:** AI that works across text, images, audio, and code in one flow.
**When to use it:** turning a rough idea into a full campaign, copy, visuals,
video, voiceover. **Tools:** Gemini, Claude 3.5 Sonnet, OpenAI Vision, Stable
Audio. Covered in {doc}`../module-1/05-multimodal-prompting` and
{doc}`../module-3/05-multimodal-applications`.

```python
# Send an image plus a question to a multimodal model on Bedrock.
import base64
img = base64.b64encode(open("chart.png", "rb").read()).decode()
msg = [{"role": "user", "content": [
    {"image": {"format": "png", "source": {"bytes": img}}},
    {"text": "What trend does this chart show?"}]}]
# llm.invoke(msg) with a multimodal model id (e.g. Claude or Nova).
```

## 6. RAG (Retrieval-Augmented Generation)

**What it is:** teaching AI to pull from your data instead of making things up.
**When to use it:** customer support, sales enablement, internal knowledge, any
case where accuracy matters. **Tools:** Pinecone, LlamaIndex, Haystack, Elastic.
Fully covered in {doc}`../module-3/03-retrieval-augmented-generation`.

```python
# Retrieve relevant chunks from a vector store, then answer from them.
docs = vectorstore.similarity_search(query="refund policy", k=3)
context = "\n".join(d.page_content for d in docs)
answer = llm.invoke(f"Answer using ONLY this context:\n{context}\n\nQ: {query}")
```

## 7. AEO / GEO (Answer & Generative Engine Optimisation)

**What it is:** SEO for the AI era, making sure your brand shows up in AI-generated
answers. **When to use it:** when prospects start asking ChatGPT instead of Google.
**Tools:** Searchable, Trakkr.ai, Screaming Frog. The skill is to structure content
(clear headings, FAQs, factual snippets, structured data) so retrieval systems and
LLMs surface it, an applied use of the RAG and embeddings ideas in this book.

```python
# Check whether your content is "answer-ready" by testing retrievability.
candidates = ["Our return window is 30 days.", "We value our customers."]
q = "what is the return window?"
ranked = sorted(candidates, key=lambda c: embedding_similarity(q, c), reverse=True)
# The most retrievable snippet is concrete and factual, not vague marketing copy.
```

## 8. AI Tool Stacking

**What it is:** combining your favourite tools so they run as one system. **When to
use it:** to build always-on workflows that cut costs and free up your team.
**Tools:** Notion AI, ClickUp AI, Airtable AI, Zapier AI. The engineering analogue
is composing services with a standard interface, exactly what LangChain provides;
see {doc}`../module-3/01-langchain-modules`.

```python
# Chain tools into one pipeline: notes -> tasks -> calendar.
notes   = notion.get_page(page_id)
tasks   = llm.invoke(f"Extract action items as a list:\n{notes}")
for t in parse_list(tasks):
    clickup.create_task(t)
    calendar.schedule(t)
```

## 9. AI Content Generation

**What it is:** producing content at scale without building a ten-person marketing
team. **When to use it:** daily posts, video edits, podcasts, repurposing
long-form into short. **Tools:** Descript, Saywhat, OpusClip, ElevenLabs. This
applies prompt engineering (skill 1) and multimodal AI (skill 5) to a content
pipeline.

```python
# Repurpose one long article into several short posts.
article = open("post.md").read()
posts = llm.invoke(
    f"Turn this article into 5 short LinkedIn posts, each under 60 words:\n{article}"
)
```

## 10. LLM Management (LLMOps and Observability)

**What it is:** controlling cost, accuracy, and performance across the AI you use.
**When to use it:** once AI becomes core to your operations and you need visibility
on ROI. **Tools:** Arize AI, TruLens, Helicone, Weights & Biases. This is the
production discipline behind the evaluation in {doc}`../module-2/01-evaluating-llms`
and the controllability dimension in
{doc}`../module-2/03-dimensions-of-responsible-ai`.

```python
# Log every call's tokens, latency, and cost for monitoring.
import time
def tracked_invoke(prompt):
    t0 = time.time()
    out = llm.invoke(prompt)
    log_metrics(tokens=count_tokens(prompt, out),
                latency=time.time() - t0,
                cost=estimate_cost(prompt, out))
    return out
```

## A simple visualization

Skills are not equally costly to adopt. A quick way to prioritize is to plot each
skill's **effort to learn** against its **impact**, and start with the
high-impact, low-effort quadrant (prompt engineering and RAG are common entry
points). The following snippet produces such a chart; it is illustrative and uses
example values you would replace with your own assessment.

```python
import matplotlib.pyplot as plt

skills = ["Prompt Eng", "Agents", "Workflow", "Agentic", "Multimodal",
          "RAG", "AEO/GEO", "Tool Stacking", "Content Gen", "LLM Mgmt"]
effort = [2, 7, 4, 8, 5, 6, 4, 3, 3, 7]   # 1 (easy) .. 10 (hard)
impact = [9, 8, 6, 7, 7, 9, 5, 6, 7, 8]   # 1 (low)  .. 10 (high)

plt.figure(figsize=(7, 5))
plt.scatter(effort, impact)
for s, e, i in zip(skills, effort, impact):
    plt.annotate(s, (e, i), fontsize=8, xytext=(4, 4), textcoords="offset points")
plt.axvline(5, color="grey", ls="--"); plt.axhline(7, color="grey", ls="--")
plt.xlabel("Effort to learn"); plt.ylabel("Impact")
plt.title("Prioritizing the 10 AI skills (start top-left: high impact, low effort)")
plt.tight_layout(); plt.show()
```

```{admonition} How to read the chart
:class: tip
Treat the upper-left region (high impact, low effort) as your first targets and
the lower-right (low impact, high effort) as the last. Replace the example numbers
with your own ratings for your role; the point is the prioritization method, not
the specific values.
```

## Key takeaways

- The ten skills form a ladder: **direct a model** (prompt engineering, multimodal)
  -> **ground it** (RAG, content) -> **let it act** (agents, agentic AI) ->
  **connect and scale** (workflow automation, tool stacking) -> **reach and
  operate** (AEO/GEO, LLM management).
- Most map directly onto chapters in this book, so you can go from a one-line skill
  to a hands-on lab.
- Tools come and go; the underlying skills, prompting, retrieval, orchestration,
  evaluation, are durable, which is why this book teaches the concepts alongside a
  concrete stack.
```{admonition} Source
:class: seealso
The ten-skill framing is adapted from a widely shared "10 AI Skills You Need to
Know in 2025" infographic by Chris Donnelly. Explanations, code, and cross-links
are original to this book.
```
