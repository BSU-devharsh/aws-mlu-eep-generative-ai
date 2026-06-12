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

```{admonition} Running the labs
:class: warning
The notebooks call live Amazon Bedrock endpoints and are rendered here for reading
rather than executed during the book build. Run them in an environment with AWS
credentials and Bedrock model access (for example Amazon SageMaker with the
`conda_python3` kernel), installing the packages in the lab's `requirements.txt`.
Lesson 1 (Evaluating LLMs) has no lab; explore Bedrock's model evaluation feature
in the console instead.
```
