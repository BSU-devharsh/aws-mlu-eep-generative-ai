import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Guardrails flow
g = Fig(1100, 480, "Guardrails sit between users and the model, on the way in and on the way out",
        "A user prompt passes an input guardrail before it reaches the model, and the model's response passes an output guardrail "
        "before it reaches the user. Amazon Bedrock Guardrails applies denied topics, content filters, word filters, and sensitive "
        "information filters for PII the same way across models. Three implementation styles: keyword-based, metric-based with a "
        "classifier and a threshold, and LLM-based with a helper model judging intent. A blocked request gets a refusal or a safer "
        "response.")
g.icon("user", 80, 200, 80, "User")
g.icon("shield", 300, 200, 80, "Input guardrail", step=1); g.icon("robot", 550, 200, 90, "Foundation model", step=2); g.icon("shield", 800, 200, 80, "Output guardrail", step=3)
g.icon("user", 1010, 200, 70, "Response", step=4)
g.arrow([(124, 200), (256, 200)], "prompt", BLUE, step=1, size=12, width=2.4); g.arrow([(344, 200), (500, 200)], "allowed", GREEN, step=2, size=12, width=2.4)
g.arrow([(600, 200), (756, 200)], "draft", BLUE, step=3, size=12, width=2.4); g.arrow([(844, 200), (970, 200)], "safe output", GREEN, step=4, size=12, width=2.4)
g.arrow([(300, 246), (300, 300), (80, 300), (80, 250)], "blocked: refusal or safer reply", RED, step=5, size=12, width=2, dash=True, label_at=.5, label_dy=20)
for n_, x in [(1, 260), (2, 506), (3, 760), (4, 980)]: g.badge(n_, x, 140, step=n_, color=GREEN if n_ in (2, 4) else BLUE)
g.badge(5, 190, 300, step=5, color=RED)
pol = [("Denied topics", "cross"), ("Content filters", "warning"), ("Word filters", "search"), ("PII filters", "idcard")]
g.text(40, 380, "Amazon Bedrock Guardrails policies, applied across models:", 14, INK, "bold", "start", step=6); g.badge(6, 24, 374, step=6)
for k, (lab, ic) in enumerate(pol):
    x = 70 + k * 240; g.icon(ic, x, 420, 30, step=6); g.text(x + 24, 426, lab, 13, INK, "bold", "start", step=6)
g.text(550, 468, "Implementation styles: keyword-based, metric-based (a classifier and a threshold), or LLM-based (a helper model judges intent).", 12, MUTED, italic=True, step=7)
g.save(OUT + "bk_guardrails")

# Verified quantized model pipeline
q = Fig(1100, 500, "Trusting a quantized model: rebuild it from the verified original",
        "Download the lab's signed original into a build environment and verify its Sigstore signature with model_signing. Record "
        "the hash of every file and store the verified files in a versioned S3 bucket that only the build role can write. For Bedrock, "
        "import the verified full-precision files with Custom Model Import, which does not take quantized models. For your own "
        "hardware, quantize in the same isolated build with a pinned tool, write a provenance record, evaluate against the original, "
        "and sign the result; deployment accepts only signed artifacts.")
st = [("certificate", "Lab's signed original", "verify the signature:\nmodel_signing verify"), ("database", "Versioned S3 bucket", "hashes recorded;\nonly the build role writes"),
      ("cloud", "Bedrock: import", "full precision via\nCustom Model Import"), ("gear", "Own hardware: quantize", "pinned tool and settings;\nprovenance record"),
      ("checklist", "Evaluate and sign", "compare with the original,\nsign with your identity")]
pos = [(100, 170), (330, 170), (560, 120), (560, 300), (800, 300)]
for i, ((ic, name, sub), (x, y)) in enumerate(zip(st, pos)):
    q.icon(ic, x, y, 70, name, sub, step=i + 1, label_size=13); q.badge(i + 1, x - 46, y - 46, step=i + 1)
