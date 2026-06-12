# Module 3: Building Applications with Foundation Models

Modules 1 and 2 covered how foundation models work and how to use them
responsibly. Module 3 is where you build. You will assemble real applications:
move from one-off prompts to stateful conversations, ground models in your own
data, give them tools so they can act, and extend everything to images and other
modalities. The connective tissue is **LangChain**, a framework for composing
LLM-powered applications, running on Amazon Bedrock models.

```{list-table}
:header-rows: 1
:widths: 8 42 50

* - #
  - Chapter
  - What you will build toward
* - 1
  - {doc}`01-langchain-modules`
  - The LangChain framework: prompt templates, output parsers, chains (LCEL), and
    memory.
* - 2
  - {doc}`02-conversational-applications`
  - Chatbots: from Q&A to conversation, chat models, caching, and memory
    strategies for long chats.
* - 3
  - {doc}`03-retrieval-augmented-generation`
  - Grounding, RAG architecture, vector databases, chunking, rerankers, and
    multimodal RAG.
* - 4
  - {doc}`04-agents`
  - Agents: tools, the ReAct pattern, LangChain agents, and agentic workflows.
* - 5
  - {doc}`05-multimodal-applications`
  - Multimodal applications: personalization, video analysis, customer service,
    and multimodal agents.
```

The chapters build on one another: a chatbot is a chain with memory; RAG adds
retrieval to that chain; an agent adds tools and reasoning on top; and multimodal
applications extend the whole stack to images and video. The labs in
{doc}`labs-overview` implement each step on Amazon Bedrock.
