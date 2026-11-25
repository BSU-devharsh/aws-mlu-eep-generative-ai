import os
import sys, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""
TEAL = "#0f766e"


def hcard(p, x, y, w, h, icon, title, sub, color, step, isz=54, tsize=16):
    """A wide card: colored left bar, icon on the left, a bold title and subtitle lines on the right."""
    p.rect(x, y, w, h, "#ffffff", color, 2.2, rx=10, step=step)
    p.rect(x, y, 8, h, color, color, 1, rx=4, step=step)
    p.icon(icon, x + 22 + isz / 2, y + h / 2, isz, step=step)
    tx = x + 34 + isz
    lines = sub.split("\n") if sub else []
    top = y + h / 2 - (len(lines) * 17 + tsize) / 2 + tsize * 0.8
    p.text(tx, top, title, tsize, color, "bold", anchor="start", step=step)
    for i, l in enumerate(lines):
        p.text(tx, top + 20 + i * 17, l, 13, INK, anchor="start", step=step)


def book_roadmap():
    p = Fig(1180, 450, "How the book is organized, from AI literacy to applications on Amazon Bedrock",
            "Five cards run left to right in reading order. The primer covers AI literacy, tools, tokens, and embeddings. "
            "Module 1 covers the fundamentals of large language models and prompting. Module 2 covers responsible AI, "
            "including evaluation and safety. Module 3 covers applications such as retrieval-augmented generation and agents. "
            "Each module ends with labs, which are Jupyter notebooks that send API calls to foundation models on Amazon Bedrock. "
            "The appendices cover traditional machine learning and a serverless backend.")
    cards = [(30, "document", "Primer", "AI literacy, tools,\ntokens, embeddings", MUTED, 1),
             (266, "chip", "Module 1", "Fundamentals,\nLLMs, prompting", BLUE, 2),
             (502, "shield", "Module 2", "Responsible AI,\nevaluation, safety", PURPLE, 3),
             (738, "nodes", "Module 3", "Applications,\nRAG, agents", GREEN, 4),
             (974, "checklist", "Appendices", "Traditional ML,\nserverless backend", ORANGE, 6)]
    for x, ic, t, sub, col, st in cards:
        p.card(x, 64, 176, 160, ic, t, sub, col, step=st, icon_size=62, title_size=17)
        p.badge(st, x + 10, 74, step=st, color=col)
    for i in range(4):
        x0 = cards[i][0] + 176
        st = cards[i + 1][5]
        p.arrow([(x0 + 6, 144), (cards[i + 1][0] - 6, 144)], None, INK, step=st)
    # labs band under modules 1 to 3
    p.zone(266, 282, 648, 150, "Labs in every module: Jupyter notebooks that call Amazon Bedrock", GREEN, "#eef7ee", step=5)
    for x in (354, 590, 826):
        p.arrow([(x, 228), (x, 278)], None, GREEN, step=5, dash=True)
    p.badge(5, 254, 272, step=5, color=GREEN)
    cy = 372
    p.icon("laptop", 380, cy, 54, "Notebook", None, step=5, label_size=14)
    p.arrow([(414, cy), (560, cy)], "API call", GREEN, step=5, size=12)
    p.icon("cloud", 590, cy, 58, "Amazon Bedrock", None, step=5, label_size=14)
    p.arrow([(622, cy), (774, cy)], "invoke", GREEN, step=5, size=12)
    p.icon("robot", 800, cy, 52, "Foundation model", None, step=5, label_size=14)
    p.save(OUT + "bk_book_roadmap")


