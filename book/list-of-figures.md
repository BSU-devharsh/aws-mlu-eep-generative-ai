# List of Figures

This list catalogs the main diagrams and illustrations that appear in the book,
grouped by part. Most figures are embedded in the hands-on labs; open the linked
page to view a figure in context. (Decorative logos and interface chrome are
omitted.)

## Primer: AI Literacy

```{list-table}
:header-rows: 1
:widths: 20 80

* - Location
  - Figure
* - {doc}`intro`
  - Reading order of the book, from the primer through the three modules and
    their labs to the appendices.
* - {doc}`primer/ai-literacy`
  - Data check to run before pasting text into an AI tool, covering PII, FERPA,
    and HIPAA.
* - {doc}`primer/ai-and-tools-reference`
  - Decision flowchart for choosing a model and effort level.
* - {doc}`primer/ai-concepts-assistants-effort`
  - Map of how AI, machine learning, deep learning, NLP, generative AI, LLMs,
    foundation models, frontier models, agentic AI, AGI and superintelligence
    relate.
* - {doc}`primer/ai-concepts-assistants-effort`
  - What changes inside a model at low, medium and high or maximum effort.
* - {doc}`primer/aws-ai-services`
  - Decision flow for choosing a task-specific AWS AI service, Amazon Bedrock, or
    Amazon SageMaker AI.
* - {doc}`primer/tokens-and-embeddings`
  - Tokens for processing text versus embeddings for comparing meaning.
* - {doc}`primer/practical-ai-workflow`
  - The seven steps of the practical AI workflow, with a feedback loop.
```

## Module 1: Fundamentals of Generative AI

```{list-table}
:header-rows: 1
:widths: 20 80

* - Location
  - Figure
* - {doc}`module-1/01-introduction-to-generative-ai`
  - How a request travels through Amazon Bedrock to models from several
    providers.
* - {doc}`module-1/02-foundation-models-and-llms`
  - Verifying a model, importing or quantizing it, evaluating it, and signing it
    before deployment.
* - {doc}`module-1/02-foundation-models-and-llms`
  - Recording how a model was built with in-toto and SLSA provenance.
* - {doc}`module-1/03-prompt-engineering`
  - The four parts of a prompt and the inference parameters that shape the
    response.
* - {doc}`module-1/04-advanced-prompting-techniques`
  - Chain-of-thought, self-consistency, and tree-of-thought on one question.
* - {doc}`module-1/05-multimodal-prompting`
  - How a multimodal LLM brings images, video, and audio into a language model.
* - {doc}`module-1/labs/Lab-4/lab4b-Tree-of-Thought`
  - Tree-of-Thought reasoning diagram.
* - {doc}`module-1/labs/Lab-5/Lab5-Multimodal`
  - Chatbot architecture; Open LLM Leaderboard; multimodal sample images
    (Amazon packages, ASL, cat-with-laptop, chart data, payment receipt, stacked
    boxes).
```

## Module 2: Responsible Generative AI

```{list-table}
:header-rows: 1
:widths: 20 80

* - Location
  - Figure
* - {doc}`module-2/01-evaluating-llms`
  - The four evaluation types in Amazon Bedrock: programmatic, human,
    LLM-as-a-judge, and RAG evaluation.
* - {doc}`module-2/01-evaluating-llms`
  - Checking that an answer is grounded in its source, and abstaining when it
    is not.
* - {doc}`module-2/02-foundations-of-responsible-ai`
  - The NIST AI Risk Management Framework, with Govern across Map, Measure, and
    Manage.
* - {doc}`module-2/02-foundations-of-responsible-ai`
  - EU AI Act Article 50 transparency duties versus Article 15 requirements for
    high-risk systems.
* - {doc}`module-2/03-dimensions-of-responsible-ai`
  - The eight dimensions of responsible AI.
* - {doc}`module-2/04-improving-security-and-safety`
  - Guardrails on the way into and out of a model.
* - {doc}`module-2/04-improving-security-and-safety`
  - How an ordinary resize step silently drops an image's C2PA credential.
* - {doc}`module-2/04-improving-security-and-safety`
  - A model API that resists extraction by returning labels, logging scores,
    and rate-limiting.
* - {doc}`module-2/04-improving-security-and-safety`
  - Threat modeling a Bedrock application, with one threat and one control per
    component.
* - {doc}`module-2/labs/Lab-3/lab3-robustness`
  - Robustness and guardrails architecture diagrams.
* - {doc}`module-2/labs/Lab-4/lab4b-watermarking`
  - Watermarking illustrations.
* - {doc}`module-2/labs-overview`
  - Retail bot workflow and agent-flow diagrams used across the Module 2 labs.
```

## Module 3: Building Applications with Foundation Models

```{list-table}
:header-rows: 1
:widths: 20 80

* - Location
  - Figure
* - {doc}`module-3/01-langchain-modules`
  - A LangChain chain written with LCEL, and the memory that carries context
    between calls.
* - {doc}`module-3/02-conversational-applications`
  - One chatbot turn with a response cache, conversation memory, and prompt
    caching.
* - {doc}`module-3/03-retrieval-augmented-generation`
  - Fine-tuning versus retrieval-augmented generation.
* - {doc}`module-3/03-retrieval-augmented-generation`
  - The RAG workflow, from indexing documents to generating a grounded answer.
* - {doc}`module-3/04-agents`
  - The ReAct loop of reasoning, acting, and observing.
* - {doc}`module-3/04-agents`
  - The tool loop of the Bedrock Converse API.
* - {doc}`module-3/04-agents`
  - Separating an agent that proposes a payment from the service that approves
    it.
* - {doc}`module-3/05-multimodal-applications`
  - A multimodal agent that looks at a photo, retrieves the manual, and walks
    the user through a fix.
* - {doc}`module-3/labs/Lab-1/lab1-langchain_modules`
  - LangChain module and chain diagrams.
* - {doc}`module-3/labs/Lab-2/lab2-chatbots`
  - Chatbot component diagram.
* - {doc}`module-3/labs/Lab-3/lab3a-retrieval_augmented_generation`
  - RAG architecture diagrams.
* - {doc}`module-3/labs/Lab-4/lab4_agents`
  - Agent-with-tools workflow diagram.
* - {doc}`module-3/labs/Lab-5/lab5a-personalization`
  - Multimodal application illustrations (personalization, product images,
    document pages).
```

## Appendix

```{list-table}
:header-rows: 1
:widths: 20 80

* - Location
  - Figure
* - {doc}`appendix-traditional-ml`
  - Traditional machine learning pipeline, from raw data to fairness checks.
```

```{admonition} Note
:class: note
Additional generated images and intermediate diagrams appear within individual lab
notebooks as you run them. The labs are the primary home for the book's figures;
most explanatory chapters use tables and worked examples, and the few diagrams
they include are drawn as SVG so they render cleanly on every device.
```
