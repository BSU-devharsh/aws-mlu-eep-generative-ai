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


def bedrock_api():
    p = Fig(1180, 400, "Amazon Bedrock puts many foundation models behind one managed API",
            "An application on the left sends a request through the AWS SDK to Amazon Bedrock. Inside Bedrock, identity and "
            "access management checks who is calling, the data is encrypted, and prompts and responses are not shared with AWS "
            "or with the model providers. Bedrock routes the request to a foundation model chosen from several providers, and "
            "the response comes back the same way. You can choose a model per task and swap it without rewriting code.")
    p.icon("laptop", 90, 200, 62, "Your application", "AWS SDK or API", step=1, label_size=14)
    p.badge(1, 52, 158, step=1)
    p.arrow([(128, 186), (300, 186)], "request", BLUE, step=2, size=12)
    p.badge(2, 150, 160, step=2)
    p.arrow([(300, 216), (128, 216)], "response", GREEN, step=5, size=12, label_dy=22, label_at=0.62)
    p.badge(5, 270, 238, step=5, color=GREEN)
    p.zone(306, 66, 330, 300, "Amazon Bedrock", BLUE, "#eef5fc", step=3)
    p.icon("cloud", 471, 156, 70, "One API", "for every model", step=3, label_size=14)
    p.icon("key", 370, 290, 38, "IAM checks", "the caller", step=3, label_size=13)
    p.icon("lock", 471, 290, 38, "Encrypted", None, step=3, label_size=13)
    p.icon("shield", 572, 290, 40, "Data stays", "private", step=3, label_size=13)
    p.badge(3, 296, 56, step=3)
    for i, (y, t) in enumerate([(110, "Provider A model"), (200, "Provider B model"), (290, "Provider C model")]):
        p.arrow([(640, 200), (772, y)], None, BLUE, step=4, width=1.8)
        p.icon("robot", 800, y, 50, None, None, step=4)
        p.text(836, y + 5, t, 14, INK, "bold", anchor="start", step=4)
    p.badge(4, 760, 70, step=4)
    p.text(906, 352, "choose a model per task; swap it without rewriting code", 13, MUTED, step=4)
    p.save(OUT + "bk_bedrock_api")


def prompt_anatomy():
    p = Fig(1180, 470, "The parts of a prompt and the knobs that shape the response",
            "On the left, a prompt is built from four parts. The context says the text is a customer email received last week. "
            "The instruction asks the model to summarize the main points. The input is the body of the email. The output format "
            "asks for a bulleted list. The prompt goes to a language model whose inference parameters, temperature, top-p, and "
            "maximum tokens, shape how it generates. The response on the right is a short bulleted list of the email's main points.")
    parts = [("Context", "The following is a customer email received last week.", "#5b9bd5", 1),
             ("Instruction", "Summarize the main points of the email ...", BLUE, 2),
             ("Input", "To whom it may concern: Following up on our last meeting ...", ORANGE, 3),
             ("Output format", "... in a bulleted list.", GREEN, 4)]
    p.rect(26, 62, 540, 380, "#ffffff", "#9aa5b1", 1.6, rx=10)
    p.text(296, 86, "The prompt", 15, INK, "bold")
    for i, (t, ex, col, st) in enumerate(parts):
        y = 104 + i * 84
        p.rect(44, y, 504, 70, "#ffffff", col, 2, rx=8, step=st)
        p.rect(44, y, 8, 70, col, col, 1, rx=4, step=st)
        p.text(92, y + 28, t, 15, col, "bold", anchor="start", step=st)
        p.text(92, y + 52, ex, 13, INK, anchor="start", italic=True, step=st)
        p.badge(st, 70, y + 23, step=st, color=col)
    p.arrow([(570, 210), (684, 210)], None, INK, step=5)
    p.icon("robot", 724, 210, 66, "LLM", None, step=5, label_size=15)
    p.rect(642, 276, 166, 120, "#f7f2fb", PURPLE, 1.6, rx=8, step=5)
    p.text(725, 298, "Inference parameters", 13, PURPLE, "bold", step=5)
    for j, k in enumerate(["temperature", "top-p", "max tokens"]):
        y = 322 + j * 26
        p.text(660, y, k, 13, INK, anchor="start", step=5)
        p.raw(f'<line x1="742" y1="{y-4}" x2="796" y2="{y-4}" stroke="#c9b6dc" stroke-width="4" stroke-linecap="round"/>'
              f'<circle cx="{752 + j * 16}" cy="{y-4}" r="6" fill="{PURPLE}"/>', step=5)
    p.badge(5, 680, 172, step=5, color=PURPLE)
    p.arrow([(772, 210), (870, 210)], None, INK, step=6)
    p.rect(874, 150, 280, 130, "#ffffff", GREEN, 2, rx=8, step=6)
    p.text(1014, 176, "Response", 15, GREEN, "bold", step=6)
    p.text(894, 208, "• Faster production proposed", 13, INK, anchor="start", step=6)
    p.text(894, 232, "• Faster delivery proposed", 13, INK, anchor="start", step=6)
    p.text(894, 256, "• Reply requested", 13, INK, anchor="start", step=6)
    p.badge(6, 884, 140, step=6, color=GREEN)
    p.save(OUT + "bk_prompt_anatomy")


