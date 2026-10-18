#!/usr/bin/env python3
"""Render the editable Markdown pages into deployable static HTML files."""

from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PAGES = (
    ("index.md", "index.html", "Home"),
    ("research.md", "research.html", "Research"),
    ("blog.md", "blog.html", "Blog"),
    ("courses.md", "courses.html", "Courses")
)


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    _, front_matter, body = text.split("---\n", 2)
    values: dict[str, str] = {}
    for line in front_matter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values, body.strip()


def inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    code_tokens: list[str] = []

    def preserve_code(match: re.Match[str]) -> str:
        code_tokens.append(f"<code>{match.group(1)}</code>")
        return f"\x00CODE{len(code_tokens) - 1}\x00"

    escaped = re.sub(r"`([^`]+)`", preserve_code, escaped)
    escaped = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        r'<img class="content-image" src="\2" alt="\1" loading="lazy">',
        escaped,
    )
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    for number, token in enumerate(code_tokens):
        escaped = escaped.replace(f"\x00CODE{number}\x00", token)
    return escaped


def resume_item_html(fields: dict[str, str]) -> str:
    """Render one compact CV-style entry from an editable Markdown block."""
    title = inline(fields.get("title", ""))
    organization = inline(fields.get("organization", ""))
    dates = inline(fields.get("dates", ""))
    advisor = inline(fields.get("advisor", ""))
    description = inline(fields.get("description", ""))

    parts = [
        '<article class="resume-item">',
        '  <div class="resume-item__header">',
        '    <div class="resume-item__identity">',
        f"      <h3>{title}</h3>",
    ]
    if organization:
        parts.append(f'      <p class="resume-item__organization">{organization}</p>')
    parts.extend(["    </div>"])
    if dates:
        parts.append(f'    <p class="resume-item__dates">{dates}</p>')
    parts.append("  </div>")
    if advisor:
        parts.append(
            f'  <p class="resume-item__advisor"><span>Advisor</span>{advisor}</p>'
        )
    if description:
        parts.append(f'  <p class="resume-item__description">{description}</p>')
    parts.append("</article>")
    return "\n".join(parts)


def markdown_to_html(source: str) -> str:
    lines = source.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    in_list = False
    in_math = False
    math: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(f"<p>{inline(' '.join(paragraph))}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            output.append("</ul>")
            in_list = False

    line_iterator = iter(lines)
    for line in line_iterator:
        stripped = line.strip()
        if stripped == "$$":
            flush_paragraph()
            close_list()
            if in_math:
                output.append('<div class="equation">\\[' + "\n".join(math) + "\\]</div>")
                math = []
            in_math = not in_math
            continue
        if in_math:
            math.append(line)
            continue
        if not stripped:
            flush_paragraph()
            close_list()
            continue
        if stripped == "::: resume":
            flush_paragraph()
            close_list()
            fields: dict[str, str] = {}
            for block_line in line_iterator:
                block_line = block_line.strip()
                if block_line == ":::":
                    break
                if not block_line or ":" not in block_line:
                    continue
                key, value = block_line.split(":", 1)
                fields[key.strip().lower()] = value.strip()
            output.append(resume_item_html(fields))
            continue
        if stripped.startswith("## "):
            flush_paragraph()
            close_list()
            output.append(f"<h2>{inline(stripped[3:])}</h2>")
            continue
        if stripped.startswith("### "):
            flush_paragraph()
            close_list()
            output.append(f"<h3>{inline(stripped[4:])}</h3>")
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            if not in_list:
                output.append("<ul>")
                in_list = True
            output.append(f"<li>{inline(stripped[2:])}</li>")
            continue
        if re.fullmatch(r"!\[[^\]]*\]\([^)]+\)", stripped):
            flush_paragraph()
            close_list()
            output.append(inline(stripped))
            continue
        if stripped.startswith("<"):
            flush_paragraph()
            close_list()
            output.append(line)
            continue
        paragraph.append(stripped)

    flush_paragraph()
    close_list()
    return "\n".join(output)


def page_html(title: str, current: str, excerpt: str, body: str) -> str:
    nav = []
    for label, target in (("Home", "index.html"), ("Research", "research.html"),("Blog", "blog.html")):
            active = ' aria-current="page"' if label == current else ""
            nav.append(f'<a href="{target}"{active}>{label}</a>')
    page_header = f'<header class="page-header">\n        <h1>{html.escape(title)}</h1>'
    if excerpt:
        page_header += f'\n        <p class="page-intro">{inline(excerpt)}</p>'
    page_header += "\n      </header>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Personal website of Shuo Guo.">
  <title>{html.escape(title)} | Shuo Guo</title>
  <link rel="stylesheet" href="assets/css/site.css">
  <script>
    window.MathJax = {{tex: {{inlineMath: [['$', '$'], ['\\\\(', '\\\\)']]}}, svg: {{fontCache: 'global'}}}};
  </script>
  <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="masthead">
    <div class="masthead__inner">
      <a class="site-title" href="index.html">Shuo Guo</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav id="site-nav" class="site-nav" aria-label="Main navigation">{''.join(nav)}</nav>
    </div>
  </header>
  <div class="page-shell">
    <aside class="profile" aria-label="Contact information">
      <img src="image.png" alt="Portrait of Shuo Guo" class="profile__photo">
      <h2>Shuo Guo</h2>
      <p class="profile__bio">Undergraduate student at CUHK-Shenzhen.</p>
      <p class="profile__bio">E-Mail: shuoguo@link.cuhk.edu.cn</p>
    </aside>
    <main id="main" class="page-content">
      {page_header}
      {body}
    </main>
  </div>
  <footer class="site-footer"><div>© {date.today().year} Shuo Guo · Built with the Minimal Mistakes sunrise-inspired static layout.</div></footer>
  <script src="assets/js/site.js"></script>
</body>
</html>
"""


def main() -> None:
    for source_name, output_name, navigation_name in PAGES:
        source = ROOT / source_name
        metadata, content = split_front_matter(source.read_text(encoding="utf-8"))
        title = metadata.get("title", navigation_name)
        excerpt = metadata.get("excerpt", "")
        rendered = page_html(title, navigation_name, excerpt, markdown_to_html(content))
        (ROOT / output_name).write_text(rendered, encoding="utf-8")
        print(f"Rendered {source_name} -> {output_name}")


if __name__ == "__main__":
    main()
