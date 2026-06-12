import os, re, sys
from weasyprint import HTML

HTML_ROOT="/tmp/pb/book/_build/html"
ORDER=[
"intro",
"primer/ai-literacy","primer/ai-and-tools-reference","primer/tokens-and-embeddings",
"primer/ten-ai-skills-2025","primer/practical-ai-workflow","primer/make-america-ai-ready",
"module-1/index","module-1/01-introduction-to-generative-ai","module-1/02-foundation-models-and-llms",
"module-1/03-prompt-engineering","module-1/04-advanced-prompting-techniques","module-1/05-multimodal-prompting",
"module-1/labs-overview",
"module-1/labs/Lab-2/lab2a-introduction-to-amazon-bedrock","module-1/labs/Lab-2/lab2b-chat_amazon_bedrock",
"module-1/labs/Lab-3/lab3-prompt-engineering","module-1/labs/Lab-4/lab4a-Self-consistency",
"module-1/labs/Lab-4/lab4b-Tree-of-Thought","module-1/labs/Lab-5/Lab5-Multimodal",
"module-2/index","module-2/01-evaluating-llms","module-2/02-foundations-of-responsible-ai",
"module-2/03-dimensions-of-responsible-ai","module-2/04-improving-security-and-safety","module-2/labs-overview",
"module-2/labs/Lab-2/lab2-data_protection","module-2/labs/Lab-3/lab3-robustness",
"module-2/labs/Lab-4/lab4b-watermarking","module-2/labs/Lab-4/lab4c-debiasing",
"module-3/index","module-3/01-langchain-modules","module-3/02-conversational-applications",
"module-3/03-retrieval-augmented-generation","module-3/04-agents","module-3/05-multimodal-applications",
"module-3/labs-overview",
"module-3/labs/Lab-1/lab1-langchain_modules","module-3/labs/Lab-2/lab2-chatbots",
"module-3/labs/Lab-3/lab3a-retrieval_augmented_generation","module-3/labs/Lab-3/lab3b-multimodal_rag",
"module-3/labs/Lab-4/lab4_agents","module-3/labs/Lab-5/lab5a-personalization",
"module-3/labs/Lab-5/lab5b-troubleshooting","module-3/labs/Lab-5/lab5c-multimodal_agents",
"list-of-figures","about-author","references",
]
CSS="""
@page { size: A4; margin: 1.5cm 1.4cm; @bottom-center{ content: counter(page); font-size:8pt; color:#777; } }
body { font-family: Georgia, serif; font-size:10.5pt; line-height:1.45; color:#1a1a1a; }
h1 { font-size:19pt; color:#154360; border-bottom:2px solid #154360; padding-bottom:3px; }
h2 { font-size:14pt; color:#1A5276; margin-top:1em; } h3{font-size:12pt;color:#21618C;} h4{font-size:10.5pt;color:#2874A6;}
h1,h2,h3,h4{ font-family:Helvetica,Arial,sans-serif; page-break-after:avoid; }
pre,pre.code{ background:#f4f6f8;border:1px solid #dde;border-radius:4px;padding:7px;font-size:8pt;line-height:1.35;white-space:pre-wrap;word-break:break-word;font-family:"DejaVu Sans Mono","Courier New",monospace;page-break-inside:avoid;}
code{ font-family:'DejaVu Sans Mono',monospace;font-size:8pt;}
table{border-collapse:collapse;width:100%;font-size:8.5pt;page-break-inside:avoid;} th,td{border:1px solid #bbb;padding:3px 5px;vertical-align:top;text-align:left;} th{background:#eaf2f8;}
.admonition{border-left:4px solid #2874A6;background:#f7fbfd;padding:5px 9px;margin:8px 0;page-break-inside:avoid;} .admonition-title{font-weight:bold;color:#1A5276;}
img{max-width:100%;} a{color:#1A5276;text-decoration:none;}
.cell_input { border-left:4px solid #2874A6; padding-left:8px; margin-top:8px; }
.cell_input::before { content:"[ IN ]"; display:inline-block; background:#2874A6; color:#fff; font:700 8pt Helvetica,Arial,sans-serif; letter-spacing:1px; padding:2px 7px; border-radius:3px; margin-bottom:3px; }
.cell_output { border-left:4px solid #1E8449; padding-left:8px; margin-top:2px; background:#F4FBF6; }
.cell_output::before { content:"[ OUT ]"; display:inline-block; background:#1E8449; color:#fff; font:700 8pt Helvetica,Arial,sans-serif; letter-spacing:1px; padding:2px 7px; border-radius:3px; margin-bottom:3px; }

"""
start=int(sys.argv[1]); end=int(sys.argv[2])
os.makedirs("/tmp/parts",exist_ok=True)
for i in range(start, min(end,len(ORDER))):
    doc=ORDER[i]; path=os.path.join(HTML_ROOT, doc+".html")
    html=open(path,encoding="utf-8").read()
    m=re.search(r'<article\b[^>]*>(.*?)</article>', html, re.S)
    body=m.group(1) if m else ""
    body=re.sub(r'<script\b.*?</script>','',body,flags=re.S)
    body=re.sub(r'<a class="headerlink".*?</a>','',body,flags=re.S)
    # add italic captions under images that have non-empty alt text
    def _cap(m):
        tag=m.group(0); alt=re.search(r'alt="([^"]*)"',tag)
        if alt and alt.group(1).strip():
            return f'<figure style="text-align:center;margin:10px 0;">{tag}<figcaption style="font-size:8.5pt;color:#555;font-style:italic;margin-top:3px;">{alt.group(1)}</figcaption></figure>'
        return tag
    body=re.sub(r'<img\b[^>]*>', _cap, body)
    # Flatten syntax-highlighted code to plain text so the PDF text layer is clean
    import html as _H
    def _plainpre(m):
        inner=re.sub(r"<[^>]+>","",m.group(1))
        inner=_H.unescape(inner)
        return '<pre class="code">'+_H.escape(inner)+'</pre>'
    body=re.sub(r'<pre\b[^>]*>(.*?)</pre>', _plainpre, body, flags=re.S)

    # Convert MathJax LaTeX (\[..\] display, \(..\) inline) to Unicode for the PDF,
    # but ONLY outside <pre> code blocks (so code regexes are not mangled).
    def _tex(x):
        x=re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1) / (\2)", x)
        for a,b in {r"\cdot":"·",r"\times":"×",r"\div":"÷",
                    r"\lVert":"‖",r"\rVert":"‖",r"\Vert":"‖",r"\|":"‖",
                    r"\leq":"≤",r"\geq":"≥",r"\neq":"≠",r"\approx":"≈",
                    r"\pm":"±",r"\langle":"⟨",r"\rangle":"⟩",
                    r"\quad":"  ",r"\qquad":"    ",r"\,":" ",r"\;":" ",r"\:":" ",r"\!":""}.items():
            x=x.replace(a,b)
        x=re.sub(r"\\(text|mathrm|mathbf|mathit|operatorname)\{([^{}]*)\}", r"\2", x)
        x=re.sub(r"\\[a-zA-Z]+"," ",x)
        x=x.replace("{","").replace("}","")
        return re.sub(r"\s+"," ",x).strip()
    def _math(seg):
        seg=re.sub(r"\\\[(.*?)\\\]", lambda m: '<div style="text-align:center;font-style:italic;margin:8px 0;">'+_tex(m.group(1))+'</div>', seg, flags=re.S)
        seg=re.sub(r"\\\((.*?)\\\)", lambda m: '<i>'+_tex(m.group(1))+'</i>', seg, flags=re.S)
        return seg
    _segs=re.split(r"(<pre\b[^>]*>.*?</pre>)", body, flags=re.S)
    for _i in range(0,len(_segs),2):
        _segs[_i]=_math(_segs[_i])
    body="".join(_segs)
    doc_html=f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    base=os.path.dirname(path)+"/"
    HTML(string=doc_html, base_url=base).write_pdf(f"/tmp/parts/{i:03d}.pdf")
    print(f"  [{i:02d}] {doc}")
print("batch done", start, end)