q.arrow([(144, 170), (286, 170)], None, BLUE, step=2, width=2.4); q.arrow([(374, 160), (516, 126)], None, BLUE, step=3, width=2.4)
q.arrow([(374, 185), (516, 290)], None, BLUE, step=4, width=2.4); q.arrow([(604, 300), (756, 300)], None, BLUE, step=5, width=2.4)
q.icon("server", 1010, 300, 70, "Deploy", "signed artifacts only", step=6); q.arrow([(844, 300), (966, 300)], None, GREEN, step=6, width=2.4); q.badge(6, 970, 250, step=6, color=GREEN)
q.icon("attacker", 1000, 110, 50, step=7); q.icon("document", 940, 110, 40, step=7); q.text(970, 160, "a hub quantization nobody verified", 12, RED, "bold", step=7)
q.arrow([(960, 170), (1000, 262)], None, RED, step=7, dash=True); q.icon("cross", 985, 220, 22, step=7); q.badge(7, 1050, 80, step=7, color=RED)
q.text(550, 470, "The lab's signature does not cover quantized files someone else made, so rebuild and sign them yourself.", 13, MUTED, italic=True, step=7)
q.save(OUT + "bk_quantized_pipeline")

# Model API that resists extraction
a = Fig(1100, 460, "A model API that resists extraction: return less, count more",
        "Behind the API the model produces full scores. The public wrapper returns one label to the caller and logs the full scores "
        "internally, so a systematic sweep can be spotted. Each caller has a daily quota, 500 queries in the example; the 501st query "
        "from a scraper returns quota exceeded. In production, API Gateway usage plans enforce per-key throttling and quotas, tied to "
        "verified customers.")
a.icon("user-laptop", 90, 130, 70, "Partner A", step=1); a.icon("attacker", 90, 290, 70, "Scraper B", step=3)
a.icon("shield", 400, 200, 80, "Public wrapper", "one label; quota 500 per day", step=1)
a.icon("robot", 680, 200, 80, "Model", "full scores", step=1); a.arrow([(444, 200), (636, 200)], None, INK, step=1, width=2.2, both=True)
a.icon("logbook", 900, 200, 60, "Internal audit log", "full scores, per caller", step=2); a.arrow([(724, 200), (866, 200)], None, MUTED, step=2, width=2)
a.arrow([(130, 130), (356, 186)], "features", BLUE, step=1, size=12, width=2.4); a.arrow([(356, 150), (130, 96)], "{label: fraud}", GREEN, step=1, size=12, width=2.4, label_dy=-6)
a.badge(1, 160, 80, step=1); a.badge(2, 900, 140, step=2)
a.arrow([(130, 290), (356, 222)], "501 queries", RED, step=3, size=12, width=2.4); a.arrow([(356, 244), (130, 312)], "quota exceeded", RED, step=4, size=12, width=2.4, label_dy=24)
a.badge(3, 160, 250, step=3, color=RED); a.badge(4, 330, 300, step=4, color=RED)
a.rect(500, 330, 570, 100, "#e8f5e9", GREEN, 1.6, rx=8, step=5); a.badge(5, 500, 330, step=5, color=GREEN)
a.text(520, 356, "Do not return logits, exact feature weights, or embeddings to callers.", 13, GREEN, "bold", "start", step=5)
a.text(520, 380, "Use API Gateway usage plans for per-key throttling and quotas,", 13, INK, anchor="start", step=5)
a.text(520, 400, "and tie keys to verified customers.", 13, INK, anchor="start", step=5)
a.save(OUT + "bk_model_api")

# Content Credentials pipeline
c = Fig(1100, 460, "Content Credentials: a signed record that must survive every step of your pipeline",
        "A camera or editing tool signs a C2PA manifest describing where the image came from and how it was edited; in JPEG files it "
        "travels in APP11 segments. An ordinary resize in a publishing pipeline drops those segments without warning, so the published "
        "thumbnail has no credential. Fix each step: preserve the credential, re-sign the result with your own certificate, or use a "
        "service that keeps it.")
