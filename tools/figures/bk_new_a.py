import os
import sys, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# RAG ingest and query
r = Fig(1100, 560, "Retrieval-augmented generation: index once, then retrieve, augment, generate",
        "Top, indexing: documents are split into overlapping chunks, each chunk is turned into an embedding, and the vectors are stored "
        "in a vector database. Bottom, a query: the user's question is cleaned into a retrieval query, embedded with the same model, "
        "matched by similarity search, optionally reranked, added to the prompt, and the LLM generates a grounded answer.")
r.text(40, 70, "Indexing (once, and on every update)", 15, BLUE, "bold", "start", step=1)
idx = [("document", "Documents", "policies, manuals, logs"), ("checklist", "Chunk", "size, overlap,\nseparators"), ("chip", "Embed", "embedding model"), ("database", "Vector database", "chunk vectors")]
for i, (ic, name, sub) in enumerate(idx):
    x = 110 + i * 250; r.icon(ic, x, 140, 60, name, sub, step=1 + i, label_size=13)
    if i < 3: r.arrow([(x + 40, 140), (x + 206, 140)], None, BLUE, step=2 + i, width=2.4)
r.badge(1, 40, 86, step=1)
r.raw('<line x1="30" y1="250" x2="1070" y2="250" stroke="#d0d6dd" stroke-width="2" stroke-dasharray="6 6"/>')
r.text(40, 282, "Answering a question", 15, GREEN, "bold", "start", step=5); r.badge(5, 24, 276, step=5, color=GREEN)
q = [("user", "Question", "What is the return\npolicy?"), ("search", "Retrieval query", "cleaned, embedded"), ("nodes", "Similarity search", "top-k chunks"),
     ("checklist", "Rerank", "keep the most relevant"), ("document", "Augment", "prompt + chunks"), ("robot", "Generate", "grounded answer")]
for i, (ic, name, sub) in enumerate(q):
    x = 80 + i * 186; r.icon(ic, x, 360, 56, name, sub, step=5 + i, label_size=13)
    if i < 5: r.arrow([(x + 36, 360), (x + 150, 360)], None, GREEN, step=6 + i, width=2.4)
r.arrow([(860, 190), (390, 330)], None, BLUE, step=7, dash=True, width=1.8); r.text(700, 270, "searches the same vector store", 11, BLUE, "bold", step=7)
r.text(550, 530, "Worked example: the bot retrieves Return policy: 15 days after purchase and cites it instead of guessing.", 13, MUTED, italic=True, step=11)
r.save(OUT + "bk_rag")

# Fine-tuning vs RAG
f = Fig(1100, 480, "Fine-tuning changes the model; RAG changes what the model sees",
        "Left: fine-tuning continues training on roughly 100 to 1,000 high-quality examples, updating the weights to create a new, "
        "specialized model; it suits knowledge that changes about yearly and needs re-evaluation for drift. Right: RAG leaves the "
        "weights alone and retrieves current data into the prompt at question time; it suits fast-changing information such as stock "
        "prices.")
f.zone(20, 60, 520, 360, "Fine-tuning", PURPLE, "#f5eef8", step=1); f.badge(1, 522, 76, step=1, color=PURPLE)
f.icon("document", 100, 180, 60, "100 to 1,000 high-", "quality examples", step=1, label_size=12); f.icon("robot", 270, 180, 70, "Base model", step=2)
f.arrow([(132, 180), (226, 180)], "train", PURPLE, step=2, size=12, width=2.4); f.icon("gear", 300, 140, 28, step=2)
f.icon("robot", 440, 180, 70, "New, specialized", "model: weights changed", step=3); f.arrow([(310, 180), (398, 180)], None, PURPLE, step=3, width=2.4)
f.text(280, 330, "+ knowledge lives inside the model", 13, GREEN, "bold", step=3); f.text(280, 352, "- poor for fast-changing data; re-evaluate for drift", 13, RED, "bold", step=3)
f.text(280, 380, "e.g. a virtual tutor trained on course content", 12, MUTED, step=3, italic=True)
f.zone(560, 60, 520, 360, "Retrieval-augmented generation", GREEN, "#eef8ef", step=4); f.badge(4, 1062, 76, step=4, color=GREEN)
f.icon("database", 640, 140, 60, "Current data", step=4, label_size=12); f.icon("document", 780, 220, 50, "prompt + context", step=5, label_size=12)
f.icon("robot", 960, 220, 70, "Same model:", "weights unchanged", step=5); f.arrow([(670, 160), (750, 205)], None, GREEN, step=5, width=2.4); f.arrow([(808, 220), (918, 220)], None, GREEN, step=5, width=2.4)
f.text(820, 330, "+ current or fluctuating data, cites sources", 13, GREEN, "bold", step=6); f.text(820, 352, "- retrieval quality limits the answer", 13, RED, "bold", step=6)
f.text(820, 380, "e.g. is it a good time to buy a company's stock?", 12, MUTED, step=6, italic=True)
f.text(550, 456, "On Bedrock, fine-tuning needs no code: upload training data to S3 and configure the job.", 13, MUTED, italic=True, step=7)
f.save(OUT + "bk_finetune_vs_rag")

