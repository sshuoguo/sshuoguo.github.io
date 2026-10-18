# Shuo Guo's personal website

This is a direct static-HTML site with a Minimal Mistakes `sunrise`-inspired
layout. GitHub Pages serves the generated `.html` files exactly as they are.
No Ruby, Jekyll, or GitHub build step is needed.

## Edit and render

Edit the Markdown source pages:

- `index.md` — home page
- `news.md` — news / updates page
- `research.md` — research page
- `notes.md` — notes and PDF links

Then **double-click `Update Website.app`** in Finder. It starts the updater in
Terminal (which has access to your Documents folder), regenerates `index.html`,
`news.html`, and `notes.html`, then opens `website-update.log`. The log
lists every generated file; if it contains an error, the update did not complete.

You can also run `Update Website.command`, or use the terminal:

```bash
make render
make serve
```

`make serve` creates the HTML first, then serves the site on
<http://127.0.0.1:8000>.

## Publish

```bash
git add .
git commit -m "Update website"
git push
```

Commit both the changed `.md` files and generated `.html` files.