def reasoning_strategies():
    p = Fig(1180, 520, "Chain-of-thought, self-consistency, and tree-of-thought on the same question",
            "Three panels answer the question, when I was 16 my sister was half my age, now I am 42, how old is my sister. In the "
            "chain-of-thought panel the model reasons in one line, sister was 8, the gap is 8 years, 42 minus 8 is 34. In the "
            "self-consistency panel the model samples three reasoning paths that answer 34, 34, and 21, and a majority vote picks "
            "34. In the tree-of-thought panel the model proposes several partial thoughts, rates each one, prunes the weak ones, "
            "expands the most promising, and backtracks when a branch fails, before choosing a final answer.")
    p.text(590, 66, "Question: when I was 16, my sister was half my age; I am 42 now; how old is she?", 14, INK, "bold")
    cols = [(30, "Chain-of-thought", BLUE), (410, "Self-consistency", ORANGE), (790, "Tree-of-thought", GREEN)]
    for x, t, c in cols:
        p.rect(x, 84, 360, 418, "#ffffff", c, 2, rx=10)
        p.text(x + 180, 112, t, 16, c, "bold")
    # CoT
    steps = ["sister was 16 / 2 = 8", "gap = 16 - 8 = 8 years", "42 - 8 = 34"]
    for i, s in enumerate(steps):
        y = 150 + i * 90
        p.box(80, y, 260, 50, s, step=1, size=14)
        if i: p.arrow([(210, y - 40), (210, y - 2)], None, BLUE, step=1)
    p.arrow([(210, 380), (210, 418)], None, BLUE, step=1)
    p.box(140, 420, 140, 44, "Answer 34", step=1, kind="ok", size=14)
    p.badge(1, 46, 126, step=1)
    # Self-consistency
    ans = [("8, gap 8, 42 - 8", "34", GREEN), ("16 - 8 = 8, so 34", "34", GREEN), ("half of 42", "21", RED)]
    for i, (r, a, c) in enumerate(ans):
        x = 428 + i * 112
        p.rect(x, 140, 100, 150, "#fff8ee", ORANGE, 1.6, rx=8, step=2)
        p.text(x + 50, 162, f"path {i+1}", 13, ORANGE, "bold", step=2)
        for k, part in enumerate(r.split(", ")):
            p.text(x + 50, 196 + k * 22, part, 12.5, INK, step=2)
        p.text(x + 50, 274, a, 18, c, "bold", step=2)
        p.arrow([(x + 50, 294), (550 + i * 40, 368)], None, ORANGE, step=3, width=1.8)
    p.badge(2, 426, 126, step=2, color=ORANGE)
    p.box(510, 372, 160, 46, "Majority vote", step=3, size=14)
    p.arrow([(590, 420), (590, 446)], None, ORANGE, step=3)
    p.box(520, 448, 140, 40, "Answer 34", step=3, kind="ok", size=14)
    p.badge(3, 480, 376, step=3, color=ORANGE)
    # ToT
    p.box(910, 136, 120, 40, "Problem", step=4, size=14)
    kids = [(852, "8 years apart", "sure", GREEN), (970, "ages double", "maybe", ORANGE), (1088, "half of 42", "no", RED)]
    for x, t, v, c in kids:
        p.arrow([(970, 178), (x, 224)], None, GREEN, step=4, width=1.8)
        p.rect(x - 54, 228, 108, 54, "#ffffff", c, 1.8, rx=8, step=4)
        p.text(x, 250, t, 12.5, INK, step=4)
        p.text(x, 272, f"rated {v}", 12.5, c, "bold", step=4)
    p.icon("cross", 1088, 302, 22, step=4)
    p.badge(4, 806, 126, step=4, color=GREEN)
    p.arrow([(852, 284), (852, 334)], None, GREEN, step=5)
    p.rect(798, 338, 108, 50, "#ffffff", GREEN, 1.8, rx=8, step=5)
    p.text(852, 360, "she is 8 years", 12.5, INK, step=5)
    p.text(852, 380, "younger", 12.5, INK, step=5)
    p.arrow([(970, 284), (970, 334)], None, ORANGE, step=5, dash=True)
    p.rect(916, 338, 108, 50, "#ffffff", ORANGE, 1.8, rx=8, step=5, dash=True)
    p.text(970, 360, "fails check,", 12.5, INK, step=5)
    p.text(970, 380, "backtrack", 12.5, RED, "bold", step=5)
    p.arrow([(852, 390), (852, 444)], None, GREEN, step=5)
    p.box(797, 446, 110, 40, "Answer 34", step=5, kind="ok", size=14)
    p.text(1042, 466, "expand the best,", 13, MUTED, step=5)
    p.text(1042, 484, "prune the rest", 13, MUTED, step=5)
    p.badge(5, 806, 318, step=5, color=GREEN)
    p.save(OUT + "bk_reasoning_strategies")


