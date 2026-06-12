---
title: "AI Literacy and Responsible Use"
---

# AI Literacy and Responsible Use

Before working with foundation models on Amazon Bedrock, it helps to be fluent in
the everyday tools and risks of generative AI. Navigating AI responsibly means
understanding what the tools are, how to manage your privacy, and the legal
constraints around sensitive data. Learning how to configure your chat settings,
protect personally identifiable information (PII), and use these platforms
securely is essential for any modern workflow, and especially for educators and
professionals who handle regulated data.

This primer is a practical foundation. It is deliberately platform-focused
(ChatGPT, Gemini, and Claude) because those are the tools most readers touch
daily, and it complements the deeper, architecture-level treatment in Module 1.

```{admonition} A note on accuracy
:class: warning
Consumer AI products change their interfaces and policies frequently. The
settings paths and retention windows below were verified against vendor help
centers and recent privacy reporting at the time of writing, but you should
confirm the current steps in each product's settings before relying on them. AI
responses, including those in this book, may contain mistakes.
```

## Part 1: AI and IT basics

**What is AI?** Artificial Intelligence is a broad branch of computer science
that builds systems capable of performing tasks that normally require human
intelligence, such as learning, reasoning, language understanding, and
problem-solving. It is an umbrella term: machine learning, deep learning, and
generative AI all sit underneath it.

**What is an LLM (large language model)?** An LLM is a specialized type of AI
trained on massive amounts of text. It learns context, grammar, and intent well
enough to predict and generate human-like text, answer questions, and perform
complex writing tasks. Mechanically, an LLM predicts the text most likely to come
next given everything before it, an idea developed in detail in
{doc}`../module-1/02-foundation-models-and-llms`.

**What does "multimodal" mean?** A multimodal AI can process and generate more
than one type of media. Instead of text alone, these models understand and
combine text, images, audio, and sometimes video, either simultaneously or in
sequence. Multimodality is covered hands-on in
{doc}`../module-1/05-multimodal-prompting`.

```{admonition} How these connect
:class: tip
AI is the broad field. An **LLM** is a kind of AI focused on language. A
**multimodal** model is an AI (often built around an LLM) that also handles
images, audio, or video. Keeping this nesting straight prevents most beginner
confusion.
```

## Part 2: Chat management and prompts

### Deleting chats

Removing a conversation from your history is the simplest privacy hygiene step.
The exact controls shift over time, but the current patterns are:

- **ChatGPT:** in the sidebar, open the menu next to a conversation (the three
  dots) and choose **Delete**.
- **Gemini:** in the sidebar, open the menu next to a conversation and choose
  **Delete**. You can also manage **Gemini Apps Activity** in your Google Account
  to auto-delete interactions on a schedule.
- **Claude:** open your **Chats** history, then delete a conversation from its
  menu (hover to reveal the selection control, or open the chat and use its menu).

```{admonition} Deletion is not always instant
:class: note
Deleting a chat removes it from your visible history, but providers typically
retain backend copies for a short period for safety and legal reasons, for
example, Claude states deleted conversations are removed from its backend within
about 30 days. Deletion reduces exposure; it is not a guarantee that data
vanishes immediately.
```

### Saving and reusing prompts

None of the major consumer tools has a perfect prompt library, so people improvise:

- **ChatGPT:** bookmark a chat's URL, or use **Custom Instructions** to persist
  standing guidance across chats.
- **Gemini:** export a useful exchange (for example, to Google Docs) or bookmark
  the conversation.
- **Claude:** there is no dedicated prompt-saving button, so bookmark the chat URL
  or, better, keep your best prompts in a separate document you control.

A simple, durable habit is to maintain your own prompt file (a plain text or
Markdown document) with your most effective, reusable prompts. It is portable
across tools and never breaks when a vendor changes its UI.

## Part 3: Sensitive data, PII, FERPA, and HIPAA

This is the part that matters most professionally. Misusing a consumer AI tool
with regulated data can create real legal exposure.

### Should you put sensitive data or PII into a consumer AI tool?

As a default, **no.** Do not input PII, Social Security numbers, confidential
financial records, unreleased business intellectual property, passwords, or
similar, into standard consumer AI models. Public, consumer-tier models often use
your input to further train their systems unless you have opted out or are on a
contract that forbids it.