st = [("eye", "Capture or edit", "C2PA manifest signed"), ("document", "Signed JPEG", "manifest in APP11"), ("gear", "Resize for a thumbnail", "ordinary image code"),
      ("browser", "Published image", "credential gone")]
for i, (ic, name, sub) in enumerate(st):
    x = 110 + i * 280; col = RED if i == 3 else (ORANGE if i == 2 else BLUE)
    a2 = c.icon(ic, x, 170, 70, name, sub, step=i + 1, label_size=13); c.badge(i + 1, x - 46, 120, step=i + 1, color=col)
    if i < 3: c.arrow([(x + 46, 170), (x + 234, 170)], None, col, step=i + 2, width=2.4)
c.icon("certificate", 420, 120, 32, step=2); c.icon("cross", 950, 120, 26, step=4)
c.text(660, 250, "APP11 segments dropped silently", 13, RED, "bold", step=3)
c.rect(40, 300, 1020, 120, "#e8f5e9", GREEN, 1.6, rx=8, step=5); c.badge(5, 40, 300, step=5, color=GREEN); c.icon("shield", 80, 360, 40, step=5)
c.text(110, 334, "Test every step that touches an image, from upload to the content delivery network, then:", 13, GREEN, "bold", "start", step=5)
for k, t in enumerate(["keep the credential through the step,", "re-sign the result with your own certificate, or", "use a service that preserves Content Credentials."]):
    c.text(130, 360 + k * 20, "- " + t, 13, INK, anchor="start", step=5)
c.save(OUT + "bk_c2pa")

# Bedrock evaluation options
e = Fig(1100, 480, "Four ways to evaluate on Amazon Bedrock",
        "Programmatic evaluation picks a model, a task type, metrics such as accuracy, robustness, and toxicity, and a dataset. Human "
        "evaluation compares up to two models with your own team or an AWS-managed team. LLM-as-a-judge uses a judge model to score "
        "correctness, completeness, faithfulness, and responsible AI metrics. RAG evaluation scores retrieval relevance and coverage, "
        "and generation faithfulness and citations. A judge has biases: position, verbosity, and self-enhancement.")
opts = [("checklist", "Programmatic", "accuracy, robustness,\ntoxicity on a dataset", BLUE), ("group", "Human", "your team or an AWS-\nmanaged work team", "#16a085"),
        ("robot", "LLM-as-a-judge", "correctness, faithfulness,\nharmfulness, custom rubric", PURPLE), ("database", "RAG evaluation", "context relevance and\ncoverage; citations", ORANGE)]
for i, (ic, name, sub, col) in enumerate(opts):
    x = 30 + i * 265; e.card(x, 70, 245, 220, ic, name, sub, col, step=i + 1, icon_size=80, title_size=16); e.badge(i + 1, x + 14, 82, step=i + 1, color=col)
e.rect(30, 320, 1040, 130, "#fff8e1", "#d9a400", 1.6, rx=8, step=5); e.icon("warning", 70, 370, 36, step=5); e.badge(5, 30, 320, step=5, color=ORANGE)
e.text(104, 350, "A judge is a model with biases: it favors the answer shown first, longer answers, and its own family's answers.", 13, INK, "bold", "start", step=5)
e.text(104, 376, "Swap answer order between runs, use a judge from a different model family, and validate its scores", 13, INK, anchor="start", step=5)
e.text(104, 396, "against a sample of human ratings before relying on them.", 13, INK, anchor="start", step=5)
e.text(104, 426, "LLM-as-a-judge and RAG evaluation became generally available on March 20, 2025.", 12, MUTED, anchor="start", step=5, italic=True)
e.save(OUT + "bk_eval_options")
print("ok")
