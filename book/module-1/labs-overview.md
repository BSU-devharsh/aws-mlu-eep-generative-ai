---
title: "Module 1 Labs"
---

# Module 1 Labs: Hands-on with Amazon Bedrock

The chapters in this module build the concepts; the labs turn them into working
code on Amazon Bedrock. The notebooks below are the original AWS Machine Learning
University lab notebooks, included here so you can read the code alongside the
theory. Each maps to a lesson you have just studied.

```{list-table}
:header-rows: 1
:widths: 14 40 46

* - Lab
  - Notebook
  - Connects to
* - 2a
  - {doc}`labs/Lab-2/lab2a-introduction-to-amazon-bedrock`
  - Ch. 1-2: calling Bedrock foundation models with Boto3.
* - 2b
  - {doc}`labs/Lab-2/lab2b-chat_amazon_bedrock`
  - Ch. 2: a simple conversational application on a decoder-only model.
* - 3
  - {doc}`labs/Lab-3/lab3-prompt-engineering`
  - Ch. 3: standard prompt-engineering techniques and inference parameters.
* - 4a
  - {doc}`labs/Lab-4/lab4a-Self-consistency`
  - Ch. 4: the self-consistency technique.
* - 4b
  - {doc}`labs/Lab-4/lab4b-Tree-of-Thought`
  - Ch. 4: the tree-of-thought technique.
* - 5
  - {doc}`labs/Lab-5/Lab5-Multimodal`
  - Ch. 5: multimodal prompting with images and text.
```

```{admonition} Expected error: "AccessDeniedException" (model access not enabled)
:class: warning
Some lab cells may display an error like:

    AccessDeniedException: An error occurred (AccessDeniedException) when calling
    the InvokeModel operation: Model access is denied due to IAM user or service
    role is not authorized to perform the required AWS Marketplace actions
    (aws-marketplace:ViewSubscriptions, aws-marketplace:Subscribe) to enable
    access to this model.

This is **not a bug in the lab code**. It means your AWS account or IAM role has
not enabled access to that specific foundation model in Amazon Bedrock. To fix it:
go to the **Amazon Bedrock console -> Model access**, request or enable the model,
make sure your role has the `aws-marketplace:ViewSubscriptions` and
`aws-marketplace:Subscribe` permissions, and re-run the cell after a few minutes.
Model availability and the exact permissions required vary by AWS Region and
account, so consult the Amazon Bedrock documentation for your setup.
```

```{admonition} Running the labs
:class: warning
These notebooks call **live Amazon Bedrock endpoints**, so they are rendered here
for reading but are **not executed** during the book build. To run them, open the
notebook in an environment with AWS credentials and Bedrock model access enabled,
ideally Amazon SageMaker with the `conda_python3` kernel, and install the
packages listed in the labs' `requirements.txt`. Lab 1 is a console walkthrough;
follow it directly in the Amazon Bedrock console.
```

```{admonition} A note on the utilities
:class: note
Several notebooks import helpers from a local `mlu_utils` package (quiz widgets,
prompt helpers, and images). That folder ships alongside the notebooks in this
book so the imports and figures resolve correctly when you open them.
```

Work through the labs in order, reading each lesson's chapter first. When you
finish Lab 5, you will have invoked Bedrock models programmatically, engineered
and tuned prompts, implemented two advanced reasoning techniques, and prompted a
multimodal model, the practical foundation for Modules 2 and 3.
