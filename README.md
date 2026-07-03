# Alexander Contreras — Portfolio website

Static multi-page site. No build step, no dependencies, free to host. Your real reports,
posters, code, and the npj paper are embedded as page thumbnails that link to the full PDFs.

## Pages
```
index.html         Home (pitch + highlights)
about.html         Bio, education (UCI / CSULB), skills
research.html      NSF combustion · UC Berkeley · UCI flow modeling  (+ poster/presentation PDFs)
projects.html      Lunar Rover (full review package) · Shock modeling (report + Python code)
publications.html  npj Advanced Manufacturing paper (thumbnail + DOI + PDF)
awards.html        2× NSF LSAMP · Aerospace Corp. Dean's Leadership Academy · leadership
contact.html       Email, phone, LinkedIn
css/style.css      Styling — recolor everything via the variables at the top
assets/files/      All source PDFs + résumé + Python code
assets/thumbs/     Page-1 thumbnail images
```

## Preview now
Double-click `index.html` — opens in your browser, no setup.

## Edit content
Text lives directly in each `.html` file. To add a project/research item, copy an existing
`<div class="card">` block. To swap colors, edit the `:root` variables at the top of `css/style.css`.

## Deploy free — GitHub Pages
1. Create a free github.com account.
2. New public repo named `yourusername.github.io`.
3. Upload the **contents** of this `website/` folder (so `index.html` sits at the repo root).
4. Settings → Pages → Source: `main` / `/root` → Save.
5. Live at `https://yourusername.github.io` in ~1 minute.

Total site size is ~50 MB (mostly the lunar-rover review PDFs) — well within GitHub Pages limits.

## Add a headshot later (optional)
Drop a photo in `assets/`, then in `about.html` replace the "Quick facts" card with an
`<img>` if you'd prefer a picture.
