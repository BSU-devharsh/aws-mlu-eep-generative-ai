---
title: "Tokens and Embeddings"
---

# Tokens and Embeddings

Two concepts underpin almost everything in this book: **tokens** (how models read
and write) and **embeddings** (how models represent meaning as numbers). They are
worth understanding in their own right because they explain context limits,
billing, semantic search, and retrieval-augmented generation. This chapter
explains both in detail with worked examples, visualizations, and runnable Python.

```{admonition} Where these appear elsewhere
:class: note
Tokens are introduced in {doc}`../module-1/02-foundation-models-and-llms` (the
context window) and {doc}`../module-1/03-prompt-engineering` (cost). Embeddings
power {doc}`../module-3/03-retrieval-augmented-generation`. This chapter is the
deep dive that both chapters point back to.
```

## Part 1: Tokens

### What is a token?

A **token** is the unit of text a language model actually processes. It is usually
not a whole word and not a single character, but a chunk somewhere in between, a
common word, a word-piece, a punctuation mark, or a space. Models convert text to
tokens (and back) with a **tokenizer**.

A practical rule of thumb for English: **one token is about four characters, and
100 tokens is about 75 words.** Numbers, code, and other languages tokenize
differently, so always measure rather than guess for anything important.

### How tokenization works

Modern LLMs use **subword tokenization** (commonly **Byte-Pair Encoding**, BPE).
The tokenizer starts from characters and merges the most frequent pairs into
larger units, so frequent words become single tokens while rare words split into
pieces. This keeps the vocabulary a fixed, manageable size while still being able
to represent any string.

```{admonition} Worked example: splitting a sentence
:class: note
The sentence **"Tokenization isn't magic."** might tokenize as:

    ["Token", "ization", " isn", "'t", " magic", "."]

Notice: a common word like "magic" is one token (with its leading space), an
unusual boundary like "isn't" splits into `" isn"` + `"'t"`, and the rarer word
"Tokenization" splits into `"Token"` + `"ization"`. That is six tokens for three
words, a reminder that tokens are not words.
```

### Visualizing a tokenized sentence

A simple way to see tokenization is to print each token with its boundary marked.
This snippet uses OpenAI's `tiktoken`, but every provider ships an equivalent.

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")   # a common BPE vocabulary
text = "Tokenization isn't magic."

ids = enc.encode(text)
tokens = [enc.decode([i]) for i in ids]

print(f"{len(text)} characters -> {len(ids)} tokens")
for tok, i in zip(tokens, ids):
    # show whitespace explicitly so boundaries are visible
    print(f"  {repr(tok):<14} id={i}")
```

To *visualize* token counts across several strings (useful for spotting why some
prompts cost more), plot characters versus tokens:

```python
import matplotlib.pyplot as plt
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
samples = [
    "Hello world",
    "Amazon Bedrock",
    "antidisestablishmentarianism",
    "def add(a, b): return a + b",
    "Привет мир",  # non-English uses more tokens
]
chars  = [len(s) for s in samples]
tokens = [len(enc.encode(s)) for s in samples]

plt.figure(figsize=(7, 4))
plt.barh(range(len(samples)), tokens)
plt.yticks(range(len(samples)), samples)
plt.xlabel("Token count")
plt.title("Tokens per string (rare words and non-English cost more)")
plt.tight_layout(); plt.show()
```

### Why tokens matter

- **Context window.** A model's limit (for example, hundreds of thousands of
  tokens) is measured in tokens, not words or characters. Input that exceeds it is
  truncated or must be chunked, the motivation for retrieval-augmented generation.
- **Cost and latency.** APIs bill per token (input plus output), so shorter prompts
  and capped responses cost less and return faster. Counting tokens before sending
  is the simplest cost control.
- **Behavior.** Because models think in tokens, odd tokenization explains quirks
  like miscounting letters in a word or mishandling rare strings.

```python
# A tiny, dependency-light cost estimate.
def estimate_cost(prompt_tokens, completion_tokens,
                  in_rate_per_1k=0.0008, out_rate_per_1k=0.0032):
    return (prompt_tokens/1000*in_rate_per_1k +
            completion_tokens/1000*out_rate_per_1k)

print(f"${estimate_cost(1200, 400):.4f} for a 1200-in / 400-out call")
```

## Part 2: Embeddings

### What is an embedding?

An **embedding** is a list of numbers (a **vector**) that represents the *meaning*
of a piece of data, text, an image, audio, in a way the computer can compare.
The key property: **things with similar meaning have vectors that are close
together**, and dissimilar things are far apart. A modern text-embedding model
might output a vector of hundreds or thousands of numbers per input.

You cannot read meaning off the raw numbers, but you can compare two vectors to
ask "how similar are these?" That single capability powers search, recommendation,
clustering, deduplication, and RAG.

### Measuring similarity: cosine similarity

The standard comparison is **cosine similarity**, the cosine of the angle between
two vectors. It ranges from -1 (opposite) through 0 (unrelated) to 1 (identical
direction). It looks at *direction*, not length, so it is robust to differences in
magnitude.

```{math}
\text{cosine}(a, b) = \frac{a \cdot b}{\lVert a \rVert \, \lVert b \rVert}
```

```python
import numpy as np

