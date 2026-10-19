import re, html, sys, os

SRC = r"U3_FIELD_RESEARCH_5_PARTICIPANTS_EN.md"
DST = r"_tmp_field_report.html"

CSS = """
@page { size: A4; margin: 2.2cm 2.0cm; }
body { font-family: "Georgia","Times New Roman",serif; font-size: 10.5pt; line-height: 1.55; color: #1a1a1a; }
h1 { font-family: "Helvetica Neue",Arial,sans-serif; font-size: 17pt; color: #111; border-bottom: 2px solid #111;
     padding-bottom: 6pt; margin-top: 26pt; margin-bottom: 12pt; page-break-before: always; page-break-after: avoid; }
h1.first { page-break-before: avoid; }
h2 { font-family: "Helvetica Neue",Arial,sans-serif; font-size: 12.5pt; color: #333; margin-top: 18pt;
     margin-bottom: 8pt; page-break-after: avoid; }
h3 { font-family: "Helvetica Neue",Arial,sans-serif; font-size: 10.5pt; color: #444; margin-top: 14pt;
     margin-bottom: 5pt; page-break-after: avoid; }
p { margin: 0 0 7pt 0; text-align: justify; }
.quote { margin: 0 0 10pt 0; }
p.qp { font-family: "Georgia","Times New Roman",serif; font-size: 10.5pt; color: #1a1a1a;
       margin: 0 0 6pt 16pt; text-align: justify; }
p.qb { margin: 0 0 2pt 26pt; text-align: left; }
p.prompt { font-family: "Helvetica Neue",Arial,sans-serif; font-size: 9pt; color: #6a6a6a;
           font-style: italic; text-align: left; margin: 0 0 6pt 0; }
p.prompt em { color: #6a6a6a; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0 12pt 0; font-size: 9.5pt;
        font-family: "Helvetica Neue",Arial,sans-serif; }
th { background: #efefef; border: 0.75pt solid #999; padding: 4pt 6pt; text-align: left; }
td { border: 0.75pt solid #bbb; padding: 4pt 6pt; vertical-align: top; }
hr { border: none; border-top: 0.75pt solid #ccc; margin: 14pt 0; }
code { font-family: Consolas,"Courier New",monospace; font-size: 9.5pt; background: #f2f2f2; padding: 0 2pt; }
ul { margin: 0 0 8pt 0; padding-left: 18pt; }
li { margin-bottom: 3pt; }
em { color: #555; }
.lines { text-align: left; }
"""


def inline(t):
    t = html.escape(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    return t


def convert(lines):
    out = []
    i = 0
    first_h1 = True
    after_q_heading = False
    while i < len(lines):
        ln = lines[i].rstrip("\n")
        s = ln.strip()

        if not s:
            i += 1
            continue

        if s == "---":
            out.append("<hr/>")
            i += 1
            continue

        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            lvl = len(m.group(1))
            cls = ""
            if lvl == 1 and first_h1:
                cls = ' class="first"'
                first_h1 = False
            out.append(f"<h{lvl}{cls}>{inline(m.group(2))}</h{lvl}>")
            after_q_heading = lvl == 3
            i += 1
            continue

        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            body = [r for r in cells if not re.match(r"^[\s:-]+$", "".join(r))]
            out.append("<table>")
            if body:
                out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in body[0]) + "</tr>")
                for r in body[1:]:
                    out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</table>")
            continue

        if s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i].rstrip("\n")))
                i += 1
            out.append('<div class="quote">')
            para = []

            QS = 'style="margin:0 0 6pt 0;margin-left:18pt;text-align:justify"'
            BS = 'style="margin:0 0 1pt 0;margin-left:30pt;text-align:left"'

            def flush():
                if para:
                    out.append(f"<p class=\"qp\" {QS}>{inline(' '.join(para))}</p>")
                    para.clear()

            for b in buf:
                bs = b.strip()
                if bs.startswith("·"):
                    flush()
                    out.append(f'<p class="qp" {BS}>{inline(bs)}</p>')
                elif bs:
                    para.append(bs)
                else:
                    flush()
            flush()
            out.append("</div>")
            after_q_heading = False
            continue

        if re.match(r"^- ", s):
            while i < len(lines) and re.match(r"^- ", lines[i].strip()):
                txt = inline(lines[i].strip()[2:])
                out.append(
                    '<p style="margin:0 0 4pt 0;margin-left:16pt;text-align:justify">'
                    f"· {txt}</p>"
                )
                i += 1
            after_q_heading = False
            continue

        # plain paragraph: merge consecutive non-empty, non-special lines,
        # but keep single newlines as <br/> (consent blocks rely on them)
        para = []
        while i < len(lines):
            cur = lines[i].strip()
            if not cur or cur == "---" or cur.startswith((">", "|", "#", "- ")):
                break
            para.append(inline(cur))
            i += 1
        if after_q_heading:
            cls = ' class="prompt"'
        elif len(para) > 1:
            cls = ' class="lines"'
        else:
            cls = ""
        out.append(f"<p{cls}>" + "<br/>".join(para) + "</p>")
        after_q_heading = False
    return "\n".join(out)


src = open(SRC, encoding="utf-8").read().split("\n")
body = convert(src)
doc = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"/>
<title>Field Research Compilation - AI Life - RCA GD Unit 3</title>
<style>{CSS}</style></head><body>
{body}
</body></html>"""
open(DST, "w", encoding="utf-8").write(doc)
print("wrote", DST, len(doc), "chars")