def aws_ai_choice():
    p = Fig(1100, 500, "Which AWS AI service fits the job, a ready-made service, a foundation model, or your own model",
            "A decision flow. Start with your task and ask whether a ready-made AI service does this exact job. If yes, use a "
            "task-specific service such as Amazon Kendra, Lex, Comprehend, Transcribe, Polly, Textract, or Translate, which need "
            "no training. If no, ask whether a pre-trained foundation model can do it with prompting or fine-tuning. If yes, use "
            "Amazon Bedrock, which offers foundation models from many providers through one API. If no, use Amazon SageMaker AI "
            "to build, train, and deploy your own model, starting from built-in algorithms. Control and effort grow from the top "
            "option to the bottom one.")
    p.icon("user", 80, 116, 58, "Your task", None, step=1, label_size=14)
    p.arrow([(114, 116), (192, 116)], None, INK, step=1)
    p.box(196, 80, 320, 72, "Does a ready-made AI service\ndo this exact job?", step=1, size=15)
    p.badge(1, 44, 76, step=1)
    # yes -> task-specific services
    p.arrow([(516, 116), (636, 116)], "yes", GREEN, step=2)
    hcard(p, 640, 66, 430, 100, "search", "Task-specific AI services", "Kendra, Lex, Comprehend, Transcribe,\nPolly, Textract, Translate; no training", GREEN, 2)
    p.badge(2, 1048, 66, step=2, color=GREEN)
    # no -> question 2
    p.arrow([(356, 152), (356, 226)], None, RED, step=3)
    p.text(368, 194, "no", 13, RED, "bold", anchor="start", step=3)
    p.box(196, 230, 320, 72, "Can a pre-trained foundation\nmodel do it, with prompts or tuning?", step=3, size=15)
    p.arrow([(516, 266), (636, 266)], "yes", GREEN, step=3)
    hcard(p, 640, 216, 430, 100, "cloud", "Amazon Bedrock", "Foundation models from many providers\nthrough one API; prompt, add RAG, or fine-tune", BLUE, 3)
    p.badge(3, 1048, 216, step=3, color=BLUE)
    # no -> SageMaker
    p.arrow([(356, 302), (356, 416), (636, 416)], None, RED, step=4)
    p.text(368, 360, "no", 13, RED, "bold", anchor="start", step=4)
    hcard(p, 640, 366, 430, 100, "gear", "Amazon SageMaker AI", "Build, train, and deploy your own models,\nstarting from built-in algorithms", PURPLE, 4)
    p.badge(4, 1048, 366, step=4, color=PURPLE)
    p.text(196, 486, "Less effort and control at the top, more at the bottom", 13, MUTED, anchor="start", step=4)
    p.save(OUT + "bk_aws_ai_choice")


def tokens_embeddings():
    p = Fig(1180, 470, "Tokens are for processing text, embeddings are for comparing meaning",
            "Two lanes. In the tokens lane, text goes into a tokenizer, which splits it into subword tokens, each mapped to an "
            "integer ID from a vocabulary. A large language model reads and writes these tokens, and its context window and "
            "billing are counted in tokens. In the embeddings lane, a whole passage goes into an embedding model, which returns "
            "one vector of floating-point numbers. The vector is compared with others in a vector index by cosine similarity, "
            "which returns the passages closest in meaning.")
    p.zone(20, 50, 1140, 190, "Tokens: the unit a model reads and writes, and the unit of context and billing", BLUE, "#eef5fc")
    cy = 150
    p.icon("document", 80, cy, 54, "Text", None, step=1, label_size=14)
    p.arrow([(110, cy), (188, cy)], None, BLUE, step=1)
    p.icon("gear", 222, cy, 54, "Tokenizer", None, step=1, label_size=14)
    p.badge(1, 40, 92, step=1)
    p.arrow([(254, cy), (318, cy)], None, BLUE, step=2)
    x = 324
    for t in ["Tok", "ens", " are", " sub", "words"]:
        w = text_width(t, 15) + 22
        p.rect(x, cy - 17, w, 34, "#ffffff", BLUE, 1.8, rx=6, step=2)
        p.text(x + w / 2, cy + 5, t.strip(), 15, INK, step=2)
        x += w + 6
    p.text(438, cy + 44, "each token maps to an integer ID", 13, MUTED, step=2)
    p.badge(2, 318, 104, step=2)
    p.arrow([(x + 4, cy), (676, cy)], None, BLUE, step=3)
    p.icon("robot", 712, cy, 56, "LLM", "reads and writes tokens", step=3, label_size=14)
    p.rect(800, cy - 22, 330, 44, "#ffffff", BLUE, 1.6, rx=6, step=3)
    p.rect(806, cy - 16, 210, 32, "#cfe0f6", "#cfe0f6", 1, rx=4, step=3)
    p.text(911, cy + 5, "prompt + reply", 13, INK, "bold", step=3)
    p.text(965, cy + 46, "context window and cost counted in tokens", 13, MUTED, step=3)
    p.arrow([(748, cy), (796, cy)], None, BLUE, step=3)
    p.badge(3, 668, 104, step=3)
    # Lane B
    p.zone(20, 266, 1140, 190, "Embeddings: one vector per passage, used to compare meaning", GREEN, "#eef7ee")
    cy = 366
    p.icon("document", 80, cy, 54, "Passage", None, step=4, label_size=14)
    p.arrow([(110, cy), (188, cy)], None, GREEN, step=4)
    p.icon("nodes", 222, cy, 54, "Embedding", "model", step=4, label_size=14)
    p.arrow([(254, cy), (318, cy)], None, GREEN, step=4)
    p.rect(324, cy - 20, 252, 40, "#ffffff", GREEN, 1.8, rx=6, step=4)
    p.text(450, cy + 5, "[0.12, -0.53, 0.08, ...]", 15, INK, step=4)
    p.text(450, cy + 44, "one vector of floats", 13, MUTED, step=4)
    p.badge(4, 40, 308, step=4, color=GREEN)
    p.arrow([(580, cy), (676, cy)], None, GREEN, step=5)
    p.icon("database", 712, cy, 56, "Vector index", None, step=5, label_size=14)
    p.arrow([(748, cy), (866, cy)], "cosine similarity", GREEN, step=5, size=12, label_dy=-12)
    p.icon("document", 900, cy, 54, "Closest passages", "by meaning", step=5, label_size=14)
    p.badge(5, 668, 320, step=5, color=GREEN)
    p.save(OUT + "bk_tokens_embeddings")


