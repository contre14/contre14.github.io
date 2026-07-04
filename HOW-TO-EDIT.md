# How to work on this site (from any computer)

This repo **is** the website. Everything the live site needs is here. GitHub is the single
source of truth, so you can work from your desktop, your laptop, or both.

Live site: https://contre14.github.io
Repo: https://github.com/contre14/contre14.github.io

---

## First time on a new computer

1. Install [Git](https://git-scm.com/downloads) if you don't have it.
2. Clone the repo:
   ```bash
   git clone https://github.com/contre14/contre14.github.io.git
   cd contre14.github.io
   ```

That's it — you now have the whole site.

## Every time you sit down to work

**Pull first** (grabs any changes made from your other computer):
```bash
git pull
```

**Preview** — just double-click `index.html`. It opens in your browser, no server needed.

**Make changes** — edit any `.html` file or `css/style.css` in any text editor
(VS Code is great and free).

**Publish** when you're happy:
```bash
git add -A
git commit -m "short description of what you changed"
git push
```
GitHub Pages rebuilds automatically — the live site updates in about a minute.
If it looks unchanged, hard-refresh your browser: **Ctrl+Shift+R**.

> Golden rule: **`git pull` before you start, `git push` when you finish.** That keeps your
> laptop and desktop in sync and avoids conflicts.

---

## Where things live

```
index.html         Home — hero pitch, highlights, "How I fit a propulsion team"
about.html         Bio, education, skills (Software / Engineering)
projects.html      Lunar Rover · Shock modeling  (case-study cards)
research.html      UCI flow modeling · NSF combustion · UC Berkeley
publications.html  npj paper + the MATLAB image-processing pipeline
awards.html        NSF LSAMP · Aerospace Corp. Academy · leadership
contact.html       Email, phone, LinkedIn
css/style.css      All styling — colors are the variables at the very top
assets/img/        The figures shown on the pages (SolidWorks renders, plots)
assets/files/      Source PDFs, résumé, and Python code
```

## Common edits

- **Change wording:** open the `.html` file, find the text, edit it. Text sits right in the page.
- **Change a color:** edit the `--accent` (and friends) variables at the top of `css/style.css`
  — recolors the whole site at once.
- **Add a project/research item:** copy an existing `<div class="pcard"> … </div>` block and
  edit its text, image (`assets/img/...`), and links.
- **Swap a figure:** drop the new image in `assets/img/` and point the `<img src="...">` at it.

## If something breaks

Every change is saved in git history, so nothing is ever truly lost. To undo the last
commit that you haven't pushed yet:
```bash
git reset --soft HEAD~1
```
Or ask Claude Code (in this project folder) to help — it can see the full history.
