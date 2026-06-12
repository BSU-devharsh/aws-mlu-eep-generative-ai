---
title: "Module 3 Labs"
---

# Module 3 Labs: Building applications

These notebooks build complete generative-AI applications on Amazon Bedrock with
LangChain. Read each chapter first, then work the corresponding lab.

```{list-table}
:header-rows: 1
:widths: 12 46 42

* - Lab
  - Notebook
  - Connects to
* - 1
  - {doc}`labs/Lab-1/lab1-langchain_modules`
  - Ch. 1: LangChain modules, chains, and memory.
* - 2
  - {doc}`labs/Lab-2/lab2-chatbots`
  - Ch. 2: building interactive chatbots.
* - 3a
  - {doc}`labs/Lab-3/lab3a-retrieval_augmented_generation`
  - Ch. 3: retrieval augmented generation.
* - 3b
  - {doc}`labs/Lab-3/lab3b-multimodal_rag`
  - Ch. 3: multimodal RAG.
* - 4
  - {doc}`labs/Lab-4/lab4_agents`
  - Ch. 4: building agents with tools.
* - 5a
  - {doc}`labs/Lab-5/lab5a-personalization`
  - Ch. 5: personalization.
* - 5b
  - {doc}`labs/Lab-5/lab5b-troubleshooting`
  - Ch. 5: troubleshooting techniques.
* - 5c
  - {doc}`labs/Lab-5/lab5c-multimodal_agents`
  - Ch. 5: multimodal agents.
```

```{admonition} Running the labs
:class: warning
These notebooks call live Amazon Bedrock endpoints and are rendered here for
reading rather than executed during the book build. Run them in an environment
with AWS credentials and Bedrock model access (for example Amazon SageMaker with
the `conda_python3` kernel), installing each lab's `requirements.txt`.
```
