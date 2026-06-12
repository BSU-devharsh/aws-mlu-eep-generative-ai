---
title: "Developing Conversational Applications"
---

# Chapter 2: Developing Conversational Applications

## Why it matters

A chatbot is the most familiar generative-AI application, and it is the natural
first thing to build with LangChain. This chapter takes you from one-off
question-answering to genuine **conversation**: how chat models work, how to
assemble a chatbot from an LLM, a prompt template, and memory, and how to keep
conversations efficient with caching and smarter memory as they grow long.

## From Q&A to conversation

Many LLMs are tuned and optimized for conversation, **instruction-tuned and chat
models**, and can take a *sequence* of messages as input: a **system** message,
plus past **human** and **AI** messages. Amazon Bedrock offers a suite of
chat-optimized models, including Amazon Nova, Anthropic Claude, Meta Llama,
Mistral, and Cohere Command; check each model card for specifics.

LangChain provides **chat prompt templates** built around these message roles:

```python
chat_template = ChatPromptTemplate([
    ("system", "You are a helpful AI bot. Your name is {name}."),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{user_input}"),
])
prompt = chat_template.invoke({"name": "Andy", "user_input": "What is your name?"})
```

The distinction that organizes this chapter:

```{list-table}
:header-rows: 1
:widths: 50 50

* - Question-Answering (Q&A)
  - Conversation
* - Context is only the latest prompt.
  - Maintains context of all past interactions.
* - Interactions do not persist.
  - Interactions persist by updating the context.
* - No additional modules required.
  - Typically uses a form of memory.
* - Used for standard predictions (content creation).
  - Used for chat applications (like ChatGPT).
```

## Building a chatbot

The simplest chatbot needs just three parts: an **LLM**, a **prompt template**
(defining the bot's role and guidelines), and a **memory module** (to persist
information across turns). The loop is: take user input, combine it with retrieved
memory in the prompt, generate a response, and save the exchange back to memory.

```python
memory = ConversationBufferMemory()
chain = prompt | llm | StrOutputParser()
chat_history = memory.load_memory_variables({}).get("chat_history", "")
response = chain.invoke({"chat_history": chat_history, "input": user_input})
memory.save_context({"input": user_input}, {"output": response})
```

## Customizing chat applications

### Caching

Each response consumes cost, compute, and time. **Response caching** stores answers
so that the same or similar prompts return instantly without regenerating,
significantly reducing inference time. Two kinds:

- **In-memory cache**: stored in the application's runtime; fastest, but lost on
  restart.
- **Persistent cache**: stored offline (preferably a database); survives restarts
  and scales better.

Cache deterministic queries (temperature zero); creative responses may be hurt by
caching. Set an expiration so cached answers do not go stale, and size your store
appropriately.

### Handling long conversations

LLMs have a finite context window, and naively keeping every message causes three
problems: messages may become redundant or obsolete, costs compound (each new
message carries all the old ones), and eventually the window overflows. Two memory
strategies address this:

```{list-table}
:header-rows: 1
:widths: 32 68

* - Strategy
  - How it works
* - **Conversation Buffer Window Memory**
  - Keeps only the last *k* interactions, a sliding window that prevents the
    buffer from growing without bound.
* - **Conversation Summary Memory**
  - Uses an LLM to summarize the history, preserving critical information from
    older messages while staying compact, useful for long conversations.
```

```python
memory = ConversationBufferWindowMemory(k=1)   # keep last 1 exchange
# or
memory = ConversationSummaryMemory(llm=llm)    # summarize the history
```

### Context is more than chat history

The context you put in a prompt need not be only past interactions; it can include
relevant information, external data, and human feedback. One natural extension is
**chatting with documents**, prompting with the full text of one or more
documents. But this runs straight into the LLM limitations from Module 1:
reliability and bias, the **context-window limit** (for instance, an early Nova Pro
release allowed up to 300,000 tokens), compute and memory cost, and potential
copyright issues. Feeding entire documents does not scale, which is exactly the
motivation for retrieval augmented generation in the next chapter.

```{admonition} AWS in practice
:class: note
On Amazon Bedrock you build these chatbots from chat-optimized models (Nova,
Claude, Llama, and others) through LangChain's `langchain-aws` integration.
Bedrock also offers managed conversational features, but understanding the memory
and caching mechanics here lets you reason about cost and quality whichever path
you choose.
```

## In the news

Conversational AI has moved from stateless chat toward **persistent memory**:
assistants that remember preferences across sessions, and long-context models that
hold entire documents or codebases at once. Both developments soften, but do not
eliminate, the context-window pressures in this chapter; summarization, windowing,
and retrieval remain essential for cost control even as raw context windows grow.

## Key takeaways

- **Chat models** consume a sequence of system, human, and AI messages; LangChain's
  **chat prompt templates** structure them.
- A chatbot is an **LLM + prompt template + memory**, looping retrieve, respond,
  and save.
- **Caching** cuts cost and latency for repeated, deterministic queries.
- Long conversations need **window** or **summary** memory; stuffing whole
  documents into the prompt does not scale, motivating RAG.

Next, we ground models in external data with retrieval augmented generation.
