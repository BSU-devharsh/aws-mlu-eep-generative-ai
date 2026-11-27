---
title: "Agents"
---

# Chapter 4: Agents

This chapter covers agents, systems in which a model plans, calls tools, and acts toward a goal. It introduces tools and the ReAct pattern, builds agents with LangChain, works through an agentic workflow, and covers the Converse API, structured outputs, the Model Context Protocol, agent memory, and Amazon Bedrock AgentCore.

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

Tools are functions or interfaces an agent can interact with, APIs, document
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

```{image} ../_static/figures/bk_react.*
:alt: ReAct loop around an agent that reasons to plan, acts by calling a tool such as a knowledge base or calculator, observes the result, and answers when done
:width: 95%
:align: center
:class: anim-fig
```

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
- Their **own reports are not proof**. An agent's statement that it finished a
  task or stayed within its permissions should be backed by limits and checks it
  cannot change: least-privilege tools, human approval for consequential actions,
  and treating fetched content as data rather than instructions. This is the
  principle of verifiable constraints rather than self-attestation
  {cite}`trivedi2026verifiable`.

```{admonition} AWS in practice
:class: note
Amazon Bedrock Agents provides a managed way to build this pattern: you define
action groups (tools/APIs), optionally attach a knowledge base for RAG, and Bedrock
orchestrates the reason-act-observe loop. The LangChain concepts here, tools,
toolkits, ReAct, and runtimes, map directly onto what the managed service does for
you.
```

## Tool use on Amazon Bedrock with the Converse API

On Amazon Bedrock the model never runs a tool itself. You send the definitions of the tools it may use along with the conversation. When the model decides it needs one, it stops and returns a request that names the tool and the input to give it. Your code runs the tool and sends the result back, and the model continues. AWS calls this **client-side tool calling**, and the Converse API offers it with the same request shape for every model that supports tools ([AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html)).

1. **Send the message and the tool definitions.** Each tool is a `toolSpec` with a `name`, a `description` the model reads to decide when to use it, and an `inputSchema` written in JSON Schema, all inside the request's `toolConfig`.
2. **Read the tool request.** If the model wants a tool, the response's `stopReason` is `tool_use` and the assistant message holds a `toolUse` block with a `toolUseId`, the tool `name`, and its `input`.
3. **Run the tool in your code.** Check that the name is one you offered and that the input is valid before you act on it.
4. **Return the result.** Add the assistant message to the conversation, then a user message with a `toolResult` block carrying the same `toolUseId` and the tool's output.
5. **Repeat until the model answers.** The loop ends when `stopReason` is something other than `tool_use`, usually `end_turn`.

```{image} ../_static/figures/bk_converse_loop.*
:alt: Converse API tool loop, where the application sends messages and tool definitions, the model returns stopReason tool_use, the application checks and runs the tool and returns a toolResult, until stopReason end_turn
:width: 95%
:align: center
:class: anim-fig
```

```python
import boto3

client = boto3.client("bedrock-runtime")
MODEL_ID = "your-model-id"   # any Bedrock model that supports tool use

tool_config = {"tools": [{"toolSpec": {
    "name": "get_weather",
    "description": "Current temperature in Celsius for a city.",
    "inputSchema": {"json": {"type": "object",
                             "properties": {"city": {"type": "string"}},
                             "required": ["city"]}}}}]}

def get_weather(city):        # your code; the model only asks for it
    return {"city": city, "celsius": 21}

TOOLS = {"get_weather": get_weather}
messages = [{"role": "user", "content": [{"text": "Is it warm in Lisbon right now?"}]}]

while True:
    response = client.converse(modelId=MODEL_ID, messages=messages, toolConfig=tool_config)
    message = response["output"]["message"]
    messages.append(message)
    if response["stopReason"] != "tool_use":
        break
    results = []
    for block in message["content"]:
        if "toolUse" in block:
            use = block["toolUse"]
            if use["name"] not in TOOLS:          # never run a tool you did not offer
                raise ValueError(f"unknown tool {use['name']}")
            output = TOOLS[use["name"]](**use["input"])
            results.append({"toolResult": {"toolUseId": use["toolUseId"],
                                           "content": [{"json": output}]}})
    messages.append({"role": "user", "content": results})

print(message["content"][0]["text"])
```

