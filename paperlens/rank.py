"""Deduplication, relevance ranking, and date filtering for papers."""

from __future__ import annotations

from datetime import date, timedelta

DEFAULT_WEIGHTS = {"title": 3.0, "abstract": 1.0}


def dedupe(papers):
    """Remove duplicate papers, keyed by arXiv ID, keeping the first copy."""
    seen = set()
    unique = []
    for paper in papers:
        if paper.arxiv_id in seen:
            continue
        seen.add(paper.arxiv_id)
        unique.append(paper)
    return unique


def score_paper(paper, keywords, weights=None) -> float:
    """Score a paper by weighted keyword occurrences.

    A hit in the title counts ``weights["title"]`` (default 3.0), a hit in
    the abstract counts ``weights["abstract"]`` (default 1.0). Matching is
    case-insensitive substring matching.
    """
    weights = {**DEFAULT_WEIGHTS, **(weights or {})}
    title = paper.title.lower()
    abstract = paper.summary.lower()
    score = 0.0
    for keyword in keywords or []:
        kw = keyword.strip().lower()
        if not kw:
            continue
        score += weights["title"] * title.count(kw)
        score += weights["abstract"] * abstract.count(kw)
    return score


def rank_papers(papers, keywords, weights=None):
    """Sort papers by relevance score (desc), then by date (desc)."""
    return sorted(
        papers,
        key=lambda p: (score_paper(p, keywords, weights), p.published.toordinal()),
        reverse=True,
    )


def filter_by_days(papers, days, today=None):
    """Keep papers published within the last ``days`` days (inclusive)."""
    if days is None:
        return list(papers)
    today = today or date.today()
    cutoff = today - timedelta(days=days)
    return [p for p in papers if cutoff <= p.published <= today]


def filter_by_range(papers, start_date=None, end_date=None):
    """Keep papers whose publication date lies in [start_date, end_date]."""
    out = []
    for paper in papers:
        if start_date and paper.published < start_date:
            continue
        if end_date and paper.published > end_date:
            continue
        out.append(paper)
    return out
