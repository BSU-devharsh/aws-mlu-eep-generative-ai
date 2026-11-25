import os
import sys, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Threat model of a Bedrock app
t = Fig(1100, 640, "Threat modeling a Bedrock application: one threat and one control per element",
        "A chat front end sends user prompts through Bedrock Guardrails to a model that retrieves from a knowledge base built on an "
        "S3 bucket and calls tools through an agent, with logs and an API endpoint. Prompt: injection, countered by the guardrails "
        "prompt attack filter. Knowledge base documents: poisoning, countered by limiting who can write to the S3 bucket. Model "
        "response: disclosure, countered by sensitive information filters. Tools: excessive agency, countered by least-privilege roles "
        "and separate approval. Logs: repudiation, countered by invocation logging and CloudTrail. API endpoint: denial of service and "
        "runaway cost, countered by quotas and token budgets.")
t.icon("user", 70, 230, 70, "User")
t.icon("browser", 220, 230, 64, "Chat front end", step=1); t.icon("shield", 400, 230, 64, "Guardrails", step=1)
t.icon("robot", 590, 230, 80, "Bedrock model", step=1); t.icon("database", 590, 420, 64, "Knowledge base", "S3 source bucket", step=1)
t.icon("gear", 800, 230, 64, "Agent tools", step=1); t.icon("logbook", 800, 420, 56, "Invocation logs", "CloudTrail", step=1)
for a_, b_ in [((104, 230), (186, 230)), ((254, 230), (366, 230)), ((434, 230), (548, 230)), ((632, 230), (766, 230))]: t.arrow([a_, b_], None, INK, step=1, width=2)
t.arrow([(590, 278), (590, 384)], None, INK, step=1, width=2, both=True); t.arrow([(630, 250), (770, 400)], None, MUTED, step=1, width=1.6, dash=True)
rows = [("User prompt", "prompt injection", "guardrails prompt attack filter", 220, 130),
        ("Knowledge base", "poisoned documents", "restrict writes to the S3 bucket; review", 590, 520),
        ("Model response", "sensitive data disclosure", "sensitive information filters", 590, 130),
        ("Tools", "excessive agency", "least-privilege roles; separate approval", 800, 130),
        ("Logs", "repudiation", "invocation logging and CloudTrail", 800, 520),
        ("API endpoint", "DoS and runaway cost", "quotas, throttling, token budgets", 400, 130)]
pos = {"User prompt": (40, 70), "API endpoint": (300, 70), "Model response": (560, 70), "Tools": (820, 70), "Knowledge base": (380, 500), "Logs": (800, 500)}
for i, (el, thr, ctl, ax, ay) in enumerate(rows):
    x, y = pos[el]; st = 2 + i
    t.rect(x, y, 250, 76 if y < 200 else 80, "#ffffff", RED, 1.6, rx=8, step=st)
    t.text(x + 12, y + 22, el, 13, INK, "bold", "start", step=st); t.icon("devil", x + 22, y + 44, 20, step=st)
    t.text(x + 38, y + 49, thr, 12, RED, "bold", "start", step=st); t.icon("shield", x + 22, y + 64, 18, step=st)
    t.text(x + 38, y + 68, ctl, 11, GREEN, "bold", "start", step=st); t.badge(st, x + 236, y + 12, step=st, color=RED)
t.text(550, 625, "When you add a tool, a data source, or a model, update the threat model in the same change and turn each row into a test.", 12, MUTED, italic=True, step=8)
t.save(OUT + "bk_threat_model")

# ReAct loop
r = Fig(1000, 540, "ReAct: reason, act, observe, until the task is done",
        "An agent receives a task and loops. It reasons with chain of thought to plan the next step, acts by calling a tool such as a "
        "knowledge base, a calculator, a weather API, or a search, observes the result, and feeds it back into its reasoning. The loop "
        "ends with an answer when the task is done.")
cx, cy, R = 500, 290, 170
r.circle(cx, cy, R, "none", "#c5ccd3", 3); r.icon("robot", cx, cy - 6, 90, "Agent", "LLM as reasoning engine")
st = [("Reason", "plan the next step", "search", BLUE), ("Act", "call a tool", "gear", ORANGE), ("Observe", "read the result", "eye", GREEN)]
for i, (name, sub, ic, col) in enumerate(st):
    ang = -90 + i * 120; a = math.radians(ang); x, y = cx + R * math.cos(a), cy + R * math.sin(a)
    r.circle(x, y, 50, "#ffffff", col, 3, step=i + 2); r.icon(ic, x, y - 2, 56, step=i + 2); r.badge(i + 2, x - 38, y - 38, step=i + 2, color=col)
    left = math.cos(a) < -0.1 or ang == -90
    tx = x + (-64 if left else 64); ta = "end" if left else "start"
    r.text(tx, y - 4, name, 17, col, "bold", ta, step=i + 2); r.text(tx, y + 16, sub, 13, INK, anchor=ta, step=i + 2)
    a2, a3 = math.radians(ang + 22), math.radians(ang + 98)
    r.arrow([(cx + R * math.cos(a2), cy + R * math.sin(a2)), (cx + R * math.cos(a3), cy + R * math.sin(a3))], None, col, step=i + 3, width=3)
