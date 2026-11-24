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