def mllm():
    p = Fig(1180, 460, "A multimodal LLM keeps a language model at its core and adds encoders for other inputs",
            "On the left are three non-text inputs, an image, a video, and an audio clip. Each goes through its own encoder, a "
            "vision encoder, a video encoder, and an audio encoder, and an adapter maps the result into embeddings that the "
            "language model already works with. The text prompt is split into tokens and embedded the same way. The language "
            "model at the center attends over all of these embeddings together and generates a text answer.")
    rows = [(130, "camera", "Image", "Vision encoder"), (230, "videocall", "Video", "Video encoder"), (330, "headset", "Audio", "Audio encoder")]
    for y, ic, t, enc in rows:
        p.icon(ic, 80, y, 50, t, None, step=1, label_size=13)
        p.arrow([(110, y), (166, y)], None, BLUE, step=1)
        p.box(170, y - 26, 170, 52, enc, step=1, size=14)
        p.arrow([(340, y), (396, y)], None, BLUE, step=2)
        p.box(400, y - 22, 120, 44, "Adapter", step=2, size=14, kind="plain")
        p.arrow([(520, y), (642, 230 + (y - 230) * 0.4)], None, BLUE, step=2)
    p.badge(1, 40, 82, step=1)
    p.badge(2, 392, 82, step=2)
    p.icon("document", 80, 414, 44, None, None, step=3)
    p.text(108, 418, "Text prompt, split into tokens", 13, INK, "bold", anchor="start", step=3)
    p.arrow([(318, 414), (700, 414), (700, 324)], None, GREEN, step=3)
    p.badge(3, 300, 386, step=3, color=GREEN)
    p.rect(646, 136, 220, 188, "#eef5fc", BLUE, 2.4, rx=12, step=4)
    p.icon("robot", 756, 196, 62, None, None, step=4)
    p.text(756, 262, "Language model", 16, BLUE, "bold", step=4)
    p.text(756, 284, "attends over shared", 13, INK, step=4)
    p.text(756, 302, "embeddings", 13, INK, step=4)
    p.badge(4, 656, 146, step=4)
    p.arrow([(866, 230), (952, 230)], None, GREEN, step=5)
    p.rect(956, 180, 200, 100, "#ffffff", GREEN, 2, rx=8, step=5)
    p.text(1056, 210, "Text answer", 15, GREEN, "bold", step=5)
    p.text(1056, 236, "describes, reads, or", 13, INK, step=5)
    p.text(1056, 256, "reasons about the input", 13, INK, step=5)
    p.badge(5, 966, 170, step=5, color=GREEN)
    p.save(OUT + "bk_mllm")


if __name__ == "__main__" and "m1" in sys.argv:
    bedrock_api(); prompt_anatomy(); reasoning_strategies(); mllm()


