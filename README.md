# Alexander Contreras — Portfolio website

Static multi-page site. No build step, no dependencies. Targeted at Fall 2026 propulsion /
thermal-fluids internships. Real work is shown inline — SolidWorks renders, plots, and paper
figures embedded as case-study cards, with the full PDFs and code linked.

**Live:** https://contre14.github.io · **Deploy:** GitHub Pages (`main` / root, already set up)

👉 **To edit the site from your desktop or laptop, see [HOW-TO-EDIT.md](HOW-TO-EDIT.md).**

## Pages
```
index.html         Home — hero pitch, highlights, "How I fit a propulsion team"
about.html         Bio, education (UCI / CSULB), skills (Software / Engineering), headshot
research.html      UCI flow modeling · NSF combustion · UC Berkeley  (case-study cards)
projects.html      Lunar Rover · Shock modeling  (renders, plots, report + Python code)
publications.html  npj Advanced Manufacturing paper + the MATLAB image-processing pipeline
awards.html        2× NSF LSAMP · Aerospace Corp. Dean's Leadership Academy · leadership
contact.html       Email, phone, LinkedIn
css/style.css      Styling — recolor everything via the :root variables at the top
assets/img/        Figures shown inline on the pages (SolidWorks renders, plots, paper figures)
assets/files/      All source PDFs + résumé + Python code
assets/thumbs/     Page-1 thumbnail images (legacy)
```

## Preview
Double-click `index.html` — opens in your browser, no setup.

## Edit content
Text lives directly in each `.html` file. To add a project/research item, copy an existing
`<div class="pcard">` block. To recolor, edit the `:root` variables at the top of `css/style.css`.
