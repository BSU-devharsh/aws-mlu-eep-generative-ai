import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# AI concepts map
m = Fig(1100, 660, "How the core AI terms relate",
        "Nested boxes from broadest to narrowest, built from the outside in: artificial intelligence, machine learning, deep learning, "
        "generative AI, foundation models and LLMs, and frontier models. A dashed NLP band cuts across every layer. To the right, agentic "
        "AI is a model placed in a loop with tools, and AGI and superintelligence are hypothetical capability levels that no agreed "
        "test says either has been reached. A note explains how to read the map: each box sits inside a broader one, and NLP spans "
        "rules, classic machine learning, deep learning and LLMs.")
lv = [("Artificial intelligence (AI)", "machines doing tasks that need human-like intelligence", "gear", "#e3eef9"),
      ("Machine learning (ML)", "learns patterns from data, not hand-written rules", "nodes", "#cfe2f5"),
      ("Deep learning (DL)", "many-layer networks that learn their own features", "chip", "#a9cbee"),
      ("Generative AI", "creates new text, images, audio, video or code", "document", "#7fb0e3"),
      ("Foundation models and LLMs", "pretrained broadly, then adapted; LLMs handle language", "code", "#4f8fd6"),
      ("Frontier models", "most capable of the moment, trained with the most compute", "robot", "#1f4e9c")]
for i, (name, sub, ic, fill) in enumerate(lv):
    x0, y0, w, h = 30 + i * 24, 60 + i * 64, 640 - i * 48, 580 - i * 76
    tc = "#ffffff" if i >= 4 else INK
    m.rect(x0, y0, w, h, fill, "#1f4e9c", 1.6, rx=14, step=i + 1)
    m.icon(ic, x0 + 30, y0 + 28, 34, step=i + 1)
    m.text(x0 + 56, y0 + 26, name, 15, tc, "bold", "start", step=i + 1); m.text(x0 + 56, y0 + 44, sub, 11, tc, anchor="start", step=i + 1)
    m.badge(i + 1, x0 + w - 16, y0 + 16, step=i + 1)
m.text(206, 442, "examples change every few months; see Part 2", 11, "#ffffff", anchor="start", step=6, italic=True)
m.rect(560, 70, 86, 556, "#f5b041", "#d68910", 2, rx=12, step=7, opacity=.25, dash=True)
m.rect(566, 84, 74, 34, "#fef5e7", "#d68910", 1, rx=6, step=7); m.text(603, 99, "NLP", 13, "#8a6d1a", "bold", step=7); m.text(603, 112, "cuts across", 10, "#8a6d1a", step=7)
m.badge(7, 566, 84, step=7, color=ORANGE)
m.rect(700, 70, 370, 250, "#e8f8f0", GREEN, 2, rx=12, step=8); m.badge(8, 1056, 86, step=8, color=GREEN)
m.text(720, 98, "Agentic AI: a model in a loop", 15, GREEN, "bold", "start", step=8)
m.icon("robot", 790, 200, 70, step=8)
for k, (ic, lab, ang) in enumerate([("search", "plan", 0), ("gear", "call tools", 1), ("check", "check results", 2), ("nodes", "decide next step", 3)]):
    xx, yy = 960, 140 + k * 44; m.icon(ic, xx - 50, yy, 28, step=8); m.text(xx - 30, yy + 5, lab, 12, INK, "bold", "start", step=8)