```{admonition} Opt out of training where you can
:class: tip
On consumer accounts you can usually turn off model-training on your data. As of
this writing the paths are roughly:

- **ChatGPT:** Settings -> Data Controls -> turn off "Improve the model for
  everyone."
- **Claude:** Settings/Privacy -> turn off "Help improve Claude."
- **Gemini:** turn off Gemini Apps Activity ("Keep Activity").

Even after opting out, providers may retain logs briefly (on the order of days)
to monitor abuse. Note that policies change: confirm your current settings rather
than assuming a default. For genuinely sensitive work, a contractual tier
(business/team/enterprise) that prohibits training on your content is safer than a
single toggle.
```

### FERPA: protecting student data (education)

The Family Educational Rights and Privacy Act (FERPA) restricts disclosure of
protected student information to unvetted third parties. To use AI tools without
violating it:

- **Anonymize first.** Strip names, student IDs, and other direct identifiers
  before any text touches an AI tool.
- **Use an institutional "walled garden."** Prefer tools your institution has
  vetted under an agreement that keeps data private and excludes it from model
  training (for example, an enterprise/education subscription), rather than a
  personal consumer account.

### HIPAA: protecting health data (healthcare)

The Health Insurance Portability and Accountability Act (HIPAA) protects Protected
Health Information (PHI). To stay compliant:

- **Never input PHI** such as patient names, medical record numbers, or specific
  conditions tied to an individual into a general consumer tool.
- **Verify compliance.** Only use AI platforms that will sign a **Business
  Associate Agreement (BAA)** and that run on secure, encrypted infrastructure
  with auditable access logs.

```{admonition} The common thread
:class: note
FERPA and HIPAA differ in the data they protect (student records vs. health
records), but the safe-use recipe is the same: **de-identify the data** and
**use a vetted, contractually bound tool**. A signed agreement (an institutional
walled garden for FERPA, a BAA for HIPAA) is what legally separates "private,
not used for training" from "consumer default."
```

## Part 4: AI for educators

A frequent question: **can educators upload documents to help grade assignments?**
Yes, with a critical condition, **de-identify the documents first**.

- **What you can do:** upload an anonymized rubric, a syllabus, or student work
  with all names and identifiers removed.
- **Best practice:** check whether your institution has an enterprise or education
  subscription (for example, a university-approved enterprise LLM or Copilot
  tenant). These accounts contractually guarantee uploaded documents stay private
  and are not used to train external models, which a personal account does not.

```{admonition} A practical grading workflow
:class: tip
1. Remove names, student IDs, and identifying details from the document.
2. Use an institution-approved, agreement-backed tool, not a personal consumer
   login.
3. Keep the AI's role to drafting feedback against an anonymized rubric; the
   educator makes the final judgment.
4. Never paste a student's identity back into the tool to "personalize" feedback;
   reattach names only in your own private records.
```

## Key takeaways

- **AI** is the broad field; an **LLM** is language-focused AI; a **multimodal**
  model also handles images, audio, or video.
- Know how to **delete chats** and **save prompts**, and remember deletion is not
  always immediate.
- By default, **keep PII and regulated data out** of consumer AI tools, and **opt
  out of training** where the setting exists.
- **FERPA** and **HIPAA** share one safe pattern: **de-identify** the data and use
  a **vetted, contractually bound** tool (walled garden or BAA).
- Educators can use AI for grading support only on **anonymized** material,
  ideally through an **institution-approved** account.

```{admonition} Sources verified for this chapter
:class: seealso
Deletion and opt-out steps were checked against the Claude Help Center and recent
2026 privacy guides; FERPA and HIPAA guidance reflects standard compliance
practice (de-identification, walled-garden agreements, and Business Associate
Agreements). Because vendor settings change often, treat specific menu paths as
starting points and confirm them in the product. Selected references:

- Claude Help Center, "How can I delete or rename a conversation?"
  <https://support.claude.com/en/articles/8230524-how-can-i-delete-or-rename-a-conversation>
- Anthropic Privacy Center, "Can you delete data sent via Claude?"
  <https://privacy.claude.com/en/articles/7996878-can-you-delete-data-sent-via-claude>
- "How to Stop AI from Training on Your Data: The 2026 Privacy Guide"
  <https://felloai.com/how-to-stop-ai-from-training-on-your-data/>
- Amazon Bedrock Documentation (for enterprise, BAA-eligible deployments)
  <https://docs.aws.amazon.com/bedrock/>
```
