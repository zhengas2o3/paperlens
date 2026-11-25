"""PaperLens command-line interface.

Subcommands:

* ``paperlens search`` — query the live arXiv API and print a digest.
* ``paperlens demo`` — build a digest from the bundled sample feed,
  with no network access.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta

from . import arxiv_client, rank, render
from .sample_data import get_sample_xml


def load_config(path):
    """Load a JSON config file; returns an empty dict when no path is given."""
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def split_keywords(text):
    """Split a comma-separated --query value into a keyword list."""
    if not text:
        return []
    return [part.strip() for part in text.split(",") if part.strip()]


def build_digest(papers, args, config, generated=None):
    """Shared pipeline: dedupe -> date filter -> rank -> render."""
    keywords = split_keywords(args.query) + list(config.get("keywords", []))
    papers = rank.dedupe(papers)
    if args.days is not None:
        papers = rank.filter_by_days(papers, args.days)
    if keywords:
        papers = rank.rank_papers(papers, keywords, config.get("weights"))
    else:
        papers = sorted(papers, key=lambda p: p.published, reverse=True)
    papers = papers[: args.max] if args.max else papers
    return render.render_digest(
        papers,
        generated=generated,
        keyword_groups=config.get("keyword_groups"),
    )


def emit(text, out_path):
    if out_path:
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"Wrote digest to {out_path}", file=sys.stderr)
    else:
        sys.stdout.write(text)


def cmd_search(args) -> int:
    config = load_config(args.config)
    keywords = split_keywords(args.query) + list(config.get("keywords", []))
    end = date.today()
    start = end - timedelta(days=args.days) if args.days else None
    papers = arxiv_client.search_arxiv(
        keywords=keywords or None,
        categories=config.get("categories"),
        start_date=start,
        end_date=end if args.days else None,
        max_results=max(args.max * 2, args.max),  # fetch extra; ranking trims
    )
    emit(build_digest(papers, args, config), args.out)
    return 0


def cmd_demo(args) -> int:
    config = load_config(args.config)
    papers = arxiv_client.parse_feed(get_sample_xml())
    # Demo data is fixed; never date-filter it away.
    args.days = None
    emit(build_digest(papers, args, config), args.out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="paperlens",
        description="Turn arXiv search results into clean Markdown literature digests.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p):
        p.add_argument("--query", default="", help="Comma-separated keywords.")
        p.add_argument("--days", type=int, default=None,
                       help="Only include papers from the last N days.")
        p.add_argument("--max", type=int, default=20,
                       help="Maximum number of papers in the digest (default 20).")
        p.add_argument("--out", default=None,
                       help="Write the digest to this file instead of stdout.")
        p.add_argument("--config", default=None,
                       help="Path to a JSON config (keywords, weights, keyword_groups).")

    add_common(sub.add_parser("search", help="Query the live arXiv API."))
    add_common(sub.add_parser("demo", help="Offline demo using the bundled sample feed."))
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "search":
        return cmd_search(args)
    return cmd_demo(args)


if __name__ == "__main__":
    sys.exit(main())
