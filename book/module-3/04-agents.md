---
title: "Agents"
---

# Chapter 4: Agents

## Why it matters

So far the model has produced language and retrieved data. **Agents** let it
*act*, deciding for itself what steps to take and using tools to carry them out.
This is the leap from a system that answers questions to one that solves problems.
This chapter explains tools and agents, the **ReAct** pattern that combines
reasoning with action, how LangChain implements agents, and a worked agentic
workflow, along with the real limitations you must design around.

## From prompting to agents

The progression across this module:

- **Prompting**: single-step inference.
- **Chains**: a pre-defined sequence of predictions.
- **Agents**: the system *automatically infers* the sequence of actions to take,
  using the **LLM as a reasoning engine**.

```{admonition} Definition
:class: tip
An **agent** is an AI system that automatically figures out how to best solve a
task, powered by an LLM as its reasoning engine and enhanced with **tools**.
```

## Tools

**Tools** are functions or interfaces an agent can interact with, APIs, document
loaders, functions, even other agents. A tool may or may not itself depend on an
LLM. Examples: a knowledge base of company documents (RAG), a calculator for
arithmetic, an API call for weather, or a Wikipedia search for facts. Tools are
what let an LLM overcome its built-in limitations (for example, doing reliable math
or fetching live data).

What can an agent do with tools? It can understand a request in natural language,
**generate a plan** using techniques like chain-of-thought, identify the resources
(APIs, data sources, tools) it needs, execute the plan by invoking those tools,
and overcome obstacles by retrying.

## ReAct: Reason + Act

The key pattern is **ReAct**, which combines two LLM strengths:

- **Reasoning**: create, track, and update an action plan, and handle errors.
- **Acting**: interface with functions, tools, knowledge bases, or environments.

The agent loops between reasoning (chain-of-thought) and acting (tool calls),
observing the result of each action and feeding it back into its reasoning,
"Reason, Act, Observe", until the task is done. ReAct suits **knowledge-intensive
tasks** (where simple prompting hallucinates and an agent can query real sources)
and **decision-making tasks** (where custom tools enhance the LLM's planning),
though performance still falls short of expert humans.

## LangChain agents

LangChain provides the machinery:

- **Tools**: functions or interfaces the agent can call; loaded with
  `load_tools(tool_names, llm)`.
- **Toolkits**: pre-defined sets of tools for a goal, for example `GitHubToolkit`,
  `JSON Toolkit`, `PythonREPL`, `SparkSQL Toolkit`, and `Jira Toolkit`.
- **Agents**: the component that decides which actions to take and executes them.
  Tools must be *described* so the agent knows each one's function, and giving the
  agent the right tools for the task matters.
- **Agent runtimes**: responsible for calling the agent and executing actions; a
  common one is the `AgentExecutor`.

## A worked agentic workflow

Consider the deceptively simple query: *"What is the age of the current U.S.
president today?"* A correct answer requires several steps:

1. Find today's date.
2. Find who is U.S. president on that date.
3. Find that person's date of birth.
4. Compute the difference between today and their birth date.
5. Format the result in years, months, and days.
6. Construct the response.

**Without an agent**, a plain LLM cannot do this reliably; it lacks real-time
information and often replies that it cannot give the current age (a real
limitation, not a quirk). **With an agent** using ReAct, the model generates this
plan and executes it step by step, using a **date tool**, a **web search tool**, a
**Wikipedia tool**, and a **calculator tool** in turn, producing an accurate answer
every day with no extra code, training, or deployment, even though the correct
answer changes daily.

## Limitations of agents

Agents are powerful but not free:

- They **require capable reasoning models**; smaller or cheaper LLMs often fail.
- Their **higher abstraction** makes intermediate steps hard to inspect and
  **debug**.
- They are **sensitive to adversarial inputs and edge cases**, which can pose
  **security risks** (an agent executing tools is a larger attack surface, tying
  back to Module 2).
- They can make **simple tasks unnecessarily complex**; not every problem needs an
  agent.

```{admonition} AWS in practice
:class: note
Amazon Bedrock Agents provides a managed way to build this pattern: you define
action groups (tools/APIs), optionally attach a knowledge base for RAG, and Bedrock
orchestrates the reason-act-observe loop. The LangChain concepts here, tools,
toolkits, ReAct, and runtimes, map directly onto what the managed service does for
you.
```

## In the news

Agents are the most active frontier in AI. **Agentic AI** has expanded into coding
agents, computer-use agents, and personal assistants (see the
{doc}`../primer/ai-and-tools-reference`), and frameworks such as LangGraph make
multi-step agent workflows easier to build and observe. The limitations above,
reliability, debuggability, and security, are precisely where current research and
engineering effort is concentrated.

## Hands-on labs

Build an agent on Amazon Bedrock in {doc}`labs/Lab-4/lab4_agents`.

## Key takeaways

- An **agent** uses an LLM as a reasoning engine plus **tools** to act, going
  beyond single prompts and fixed chains.
- **ReAct** interleaves **reasoning** (planning) and **acting** (tool use), with
  observation between steps.
- LangChain provides **tools, toolkits, agents, and runtimes**; Amazon Bedrock
  Agents offers this as a managed service.
- Agents need capable models, are hard to debug, raise security risks, and are
  overkill for simple tasks.

Finally, we extend applications across modalities.