The same loop is what LangChain agents and Bedrock Agents run for you; seeing it bare makes clear where the controls belong. The model proposes, and your code decides whether to execute.

### Stop conditions and safe retries

The loop above is an **agent harness** in miniature: ordinary code that calls the model, checks each proposed action, runs the allowed ones, and decides when to stop. As written it stops only when the model says so, which is the one condition you cannot rely on. A production harness adds **stop conditions** that it enforces itself:

- a step limit, so a model that keeps asking for tools is cut off after, say, ten turns;
- a token or cost budget, read from the `usage` field (`inputTokens`, `outputTokens`, `totalTokens`) that every Converse response returns;
- loop detection, which ends the run when the same tool is requested with the same input twice in a row;
- a time limit, and a kill switch an operator can use.

```python
MAX_STEPS, MAX_TOKENS = 10, 20_000
steps, tokens_used, seen = 0, 0, set()

while True:
    steps += 1
    if steps > MAX_STEPS:
        raise RuntimeError("stopped: step limit reached")
    response = client.converse(modelId=MODEL_ID, messages=messages, toolConfig=tool_config)
    tokens_used += response["usage"]["totalTokens"]
    if tokens_used > MAX_TOKENS:
        raise RuntimeError("stopped: token budget spent")
    message = response["output"]["message"]
    messages.append(message)
    if response["stopReason"] != "tool_use":
        break
    for block in message["content"]:
        if "toolUse" in block:
            key = (block["toolUse"]["name"], repr(sorted(block["toolUse"]["input"].items())))
            if key in seen:
                raise RuntimeError("stopped: repeated identical tool call")
            seen.add(key)
    # ... run the tools and append the toolResult message as before ...
```

Calls fail too. Bedrock returns a `ThrottlingException` when you exceed your quota, and the AWS SDK for Python can retry for you with **exponential backoff**, waiting longer after each failure and adding random jitter so that many clients do not retry in step: create the client with `botocore.config.Config(retries={"total_max_attempts": 5, "mode": "standard"})`, where `total_max_attempts` counts the first request. Setting the mode to `"adaptive"`, which Boto3 labels experimental, adds client-side rate limiting. Retries are only safe when the action they repeat is **idempotent**, meaning it has the same effect whether it runs once or twice. Reading the weather is idempotent; sending a payment is not, so give such tools an idempotency key that the downstream service uses to ignore duplicates.

Limits stop runaway agents but not manipulated ones. The cybersecurity textbook's subsection on [designing agents to contain prompt injection](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#designing-agents-to-contain-prompt-injection) covers the design patterns that do, such as **plan-then-execute**, where the list of tool calls is fixed before the agent reads any untrusted content, and the **dual LLM** pattern, where the model that can act never sees untrusted text.

### Separating initiation from approval

