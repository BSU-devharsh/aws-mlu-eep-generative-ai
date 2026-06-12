# Module 1: Fundamentals of Generative AI

This first module builds the foundation for everything that follows. By the end
of it you will understand what foundation models and large language models are,
how the transformer architecture made them possible, how to steer them with
careful prompting, and how the same ideas extend from text into images and other
modalities. Throughout, you will see how these capabilities are delivered as a
managed service through Amazon Bedrock.

The module is organized as a continuous arc. We start broad, with the idea of a
model that can generate new content, and progressively sharpen the picture:

```{list-table}
:header-rows: 1
:widths: 8 40 52

* - No.
  - Chapter
  - What you will learn
* - 1
  - {doc}`01-introduction-to-generative-ai`
  - What generative AI is, where LLMs are used, and how Amazon Bedrock exposes
    foundation models through a single API.
* - 2
  - {doc}`02-foundation-models-and-llms`
  - How foundation models differ from traditional ML, the transformer
    architecture and attention, and the practical limits of LLMs.
* - 3
  - {doc}`03-prompt-engineering`
  - The anatomy of a prompt, inference parameters, best practices, and
    in-context (zero-, one-, and few-shot) learning.
* - 4
  - {doc}`04-advanced-prompting-techniques`
  - Chain-of-thought, self-consistency, and tree-of-thought prompting for
    multi-step reasoning.
* - 5
  - {doc}`05-multimodal-prompting`
  - Multimodal LLMs, how to prompt with images, and visual use cases.
```

Each chapter ends by pointing you to the labs in {doc}`labs-overview`, where the
concepts become working Bedrock code.

## How the pieces connect

Generative AI sits on top of **foundation models**: large models pre-trained on
vast data that can be adapted to many tasks. **Large language models** are
foundation models trained on text. The **transformer** is the architecture that
made today's LLMs practical. Once you have a capable model, **prompt
engineering** is how you direct it, and **advanced prompting** squeezes reliable
reasoning out of it. Finally, **multimodal** models extend the same machinery
beyond text to images and more. Keep this chain in mind as you read; every
chapter adds one link.
