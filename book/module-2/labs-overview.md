---
title: "Module 2 Labs"
---

# Module 2 Labs: Responsible AI in practice

These notebooks implement the responsible-AI techniques from Module 2 on Amazon
Bedrock. Read each chapter first, then work the lab.

```{list-table}
:header-rows: 1
:widths: 14 44 42

* - Lab
  - Notebook
  - Connects to
* - 2
  - {doc}`labs/Lab-2/lab2-data_protection`
  - Ch. 3: privacy and security, protecting sensitive data.
* - 3
  - {doc}`labs/Lab-3/lab3-robustness`
  - Ch. 3: implementing robustness against noisy and adversarial inputs.
* - 4b
  - {doc}`labs/Lab-4/lab4b-watermarking`
  - Ch. 4: watermarking AI-generated text.
* - 4c
  - {doc}`labs/Lab-4/lab4c-debiasing`
  - Ch. 4: debiasing model outputs.
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
The notebooks call live Amazon Bedrock endpoints and are rendered here for reading
rather than executed during the book build. Run them in an environment with AWS
credentials and Bedrock model access (for example Amazon SageMaker with the
`conda_python3` kernel), installing the packages in the lab's `requirements.txt`.
Lesson 1 (Evaluating LLMs) has no lab; explore Bedrock's model evaluation feature
in the console instead.
```