def grounding_check():
    p = Fig(1180, 420, "Checking that an answer is grounded in its source, and abstaining when it is not",
            "A user asks what the fee is, and the source document says the fee is 2 percent. The model drafts an answer that "
            "says 3 percent, an intrinsic hallucination because it contradicts the source. A contextual grounding check in "
            "Amazon Bedrock Guardrails takes the source, the query, and the response and scores the response for grounding and "
            "relevance. If both scores meet the thresholds you set, the answer is returned. If either falls below its threshold, "
            "the response is blocked and the system abstains, by declining, asking a clarifying question, or handing off to a person.")
    p.icon("user", 80, 120, 56, "Question", "What is the fee?", step=1, label_size=14)
    p.icon("document", 80, 300, 54, "Source", "the fee is 2 percent", step=1, label_size=14)
    p.badge(1, 30, 70, step=1)
    p.arrow([(112, 120), (200, 196)], None, INK, step=2)
    p.arrow([(112, 300), (200, 226)], None, INK, step=2)
    p.icon("robot", 240, 210, 62, "Model", None, step=2, label_size=14)
    p.arrow([(276, 210), (336, 210)], None, INK, step=2)
    p.rect(340, 174, 190, 72, "#fdecea", RED, 1.8, rx=8, step=2)
    p.text(435, 202, "Draft answer", 14, RED, "bold", step=2)
    p.text(435, 226, "the fee is 3 percent", 13, INK, step=2)
    p.badge(2, 214, 150, step=2)
    p.arrow([(530, 210), (592, 210)], None, INK, step=3)
    p.rect(596, 130, 260, 160, "#f7f2fb", PURPLE, 2, rx=10, step=3)
    p.icon("shield", 640, 170, 46, step=3)
    p.text(756, 166, "Contextual", 14, PURPLE, "bold", step=3)
    p.text(756, 184, "grounding check", 14, PURPLE, "bold", step=3)
    p.text(726, 226, "grounding score vs threshold", 13, INK, step=3)
    p.text(726, 248, "relevance score vs threshold", 13, INK, step=3)
    p.text(726, 274, "thresholds from 0 to 0.99", 12, MUTED, step=3)
    p.badge(3, 606, 120, step=3, color=PURPLE)
    p.arrow([(856, 150), (930, 150)], "both pass", GREEN, step=4, size=12)
    hcard(p, 934, 76, 226, 92, "check", "Return", "the grounded\nanswer", GREEN, 4, isz=40)
    p.badge(4, 1140, 76, step=4, color=GREEN)
    p.arrow([(856, 270), (930, 270)], "either fails", RED, step=5, size=12)
    p.rect(934, 230, 226, 150, "#ffffff", RED, 2.2, rx=10, step=5)
    p.rect(934, 230, 8, 150, RED, RED, 1, rx=4, step=5)
    p.text(958, 260, "Block and abstain", 16, RED, "bold", anchor="start", step=5)
    for i, t in enumerate(["decline the request", "ask a clarifying question", "hand off to a person"]):
        p.text(958, 292 + i * 26, "• " + t, 13, INK, anchor="start", step=5)
    p.badge(5, 1140, 230, step=5, color=RED)
    p.text(435, 330, "An intrinsic hallucination contradicts", 13, MUTED, step=2)
    p.text(435, 348, "the source; an extrinsic one adds", 13, MUTED, step=2)
    p.text(435, 366, "claims the source cannot support.", 13, MUTED, step=2)
    p.save(OUT + "bk_grounding_check")


def nist_rmf():
    p = Fig(1180, 490, "The NIST AI Risk Management Framework, Govern across Map, Measure, and Manage",
            "Govern sits in the center as a culture of risk management, with policies, accountability, roles, and oversight that "
            "cut across the other three functions. Around it, Map establishes the context and identifies risks, Measure analyzes, "
            "assesses, and tracks those risks with quantitative and qualitative methods, and Manage prioritizes and acts on them "
            "with mitigations such as guardrails and oversight, and monitors over time. Arrows run from Map to Measure to Manage "
            "and back to Map, because the cycle repeats as the system and its risks change.")
    cx, cy = 590, 250
    p.circle(cx, cy, 96, "#eef5fc", BLUE, 2.6, step=1)
    p.icon("checklist", cx, cy - 40, 50, step=1)
    p.text(cx, cy + 14, "Govern", 20, BLUE, "bold", step=1)
    p.text(cx, cy + 38, "policies, roles,", 13, INK, step=1)
    p.text(cx, cy + 56, "accountability, oversight", 13, INK, step=1)
    p.badge(1, cx - 78, cy - 78, step=1)
    cards = [(120, 120, "nodes", "Map", "set the context and\nidentify risks", GREEN, 2),
             (830, 120, "search", "Measure", "analyze, assess, and\ntrack risks", ORANGE, 3),
             (475, 412, "shield", "Manage", "mitigate, prioritize,\nand monitor", PURPLE, 4)]
    for x, y, ic, t, sub, col, st in cards:
        hcard(p, x, y - 46, 230, 92, ic, t, sub, col, st, isz=44)
        p.badge(st, x + 212, y - 46, step=st, color=col)
    p.arrow([(352, 84), (826, 84)], None, INK, step=3)
    p.arrow([(946, 168), (946, 412), (707, 412)], None, INK, step=4)
    p.arrow([(473, 412), (234, 412), (234, 170)], "repeat as risks change", INK, step=4, label_at=0.3, label_dy=20)
    for x, y in [(352, 120), (830, 120), (590, 354)]:
        pass
    p.raw(f'<path d="M352 140 L498 210" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="5 5" fill="none"/>'
          f'<path d="M828 140 L682 210" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="5 5" fill="none"/>'
          f'<path d="M590 346 L590 364" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="5 5" fill="none"/>', step=4)
    p.save(OUT + "bk_nist_rmf")


