# Generative AI with Amazon Bedrock

Welcome to **Generative AI with Amazon Bedrock**, an online textbook that turns a
hands-on Generative AI curriculum into a structured, readable learning path. The
book moves from the fundamentals of generative models, through the responsible
use of large language models, and on to building real applications with
foundation models. Each chapter pairs theory with worked examples and links
directly to runnable Jupyter lab notebooks that use Amazon Bedrock.

This material is adapted from the AWS Machine Learning University Early Talent
(EEP) Generative AI curriculum. It reorganizes the original slide decks and lab
notebooks into a continuous narrative so that concepts build on one another from
the first page to the last.

## Who this book is for

You will get the most out of this book if you are comfortable reading Python,
have access to an AWS account, and have a basic grounding in machine learning.
None of the chapters assume prior experience with generative AI specifically.
The prerequisites are deliberately light:

- Basic Python programming.
- An AWS account with permissions to use Amazon Bedrock.
- Familiarity with Jupyter notebooks.
- Basic machine learning concepts.
- Light familiarity with natural language processing and computer vision ideas.

## How the book is organized

The book is divided into three modules. Each module contains several chapters of
explanation followed by a set of labs.

```{list-table}
:header-rows: 1
:widths: 18 52 30

* - Module
  - Focus
  - Outcome
* - **Module 1**
  - Fundamentals of Generative AI: foundation models, the transformer
    architecture, prompt engineering, advanced prompting, and multimodal models.
  - Understand how LLMs work and how to prompt them well on Amazon Bedrock.
* - **Module 2**
  - Responsible Generative AI: evaluating LLMs, principles and dimensions of
    responsible AI, security and safety.
  - Evaluate, secure, and responsibly deploy generative models.
* - **Module 3**
  - Building Applications with Foundation Models: LangChain, chatbots, retrieval
    augmented generation, agents, and multimodal applications.
  - Build production-style generative AI applications.
```

```{note}
Module 1 is fully built out in this edition. Modules 2 and 3 are added in
subsequent build batches and will appear in the table of contents as they are
completed.
```

## How to read each chapter

Every chapter follows the same rhythm so you always know where you are:

1. **Why it matters** sets the scene and connects the topic to the previous chapter.
2. **Theory** explains the core ideas, with diagrams and definitions.
3. **AWS in practice** shows how the idea maps to Amazon Bedrock services and tools.
4. **Worked examples** walk through concrete prompts, inputs, and outputs.
5. **In the news** highlights recent developments that put the topic in context.
6. **Hands-on labs** point you to the notebooks where you implement the ideas.
7. **Key takeaways** summarize what to remember before moving on.

## Running the labs

The lab notebooks are designed to run where you have Jupyter configured with AWS
credentials, ideally on Amazon SageMaker using the `conda_python3` kernel, with
Amazon Bedrock model access enabled. Because the labs call live Bedrock
endpoints, they are rendered in this book for reading but are not executed during
the book build. To run them yourself, open the corresponding notebook from the
source repository in your own AWS environment.

```{tip}
Read the chapter for a lesson first, then open its lab. The chapters give you the
vocabulary and mental model that make the lab code easy to follow.
```

Let's begin with the fundamentals.
