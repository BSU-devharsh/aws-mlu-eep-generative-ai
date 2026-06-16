---
title: "AI, ML, and AWS AI Services"
---

# AI, ML, and AWS AI Services

Before going deep into generative AI, it helps to place it in the wider AI and
machine-learning landscape and to know the **managed AWS AI services** that solve
common tasks out of the box. This chapter reviews the core definitions and then
tours the AWS services for search, language, speech, documents, and model building.

```{admonition} Verify service details
:class: warning
AWS service features, editions, billing, and Region availability change over time.
The service-fact tables below are a quick reference; confirm specifics in the
current AWS documentation before you design or budget around them.
```

## Core definitions

**Artificial Intelligence (AI)** is the field of computer science devoted to
solving cognitive problems associated with human intelligence, such as learning,
problem-solving, and pattern recognition.

**Machine Learning (ML)** is the science of building algorithms and statistical
models that perform tasks without explicit instructions, relying instead on
patterns and inference learned from data. ML algorithms process large amounts of
historical data, find patterns in it, and use those patterns to predict outcomes
for new inputs. For example, you could train a medical application to flag cancer
in x-ray images by learning from millions of past scans and their diagnoses.

**Generative AI** is a type of AI that creates new content and ideas, including
conversations, stories, images, video, and music. Like all AI it is powered by ML
models, but generative AI specifically uses very large models pre-trained on vast
data, the **foundation models (FMs)** introduced in
{doc}`../module-1/01-introduction-to-generative-ai`. A generative model reuses what
it learned to solve new problems, for example, learning English vocabulary and
then composing a poem. Organizations apply it to digital assistants, media
creation, product design, and more.

```{admonition} The nesting, again
:class: tip
**AI** is the broad field, **ML** is the data-driven subset that learns from
examples, and **generative AI** is the slice of ML built on large foundation
models. AWS offers managed services at each level, from task-specific AI APIs to
full ML platforms.
```

## Intelligent search: Amazon Kendra

**Amazon Kendra** is an ML-powered enterprise search service. Instead of matching
keywords, it understands the **context and meaning** of a query and finds relevant
information across scattered sources, document repositories, SharePoint,
Salesforce, databases, file shares, and more. It learns an organization's own
vocabulary, can answer questions, and can return summaries rather than just a list
of documents, which speeds up finding information and making decisions. It works
using natural language processing (NLP) and ML over your content.

```{list-table} Amazon Kendra at a glance
:header-rows: 1
:widths: 30 70

* - Attribute
  - Detail
* - Billing
  - Billed per hour for each Kendra index.
* - Editions
  - Enterprise Edition and Developer Edition.
* - Infrastructure type
  - Regional
* - Management type
  - Self-managed (service)
* - Service category
  - Machine learning
```

## Text and language: NLP services

**Natural Language Processing (NLP)** is the area of AI focused on analyzing,
understanding, and generating human language. AWS offers several task-specific,
fully managed text and speech services you can call from the console or an API:

```{list-table}
:header-rows: 1
:widths: 26 74

* - Service
  - What it does
* - **Amazon Transcribe**
  - Speech-to-text: converts spoken audio into written text (captions, dictation,
    call transcripts).
* - **Amazon Polly**
  - Text-to-speech: turns written text into lifelike spoken audio.
* - **Amazon Textract**
  - Extracts text, forms, and tables from scanned documents and images (beyond
    simple OCR).
* - **Amazon Translate**
  - Machine translation between languages for fast, scalable localization.
```

These map onto the single-modality tasks in {doc}`ai-literacy` (speech-to-text,
text-to-speech, image-to-text) delivered as managed APIs.

## Conversational interfaces: Amazon Lex

**Amazon Lex** lets you build conversational interfaces, chatbots and voice
assistants, into your applications. It uses the same deep-learning technology
behind Amazon Alexa to provide natural language understanding (NLU) and automatic
speech recognition. You define the conversation flow and language models (the
**intents**), and Lex handles the NLP and speech recognition; when a user speaks
or types, Lex identifies their intent and returns it to your app so it can respond
or act. This makes applications more accessible by letting users interact in
natural language instead of menus and forms.

```{list-table} Amazon Lex at a glance
:header-rows: 1
:widths: 30 70

* - Attribute
  - Detail
* - Billing
  - Pay-as-you-go: charged for speech/text requests, speech intervals, and
    automated chatbot-design training minutes.
* - Infrastructure type
  - Regional
* - Management type
  - Fully managed
* - Service category
  - Machine learning
```

## Document insights: Amazon Comprehend

**Amazon Comprehend** uses NLP to extract insights from text with no preprocessing
required. It analyzes UTF-8 text to recognize entities, key phrases, language,
sentiment, and other elements, so you can scan a document repository for key
phrases, monitor social feeds for product mentions, or discover the topics in a
set of documents. It relies on a continuously trained, pre-trained model, so you
do not supply training data.

Benefits include: powerful NLP through a simple API (no text-analysis expertise
needed), deep-learning-based accuracy that improves as AWS retrains across
domains, and the scale to analyze millions of documents. This is the managed-service
counterpart to the unstructured-text problem many organizations face in retail,
finance, healthcare, and beyond.

```{list-table} Amazon Comprehend at a glance
:header-rows: 1
:widths: 30 70

* - Attribute
  - Detail
* - Billing
  - Charged by the Comprehend option chosen and the type of API call.
* - Infrastructure type
  - Regional
* - Management type
  - Fully managed
* - Service category
  - Machine learning
```

## Building models: SageMaker and Bedrock

Two services anchor ML on AWS, and they sit at different layers:

- **Amazon SageMaker** is the platform for building, training, and deploying your
  own ML models. It provides pre-built algorithms and models as starting points,
  so you can pick one and customize it without being an ML expert.
- **Amazon Bedrock** provides pre-trained **foundation models** through an API,
  which you can fine-tune to your needs without training from scratch. It is the
  backbone of this book; see {doc}`../module-1/01-introduction-to-generative-ai`.

In short: reach for **SageMaker** when you want to build and operate models
yourself, and **Bedrock** when you want to consume and adapt foundation models. The
task-specific services above (Kendra, Lex, Comprehend, Transcribe, Polly, Textract,
Translate) sit one level higher still, ready-made AI for a specific job.

## Key takeaways

- **AI -> ML -> generative AI** is a nesting; AWS has managed services at each
  level.
- **Amazon Kendra** is intelligent, meaning-aware enterprise search.
- **Transcribe, Polly, Textract, Translate** are task-specific NLP/speech/document
  services; **Amazon Lex** builds chatbots and voice assistants; **Amazon
  Comprehend** extracts insights from text.
- **SageMaker** builds and operates custom models; **Bedrock** delivers and
  fine-tunes foundation models.

```{admonition} Attribution
:class: seealso
Service descriptions are summarized from AWS training and documentation. Confirm
current features, editions, and pricing on the official AWS documentation before
relying on them.
```