def rai_dimensions():
    p = Fig(1180, 560, "The eight dimensions of responsible AI",
            "A hub labeled responsible AI connects to eight cards. Controllability means mechanisms to monitor and steer system "
            "behavior. Privacy and security means obtaining, using, and protecting data and models appropriately. Safety means "
            "preventing harmful output and misuse. Fairness means considering the impact on different groups of stakeholders. "
            "Veracity and robustness means correct output even with unexpected or adversarial input. Explainability means "
            "understanding and evaluating outputs. Transparency means helping stakeholders make informed choices about using the "
            "system. Governance means best practices across the AI supply chain, for providers and deployers alike.")
    import math
    cx, cy = 590, 300
    dims = [("gear", "Controllability", "monitor and steer\nbehavior", BLUE),
            ("lock", "Privacy and security", "protect data\nand models", BLUE),
            ("shield", "Safety", "prevent harmful output\nand misuse", GREEN),
            ("group", "Fairness", "weigh the impact\non every group", GREEN),
            ("check", "Veracity, robustness", "correct output, even\non unexpected input", ORANGE),
            ("search", "Explainability", "understand and\nevaluate outputs", ORANGE),
            ("eye", "Transparency", "let people make\ninformed choices", PURPLE),
            ("checklist", "Governance", "best practices across\nthe supply chain", PURPLE)]
    w, h = 262, 92
    pos = []
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4
        pos.append((cx + 410 * math.cos(a), cy + 196 * math.sin(a)))
    for i, ((x, y), (ic, t, sub, col)) in enumerate(zip(pos, dims)):
        p.raw(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#b8c2cc" stroke-width="2"/>', step=i + 1)
    p.circle(cx, cy, 78, "#ffffff", INK, 2.4)
    p.text(cx, cy - 4, "Responsible", 17, INK, "bold")
    p.text(cx, cy + 18, "AI", 17, INK, "bold")
    for i, ((x, y), (ic, t, sub, col)) in enumerate(zip(pos, dims)):
        hcard(p, x - w / 2, y - h / 2, w, h, ic, t, sub, col, i + 1, isz=42, tsize=15)
        p.badge(i + 1, x - w / 2 + w - 16, y - h / 2, step=i + 1, color=col)
    p.save(OUT + "bk_rai_dimensions")


if __name__ == "__main__" and "m2" in sys.argv:
    grounding_check(); nist_rmf(); rai_dimensions()


def langchain_chain():
    p = Fig(1180, 470, "A LangChain chain written with LCEL, and the memory that carries context between calls",
            "The top row is the chain prompt_template piped into llm piped into StrOutputParser. Input variables, content type "
            "bedtime story and topic a cat, fill the prompt template to make the prompt, tell me a bedtime story about a cat. "
            "A chat model on Amazon Bedrock generates a reply, and the output parser turns it into a plain string. The bottom row "
            "shows memory. Before a call, the application retrieves the conversation history from memory and adds it to the "
            "prompt. After the call, it writes the new exchange back to memory, so the next call knows what came before.")
    p.rect(30, 62, 1120, 40, "#f4f6f8", "#9aa5b1", 1.2, rx=6)
    p.text(590, 88, "chain = prompt_template | llm | StrOutputParser()", 16, INK, "bold")
    cy = 196
    p.rect(30, cy - 44, 170, 88, "#ffffff", MUTED, 1.6, rx=8, step=1)
    p.text(115, cy - 18, "Input variables", 13, MUTED, "bold", step=1)
    p.text(115, cy + 6, "content_type:", 12.5, INK, step=1)
    p.text(115, cy + 24, "bedtime story; topic: a cat", 11.5, INK, step=1)
    p.arrow([(200, cy), (246, cy)], None, INK, step=1)
    hcard(p, 250, cy - 50, 240, 100, "document", "Prompt template", "Tell me a {content_type}\nabout {topic}.", BLUE, 1, isz=40)
    p.badge(1, 470, cy - 50, step=1)
    p.arrow([(490, cy), (556, cy)], None, INK, step=2)
    hcard(p, 560, cy - 50, 230, 100, "robot", "Chat model", "on Amazon Bedrock\ngenerates a reply", PURPLE, 2, isz=40)
    p.badge(2, 770, cy - 50, step=2, color=PURPLE)
    p.arrow([(790, cy), (856, cy)], None, INK, step=3)
    hcard(p, 860, cy - 50, 290, 100, "gear", "Output parser", "StrOutputParser returns\nOnce upon a time, ...", GREEN, 3, isz=40)
    p.badge(3, 1130, cy - 50, step=3, color=GREEN)
    # memory row
    p.rect(250, 300, 540, 150, "#fff8ee", ORANGE, 2, rx=10, step=4)
    p.text(776, 436, "Memory: the model itself is stateless", 14, ORANGE, "bold", anchor="end", step=4)
    p.icon("database", 330, 394, 50, "Conversation history", None, step=4, label_size=13)
    p.arrow([(330, 368), (330, 252)], "retrieve and add\nto the prompt", ORANGE, step=4, size=12, label_dy=6, label_anchor="start")
    p.badge(4, 240, 296, step=4, color=ORANGE)
    p.arrow([(675, 252), (675, 394), (362, 394)], "write the new exchange", ORANGE, step=5, size=12, label_at=0.78, label_dy=-10)
    p.badge(5, 690, 276, step=5, color=ORANGE)
    p.save(OUT + "bk_langchain_chain")


def chat_turn():
    p = Fig(1180, 470, "One chatbot turn with a response cache, conversation memory, and prompt caching",
            "A user message first goes to a response cache. On a hit, which suits deterministic questions, the cached answer "
            "returns at once. On a miss, the application builds the prompt from a long system prompt marked as a cached prefix, "
            "the recent conversation held in memory, either the last k turns or a running summary, and the new message. The "
            "Bedrock Converse API returns the reply, reading the cached prefix more cheaply. The application then writes the "
            "exchange to memory and stores the reply in the cache with an expiry time.")
    p.icon("user", 70, 150, 56, "User", "new message", step=1, label_size=14)
    p.arrow([(102, 150), (196, 150)], None, INK, step=1)
    p.badge(1, 30, 100, step=1)
    hcard(p, 200, 104, 230, 92, "memory", "Response cache", "same question asked\nbefore? check here", ORANGE, 2, isz=40)
    p.badge(2, 410, 104, step=2, color=ORANGE)
    p.arrow([(316, 104), (316, 74), (70, 74), (70, 116)], "hit: return the cached answer", GREEN, step=2, size=12, label_at=0.5)
    p.arrow([(316, 196), (316, 252)], None, RED, step=3)
    p.text(328, 230, "miss", 13, RED, "bold", anchor="start", step=3)
    p.rect(150, 256, 420, 170, "#ffffff", BLUE, 2, rx=10, step=3)
    p.text(170, 282, "Prompt", 15, BLUE, "bold", anchor="start", step=3)
    rows = [("System prompt, long and fixed", "cached prefix (cachePoint)", "#cfe0f6"),
            ("Memory: last k turns or a summary", "keeps the window small", "#ffe8cc"),
            ("New user message", "changes every turn", "#e6f4e6")]
    for i, (a, b, col) in enumerate(rows):
        y = 296 + i * 42
        p.rect(170, y, 380, 34, col, col, 1, rx=5, step=3)
        p.text(182, y + 22, a, 13, INK, "bold", anchor="start", step=3)
        p.text(540, y + 22, b, 12, MUTED, anchor="end", step=3)
    p.badge(3, 140, 246, step=3)
    p.arrow([(570, 340), (694, 340)], None, INK, step=4)
    p.icon("cloud", 726, 330, 66, "Bedrock", "Converse API", step=4, label_size=14)
    p.text(726, 270, "reads the cached prefix", 12, MUTED, step=4)
    p.text(726, 286, "at a lower cost", 12, MUTED, step=4)
    p.badge(4, 680, 300, step=4, color=PURPLE)
    p.arrow([(776, 330), (856, 330)], "reply", INK, step=5, size=12)
    hcard(p, 860, 280, 290, 100, "database", "Write back", "exchange into memory;\nreply into the cache, with expiry", GREEN, 5, isz=40)
    p.badge(5, 1130, 280, step=5, color=GREEN)
    p.arrow([(1005, 280), (1005, 150), (434, 150)], None, GREEN, step=5, dash=True)
    p.save(OUT + "bk_chat_turn")


def multimodal_agent():
    p = Fig(1180, 440, "A multimodal agent that looks at a photo, retrieves the manual, and walks the user through a fix",
            "A user sends a photo of a broken device and asks how to fix it. The agent reasons about the request with the "
            "ReAct pattern. It calls an image tool, a multimodal model that describes what the photo shows, and a retrieval tool "
            "that searches a knowledge base of manuals with multimodal embeddings and returns the matching manual page. The "
            "agent reasons over both results and answers with step-by-step instructions.")
    p.icon("user-laptop", 80, 210, 64, "User", "photo + question", step=1, label_size=14)
    p.badge(1, 36, 150, step=1)
    p.arrow([(118, 210), (226, 210)], None, INK, step=1)
    p.rect(230, 130, 250, 160, "#eef5fc", BLUE, 2.2, rx=12, step=2)
    p.icon("robot", 300, 196, 58, step=2)
    p.text(400, 180, "Agent", 17, BLUE, "bold", step=2)
    p.text(400, 204, "reasons with", 13, INK, step=2)
    p.text(400, 222, "ReAct", 13, INK, "bold", step=2)
    p.text(355, 270, "reason, act, observe, repeat", 12, MUTED, step=2)
    p.badge(2, 240, 140, step=2)
    p.arrow([(480, 170), (626, 110)], "call", PURPLE, step=3, size=12)
    hcard(p, 630, 60, 290, 96, "eye", "Image tool", "a multimodal model describes\nthe damage in the photo", PURPLE, 3, isz=42)
    p.badge(3, 900, 60, step=3, color=PURPLE)
    p.arrow([(480, 250), (626, 310)], "call", ORANGE, step=4, size=12, label_dy=22)
    hcard(p, 630, 264, 290, 96, "database", "Retrieval tool", "multimodal RAG over manuals\nreturns the right page", ORANGE, 4, isz=42)
    p.badge(4, 900, 264, step=4, color=ORANGE)
    p.arrow([(920, 108), (1053, 108), (1053, 174)], None, PURPLE, step=5, dash=True)
    p.arrow([(920, 312), (1053, 312), (1053, 246)], None, ORANGE, step=5, dash=True)
    p.rect(946, 178, 214, 64, "#e8f5e9", GREEN, 1.8, rx=8, step=5)
    p.text(1053, 206, "Step-by-step fix", 14, GREEN, "bold", step=5)
    p.text(1053, 228, "answer to the user", 12, INK, step=5)
    p.badge(5, 940, 172, step=5, color=GREEN)
    p.text(590, 410, "On AWS: multimodal models in Amazon Bedrock, Bedrock Knowledge Bases for retrieval, and Bedrock Agents to orchestrate", 13, MUTED)
    p.save(OUT + "bk_multimodal_agent")


if __name__ == "__main__" and "m3" in sys.argv:
    langchain_chain(); chat_turn(); multimodal_agent()


def serverless_backend():
    p = Fig(1180, 420, "A free serverless backend, a Lambda Function URL in front of a DynamoDB table",
            "The figure follows the five steps of the appendix. A DynamoDB table named TodoTable with partition key id uses "
            "provisioned capacity of 5 read and 5 write units. An IAM role named LambdaTodoRole gives the function table access "
            "and CloudWatch logging. A Lambda function named TodoHandler reads and writes the table. A Lambda Function URL with "
            "CORS exposes the function over HTTPS; its auth type NONE makes it public, so a real system should use AWS_IAM or "
            "API Gateway. A client tests it with curl, sending POST to add a task and GET to list tasks.")
    cy = 180
    hcard(p, 870, cy - 60, 280, 120, "database", "DynamoDB table", "TodoTable, key id\nprovisioned 5 RCU, 5 WCU", BLUE, 1, isz=46)
    p.badge(1, 1130, cy - 60, step=1)
    p.rect(560, 290, 260, 88, "#ffffff", PURPLE, 2, rx=10, step=2)
    p.icon("idcard", 600, 334, 44, step=2)
    p.text(632, 322, "IAM role", 15, PURPLE, "bold", anchor="start", step=2)
    p.text(632, 344, "LambdaTodoRole: table", 12.5, INK, anchor="start", step=2)
    p.text(632, 362, "access, CloudWatch logs", 12.5, INK, anchor="start", step=2)
    p.badge(2, 800, 290, step=2, color=PURPLE)
    hcard(p, 560, cy - 60, 260, 120, "code", "Lambda function", "TodoHandler, Python\nreads and writes tasks", ORANGE, 3, isz=46)
    p.badge(3, 800, cy - 60, step=3, color=ORANGE)
    p.arrow([(690, 288), (690, 244)], None, PURPLE, step=3)
    p.text(700, 272, "assumes", 12, PURPLE, "bold", anchor="start", step=3)
    p.arrow([(820, cy), (866, cy)], None, INK, step=3, both=True)
    p.rect(300, cy - 60, 210, 120, "#ffffff", GREEN, 2, rx=10, step=4)
    p.icon("lock", 340, cy, 40, step=4)
    p.text(370, cy - 18, "Function URL", 15, GREEN, "bold", anchor="start", step=4)
    p.text(370, cy + 4, "HTTPS, CORS on", 12.5, INK, anchor="start", step=4)
    p.text(370, cy + 24, "auth NONE is public", 12.5, RED, anchor="start", step=4)
    p.badge(4, 490, cy - 60, step=4, color=GREEN)
    p.arrow([(510, cy), (556, cy)], None, INK, step=4)
    p.icon("laptop", 100, cy, 60, "Client", "curl or a web page", step=5, label_size=14)
    p.arrow([(136, cy - 14), (296, cy - 14)], "POST a task", INK, step=5, size=12)
    p.arrow([(296, cy + 14), (136, cy + 14)], "GET all tasks", INK, step=5, size=12, label_dy=24)
    p.badge(5, 60, cy - 70, step=5)
    p.text(40, 370, "For real use, switch to AWS_IAM auth or", 13, MUTED, anchor="start")
    p.text(40, 388, "API Gateway, and scope the role to one table.", 13, MUTED, anchor="start")
    p.save(OUT + "bk_serverless_backend")


if __name__ == "__main__" and "m4" in sys.argv:
    serverless_backend()


def agent_breaker():
    p = Fig(1180, 492, "Where the ten Agent Breaker attacks enter an agent, and where to stop them",
            "An agent in the center combines a model with tools. On the left, an attacker types into the chat directly, the "
            "path used against Cycling Coach, Solace AI, Thingularity, and CorpConnect Messenger. Above and below, six indirect "
            "paths carry the attack inside content the agent reads: a web page for Trippy Planner, an uploaded PDF for "
            "PortfolioIQ Advisor, a memory entry for MindfulChat, a repository rules file for Curs-ed CodeReview, an MCP tool "
            "description for OmniChat Desktop, and a retrieved court filing for Clause AI. On the right are the results the "
            "attacks aim for: a leaked prompt or tool list, profanity, a phishing link, a wrong recommendation, malicious code, "
            "or an email sent for the attacker. A shield on the path out stands for the defenses: check untrusted text before "
            "the model reads it, ask a person to confirm actions, and give tools the least privilege they need.")
    cx, cy = 590, 262
    p.rect(480, 192, 220, 140, "#eef5fc", BLUE, 2.4, rx=12)
    p.icon("robot", 530, cy - 8, 56)
    p.text(632, cy - 14, "Agent", 17, BLUE, "bold")
    p.text(632, cy + 10, "model + tools", 13, INK)
    p.icon("attacker", 100, cy, 58, "Chat (direct)", None, step=1, label_size=14, label_color=RED)
    p.text(100, cy + 64, "Cycling Coach, Solace AI,", 12, MUTED, step=1)
    p.text(100, cy + 80, "Thingularity, CorpConnect", 12, MUTED, step=1)
    p.arrow([(134, cy), (476, cy)], "typed by the attacker", RED, step=1, size=12)
    p.badge(1, 62, cy - 42, step=1, color=RED)
    top = [(330, "browser", "Web page", "Trippy Planner", (520, 188)),
           (590, "document", "Uploaded PDF", "PortfolioIQ Advisor", (590, 188)),
           (850, "memory", "Memory entry", "MindfulChat", (660, 188))]
    bot = [(330, "code", "Rules file", "Curs-ed CodeReview", (520, 336)),
           (590, "gear", "Tool description", "OmniChat Desktop", (590, 336)),
           (850, "database", "Retrieved filing", "Clause AI", (660, 336))]
    n = 2
    for x, ic, t, app, end in top:
        p.icon(ic, x, 92, 46, None, None, step=n)
        p.text(x + 32, 88, t, 14, ORANGE, "bold", anchor="start", step=n)
        p.text(x + 32, 106, app, 12, MUTED, anchor="start", step=n)
        p.arrow([(x, 118), end], None, ORANGE, step=n, width=1.8)
        p.badge(n, x - 34, 70, step=n, color=ORANGE)
        n += 1
    for x, ic, t, app, end in bot:
        p.icon(ic, x, 432, 46, None, None, step=n)
        p.text(x + 32, 428, t, 14, ORANGE, "bold", anchor="start", step=n)
        p.text(x + 32, 446, app, 12, MUTED, anchor="start", step=n)
        p.arrow([(x, 406), end], None, ORANGE, step=n, width=1.8)
        p.badge(n, x - 34, 410, step=n, color=ORANGE)
        n += 1
    p.text(1004, 150, "Indirect: the attack hides in content the agent reads", 12.5, ORANGE, "bold", anchor="middle")
    p.rect(928, 186, 232, 152, "#fdecea", RED, 2, rx=10, step=8)
    p.text(1044, 210, "What the attacks aim for", 13.5, RED, "bold", step=8)
    for i, t in enumerate(["leaked prompt or tool list", "profanity", "phishing link in a plan",
                           "wrong recommendation", "malicious code, rogue email"]):
        p.text(944, 236 + i * 20, "• " + t, 12.5, INK, anchor="start", step=8)
    p.arrow([(704, cy), (924, cy)], None, RED, step=8)
    p.icon("shield", 814, cy, 44, step=8)
    p.text(814, cy + 40, "check untrusted text,", 12, GREEN, "bold", step=8)
    p.text(814, cy + 56, "confirm actions,", 12, GREEN, "bold", step=8)
    p.text(814, cy + 72, "least privilege", 12, GREEN, "bold", step=8)
    p.badge(8, 784, cy - 46, step=8, color=GREEN)
    p.save(OUT + "bk_agent_breaker")


if __name__ == "__main__" and "m5" in sys.argv:
    agent_breaker()
