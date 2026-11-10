#!/usr/bin/env python3
"""Regenerate site/content/docs and site/content/source from ../docs and ../src."""
import pathlib, re, shutil

here = pathlib.Path(__file__).resolve().parent
repo = here.parent
content = here / "content"

def reset(d):
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)

def page(path, title, body, weight, summary=None, hide_home=False):
    fm = ["---", f'title: "{title}"', f"weight: {weight}"]
    if hide_home:
        fm.append("hiddenInHomeList: true")
    if summary:
        fm.append(f'summary: "{summary}"')
    fm.append("---\n")
    path.write_text("\n".join(fm) + "\n" + body.strip() + "\n")

# ---- documents -----------------------------------------------------------
docs = content / "docs"
reset(docs)
page(docs / "_index.md", "Documents",
     "The original 1994 project documents, transcribed from photographs of the printed copies.", 0)
for i, (src, title, summary) in enumerate([
    ("01-project-proposal.md", "Project Proposal", "January 23 1994"),
    ("02-progress-report.md", "Progress Report #1", "February 21 1994"),
    ("03-final-report.md", "Final Report", "Project summary and acknowledgments"),
], 1):
    body = (repo / "docs" / src).read_text()
    body = re.sub(r"\A# .*\n+", "", body)
    page(docs / src.split("-", 1)[1], title, body, i * 10, summary)

# ---- source --------------------------------------------------------------
source = content / "source"
reset(source)
page(source / "_index.md", "Source",
     "The AutoLISP listing, pages 19 to 26 of the original, split by function. "
     "Pages 1 to 18 (the `GO` entry point and the start of `getparams`) are not yet transcribed. Includes the variable listing from page 27.", 0)
for i, f in enumerate(sorted((repo / "src").glob("*.lsp")), 1):
    text = f.read_text()
    m = re.match(r"((?:;;;.*\n)+)", text)
    header = m.group(1) if m else ""
    lines = [re.sub(r"^;;;\s?", "", l) for l in header.splitlines()]
    intro = ""
    for l in lines:
        intro += ("\n\n" if re.match(r"(Source|NOTE):", l) or not intro else "\n") + l
    intro = intro.strip()
    first = intro.splitlines()[0] if intro else f.name
    title = f.name
    summary = first.split("--", 1)[-1].strip()
    body = f"{intro}\n\n```lisp\n{text[len(header):].lstrip()}```\n"
    page(source / (f.stem + ".md"), title, body, i * 10, summary)

# the variable listing is page 27 of the program listing, so it lives with the source
vl = (repo / "docs" / "04-variable-listing.md").read_text()
vl = re.sub(r"\A# .*\n+", "", vl)
page(source / "variable-listing.md", "Variable Listing", vl, 100, "Every variable in the program, with type and scope")
print("synced")