def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

# Illustrative 3-D "embeddings" (real ones have hundreds of dimensions).
vecs = {
    "king":   [0.95, 0.10, 0.20],
    "queen":  [0.90, 0.15, 0.25],
    "apple":  [0.10, 0.95, 0.05],
    "banana": [0.12, 0.90, 0.08],
}
print("king~queen :", round(cosine(vecs["king"],  vecs["queen"]),  3))   # high
print("king~apple :", round(cosine(vecs["king"],  vecs["apple"]),  3))   # low
print("apple~banana:", round(cosine(vecs["apple"], vecs["banana"]), 3))  # high
```

The royalty words cluster together and the fruits cluster together, even though no
two vectors are identical, that clustering *is* the semantic information.

### Visualizing an embedding space

Real embeddings have too many dimensions to plot, so you reduce them to 2-D (with
PCA or t-SNE) and scatter them. Similar items land near each other:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

words = ["king", "queen", "prince", "apple", "banana", "grape",
         "car", "truck", "bus"]
# In practice, get these from an embedding model (see below).
emb = np.random.RandomState(0).rand(len(words), 50)  # placeholder vectors

xy = PCA(n_components=2).fit_transform(emb)
plt.figure(figsize=(6, 5))
plt.scatter(xy[:, 0], xy[:, 1])
for (x, y), w in zip(xy, words):
    plt.annotate(w, (x, y), fontsize=9, xytext=(4, 4), textcoords="offset points")
plt.title("Embeddings projected to 2-D (clusters = related meanings)")
plt.tight_layout(); plt.show()
```

```{admonition} Reading the plot
:class: tip
With real embeddings, "king / queen / prince" would form one cluster, the fruits
another, and the vehicles a third, with the gaps between clusters reflecting how
unrelated the groups are. Distance on the plot approximates difference in meaning. (This particular
example uses random vectors solely to demonstrate the plotting mechanics, so the
clusters it shows are not meaningful.)
```

### Getting real embeddings on Amazon Bedrock

In practice you call an embedding model rather than inventing vectors. With Amazon
Titan Embeddings via Bedrock:

```python
import json, boto3

bedrock = boto3.client("bedrock-runtime")

def embed(text, model_id="amazon.titan-embed-text-v2:0"):
    resp = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps({"inputText": text}),
    )
    return json.loads(resp["body"].read())["embedding"]

docs = ["Return policy: 15 days after purchase.",
        "Our office hours are 9am to 5pm.",
        "You can return items within two weeks."]
query = "How long do I have to return something?"

doc_vecs = [embed(d) for d in docs]
q_vec = embed(query)
scores = [cosine(q_vec, dv) for dv in doc_vecs]

best = max(range(len(docs)), key=lambda i: scores[i])
print("Best match:", docs[best])   # the return-policy lines score highest
```

This is the heart of **semantic search** and **RAG**: embed your documents once,
embed each query, and return the documents whose vectors are closest. Unlike
keyword search, it matches *meaning*, so "return something" finds "return policy"
and "return items within two weeks" even with different words. A **vector
database** (see the {doc}`ai-and-tools-reference` chapter) stores these vectors and does
the nearest-neighbor search efficiently at scale.

## How tokens and embeddings relate

They are different stages of the pipeline, do not confuse them:

```{list-table}
:header-rows: 1
:widths: 20 40 40

* - Aspect
  - Tokens
  - Embeddings
* - **What**
  - Discrete pieces of text (IDs from a vocabulary).
  - Continuous vectors capturing meaning.
* - **Purpose**
  - The unit a model reads and writes; the unit of context and billing.
  - Comparing items by meaning (search, RAG, clustering).
* - **Form**
  - Integers (token IDs).
  - Arrays of floats.
* - **You use it for**
  - Counting cost, fitting the context window.
  - Similarity search and retrieval.
```

A useful mental model: text is first **tokenized** into pieces a model can ingest;
internally the model turns each token into a vector and processes them; and a
dedicated **embedding model** can output a single vector for a whole passage that
you compare against others. Tokens are about *processing* text; embeddings are
about *comparing* meaning.

## Key takeaways

- A **token** is the subword unit models read and write; ~4 characters of English or ~0.75
  words each. Tokens define the **context window** and **billing**, so count them.
- Tokenizers use **subword (BPE)** encoding, so rare words split into pieces and
  token count is not word count.
- An **embedding** is a vector representing meaning; **cosine similarity** measures
  how close two embeddings are.
- Embeddings power **semantic search and RAG**: embed documents and queries, then
  retrieve the nearest vectors. Amazon **Titan Embeddings** provides this on
  Bedrock.
```{admonition} Try it
:class: tip
Install `tiktoken`, `numpy`, `scikit-learn`, and `matplotlib`, then run the
snippets above against your own text. Replace the placeholder embedding vectors
with real ones from `embed(...)` to see genuine clusters form.
```
