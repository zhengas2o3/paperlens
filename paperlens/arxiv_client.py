"""Client for the arXiv API.

The module is split into three layers so the interesting logic can be
tested without any network access:

* :func:`build_query_url` — pure function that builds an arXiv API URL.
* :func:`fetch_feed` — the only function that touches the network.
* :func:`parse_feed` — pure function that turns Atom XML into ``Paper``
  objects.
"""

from __future__ import annotations

import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date, datetime

API_URL = "https://export.arxiv.org/api/query"

ATOM = "http://www.w3.org/2005/Atom"
ARXIV = "http://arxiv.org/schemas/atom"
NS = {"atom": ATOM, "arxiv": ARXIV}

_VERSION_SUFFIX = re.compile(r"v\d+$")


@dataclass
class Paper:
    """One arXiv paper, normalised from an Atom entry."""

    title: str
    authors: list
    summary: str
    published: date
    arxiv_id: str  # versionless, e.g. "2601.01234"
    link: str
    categories: list = field(default_factory=list)
    primary_category: str = ""

    @property
    def abs_url(self) -> str:
        return f"https://arxiv.org/abs/{self.arxiv_id}"


def _normalise_ws(text: str) -> str:
    return " ".join((text or "").split())


def _strip_version(raw_id: str) -> str:
    """Turn ``http://arxiv.org/abs/2601.01234v2`` into ``2601.01234``."""
    tail = raw_id.rstrip("/").rsplit("/", 1)[-1]
    return _VERSION_SUFFIX.sub("", tail)


def build_query_url(
    keywords=None,
    categories=None,
    start_date=None,
    end_date=None,
    max_results: int = 20,
    start: int = 0,
    sort_by: str = "submittedDate",
    sort_order: str = "descending",
) -> str:
    """Build an arXiv API query URL.

    ``keywords`` are matched against all fields (OR-combined),
    ``categories`` are arXiv category codes such as ``"cs.LG"``, and
    ``start_date`` / ``end_date`` (``datetime.date``) bound the submission
    date range.
    """
    parts = []
    if keywords:
        kw = " OR ".join(f'all:"{k}"' for k in keywords)
        parts.append(f"({kw})" if len(keywords) > 1 else kw)
    if categories:
        cats = " OR ".join(f"cat:{c}" for c in categories)
        parts.append(f"({cats})" if len(categories) > 1 else cats)
    if start_date or end_date:
        lo = start_date.strftime("%Y%m%d0000") if start_date else "199101010000"
        hi = end_date.strftime("%Y%m%d2359") if end_date else "209912312359"
        parts.append(f"submittedDate:[{lo} TO {hi}]")
    if not parts:
        parts.append("all:*")

    params = {
        "search_query": " AND ".join(parts),
        "start": start,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    return f"{API_URL}?{urllib.parse.urlencode(params)}"


def fetch_feed(url: str, timeout: int = 30) -> str:
    """Fetch an arXiv API URL and return the raw Atom XML text."""
    request = urllib.request.Request(
        url, headers={"User-Agent": "paperlens/0.1 (https://github.com/zhengas2o3/paperlens)"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def search_arxiv(keywords=None, categories=None, max_results: int = 20, **kwargs):
    """Convenience wrapper: build a query, fetch it, and parse the feed."""
    url = build_query_url(
        keywords=keywords, categories=categories, max_results=max_results, **kwargs
    )
    return parse_feed(fetch_feed(url))


def _parse_date(text: str) -> date:
    text = (text or "").strip()
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return date.min


def parse_feed(xml_text: str) -> list:
    """Parse an arXiv Atom feed into a list of :class:`Paper` objects."""
    root = ET.fromstring(xml_text)
    papers = []
    for entry in root.findall("atom:entry", NS):
        raw_id = entry.findtext("atom:id", default="", namespaces=NS)
        arxiv_id = _strip_version(raw_id)

        link = ""
        for link_el in entry.findall("atom:link", NS):
            if link_el.get("rel") == "alternate":
                link = link_el.get("href", "")
                break
        if not link:
            link = f"https://arxiv.org/abs/{arxiv_id}"

        categories = [
            cat.get("term", "")
            for cat in entry.findall("atom:category", NS)
            if cat.get("term")
        ]
        primary_el = entry.find("arxiv:primary_category", NS)
        primary = primary_el.get("term", "") if primary_el is not None else ""
        if not primary and categories:
            primary = categories[0]

        papers.append(
            Paper(
                title=_normalise_ws(entry.findtext("atom:title", default="", namespaces=NS)),
                authors=[
                    _normalise_ws(a.findtext("atom:name", default="", namespaces=NS))
                    for a in entry.findall("atom:author", NS)
                ],
                summary=_normalise_ws(entry.findtext("atom:summary", default="", namespaces=NS)),
                published=_parse_date(entry.findtext("atom:published", default="", namespaces=NS)),
                arxiv_id=arxiv_id,
                link=link,
                categories=categories,
                primary_category=primary,
            )
        )
    return papers
