# Shuo Guo's personal website

This is a static GitHub Pages site generated from small, readable `.jemdoc`
source files with [wsshin/jemdoc_mathjax](https://github.com/wsshin/jemdoc_mathjax).
The generator is vendored as `./jemdoc`, so Python 3 is the only build
dependency. The vendored copy comes from upstream commit
`4b83aa41b6d21496171cf97cd93d90c8ed1496fd`.
The vendored script has one small local fix so external-link attributes remain
valid HTML and include `rel="noopener noreferrer"`.

## The normal editing workflow

1. Edit the matching source file:
   - `index.jemdoc` -- home page
   - `research.jemdoc` -- research page
   - `notes.jemdoc` -- PDF notes list
   - `cv.jemdoc` -- CV page
   - `MENU` -- navigation
   - `jemdoc.css` -- appearance
2. Run `make` to regenerate the HTML files.
3. Run `make serve`, then open <http://localhost:8000> to preview locally.
4. Commit both the `.jemdoc` source and generated `.html` files, then push.

```bash
make
make serve
git add .
git commit -m "Update website"
git push
```

GitHub Pages serves `index.html` directly, so no server-side build step is
needed.

## Common changes

Add a paragraph or list item by editing the relevant `.jemdoc` file, then run
`make`.

Add a PDF note by copying it into the repository and adding a line like this to
`notes.jemdoc`:

```text
- [/my-note.pdf My New Note].
```

Write inline mathematics as `$x_{k+1}=x_k-\eta\nabla f(x_k)$`. Use this form
for displayed mathematics:

```text
\(
x_{k+1}=x_k-\eta\nabla f(x_k).
\)
```

Add a page by creating `name.jemdoc`, adding `name` to `PAGES` in `Makefile`,
and adding its link to `MENU`.

## Files that are not generated

PDFs, `image.png`, `bird.html`, and `Songs.md` are static assets or standalone
content. Running `make` does not modify them.
