"""Render a list of papers as a Markdown literature digest."""

from __future__ import annotations

from datetime import date


def truncate(text: str, limit: int = 280) -> str:
    """Truncate ``text`` to at most ``limit`` characters, on a word boundary."""
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(".,;:") + "…"


def group_papers(papers, keyword_groups=None):
    """Group papers into ``[(group_name, [papers]), ...]``.

    If ``keyword_groups`` is given (a list of ``{"name": ..., "keywords":
    [...]}`` dicts), each paper joins the first group with a keyword hit in
    its title or abstract. Papers that match no group — and all papers when
    no groups are configured — fall back to their arXiv primary category.
    Group order follows the config order, then first appearance.
    """
    groups = {}
    order = []

    def add(name, paper):
        if name not in groups:
            groups[name] = []
            order.append(name)
        groups[name].append(paper)

    configured = [g for g in (keyword_groups or []) if g.get("name")]
    for paper in papers:
        assigned = None
        haystack = f"{paper.title} {paper.summary}".lower()
        for group in configured:
            if any(kw.lower() in haystack for kw in group.get("keywords", [])):
                assigned = group["name"]
                break
        add(assigned or paper.primary_category or "Other", paper)

    return [(name, groups[name]) for name in order]


def _render_paper(paper, abstract_chars: int) -> str:
    authors = ", ".join(paper.authors) if paper.authors else "Unknown authors"
    lines = [
        f"### {paper.title}",
        f"**Authors:** {authors} · **Published:** {paper.published.isoformat()} · "
        f"**arXiv:** [{paper.arxiv_id}]({paper.link})",
        "",
        truncate(paper.summary, abstract_chars),
        "",
    ]
    return "\n".join(lines)


def render_digest(
    papers,
    title: str = "PaperLens Digest",
    generated: date = None,
    abstract_chars: int = 280,
    keyword_groups=None,
) -> str:
    """Render ``papers`` as a Markdown digest string."""
    generated = generated or date.today()
    out = [
        f"# {title}",
        "",
        f"Generated: {generated.isoformat()} · {len(papers)} paper"
        + ("s" if len(papers) != 1 else ""),
        "",
    ]
    if not papers:
        out += ["_No papers matched._", ""]
        return "\n".join(out)
    for group_name, group in group_papers(papers, keyword_groups):
        out.append(f"## {group_name}")
        out.append("")
        for paper in group:
            out.append(_render_paper(paper, abstract_chars))
    return "\n".join(out).rstrip() + "\n"