The cybersecurity textbook works through a question about an agent that both initiates vendor payments and approves them. That design violates separation of duties, and the fix is to split initiation and approval across separate identities ([separation of duties for AI agents](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#separation-of-duties-for-ai-agents-who-initiates-and-who-approves)). This section builds the split into the tool loop above. Three design rules carry most of the weight.

1. Give the agent a tool that proposes a payment and no tool that approves one. Approval runs in a separate service, under the approver's own credentials.
2. Let the harness, not the model, supply the caller's identity. A tool input field such as `approver` would let injected text claim to be someone else.
3. Check independence where the approval happens: the approver is not the initiator, does not share its sponsor, and is a person above a set amount.

```{image} ../_static/figures/bk_approval_separation.*
:alt: The AP agent can only propose a payment into a queue; a separate approval service with its own identity checks that the approver is not the initiator, does not share the sponsor, and is a person above 10,000 dollars before release
:width: 95%
:align: center
:class: anim-fig
```

```python
from dataclasses import dataclass, field
import uuid

@dataclass
class Payment:
    vendor: str
    amount: float                      # US dollars
    initiator: str                     # identity that proposed the payment
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    status: str = "pending_approval"
    approver: str | None = None

SPONSOR = {"ap-agent": "dana", "ap-agent-clone": "dana", "review-agent": "lee",
           "dana": "dana", "lee": "lee", "sam": "sam"}
HUMANS = {"dana", "lee", "sam"}
HUMAN_ABOVE = 10_000
queue: dict[str, Payment] = {}

def propose_payment(vendor: str, amount: float, *, caller: str) -> dict:
    """The only payment tool the agent can call: it queues, it never pays."""
    p = Payment(vendor, amount, initiator=caller)
    queue[p.id] = p
    return {"payment_id": p.id, "status": p.status}

def approve_payment(payment_id: str, *, approver: str) -> Payment:
    """Runs in the approval service under the approver's own credentials."""
    p = queue[payment_id]
    if approver == p.initiator:
        raise PermissionError("initiator cannot approve its own payment")
    if SPONSOR[approver] == SPONSOR[p.initiator]:
        raise PermissionError("approver shares the initiator's sponsor")
    if p.amount > HUMAN_ABOVE and approver not in HUMANS:
        raise PermissionError("amount needs a human approver")
    p.status, p.approver = "approved", approver
    return p

# The harness exposes only propose_payment and supplies the caller identity itself
AGENT_ID = "ap-agent"
TOOLS = {"propose_payment": propose_payment}

def run_tool(tool_use: dict) -> dict:
    fn = TOOLS.get(tool_use["name"])
    if fn is None:
        return {"toolUseId": tool_use["toolUseId"], "status": "error",
                "content": [{"text": f"tool {tool_use['name']} is not available to this agent"}]}
    result = fn(**tool_use["input"], caller=AGENT_ID)   # identity comes from the harness, not the model
    return {"toolUseId": tool_use["toolUseId"], "content": [{"json": result}]}
```

The test sends the harness stub tool requests shaped like the `toolUse` blocks of a Converse response, including one that an injected instruction might produce, and then tries several approvers.

```python
from approval import run_tool, approve_payment, queue
# Stub tool requests, shaped like toolUse blocks from a Converse response
injected = {"toolUseId": "t1", "name": "approve_payment", "input": {"payment_id": "x"}}
print(run_tool(injected)["content"][0]["text"])
small = run_tool({"toolUseId": "t2", "name": "propose_payment", "input": {"vendor": "Acme", "amount": 4200}})
large = run_tool({"toolUseId": "t3", "name": "propose_payment", "input": {"vendor": "Acme", "amount": 48000}})
pid_small, pid_large = small["content"][0]["json"]["payment_id"], large["content"][0]["json"]["payment_id"]
for pid, who in [(pid_small, "ap-agent"), (pid_small, "ap-agent-clone"), (pid_small, "dana"),
                 (pid_large, "review-agent"), (pid_small, "review-agent"), (pid_large, "sam")]:
    try:
        p = approve_payment(pid, approver=who)
        print(f"{queue[pid].amount:>8,.0f} USD by {who:<15} -> approved")
    except PermissionError as e:
        print(f"{queue[pid].amount:>8,.0f} USD by {who:<15} -> refused: {e}")
```

```text
tool approve_payment is not available to this agent
   4,200 USD by ap-agent        -> refused: initiator cannot approve its own payment
   4,200 USD by ap-agent-clone  -> refused: approver shares the initiator's sponsor
   4,200 USD by dana            -> refused: approver shares the initiator's sponsor
  48,000 USD by review-agent    -> refused: amount needs a human approver
   4,200 USD by review-agent    -> approved
  48,000 USD by sam             -> approved
```

The injected approval never reaches the payment service, because the tool does not exist for this agent. The clone and the agent's own sponsor are refused even though they are different identities, and the review agent can approve the small payment but not the large one. In production the queue is a database table or a workflow step, the approver signs in through its own identity provider, and the agent's AWS Identity and Access Management (IAM) role has no permission to call the approval API at all.

Amazon Bedrock offers two managed checks that help but do not replace the split.

- **User confirmation.** Bedrock Agents can ask the end user to confirm before invoking an action group function. Set `requireConfirmation` to `ENABLED` for the function, or `x-requireConfirmation` in an OpenAPI schema, and the agent asks a confirmation question before it acts; AWS recommends this as a safeguard against malicious prompt injection ([AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-userconfirmation.html)). **Return of control** goes further and hands the action's parameters back to your application to carry out ([AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/action-handle.html)). The person who confirms is usually the user who asked for the payment, so confirmation checks intent, not separation of duties. Route the approval to a different person.
- **AgentCore Policy.** Policy, described later in this chapter, evaluates an agent's tool calls against Cedar rules that live outside the agent's code, so a rule can deny the agent's identity any call to an approval tool even if a prompt injection asks for one.

## Structured outputs and strict tool use

A model asked for JSON usually returns JSON, but usually is not good enough for a program that parses every reply. Since February 4, 2026, Amazon Bedrock has offered **structured outputs**, which use **constrained decoding**: at each step the service allows only the tokens that keep the reply valid against a JSON schema you supply, so the model cannot produce output that breaks it ([AWS](https://aws.amazon.com/about-aws/whats-new/2026/02/structured-outputs-available-amazon-bedrock)). It works with the Converse, ConverseStream, InvokeModel, and InvokeModelWithResponseStream APIs; in the Converse API the schema goes in the request's `outputConfig.textFormat` field. A second mechanism, **strict tool use**, adds `strict: true` to a tool definition so that the tool name and input the model returns are guaranteed to match the tool's input schema.

The schemas follow a supported subset of JSON Schema Draft 2020-12. Every object must set `additionalProperties` to `false`, Bedrock rejects a schema with unsupported features with an error, and the first request with a new schema can take minutes while the service compiles it into a grammar ([AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html)). Support began with Anthropic's Claude 4.5 models and selected open-weight models and has since been extended, so check the model support table before you rely on it.

A schema guarantees the shape of an answer, not its truth or safety. A valid `summary` field can still be wrong, or can carry text it should not, so validate the values too.

## The Model Context Protocol

Tool definitions written into one application work only in that application. The **Model Context Protocol (MCP)**, released by Anthropic in November 2024 and placed under the Linux Foundation's Agentic AI Foundation in December 2025, standardizes the connection instead, so a tool is built once as an MCP server and used by any MCP-aware application.

- **Host, clients, and servers.** The **host** is the AI application, such as a chat app, an IDE, or an agent. For each server it connects to, the host runs one **client**. A **server** offers capabilities through three primitives: **tools** the model can call, **resources** such as files and records it can read, and **prompts**, which are reusable templates.
- **Transports.** A local server usually talks over standard input and output (stdio); a remote server uses **Streamable HTTP**.
- **The current version.** The specification dated July 28, 2026 made the protocol stateless. The old initialize handshake and session identifier are gone; every request carries its own protocol version and capabilities, so any server instance behind a load balancer can answer it, and HTTP requests name the method and tool in headers that gateways can route on. Requests that a server once sent back to the client, such as asking the user a question, now travel as Multi Round-Trip Requests inside the original call ([MCP specification](https://modelcontextprotocol.io/specification/2026-07-28)).

MCP and Converse tool use fit together. MCP is how the host discovers a server's tools and calls them; Converse tool use is how the model asks for one. A host lists an MCP server's tools, turns each into a `toolSpec`, and when the model returns a `toolUse` block, calls the matching tool on the server.

```{admonition} Security view
:class: warning
A tool's description goes straight into the model's context, so a malicious or compromised MCP server can hide instructions in it, the attack known as tool poisoning. Connect only servers you trust, pin and review their tool definitions, give each server the narrowest credentials it needs, and require a person to approve actions that cannot be undone. The companion textbook covers the attack and the controls in detail ([Section 17.13, MCP Tool Poisoning](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#mcp-tool-poisoning-when-tool-metadata-is-the-attack)).
```

## Agent memory and session state

A model call has no memory; everything the model knows about the conversation is in the prompt you send. Agents that work across many steps or sessions therefore keep **memory** outside the model. **Short-term memory** is the working context of the current task: the conversation, tool results, and intermediate notes, trimmed or summarized to fit the context window. **Long-term memory** is an external store, often a database or vector index, that holds facts, preferences, and summaries of past sessions, and that the agent queries when it needs them. In multi-agent systems some memory is **shared**, so one agent's notes become another agent's input. AgentCore Memory, below, provides both short-term and long-term stores as a managed service. **Session persistence** is the related job of keeping an agent's state, memory, and credentials consistent across turns, retries, and restarts, so that a long task can resume without starting over.

```{admonition} Security view
:class: warning
Memory turns a one-time attack into a lasting one. An injected instruction that the agent saves as a user preference will be read back in every later session. That is why the OWASP Top 10 for Agentic Applications, released in December 2025, lists memory and context poisoning as ASI06. Write to long-term memory only through validated, attributable operations, keep each user's memory separate, expire what is no longer needed, and let users see and delete what the agent remembers. The companion textbook covers memory poisoning with the other agentic threats ([Threat Modeling AI Systems](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#threat-modeling-ai-systems-from-stride-to-maestro)).
```

## Amazon Bedrock AgentCore

Building an agent is one problem; running it in production is another. **Amazon Bedrock AgentCore**, generally available since October 13, 2025, is a set of managed services for running agents built with any framework, such as LangGraph, CrewAI, LlamaIndex, Google ADK, or the OpenAI Agents SDK, and any model ([AWS](https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available)). Bedrock Agents, described above, builds the agent for you; AgentCore hosts and governs agents you build yourself.

```{list-table}
:header-rows: 1
:widths: 22 78

* - Service
  - What it does
* - Runtime
  - Serverless hosting for agents, with each session isolated from the others
* - Memory
  - Short-term context within a session and long-term memory across sessions
* - Gateway
  - Turns existing APIs and AWS Lambda functions into tools agents can call over MCP, and connects to MCP servers
* - Identity
  - Gives agents their own identities and manages the credentials they use to reach other services on a user's behalf
* - Code Interpreter
  - Runs code the agent writes in an isolated environment
* - Browser
  - A managed web browser the agent can drive
* - Observability
  - Traces, metrics, and dashboards in Amazon CloudWatch
* - Policy
  - Rules, written in the Cedar policy language or drafted from plain English, that allow or deny an agent's tool calls; generally available since March 3, 2026
* - Evaluations
  - Built-in and custom evaluators that score agent quality continuously; generally available since March 31, 2026
```

Policy and Evaluations were announced in preview on December 2, 2025 and reached general availability in March 2026 ([AWS News Blog](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/)). Policy matters because it is enforced outside the model: policies attach to an AgentCore Gateway, which checks every agent-to-tool request before the tool runs, so a prompt cannot talk its way past a rule.

```{admonition} Security view
:class: warning
Isolation settings deserve testing, not trust. In March 2026, researchers at BeyondTrust disclosed that the Code Interpreter's Sandbox network mode still let DNS queries out, enough to run commands and move data over DNS. AWS fixed the DNS path in April 2026 and recommends VPC mode when you need full control of traffic. The companion textbook explains this case and the output-side controls that contain an agent ([Section 17.13, The Output Channel as an Exfiltration Path](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#the-output-channel-as-an-exfiltration-path)).
```

## Sandboxing tool code: seccomp profiles

An agent that runs code, or a tool server that parses files users upload, is a process that may one day run an attacker's instructions. Whatever that code then tries, it has to ask the kernel through system calls. **Seccomp**, short for secure computing mode, lets a process install a filter that decides which system calls it may make, and a **seccomp profile** is the set of rules a container runtime turns into that filter. A typical model server or tool server needs a few dozen of the hundreds of calls Linux offers, so a profile removes most of the kernel an attacker could reach. The figure shows where the filter sits and who sets it on AWS.

```{image} ../_static/figures/bk_seccomp_filter.*
:alt: How seccomp filters system calls for model servers and agent tools on AWS. Step 1, a model server or tool sandbox makes normal calls such as read, futex, and sendto, while injected attacker code tries unshare and mount. Step 2, the seccomp filter, a small BPF program, checks each call's number and raw argument values but cannot follow pointers, so it never sees a file path. Step 3, allowed calls run in the kernel. Step 4, denied calls return an EPERM error or the process is killed. Step 5, a profile is built by recording a test run in log mode and allowing only the recorded calls. Step 6 lists the Kubernetes profile types, RuntimeDefault, Localhost, and Unconfined, which is the default unless the kubelet's seccomp-default setting is on. Step 7 shows who sets the filter on AWS. AgentCore runs each session in its own microVM, Firecracker filters its own virtual machine monitor, on EKS with EC2 nodes you set the profile, and on ECS with Fargate AWS runs the container runtime.
:width: 95%
:align: center
:class: anim-fig
```

### What the filter can and cannot do

The filter is a small Berkeley Packet Filter (BPF) program that the kernel runs before each system call. It sees the call's number and its raw argument values and can allow the call, fail it with an error, or kill the process. It cannot follow pointers, so it can block `unshare` or `mount` but cannot tell which file an allowed `openat` call opens; the kernel documentation says plainly that system call filtering is not a sandbox, only a way to shrink the kernel surface a process can reach ([Linux kernel documentation](https://docs.kernel.org/userspace-api/seccomp_filter.html)). Defaults also differ by platform. Docker applies a default profile to every container that disables around 44 of more than 300 system calls ([Docker](https://docs.docker.com/engine/security/seccomp/)), but a Kubernetes Pod that sets no profile runs Unconfined, with no filter, unless the kubelet's seccomp-default setting, stable since Kubernetes 1.27, is turned on ([Kubernetes](https://kubernetes.io/docs/tutorials/security/seccomp/)). That gap mattered in 2022, when Docker's default profile blocked the `unshare` route to the CVE-2022-0185 kernel exploit while Pods running Unconfined stayed exposed ([CrowdStrike](https://www.crowdstrike.com/en-us/blog/cve-2022-0185-kubernetes-container-escape-using-linux-kernel-exploit/)).

### Who sets the filter on AWS

The answer depends on where the code runs.

- **AgentCore Runtime and Code Interpreter.** Each session runs in its own microVM with isolated CPU, memory, and file system, and the microVM is terminated and its memory sanitized when the session ends ([AWS documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html)). AWS describes these as hardware-isolated Firecracker microVMs ([AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/run-agents-securely-and-efficiently-with-the-next-generation-agentcore-runtime/)), and Firecracker installs its own seccomp filters on its virtual machine monitor by default ([Firecracker design](https://raw.githubusercontent.com/firecracker-microvm/firecracker/main/docs/design.md)). You do not write a profile here; the microVM is the boundary, and the DNS case above shows why its settings still deserve testing.
- **Amazon EKS on EC2 nodes.** You set the profile. The EKS best practices guide recommends `RuntimeDefault` in each Pod's `securityContext`, or the kubelet's `--seccomp-default` flag for every Pod on a node, and points to tools such as the Security Profiles Operator for recording custom profiles ([Amazon EKS Best Practices Guide](https://docs.aws.amazon.com/eks/latest/best-practices/runtime-security.html)).
- **Amazon ECS on Fargate.** AWS runs the container runtime, and the `dockerSecurityOptions` parameter that would pass Docker security options is not valid for Fargate tasks ([AWS documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html)).

For a tool server you host yourself on EKS, such as an MCP server that converts uploaded documents, a Pod like the one below meets the Kubernetes Restricted Pod Security Standard for seccomp, privilege escalation, and capabilities ([Kubernetes](https://kubernetes.io/docs/concepts/security/pod-security-standards/)). Setting `allowPrivilegeEscalation: false` also sets the `no_new_privs` flag that the kernel requires before an unprivileged process can install a seccomp filter.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: doc-converter-tool
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault          # or Localhost with a profile recorded from your test suite
  containers:
    - name: converter
      image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/doc-converter@sha256:<digest>
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
```

Seccomp is one layer. Pair it with network policy, because an allowed `connect` call can still send data out, and run code you do not trust, such as code an agent wrote, inside a microVM such as an AgentCore session rather than in a shared container. The companion textbook explains the mechanism in depth and simulates a recorded profile against an attacker's calls ([Seccomp Profiles: Filtering System Calls](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#seccomp-profiles-filtering-system-calls)).

#### Check your understanding: seccomp

Try this question before you open the answer. Your team hosts an MCP tool server on Amazon EKS with EC2 nodes. It converts PDFs that users upload, and its Pod spec sets no `securityContext`. A reviewer argues that running in a container already sandboxes it. What is the best response?

- **A.** Agree, because Kubernetes blocks dangerous system calls in every container by default
- **B.** Raise the Pod's CPU limit and timeout so a malicious PDF cannot crash the server
- **C.** Set a `RuntimeDefault` or recorded `Localhost` seccomp profile, drop all capabilities, and disallow privilege escalation, because Kubernetes runs such a Pod Unconfined
- **D.** Turn on verbose logging, which blocks the system calls the server does not need

```{admonition} Answer
:class: dropdown
**C.** A Pod with no seccomp setting runs Unconfined unless the kubelet's seccomp-default setting is on, so A is wrong for Kubernetes even though Docker on its own applies a default profile. CPU limits and timeouts in B change how much the process consumes, not which system calls it can make, and logging in D records activity without removing a single call.
```

## Identity posture for agents: ISPM on AWS

Every agent you deploy adds identities: an IAM execution role, an AgentCore workload identity, OAuth tokens for the services it calls, and API keys for its tools. Over months, some of them stop being used, lose their owners, or hold more access than the agent needs. **Identity security posture management (ISPM)** is the practice, and the product category, of watching all of these identities continuously. Gartner's Hype Cycle for Digital Identity, 2026 describes it as a discipline that continuously assesses, monitors, and manages IAM policies and configurations ([as quoted by Delinea](https://delinea.com/blog/identity-security-posture-management-in-the-agentic-era)). The figure shows the loop as it applies to a Bedrock account.

```{image} ../_static/figures/bk_ispm_loop.*
:alt: Identity security posture management for a Bedrock account as a continuous loop. Step 1 discovers IAM users and roles and agent and tool identities. Step 2 correlates trust policies, role chains, and effective access into a graph. Step 3 finds weak posture such as unused roles and keys, unused actions, and missing MFA. Step 4 ranks findings by paths to models, data, and stored OAuth tokens. Step 5 fixes findings with guardrails, automating only low-risk, reversible hygiene. Step 6 verifies that nothing broke and scans again. Step 7 compares four tools. Identity governance asks who should have access, ISPM asks whether posture is risky now, identity threat detection and response asks whether an identity attack is under way, and AI security posture management asks whether AI models and data are exposed.
:width: 95%
:align: center
:class: anim-fig
```

### What AWS gives you

Two AWS services supply most of the raw material for this loop on a Bedrock account.

- **AgentCore Identity** keeps an agent identity directory. Each agent identity gets its own ARN inside a directory hierarchy, so a policy can target one agent or a whole group of them ([AWS documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/key-features-and-benefits.html)). Its token vault stores OAuth 2.0 access and refresh tokens, API keys, and client secrets, encrypted with AWS KMS keys, including customer managed keys ([AWS Security Blog](https://aws.amazon.com/blogs/security/securing-ai-agents-with-amazon-bedrock-agentcore-identity)). An agent reaches the vault with a workload access token that carries both its own identity and the identity of the user it acts for, so the directory doubles as an inventory of which agent holds which credential for whom.
- **IAM Access Analyzer** can run an unused access analyzer that reports IAM roles nobody assumed, access keys and passwords nobody used, and services and actions a role or user never called. You choose a tracking period from 1 to 365 days; the default is 90 ([AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-create-unused.html)). For unused permissions it proposes a replacement policy, and it charges per IAM role and user analyzed each month ([AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html)).

Commercial ISPM products add what these services do not: one view across AWS, your identity provider, and SaaS applications; attack path analysis across those systems; and discovery of agents built on other platforms. Much of what vendors call AI in these products is graph analysis, peer-group statistics, or language model summaries, so ask which one a finding came from. The companion textbook separates these techniques and adds a worked posture scan ([Identity Security Posture Management](https://book.com.puter.tips/chapters/17_emerging/chapter17.html#identity-security-posture-management-watching-every-identity-at-once)).

### Why agent tokens need posture management

The 2025 Salesloft Drift campaign is the case to remember. Attackers used stolen OAuth and refresh tokens belonging to Drift, an AI chat agent connected to customers' Salesforce instances, to export large volumes of data from numerous instances between August 8 and at least August 18, 2025. They then searched the stolen records for secrets such as AWS access keys ([Google Threat Intelligence Group](https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift)). No Salesforce vulnerability was involved; the access had been granted to a third party, and the attackers used it. Two lessons carry over directly. An agent's tokens are as valuable as the data behind them, and secrets pasted into tickets or records that an agent can read extend every attack path that passes through that agent. The OWASP Top 10 for Agentic Applications lists this class of failure as ASI03, Identity and Privilege Abuse.

### A posture checklist for Bedrock agents

These steps keep agent identities from drifting into risk.

1. **One identity per agent.** Give each agent its own workload identity and execution role. Never let it run on a person's credentials or a role shared with other agents.
2. **An owner for every identity.** Record the person accountable for each agent's purpose, permissions, and retirement, for example in a tag.
3. **A tracking window longer than the slowest job.** Set the unused access analyzer's tracking period longer than the longest interval between legitimate runs, so a quarterly job does not look unused.
4. **Narrow, vaulted tokens.** Request the narrowest OAuth scopes, keep tokens in the AgentCore token vault, and never place them in prompts, code, or agent memory.
5. **Exposure first.** Fix first the identities that can reach model invocation, training data, knowledge bases, or stored tokens.
6. **Guardrails on automation.** Automate only reversible, low-risk fixes, disable before you delete, and send anything on a path to sensitive data to its owner for approval.
7. **Clean retirement.** When an agent is retired, revoke its tokens, delete its workload identity, and remove its execution role.

#### Check your understanding: identity posture for agents

Try this question before you open the answer. IAM Access Analyzer reports two findings. A Bedrock agent's execution role has never used its `s3:DeleteObject` permission on the training data bucket. A role created for an old proof of concept has not been assumed in 200 days, has no owner tag, and can only read a public sample bucket. An ISPM tool offers to delete both automatically. What is the best response?

- **A.** Approve both deletions, because unused access is always safe to remove
- **B.** Wait for an identity threat detection alert, because posture findings matter only once an attack begins
- **C.** Ignore the agent role, because it has only one finding
- **D.** Remove the agent's unused delete permission through a reviewed policy change, and disable the stale role now and delete it later

```{admonition} Answer
:class: dropdown
**D.** The agent's role sits on a path to the training data, so the change goes through review even though it has a single finding, which rules out C. The stale role is dormant, unowned, and reaches nothing sensitive, which makes it low-risk hygiene that can be disabled reversibly at once. A skips the guardrails that keep an automated fix from breaking a job that runs rarely, and B confuses posture management with threat detection, which works on attacks already under way.
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

The points below summarize what agents add and how to keep them safe and reliable.

- An **agent** uses an LLM as a reasoning engine plus **tools** to act, going
  beyond single prompts and fixed chains.
- **ReAct** interleaves **reasoning** (planning) and **acting** (tool use), with
  observation between steps.
- LangChain provides **tools, toolkits, agents, and runtimes**; Amazon Bedrock
  Agents offers this as a managed service.
- Agents need capable models, are hard to debug, raise security risks, and are
  overkill for simple tasks.
- On Amazon Bedrock the model only **requests** a tool; your code runs it. The
  Converse API loop is `toolUse` out, `toolResult` back, until `stopReason` is
  no longer `tool_use`.
- Keep **initiation and approval** in separate identities: give the agent a
  propose tool only, let the harness supply the caller's identity, and check
  independence in the approval service. User confirmation checks intent, not
  separation of duties.
- **Structured outputs** and **strict tool use** guarantee the shape of JSON
  answers and tool inputs through constrained decoding, not their truth.
- **MCP** standardizes how hosts connect to tool servers; its July 2026 version
  is stateless. Tool descriptions are untrusted input.
- **AgentCore** runs and governs agents built with any framework; its Policy
  service enforces tool rules at the gateway, outside the model.
- **Seccomp** profiles limit the system calls a model or tool server can make;
  Kubernetes runs Pods Unconfined unless you set `RuntimeDefault` or enable
  seccomp-default, while AgentCore sessions run in their own microVMs.
- **Identity posture** decays: give each agent its own identity and owner, keep
  its tokens in a vault, find unused access with IAM Access Analyzer, and fix
  first what reaches sensitive data.

Finally, we extend applications across modalities.
