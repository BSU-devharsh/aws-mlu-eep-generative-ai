from weasyprint import HTML
LOGO="/tmp/pb/book/_build/html/_static/MLU-NEW-logo.png"
import os
logo_tag = f'<img src="file://{LOGO}" style="height:70px;margin-bottom:18px;"/>' if os.path.exists(LOGO) else ""
html=f"""
<!DOCTYPE html><html><head><meta charset='utf-8'><style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: Helvetica, Arial, sans-serif; color:#1a1a1a; }}
.band {{ background: linear-gradient(135deg,#154360 0%,#1A5276 55%,#2874A6 100%); color:#fff;
        padding: 70px 56px 54px 56px; }}
.kicker {{ font-size:13pt; letter-spacing:3px; text-transform:uppercase; opacity:.85; margin-bottom:10px; }}
.title {{ font-size:40pt; font-weight:800; line-height:1.08; margin:0 0 14px 0; }}
.subtitle {{ font-size:17pt; font-weight:400; opacity:.95; }}
.accent {{ height:6px; width:120px; background:#F39C12; margin:26px 0 0 0; border-radius:3px; }}
.body {{ padding: 48px 56px; }}
.author {{ font-size:15pt; font-weight:700; color:#154360; margin-bottom:2px; }}
.aff {{ font-size:11.5pt; color:#333; line-height:1.5; }}
.meta {{ margin-top:30px; font-size:10.5pt; color:#444; line-height:1.7; }}
.meta b {{ color:#154360; }}
.foot {{ position:absolute; bottom:38px; left:56px; right:56px; font-size:9pt; color:#777;
        border-top:1px solid #ddd; padding-top:12px; }}
.badge {{ display:inline-block; background:#EAF2F8; color:#154360; border:1px solid #AED6F1;
         border-radius:14px; padding:3px 12px; font-size:9.5pt; font-weight:700; }}
</style></head><body>
<div class="band">
  {logo_tag}
  <div class="kicker">An Online Textbook</div>
  <div class="title">Generative AI<br/>with Amazon Bedrock</div>
  <div class="subtitle">Fundamentals, Responsible AI, and Building Applications with Foundation Models</div>
  <div class="accent"></div>
</div>
<div class="body">
  <div class="author">Devharsh Trivedi, Ph.D., CISSP</div>
  <div class="aff">Department of Computer Science<br/>Bowie State University</div>
  <div class="aff">ORCID: 0000-0001-6374-7249</div>
  <div class="meta">
    <span class="badge">Version June 2026</span><br/><br/>
    <b>Includes:</b> an AI Literacy Primer, tokens &amp; embeddings, the ten AI skills,
    a practical AI workflow, and alignment with the U.S. DOL "Make America AI-Ready"
    framework, the NIST AI RMF 1.0, ABET student outcomes, and Bloom's taxonomy.<br/><br/>
    <b>Modules:</b> (1) Fundamentals of Generative AI, (2) Responsible Generative AI,
    (3) Building Applications with Foundation Models, with hands-on Amazon Bedrock labs.
  </div>
  <div class="foot">
    Adapted from the AWS Machine Learning University Generative AI curriculum.
    Licensed under CC-BY-SA-4.0 (documentation) and MIT-0 (sample code).<br/>
    https://github.com/BSU-devharsh/aws-mlu-eep-generative-ai
  </div>
</div>
</body></html>
"""
open("/tmp/cover.html","w").write(html)
HTML(string=html).write_pdf("/tmp/cover.pdf")
print("cover.pdf written")