# Converse API tool loop
t = Fig(1100, 540, "Tool use with the Converse API: the model proposes, your code decides",
        "Your application sends the conversation and tool definitions to Amazon Bedrock. If the model needs a tool, the response's "
        "stopReason is tool_use with a toolUse block naming the tool and its input. Your code checks the tool is one you offered and "
        "the input is valid, runs it, and returns a toolResult with the same toolUseId. The loop repeats until stopReason is end_turn "
        "and the model answers.")
t.icon("desktop", 140, 210, 100, "Your application", "boto3 converse()")
t.icon("cloud", 900, 190, 150, step=1); t.icon("robot", 900, 184, 54, step=1); t.text(900, 120, "Amazon Bedrock model", 14, INK, "bold", step=1)
t.arrow([(200, 170), (820, 170)], "messages + toolConfig (toolSpec: name, description, inputSchema)", BLUE, step=1, size=12, width=2.6); t.badge(1, 210, 150, step=1)
t.arrow([(820, 206), (200, 206)], "stopReason: tool_use, toolUse {toolUseId, name, input}", ORANGE, step=2, size=12, width=2.6, label_dy=20); t.badge(2, 790, 224, step=2, color=ORANGE)
t.icon("gear", 330, 330, 60, "Run get_weather(city)", step=3, label_size=12); t.icon("shield", 400, 300, 28, step=3)
t.text(420, 296, "check: a tool you offered,", 12, GREEN, "bold", "start", step=3); t.text(420, 312, "and valid input", 12, GREEN, "bold", "start", step=3)
t.arrow([(190, 250), (296, 316)], None, ORANGE, step=3, width=2.4); t.badge(3, 230, 300, step=3, color=ORANGE)
t.arrow([(330, 384), (330, 420), (600, 420), (860, 250)], None, BLUE, step=4, width=2.6); t.text(470, 442, "toolResult {toolUseId, content}", 12, BLUE, "bold", step=4); t.badge(4, 600, 420, step=4)
t.arrow([(950, 250), (950, 400)], None, GREEN, step=5, width=2.6); t.rect(830, 404, 230, 60, "#e8f5e9", GREEN, 1.6, rx=8, step=5)
t.text(945, 428, "stopReason: end_turn", 13, GREEN, "bold", step=5); t.text(945, 448, "final answer", 13, INK, step=5); t.badge(5, 830, 404, step=5, color=GREEN)
t.text(550, 510, "Steps 2 to 4 repeat for as many tool calls as the model needs.", 13, MUTED, italic=True, step=5)
t.save(OUT + "bk_converse_loop")

# Separating initiation from approval
s = Fig(1100, 520, "Separating initiation from approval for an AI agent that handles payments",
        "The accounts-payable agent has a propose_payment tool and no approve tool; it can only queue a payment as pending approval. "
        "Approval runs in a separate service under the approver's own credentials, and the harness, not the model, supplies the "
        "caller's identity. The service checks that the approver is not the initiator, does not share its sponsor, and is a person "
        "above 10,000 dollars. Only then is the payment released.")
s.icon("robot", 110, 200, 90, "AP agent", "sponsor: dana")
s.icon("gear", 330, 200, 70, "propose_payment", "the only payment tool", step=1); s.arrow([(160, 200), (290, 200)], None, BLUE, step=1, width=2.4); s.badge(1, 290, 140, step=1)
s.icon("cross", 110, 330, 30, step=2); s.text(140, 336, "no approve tool", 13, RED, "bold", "start", step=2)
s.icon("checklist", 540, 200, 70, "Queue", "status: pending_approval", step=2); s.arrow([(370, 200), (500, 200)], None, BLUE, step=2, width=2.4); s.badge(2, 500, 140, step=2)
s.zone(640, 60, 430, 300, "Approval service (separate identity)", GREEN, "#eef8ef", step=3); s.badge(3, 1052, 76, step=3, color=GREEN)
s.icon("user", 720, 200, 70, "Approver", "identity from the harness", step=3)
for k, ch in enumerate(["approver is not the initiator", "approver does not share the sponsor", "a person above $10,000"]):
    s.icon("check", 830, 130 + k * 40, 22, step=4); s.text(846, 135 + k * 40, ch, 12, INK, "bold", "start", step=4)
s.badge(4, 810, 104, step=4, color=GREEN); s.arrow([(580, 200), (690, 190)], None, GREEN, step=3, width=2.4)
s.icon("money", 860, 310, 54, step=5); s.text(900, 316, "released", 14, GREEN, "bold", "start", step=5); s.badge(5, 820, 290, step=5, color=GREEN)
s.rect(30, 400, 1040, 90, "#fdecea", RED, 1.6, rx=8, step=6); s.icon("devil", 70, 444, 40, step=6); s.badge(6, 30, 400, step=6, color=RED)
s.text(104, 432, "Injected text that says approve as dana, or a clone of the agent under the same sponsor, gets nowhere:", 13, RED, "bold", "start", step=6)
s.text(104, 456, "the model never supplies the identity, and the independence checks run where approval happens.", 13, RED, "bold", "start", step=6)
s.save(OUT + "bk_approval_separation")
print("ok")
