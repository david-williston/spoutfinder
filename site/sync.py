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

def page(path, title, body, weight, summary=None, hide_home=False, toc=False):
    fm = ["---", f'title: "{title}"', f"weight: {weight}"]
    if toc:
        fm.append("ShowToc: true")
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
    ("04-variable-listing.md", "Variable Listing", "Every variable in the program, with type and scope"),
], 1):
    body = (repo / "docs" / src).read_text()
    body = re.sub(r"\A# .*\n+", "", body)
    page(docs / src.split("-", 1)[1], title, body, i * 10, summary)

# ---- source --------------------------------------------------------------
source = content / "source"
reset(source)
page(source / "_index.md", "Source",
     "The AutoLISP listing, pages 19 to 26 of the original, taken apart function by function. "
     "Pages 1 to 18 (the `GO` entry point and the start of `getparams`) are not yet transcribed. Includes the variable listing from page 27.", 0)

# What each piece does, in plain words. Everything here is read from the code itself.
NOTES = {
 "getparams.lsp": {
  "plain": "This is the tail of the routine that interviews the operator. For each setting it checks for a value left over from the last run: if there is one, it is shown in angle brackets as the default and kept when the operator just presses Enter; if not, an answer is required. After the prompts it works out the area of one spout circle and asks the operator to pick the pockets.",
  "segments": {
   "getparams": {
    "title": "The prompts (tail of getparams)",
    "what": "Asks for the spout pitch, the increment distance, the number of spouts and increments, the accuracy and the output file name. Then it calculates the valid area, switches to the graphics screen and calls SSGET so the operator can select the pockets.",
    "note": "The numbers passed to INITGET are added bit flags: 1 means an answer is required, 2 forbids zero and 4 forbids negatives, so (+ 1 2 4) demands a positive number. Pi is typed in as 3.14159. Remembering the last values works because they live in global variables that survive between runs."}}},
 "pocket.lsp": {
  "plain": "Three small helpers that ask AutoCAD's solid modeler about the pocket being worked on: its flat surface, its volume, and its bounding box.",
  "segments": {
   "pocketsurf": {
    "what": "Slices the current pocket with the XY plane (SOLSECT) to get its flat surface region, then asks AME for that region's mass properties (SOLMASSP). The slice and the property list are kept for the later steps.",
    "note": "It switches to a layer called pocketsurf first, so the working slices stay apart from the model."},
   "pocketvolume": {
    "what": "Asks AME for the current pocket's mass properties and keeps item 1 of the returned list, its volume.",
    "note": "The \"n\" given to SOLMASSP presumably answers its prompt about writing a report file."},
   "seeiflocal": {
    "what": "A cheap pre-check. It reads two corner points of the pocket surface's bounding box out of the SOLMASSP list and tests whether the current spout position lies inside that box.",
    "note": "The local-variable list names yx where the body uses yc, so yc quietly becomes a global. In a language with no compiler warnings, a typo like that was easy to make and hard to see."}}},
 "intersect.lsp": {
  "plain": "The heart of the program. For one spout position it builds a circle, intersects it with the pocket surface, and decides whether the spout fits.",
  "segments": {
   "doint": {
    "what": "Draws a circle at the current point on the cell layer, turns it into a region (SOLIDIFY), copies the pocket surface, and intersects the two with SOLINT. It returns the selection set holding the overlap.",
    "note": "A fresh circle and a fresh copy are made every time because SOLINT empties the set it is given, so the code saves the entity names first. Selection sets are set to nil as soon as they are used so AutoLISP does not run out of them."},
   "check": {
    "what": "Judges the overlap. No result means the spout is outside the pocket, so the circle and the copied surface are erased. Otherwise it measures the overlap with SOLAREA and calls the spout valid if the shortfall from a full circle is under the accuracy tolerance, drawing a circle there.",
    "note": "Every purgeflag cycles it calls SOLPURGE to clear erased solids out of the drawing file; the value of purgeflag is set on the missing pages. The result is the global validity flag, which the next step reads."}}},
 "locations.lsp": {
  "plain": "Walks the grid of spout positions and keeps the results: one list per pocket, merged into a single list for the whole job.",
  "segments": {
   "buildlist": {
    "what": "Adds one entry to the temporary list for the current position: the pocket's entity name where a spout is valid, 0 where it is not. A position of (0, 0) starts a new list.",
    "note": "The comment explains the entity name is a stand-in; it was meant to be replaced by a time value once the pour volume was calculated."},
   "nextspout": {
    "what": "Moves the current point one spout pitch along y."},
   "nextrow": {
    "what": "Resets y to 0 and moves x over by the increment distance, starting the next row."},
   "combine": {
    "what": "Merges the list for the current pocket into the running list for all pockets. Position by position it keeps an entity name from the earlier list if there is one, otherwise takes the new list's entry.",
    "note": "The list length is always spouts times increments, so the two lists line up exactly and can be merged with a simple counter."}}},
 "session.lsp": {
  "plain": "Housekeeping. It restores AutoCAD to how the operator left it, handles errors politely, and supplies the default settings.",
  "segments": {
   "my_reset": {
    "what": "Ends the undo group, then restores object snap, command echo and blip mode, and puts AutoCAD's own error handler back.",
    "note": "It is called both at the end of a run and from the error handler, so the drawing environment is put right whichever way the program ends."},
   "my_error": {
    "what": "Replaces AutoCAD's error handler. For a user cancel it just says the program was terminated. For a real error it shows the error number in an alert and tells the operator to type U to undo everything the program did.",
    "note": "Undoing a whole run with one command is possible because the work happens inside a single undo group; the group is opened by a setup routine on the missing pages."},
   "setdefaults": {
    "what": "Sets the values the prompts offer on the first run: flow rate 1, spout diameter 1, pitch 1, increment 1, 8 increments, 8 spouts, accuracy 0.02 and the file name output.sdf."}}},
 "output.lsp": {
  "plain": "Writes the answer to disk and says hello. Once every pocket has been processed, the merged list becomes a plain text file the pouring machine can read.",
  "segments": {
   "output": {
    "what": "Opens the file, writes a header line, then writes one line per increment with one space-separated entry per spout. It prints a dot to the screen for each spout so the operator can see it is working, then closes the file.",
    "note": "Everything is written with PRINC to a file handle. The header still says V0.1 beta, even though the program is called V1.0."},
   "banner": {
    "title": "The startup banner",
    "what": "Runs when the file is loaded: clears to the text screen and tells the operator SpoutFinder is loaded and to type GO to run.",
    "note": "GO is defined on the missing pages, so the banner promises a command this transcription cannot yet deliver."}}},
}