def ai_workflow():
    p = Fig(1180, 350, "Seven steps that make an assistant do the heavy lifting",
            "Seven cards in a row. Steps 1 to 3 set up the assistant: get a capable assistant, write a master prompt with your "
            "context, and build system prompts that hold your formulas. Steps 4 to 6 make the setup persistent: use project "
            "folders for lasting context, set custom instructions as your defaults, and turn a workflow into a custom assistant. "
            "Step 7 uses AI to improve the setup, and an arrow loops from it back to steps 2 to 6.")
    cards = [("laptop", "Assistant", "a capable\nmodel", BLUE), ("document", "Master prompt", "your\ncontext", BLUE),
             ("checklist", "System prompts", "your\nformulas", BLUE), ("database", "Project folders", "persistent\ncontext", GREEN),
             ("gear", "Instructions", "your\ndefaults", GREEN), ("robot", "Custom assistant", "a workflow,\nsaved", GREEN),
             ("search", "Improve", "AI refines\nyour setup", PURPLE)]
    w, gap, x0, y0 = 144, 22, 20, 96
    for i, (ic, t, sub, col) in enumerate(cards):
        x = x0 + i * (w + gap)
        p.card(x, y0, w, 150, ic, t, sub, col, step=i + 1, icon_size=56, title_size=15)
        p.badge(i + 1, x + 10, y0 + 10, step=i + 1, color=col)
        if i:
            p.arrow([(x - gap + 1, y0 + 75), (x - 1, y0 + 75)], None, INK, step=i + 1, width=1.8)
    # group labels
    for a, b, label, col in [(0, 2, "Set it up", BLUE), (3, 5, "Make it persistent", GREEN), (6, 6, "Improve it", PURPLE)]:
        xa = x0 + a * (w + gap); xb = x0 + b * (w + gap) + w
        p.raw(f'<path d="M{xa+4} 82 L{xa+4} 74 L{xb-4} 74 L{xb-4} 82" fill="none" stroke="{col}" stroke-width="2"/>', step=a + 1)
        p.text((xa + xb) / 2, 66, label, 14, col, "bold", step=a + 1)
    # feedback loop
    x7 = x0 + 6 * (w + gap) + w / 2
    x2 = x0 + 1 * (w + gap) + w / 2
    p.arrow([(x7, y0 + 154), (x7, 316), (x2, 316), (x2, y0 + 154)], "step 7 feeds back into steps 2 to 6", PURPLE, step=7, label_dy=-8)
    p.save(OUT + "bk_ai_workflow")


def data_check():
    p = Fig(1180, 390, "Before you paste, check the data against the tool",
            "A decision flow. Start with the text you want to paste and ask whether it contains personally identifiable "
            "information, student records, or health data. If not, a consumer AI tool is acceptable, after you opt out of model "
            "training in its settings. If it does, first de-identify the text by stripping names, IDs, and record numbers, and "
            "then use only a vetted tool bound by contract, an institutional agreement for student data under FERPA or a signed "
            "Business Associate Agreement for health data under HIPAA.")
    p.icon("document", 80, 136, 56, "Your text", None, step=1, label_size=14)
    p.arrow([(112, 136), (192, 136)], None, INK, step=1)
    p.box(196, 96, 330, 80, "Does it contain PII, student\nrecords, or health data?", step=1, size=15)
    p.badge(1, 52, 100, step=1)
    p.arrow([(526, 136), (676, 136)], "no", GREEN, step=2)
    hcard(p, 680, 86, 470, 100, "laptop", "A consumer tool is acceptable", "after you opt out of model training\nin its settings", GREEN, 2)
    p.badge(2, 1128, 86, step=2, color=GREEN)
    p.arrow([(361, 176), (361, 316), (416, 316)], None, RED, step=3)
    p.text(374, 250, "yes", 13, RED, "bold", anchor="start", step=3)
    hcard(p, 420, 266, 330, 100, "idcard", "De-identify first", "strip names, IDs,\nand record numbers", ORANGE, 3)
    p.badge(3, 728, 266, step=3, color=ORANGE)
    p.arrow([(750, 316), (796, 316)], None, INK, step=4)
    hcard(p, 800, 266, 350, 100, "certificate", "Use a vetted tool", "an institutional agreement (FERPA)\nor a signed BAA (HIPAA)", PURPLE, 4)
    p.badge(4, 1128, 266, step=4, color=PURPLE)
    p.save(OUT + "bk_data_check")


if __name__ == "__main__":
    book_roadmap(); aws_ai_choice(); tokens_embeddings(); ai_workflow(); data_check()
