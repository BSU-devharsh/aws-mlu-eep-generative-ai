---
title: "Multimodal Prompting"
---

# Chapter 5: Multimodal Prompting

## Why it matters

Every technique so far has worked on text. But the world is not only text. People
perceive through many senses at once and communicate with gestures, expressions,
and images as much as words. **Multimodal** models bring that richness to
generative AI, accepting and relating multiple data types, especially text and
images, so a single model can look at a picture and talk about it. This closing
chapter of Module 1 explains why multimodality matters, what a multimodal LLM is,
how to prompt one, and the use cases it unlocks. It also sets up Module 3, where
multimodal retrieval and agents appear.

## A motivating problem

Imagine a marketing company hired by a pet shop. The shop needs an individual
flyer for each pet, generated from the pet's **image** and a short **bio**. How
would you do this with traditional, single-modality models?

**An image-only model** (computer vision) learns only from images. It can
classify images, detect objects, and segment scenes, so it could sort pets into
"cat" and "dog" classes. But it cannot read the bio text or generate the flyer's
written description.

**A text-only model** learns only from text. It can generate a campaign
description from a written brief, but it cannot see the pet, so it cannot describe
an animal from its photo.

Neither model alone solves the task. You need one system that understands *both*
the image and the text, and that is precisely what a multimodal model provides.

## What "multimodal" means

Humans are naturally multimodal. We perceive the world through vision, hearing,
smell, taste, and touch, and we communicate non-verbally through gestures, facial
expressions, body language, eye contact, and appearance. Multimodality in AI is
an attempt to give models a similarly broad channel to the world.

The motivation is practical: generative AI has shifted from **prediction** to
**interaction**, and handling multiple modalities is a direct way to make AI
better at interacting with people to solve real problems.

### Data modalities

This course focuses mainly on two modalities, and it is worth understanding why.

```{list-table}
:header-rows: 1
:widths: 18 82

* - Modality
  - Why it matters
* - **Image**
  - The most versatile **input** format. There is far more visual data than text
    data, phones and webcams generate it constantly, and images can represent
    text, tabular data, audio (as spectrograms), and to some extent video.
* - **Text**
  - A powerful **output** format. A model that understands and generates text can
    summarize, translate, reason, and answer questions.
```

Other modalities, video, audio, haptic data, and electrical signals, exist too,
but text and image are the focus here.

## Multimodal LLMs

Recall that an LLM is a foundation model trained on text whose core skill is
predicting words in context. A **multimodal LLM (MLLM)** is a large language
model trained on **multiple modalities**.

The common architectural trick is to keep a capable language model at the core
and **equip it with cross-modal capabilities** using **encoders and adapters**.
For example:

- a **vision encoder** converts an image into a representation the language model
  can attend to,
- a **video encoder** does the same for video,
- an **audio encoder** does the same for sound.

In other words, the encoders translate non-text inputs into the same kind of
internal representation, embeddings, that the language model already knows how to
work with. This is the same embedding idea introduced with Titan Embeddings in
Chapter 1, now applied across modalities.

## Prompting multimodal LLMs

Prompting an MLLM combines everything from Chapter 3 with a new set of
considerations for images.

**Text prompts** follow the same best practices as before: clear, specific,
positive, well-structured instructions.

**Image prompts** add format and quality constraints that you must respect or the
model will reject or misread the input:

```{list-table}
:header-rows: 1
:widths: 28 72

* - Consideration
  - Guidance
* - Input format
  - Most MLLMs expect **base64-encoded** images.
* - Image size
  - Stay within size limits (for example, under ~5 MB).
* - Multiple images
  - Most MLLMs can analyze only a limited number of images per request.
* - Image format
  - Use a supported format (jpg, png, etc.).
* - Image clarity
  - Avoid blurry images.
* - Image placement
  - It often works better when the image comes **before** the text.
* - Image resolution
  - Stay within the model's resolution limits.
```

```{admonition} Worked example: the pet-shop flyer, revisited
:class: note
With an MLLM, the pet-shop task becomes a single prompt: supply the pet's photo
(base64-encoded, placed first) followed by a text instruction such as "Using the
image and this bio, write a warm one-paragraph adoption flyer highlighting the
pet's appearance and personality," then the bio text. One model now reads the
image *and* the bio *and* writes the description, the task that defeated both
single-modality models.
```

## Multimodal use cases

Several application patterns recur across industries.

**Visual question answering (VQA).** Give the model both text and an image and ask
about the image, for example, "What is the purpose of the highlighted part in
this circuit board?" The model generates a text description or answers a question
grounded in the picture.

**Text-based image retrieval.** Given a text query, find the images whose
captions, metadata, or embeddings are closest to the query, "find chairs in
stock," returning matching product images. This matters not only for search
engines but for enterprises searching their internal images and documents.

**Deep image similarity retrieval.** Given an image, find similar images, for
example retrieving visually similar Amazon products or identifying other products
from the same manufacturer.

```{admonition} AWS in practice
:class: note
On Amazon Bedrock, multimodal capability shows up in two complementary places.
Multimodal generative models accept images alongside text for tasks like visual
question answering and captioning. Multimodal **embedding** models (in the Titan
family) turn images and text into a shared vector space, which is exactly what
powers the retrieval use cases above and the retrieval-augmented generation you
will build in Module 3.
```

## In the news

Multimodality has become a baseline expectation rather than a special feature.
Leading models now routinely accept images alongside text, and the modality set
keeps widening toward audio and video, moving the field closer to the
multi-sense interaction this chapter described. On AWS, the Titan and newer Nova
model families provide both multimodal understanding and multimodal embeddings,
bringing the patterns here, visual Q&A, image retrieval, and similarity search,
into managed services. As always, consult the
[Amazon Bedrock documentation](https://docs.aws.amazon.com/bedrock/) for the
current multimodal model lineup.

## Hands-on labs

Bring the module to a close with {doc}`labs/Lab-5/Lab5-Multimodal`, which prompts
a multimodal model on Amazon Bedrock using both images and text and explores
visual use cases hands-on.

## Key takeaways

- Single-modality models cannot solve tasks that require both seeing and writing;
  **multimodal** models can.
- An **MLLM** keeps a language model at its core and adds **encoders/adapters** to
  bring images, video, and audio into a shared representation.
- Prompting an MLLM combines text best practices with image constraints (base64
  encoding, size and format limits, clarity, and placement).
- Key use cases are **visual question answering**, **text-based image retrieval**,
  and **image similarity retrieval**, all powered by embeddings.

This completes Module 1. You now understand foundation models and LLMs, the
transformer architecture, prompt engineering from basic to advanced, and
multimodal models, the full toolkit for working with foundation models on Amazon
Bedrock. Module 2 turns to using these models *responsibly*: evaluating them,
applying responsible-AI principles, and improving their security and safety.
