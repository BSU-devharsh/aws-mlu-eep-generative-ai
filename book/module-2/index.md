# Module 2: Responsible Generative AI

Module 1 gave you a capable model and the skills to prompt it. Module 2 asks the
harder question: how do you know it is any good, and how do you deploy it without
causing harm? Powerful models are also unpredictable ones. They hallucinate,
absorb bias, leak data, and can be manipulated. Using them responsibly is not an
optional extra; it is a core engineering competency.

This module builds responsible AI from the ground up: first how to **evaluate**
models, then the **foundations** and **dimensions** of responsible AI as a
practice, and finally concrete techniques to **improve security and safety**.

```{list-table}
:header-rows: 1
:widths: 8 42 50

* - No.
  - Chapter
  - What you will learn
* - 1
  - {doc}`01-evaluating-llms`
  - Why evaluation is hard, metric- and dataset-based approaches, benchmarks, and
    evaluation on Amazon Bedrock.
* - 2
  - {doc}`02-foundations-of-responsible-ai`
  - What responsible AI is, its dimensions, the design-build-operate lifecycle,
    and how to assess an application's risk.
* - 3
  - {doc}`03-dimensions-of-responsible-ai`
  - The eight dimensions in depth: privacy and security, robustness, veracity,
    fairness and safety, transparency and explainability, governance, and
    controllability.
* - 4
  - {doc}`04-improving-security-and-safety`
  - Jailbreaking and prompt injection, guardrails, watermarking, and debiasing.
```

The arc is deliberate: you cannot manage what you cannot measure (evaluation
first), you cannot act responsibly without a shared framework (foundations and
dimensions), and only then can you apply targeted defenses (security and safety).
The labs in {doc}`labs-overview` make the defenses concrete on Amazon Bedrock.
