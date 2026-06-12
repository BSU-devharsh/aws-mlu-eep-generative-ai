---
title: "Alignment with Make America AI-Ready"
---

# Alignment with the U.S. DOL "Make America AI-Ready" Initiative

This book is designed to support **AI literacy** in the spirit of the U.S.
Department of Labor's **Make America AI-Ready** initiative. This chapter maps the
book's content to the initiative's official AI literacy framework, situates it
among recognized AI literacy programs, and provides language useful for faculty
and workforce-development grant proposals.

```{admonition} About this alignment
:class: note
The framework below is summarized from the U.S. Department of Labor's "AI Ready"
page (<https://beta.dol.gov/ai-ready>) as of June 2026. Program descriptions are
summarized from the providers' own pages. Details of government initiatives and
third-party courses change; verify the current specifics before citing them in a
proposal.
```

## What is Make America AI-Ready?

Make America AI-Ready is a free AI literacy course offered by the U.S. Department
of Labor, delivered over one week as short daily text-message lessons (about ten
minutes a day, at no cost, accessible from any phone). According to the
Department, the initiative is "designed to ensure every American worker has the
chance to learn the foundational skills to benefit from AI" (attributed to U.S.
Secretary of Labor Lori Chavez-DeRemer on the DOL page). It is positioned as a
*starting point* that points learners toward further skill-building and AI-related
careers.

The initiative is organized around a **5-pillar AI literacy framework**.

## The five pillars and how this book covers them

```{list-table}
:header-rows: 1
:widths: 26 36 38

* - DOL pillar
  - What it means
  - Where this book develops it
* - **Understand AI Principles**
  - Core concepts, capabilities, and limitations of AI, the foundation for
    effective use.
  - {doc}`ai-and-tools-reference`; Module 1
    {doc}`../module-1/01-introduction-to-generative-ai` and
    {doc}`../module-1/02-foundation-models-and-llms`.
* - **Explore AI Uses**
  - Exploring AI tools and use cases, and how AI complements human expertise.
  - Use-case sections throughout Module 1, and the application patterns in Module 3
    ({doc}`../module-3/index`).
* - **Direct AI Effectively**
  - Providing the right context and writing clear prompts that produce effective
    outputs.
  - Module 1 {doc}`../module-1/03-prompt-engineering` and
    {doc}`../module-1/04-advanced-prompting-techniques`.
* - **Evaluate AI Outputs**
  - Assessing AI results for accuracy and relevance, and iterating on outputs.
  - Module 2 {doc}`../module-2/01-evaluating-llms`; the veracity discussion in
    {doc}`../module-2/03-dimensions-of-responsible-ai`.
* - **Use AI Responsibly**
  - Using AI ethically and securely, protecting information, ensuring
    accountability.
  - {doc}`ai-literacy`; Module 2
    {doc}`../module-2/02-foundations-of-responsible-ai` and
    {doc}`../module-2/04-improving-security-and-safety`.
```

Every pillar of the DOL framework maps onto material in this book, and the book
goes further by adding hands-on Amazon Bedrock labs for each concept. In short,
the DOL course is an on-ramp; this book is the deeper course a learner can take
next.

## The broader AI literacy landscape

AI literacy courses equip learners to understand, evaluate, and responsibly use AI
tools in daily and professional life. They typically focus on practical prompting,
ethical awareness, identifying AI-generated bias, and recognizing limitations such
as hallucinations, all themes this book treats in depth. Recognized programs
include:

```{list-table}
:header-rows: 1
:widths: 30 30 40

* - Program
  - Audience
  - Focus
* - **IBM SkillsBuild, AI Literacy**
  - Students and lifelong learners
  - A free program covering real-world use cases and hands-on business
    problem-solving.
* - **AI Literacy for the Modern Workplace** (Udemy)
  - Non-technical professionals
  - How LLMs work, risk mitigation, and effective prompting.
* - **Digital Education Council, AI Literacy for All**
  - Executives and institutions
  - Foundational knowledge to scale AI learning across disciplines.
* - **LinkedIn Learning, Building AI Literacy**
  - Professionals and teams
  - Curated learning paths to integrate AI into a standard skill set.
```

This book complements those offerings: where many AI literacy courses are
tool-agnostic and conceptual, this book pairs the concepts with a specific,
industry-standard implementation stack (Amazon Bedrock and LangChain) and runnable
labs, making it suitable as a credit-bearing or workforce course rather than only
an awareness module.