m.arrow([(830, 190), (900, 150)], None, GREEN, step=8); m.arrow([(900, 272), (830, 220)], None, GREEN, step=8)
m.text(885, 306, "a way of using models, not a new layer", 12, MUTED, step=8, italic=True)
m.arrow([(500, 420), (698, 250)], None, "#1f4e9c", step=8, width=1.6, dash=True)
m.rect(700, 350, 370, 180, "#fdf2e9", RED, 2, rx=12, step=9, dash=True); m.badge(9, 1056, 366, step=9, color=RED)
m.text(720, 378, "AGI and superintelligence", 15, RED, "bold", "start", step=9)
m.text(720, 404, "hypothetical capability levels, not techniques", 12, INK, anchor="start", step=9)
m.text(720, 430, "AGI: human-level across most intellectual tasks", 12, INK, anchor="start", step=9)
m.text(720, 452, "Superintelligence: far beyond the best humans", 12, INK, anchor="start", step=9)
m.text(720, 470, "in nearly every field", 12, INK, anchor="start", step=9)
m.text(720, 500, "No agreed test says either has been reached.", 12, RED, anchor="start", step=9, italic=True)
m.rect(700, 548, 370, 92, "#f4f6f8", MUTED, 1.2, rx=12, step=10); m.badge(10, 1056, 564, step=10, color=MUTED)
m.text(720, 572, "How to read this map", 13, INK, "bold", "start", step=10)
m.text(720, 594, "Each box sits inside a broader one: every LLM is", 12, INK, anchor="start", step=10)
m.text(720, 612, "deep learning, and every deep-learning model is ML.", 12, INK, anchor="start", step=10)
m.text(720, 630, "NLP spans rules, classic ML, deep learning and LLMs.", 12, INK, anchor="start", step=10)
m.save(OUT + "bk_ai_concepts_map")

# Effort levels
e = Fig(1100, 470, "What changes when you raise the effort level",
        "The same model answers the same prompt at three settings. Low effort: one short thinking step before the answer. Medium: a few "
        "thinking steps and one tool call. High or maximum: many thinking steps, several tool calls, and a self-check before a longer "
        "answer. Waiting time, tokens used, and checking all grow with effort. Illustrative, not to scale.")
rows = [("Low", "quick replies", "T"), ("Medium", "everyday work", "TTTCT"), ("High / Max", "hard, high-stakes work", "TTTTCTTCTTCTS")]
cols = {"T": ("#f5b041", None), "C": ("#48c9b0", "gear"), "S": ("#f1948a", "check")}
for i, (name, sub, seq) in enumerate(rows):
    y = 100 + i * 100; st = i + 1
    e.text(40, y, name, 16, INK, "bold", "start", step=st); e.text(40, y + 18, sub, 12, MUTED, anchor="start", step=st)
    e.icon("user", 230, y, 44, step=st); e.text(230, y + 34, "prompt", 11, MUTED, step=st)
    x = 270
    for ch in seq:
        col, ic = cols[ch]
        e.rect(x, y - 16, 30, 32, col, "#ffffff", 1, rx=5, step=st)
        if ic: e.icon(ic, x + 15, y, 20, step=st)
        x += 34
    e.arrow([(x + 4, y), (x + 40, y)], None, INK, step=st)
    e.rect(x + 44, y - 20, 120 + i * 40, 40, "#1f4e9c", "#1f4e9c", 1, rx=8, step=st); e.text(x + 104 + i * 20, y + 6, "answer", 14, "#ffffff", "bold", step=st)
    e.badge(st, 210, y - 26, step=st)
for k, (col, lab) in enumerate([("#f5b041", "thinking (reasoning tokens)"), ("#48c9b0", "tool call (search, code, file)"), ("#f1948a", "self-check")]):
    e.rect(260 + k * 240, 50, 20, 16, col, col, 1, rx=3); e.text(286 + k * 240, 63, lab, 12, INK, anchor="start")
e.arrow([(1040, 90), (1040, 330)], None, RED, step=4, width=3)
for k, t in enumerate(["longer wait", "more tokens:", "cost and usage", "more checking"]): e.text(1030, 150 + k * 40 - (12 if k == 2 else 0), t, 12, RED, "bold", "end", step=4)
e.badge(4, 1040, 76, step=4, color=RED)
e.text(550, 372, "Same model, same prompt: only the work before and during the answer grows.", 13, INK, "bold", step=5)
e.text(550, 400, "Illustrative, not to scale. Effort changes how much work the model does on this request, not what it knows.", 13, MUTED, italic=True, step=5)
e.text(550, 420, "With adaptive thinking, a high setting on an easy question may still produce little or no thinking.", 13, MUTED, italic=True, step=5)
e.save(OUT + "bk_effort_levels")

