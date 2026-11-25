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