### Courses aimed at working professionals

A second tier of programs targets professionals who want practical, no-code AI
skills, generative AI, prompt engineering, and responsible use, without a
technical background:

```{list-table}
:header-rows: 1
:widths: 34 66

* - Program
  - Focus
* - **Google AI Essentials**
  - A practical course on using generative AI in daily workflows, prompt
    generation, and task automation, no technical background required.
* - **Google Prompting Essentials** (Coursera)
  - A short, beginner-friendly specialization on building a library of reusable
    prompts and refining AI tone and output settings for productivity.
* - **IBM, Generative AI: Prompt Engineering Basics** (Coursera)
  - Practical techniques for tailoring AI responses and managing instructions for
    business use cases.
* - **Anthropic, AI Fluency: Framework & Foundations**
  - A structured framework for human-AI collaboration and understanding the
    limitations of current tools.
* - **AI Workflow & Prompt Engineering Certification (SSGI)**
  - A deeper, self-paced certification on designing AI processes that augment
    rather than replace human work.
```

These professional courses emphasize moving beyond basic chat to **structured,
scalable AI integration**, building reusable prompt libraries and setting
inference controls (temperature and context), which this book teaches concretely
in {doc}`../module-1/03-prompt-engineering` and the
{doc}`ai-and-tools-reference`.

#### LinkedIn Learning modules worth noting

LinkedIn Learning's **Building AI Literacy** path (about nine hours) bundles
several practical modules that map directly onto this book's prompting chapters:

- **Prompt Engineering: How to Talk to the AIs** and **Advanced Prompt Engineering
  Techniques**, foundational and advanced prompting, paralleling
  {doc}`../module-1/03-prompt-engineering` and
  {doc}`../module-1/04-advanced-prompting-techniques`.
- **Iterate and refine your prompts**, setting constraints, defining specific
  outputs, and pushing the AI through three to five refinement cycles to remove
  generic, low-effort language, the iterative loop this book stresses, combined
  with the **effort levels** idea from {doc}`ai-and-tools-reference`.
- **Prompt Engineering and AI Agents with ChatGPT**, archiving reusable chats,
  using custom instructions to personalize an AI library, and converting prompts
  into automated workflows, the same habits formalized in
  {doc}`practical-ai-workflow`.

```{admonition} Note
:class: note
These third-party course titles and durations are summarized from the providers'
listings and are mentioned for orientation, not endorsement; confirm current
details on the platform.
```

### A ready-to-adapt course description

For faculty or training leads building a syllabus, the following description and
learning outcomes summarize a no-prerequisite professional AI literacy course that
this book can support end to end.

```{admonition} Sample course description
:class: note
This asynchronous, self-paced course equips professionals across industries with a
clear, practical understanding of artificial intelligence. No technical background
is required. Through real-world examples and hands-on exploration of user-friendly
AI tools, participants learn how AI is transforming the workplace and how to use it
responsibly and effectively. Topics include the fundamentals of AI and machine
learning, automation and augmentation in business, generative AI applications, data
ethics, algorithmic bias, and prompt generation. By the end, professionals can
engage confidently with AI technologies, make informed decisions about their use,
and contribute to responsible AI integration in their organizations.
```

**Learning outcomes.** On completion, a learner will be able to:

- Understand key AI concepts and how they apply in professional settings.
- Identify AI tools relevant to their industry and evaluate their value.
- Recognize the risks, limitations, and ethical considerations of AI use.
- Explore the impact of AI on workforce trends, decision-making, and productivity.
- Build foundational literacy to support informed collaboration with technical
  teams.

Each outcome is supported by this book: the first by the Primer and Module 1; the
second by the tools reference and Module 3 use cases; the third by Module 2; the
fourth by the use-case and "In the news" sections throughout; and the fifth by the
hands-on labs that bridge non-technical learners toward technical collaboration.