# Choose a model and effort level
c = Fig(1100, 520, "Choosing a model and effort level, step by step",
        "Five steps: match the modality, text, image, or audio; match difficulty to effort, starting low and raising it if needed; weigh "
        "cost and context, since a smaller model is often enough; respect privacy and compliance, using an enterprise tier or Amazon "
        "Bedrock for regulated data; then test and iterate on your own examples before deploying. If the model makes reasoning errors, "
        "loop back and raise the effort.")
steps = [("Match the modality", "text, image, or audio?", "eye"), ("Match difficulty to effort", "start low, raise if needed", "gear"),
         ("Weigh cost and context", "smaller is often enough", "money"), ("Privacy and compliance", "regulated data? an enterprise\ntier or Amazon Bedrock", "lock"),
         ("Test and iterate", "compare candidates\non your own examples", "checklist")]
for i, (name, sub, ic) in enumerate(steps):
    x = 30 + i * 212; col = ORANGE if i == 4 else BLUE
    c.card(x, 120, 192, 210, ic, name, sub, col, step=i + 1, icon_size=70, title_size=14); c.badge(i + 1, x + 14, 132, step=i + 1, color=col)
    if i < 4: c.arrow([(x + 194, 225), (x + 210, 225)], None, col, step=i + 2, width=2.6)
c.text(550, 80, "Choose a model and effort", 18, BLUE, "bold", step=1)
c.arrow([(932, 334), (932, 400), (338, 400), (338, 334)], "errors? raise the effort", ORANGE, step=6, dash=True, width=2.4, label_at=.5)
c.badge(6, 470, 400, step=6, color=ORANGE)
c.icon("cloud", 990, 460, 60, step=7); c.text(1020, 466, "Deploy", 16, GREEN, "bold", "start", step=7); c.arrow([(990, 334), (990, 428)], None, GREEN, step=7, width=2.6)
c.badge(7, 950, 440, step=7, color=GREEN)
c.save(OUT + "bk_choose_model")

# ML pipeline
p = Fig(1100, 380, "The supervised machine learning pipeline",
        "Left to right: raw data in rows and columns; exploratory data analysis to explore and clean; feature engineering to impute, "
        "scale, and encode; train the model on the training set; evaluate metrics on the test set; and check fairness for per-group "
        "gaps. A dashed loop returns from evaluation to feature engineering when the metrics are poor.")
st = [("Raw data", "rows and columns", "database"), ("EDA", "explore and clean", "search"), ("Features", "impute, scale, encode", "gear"),
      ("Train model", "fit on the train set", "chip"), ("Evaluate", "metrics on the test set", "checklist"), ("Check fairness", "per-group gaps", "group")]
for i, (name, sub, ic) in enumerate(st):
    x = 95 + i * 182; col = ORANGE if i == 5 else BLUE
    p.circle(x, 150, 56, "#ffffff", col, 3, step=i + 1); p.icon(ic, x, 146, 64, step=i + 1)
    p.text(x, 232, name, 15, col, "bold", step=i + 1); p.text(x, 250, sub, 12, INK, step=i + 1); p.badge(i + 1, x - 46, 104, step=i + 1, color=col)
    if i < 5: p.arrow([(x + 58, 150), (x + 124, 150)], None, col, step=i + 2, width=2.6)
p.arrow([(823, 268), (823, 320), (459, 320), (459, 268)], "iterate: improve features if metrics are poor", ORANGE, step=7, dash=True, width=2.4, label_at=.5)
p.badge(7, 823, 294, step=7, color=ORANGE)
p.save(OUT + "bk_ml_pipeline")
print("ok")