# pass 1: parse every file into segments (a segment is whatever sits between two ;------ rules)
SEP = re.compile(r"^;-{5,}")
files = sorted((repo / "src").glob("*.lsp"))
parsed = {}
for f in files:
    text = f.read_text()
    m = re.match(r"((?:;;;.*\n)+)", text)
    header = m.group(1) if m else ""
    rest = text[len(header):]
    rest = re.sub(r"^\);-{5,}.*$", ")\n;--------", rest, flags=re.M)   # a rule glued to a closing paren
    segs, cur = [], []
    for line in rest.splitlines():
        if SEP.match(line):
            if any(l.strip() for l in cur):
                segs.append(cur)
            cur = []
        else:
            cur.append(line)
    if any(l.strip() for l in cur):
        segs.append(cur)
    out = []
    for lines in segs:
        code = "\n".join(lines).strip("\n")
        d = re.search(r"^\(defun\s+([\w\-\*]+)", code, flags=re.M)
        out.append({"name": d.group(1) if d else None, "code": code})
    parsed[f.name] = {"header": header, "segs": out}
# give the two loose segments names
parsed["getparams.lsp"]["segs"][0]["name"] = "getparams"
for sg in parsed["output.lsp"]["segs"]:
    if sg["name"] is None:
        sg["name"] = "banner"