```{admonition} For grant and proposal writing
:class: tip
When proposing AI literacy work, you can position this open-source textbook as a
ready-made, standards-aligned curriculum:

- **Framework alignment.** It covers all five pillars of the DOL Make America
  AI-Ready AI literacy framework (Understand, Explore, Direct, Evaluate, Use
  Responsibly), with an explicit mapping (the table above).
- **Open and reusable.** It is released under CC-BY-SA-4.0 (with MIT-0 sample
  code), so institutions can adopt, adapt, and redistribute it at no cost,
  supporting broad workforce access.
- **Hands-on and assessable.** It includes runnable labs and worked examples,
  enabling competency-based assessment rather than awareness-only outcomes.
- **Responsible-AI grounded.** A full module on evaluation, responsible-AI
  dimensions, and security and safety addresses ethics, bias, and accountability
  requirements common in workforce grants.
- **Accessible on-ramp.** It explicitly connects to the free, phone-based DOL
  course as an entry point, supporting learners with limited prior exposure or
  technology access.

State factual claims (dates, dollar amounts, enrollment figures, specific program
features) only after confirming them against current primary sources; this book
deliberately avoids inventing such specifics.
```

## Mapping to ABET student outcomes

For programs seeking or maintaining **ABET** accreditation, this book's activities
support all six **Computing Accreditation Commission (CAC) student outcomes**. The
outcome statements below are summarized; confirm the exact current wording against
the ABET *Criteria for Accrediting Computing Programs*.

```{list-table}
:header-rows: 1
:widths: 8 52 40

* - #
  - ABET CAC student outcome (summarized)
  - Where this book supports it
* - 1
  - Analyze a complex computing problem and apply principles of computing to
    identify solutions.
  - Prompt-engineering and advanced-prompting chapters; RAG and agent design.
* - 2
  - Design, implement, and evaluate a computing-based solution to meet
    requirements.
  - The Module 1-3 labs (Bedrock apps, chatbots, RAG, agents) and worked examples.
* - 3
  - Communicate effectively in a variety of professional contexts.
  - "In the news," worked examples, and the writing/summarization use cases.
* - 4
  - Recognize professional responsibilities and make informed judgments based on
    legal and ethical principles.
  - Module 2 (responsible AI, evaluation, security and safety) and the AI Literacy
    primer (PII, FERPA, HIPAA).
* - 5
  - Function effectively as a member or leader of a team.
  - Team-oriented lab and project use (e.g., shared prompt libraries, evaluation
    work teams in {doc}`../module-2/01-evaluating-llms`).
* - 6
  - Apply computer science theory and software development fundamentals to produce
    computing-based solutions.
  - Foundation-model and transformer theory ({doc}`../module-1/02-foundation-models-and-llms`),
    tokens and embeddings, and the runnable labs.
```

## Mapping to Bloom's taxonomy

The book is structured so learners move up the six levels of the revised **Bloom's
taxonomy**, from recall to creation. Each chapter's "Key takeaways," worked
examples, and labs target progressively higher levels.

```{list-table}
:header-rows: 1
:widths: 18 38 44

* - Bloom level
  - Cognitive activity
  - How the book targets it
* - **Remember**
  - Recall facts and terms.
  - Definitions, the AI and tools reference, and "Key takeaways" summaries.
* - **Understand**
  - Explain ideas and concepts.
  - The theory sections and "How these connect" callouts throughout.
* - **Apply**
  - Use knowledge in new situations.
  - Worked examples and the hands-on Bedrock labs.
* - **Analyze**
  - Draw connections and compare.
  - Comparison tables (fine-tuning vs. RAG, Q&A vs. conversation) and the
    evaluation chapter.
* - **Evaluate**
  - Justify a decision or judge quality.
  - Model-selection guidance, responsible-AI risk assessment, and LLM evaluation.
* - **Create**
  - Produce original work.
  - Capstone labs: building chatbots, RAG systems, agents, and multimodal
    applications.
```

```{admonition} For course and grant proposals
:class: tip
Together, the ABET and Bloom mappings let you show that the curriculum is both
**accreditation-aligned** (ABET CAC outcomes 1-6) and **pedagogically scaffolded**
(Bloom's six levels), alongside the DOL AI-literacy framework alignment above.
Verify ABET outcome wording and any accreditation specifics against current ABET
documents before submission.
```

## Key takeaways

- The DOL **Make America AI-Ready** initiative defines a **5-pillar AI literacy
  framework**: Understand AI Principles, Explore AI Uses, Direct AI Effectively,
  Evaluate AI Outputs, and Use AI Responsibly.
- **Every pillar maps onto this book**, which extends the framework with Amazon
  Bedrock labs and worked examples.
- The book complements established AI literacy programs (IBM SkillsBuild, Udemy,
  the Digital Education Council, and LinkedIn Learning) by adding a concrete,
  hands-on implementation stack.
- Its open license and standards alignment make it well suited to cite in
  faculty and workforce-development grant proposals.