r.icon("user", 90, 120, 60, "Task", step=1); r.arrow([(130, 120), (330, 160)], None, INK, step=1); r.badge(1, 60, 80, step=1)
tools = [("database", "knowledge base"), ("checklist", "calculator"), ("cloud", "weather API"), ("search", "search")]
for k, (ic, lab) in enumerate(tools): r.icon(ic, 880, 280 + k * 50, 30, step=3); r.text(860, 285 + k * 50, lab, 12, INK, "bold", "end", step=3)
r.icon("check", 160, 440, 44, "Answer when done", step=5); r.arrow([(360, 400), (196, 436)], None, GREEN, step=5, width=2.4); r.badge(5, 120, 410, step=5, color=GREEN)
r.save(OUT + "bk_react")
print("ok")



# Model provenance on AWS: record how a quantized model was built, sign it outside the build, check it before deployment
p = Fig(1180, 600, "Model provenance: record how the files were built, sign it outside the build, check it before use",
        "The verified original model sits in a versioned S3 bucket. An isolated build job quantizes it with a pinned tool and recipe "
        "and writes the quantized files and an in-toto Statement whose SLSA provenance predicate lists the quantized files' digests as "
        "subjects and the original's digests, the tool, and the recipe as resolved dependencies. A separate signer, not the build job, "
        "signs the statement through an AWS KMS key inside a DSSE envelope. S3 stores the files and the envelope. A deployment gate "
        "admits the model only if KMS Verify passes, the file digests match the subjects, and the original is the approved one; a "
        "changed file, a wrong signer, or an unapproved original is refused.")
# 1 source
p.icon("database", 90, 200, 62, "Verified original", "versioned S3 bucket", step=1, label_size=14)
p.badge(1, 46, 150, step=1)
# 2 build platform
p.arrow([(132, 200), (252, 200)], None, INK, step=2)
p.icon("server", 290, 200, 76, "Isolated build job", "pinned tool and recipe", step=2, label_size=14)
p.badge(2, 238, 146, step=2)
# 3 artifact lane
p.arrow([(332, 176), (470, 120)], "files", BLUE, step=3, size=12)
p.icon("document", 530, 112, 56, "Quantized files", "sha256 per file", step=3, label_size=14)
p.badge(3, 490, 78, step=3)
# 4 evidence lane: the in-toto Statement with the SLSA provenance predicate
p.arrow([(300, 290), (414, 372)], None, PURPLE, step=4)
p.text(356, 346, "evidence", 12, PURPLE, "bold", "end", step=4)
p.rect(424, 300, 262, 176, "#f7f2fb", PURPLE, 1.8, rx=10, step=4)
p.text(555, 324, "in-toto Statement", 14, PURPLE, "bold", step=4)
for i, line in enumerate(["subject: quantized files + sha256", "predicateType: SLSA provenance v1",
                          "dependencies: original's digests", "tool version and recipe",
                          "builder.id: the build job"]):
    p.text(438, 350 + i * 24, line, 12.5, INK, anchor="start", step=4)
p.badge(4, 424, 300, step=4, color=PURPLE)
# 5 DSSE envelope around the statement, signed with the platform key
p.rect(404, 270, 302, 230, "none", PURPLE, 2.2, rx=14, step=5, dash=True)
p.icon("key", 690, 284, 40, step=5)
p.badge(5, 414, 518, step=5, color=PURPLE)
p.text(434, 523, "DSSE envelope signed by a separate signer via AWS KMS", 12.5, PURPLE, "bold", "start", step=5)
p.text(434, 543, "the build job has no kms:Sign permission", 12.5, INK, anchor="start", step=5)
# 6 registry keeps the artifact and its attestation together
p.text(772, 168, "Amazon S3", 14, INK, "bold", step=6)
p.text(772, 186, "files + envelope", 12.5, MUTED, step=6)
p.icon("database", 772, 232, 62, step=6)
p.arrow([(562, 112), (730, 214)], None, BLUE, step=6)
p.arrow([(706, 400), (772, 400), (772, 272)], None, PURPLE, step=6)
p.badge(6, 734, 262, step=6)
# 7 deployment gate
p.arrow([(808, 232), (856, 232)], None, INK, step=7)
p.icon("shield", 900, 230, 70, "Deployment gate", None, step=7, label_size=14)
for i, line in enumerate(["KMS Verify passes", "digests match subjects", "original is the approved one"]):
    p.icon("check", 976, 199 + i * 26, 18, step=7)
    p.text(990, 204 + i * 26, line, 12.5, INK, anchor="start", step=7)
p.badge(7, 858, 186, step=7)
# 8 admit, 9 refuse
p.arrow([(935, 196), (1072, 112)], None, GREEN, step=8)
p.text(990, 146, "admit", 12, GREEN, "bold", "end", step=8)
p.icon("server", 1110, 96, 56, "Your own server", None, step=8, label_size=13, label_color=GREEN)
p.badge(8, 1074, 62, step=8, color=GREEN)
p.arrow([(980, 266), (1090, 398)], None, RED, step=9)
p.text(1040, 318, "refuse", 12, RED, "bold", "start", step=9)
p.icon("cross", 1110, 420, 44, "Refused", None, step=9, label_size=13, label_color=RED)
p.text(1110, 478, "changed file,", 12, INK, step=9)
p.text(1110, 494, "wrong signer, or", 12, INK, step=9)
p.text(1110, 510, "unapproved original", 12, INK, step=9)
p.badge(9, 1150, 402, step=9, color=RED)
p.save(OUT + "bk_model_provenance")