defined = {sg["name"]: fn for fn, p in parsed.items() for sg in p["segs"] if sg["name"] not in ("banner",)}
defined = {n: fn for n, fn in defined.items() if n != "getparams"}
calls = {}
for fn, p in parsed.items():
    for sg in p["segs"]:
        body = sg["code"]
        calls[sg["name"]] = sorted({n for n in defined if n != sg["name"] and re.search(r"\(\s*" + re.escape(n) + r"[\s)]", body)})
called_by = {n: sorted(k for k, v in calls.items() if n in v) for n in list(calls)}

# shared state: the global variables from the page-27 table
gvars = []
for row in (repo / "docs" / "04-variable-listing.md").read_text().splitlines():
    cells = [c.strip() for c in row.strip("|").split("|")]
    if len(cells) >= 3 and cells[2] == "G":
        gvars.append(cells[0].lower())
gvars = [v.rstrip("m") if v == "currentpocketvolum" else v for v in gvars]
gvars = ["currentpocketvolume" if v == "currentpocketvolum" else v for v in gvars]

def short(t):
    parts = t.split(". ")
    out = parts[0].rstrip(".")
    if len(out) < 45 and len(parts) > 1:
        out += ". " + parts[1].rstrip(".")
    return out + "."

def link(n):
    fn = defined.get(n)
    return f"[`{n}`](../{fn[:-4]}/#{n})" if fn else f"`{n}`"

for i, f in enumerate(files, 1):
    p = parsed[f.name]
    note = NOTES[f.name]
    lines = [re.sub(r"^;;;\s?", "", l) for l in p["header"].splitlines()]
    intro = ""
    for l in lines:
        intro += ("\n\n" if re.match(r"(Source|NOTE):", l) or not intro else "\n") + l
    intro = intro.strip()
    first = intro.splitlines()[0] if intro else f.name
    summary = first.split("--", 1)[-1].strip()
    total_lines = sum(1 for sg in p["segs"] for l in sg["code"].splitlines() if l.strip())
    comment_lines = sum(1 for sg in p["segs"] for l in sg["code"].splitlines() if l.strip().startswith(";"))

    body = [intro, "", f"## In plain English\n\n{note['plain']}"]
    body.append(f"\n*{total_lines} lines of code and comments, {comment_lines} of them comments.*")
    # function table
    rows = ["| Piece | What it is | Calls | Called by |", "| --- | --- | --- | --- |"]
    for sg in p["segs"]:
        n = sg["name"]; info = note["segments"][n]
        rows.append("| [{t}](#{a}) | {w} | {c} | {b} |".format(
            t=info.get("title", f"`{n}`"), a=n, w=short(info["what"]),
            c=", ".join(link(x) for x in calls[n]) or "–",
            b=", ".join(link(x) for x in called_by[n]) or ("`GO` (missing pages, inferred)" if n != "banner" else "when the file loads")))
    body.append("\n## The pieces\n\n" + "\n".join(rows))
    # one section per segment
    for sg in p["segs"]:
        n = sg["name"]; info = note["segments"][n]
        used = sorted(v for v in gvars if re.search(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", sg["code"], flags=re.I))
        n_lines = sum(1 for l in sg["code"].splitlines() if l.strip())
        body.append(f"\n## {info.get('title', n)} {{#{n}}}\n")
        body.append(f"{info['what']}\n")
        meta = f"**{n_lines} lines.**"
        if used:
            meta += " Shared state it touches: " + ", ".join(f"`{v}`" for v in used) + "."
        body.append(meta + "\n")
        body.append("```lisp\n" + sg["code"] + "\n```\n")
        if info.get("note"):
            body.append(f"> **Look closely.** {info['note']}\n")
    page(source / (f.stem + ".md"), f.name, "\n".join(body), i * 10, summary, hide_home=True, toc=True)

# the variable listing is page 27 of the program listing, so it lives with the source
vl = (repo / "docs" / "04-variable-listing.md").read_text()
vl = re.sub(r"\A# .*\n+", "", vl)
page(source / "variable-listing.md", "Variable Listing", vl, 100, "Every variable in the program, with type and scope", hide_home=True)
print("synced")
