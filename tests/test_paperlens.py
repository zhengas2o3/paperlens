"""Unit tests for PaperLens (stdlib unittest only)."""

import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from paperlens import arxiv_client, rank, render
from paperlens.sample_data import get_sample_xml


class ParseFeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.papers = arxiv_client.parse_feed(get_sample_xml())

    def test_parse_count(self):
        self.assertEqual(len(self.papers), 6)

    def test_parse_fields(self):
        paper = self.papers[0]
        self.assertEqual(
            paper.title, "Evidence-Driven Multimodal Fusion for Medical Image Diagnosis"
        )
        self.assertEqual(paper.authors, ["Haoran Li", "Mei Chen", "Jonas Weber"])
        self.assertEqual(paper.arxiv_id, "2601.01234")
        self.assertEqual(paper.published, date(2026, 1, 12))
        self.assertEqual(paper.primary_category, "cs.CV")
        self.assertIn("cs.AI", paper.categories)
        self.assertIn("2601.01234", paper.link)
        self.assertIn("multimodal", paper.summary.lower())

    def test_version_suffix_stripped(self):
        ids = {p.arxiv_id for p in self.papers}
        self.assertIn("2601.03456", ids)  # source entry is ...v2
        self.assertNotIn("2601.03456v2", ids)


class RankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.papers = arxiv_client.parse_feed(get_sample_xml())

    def test_dedupe_by_arxiv_id(self):
        duplicated = self.papers + [self.papers[0], self.papers[2]]
        self.assertEqual(len(rank.dedupe(duplicated)), 6)
        self.assertEqual(len(rank.dedupe(self.papers)), 6)

    def test_scoring_prefers_title_hits(self):
        ranked = rank.rank_papers(self.papers, ["attention"])
        self.assertEqual(ranked[0].arxiv_id, "2601.04567")  # keyword in title
        scores = [rank.score_paper(p, ["attention"]) for p in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_title_weight_beats_abstract_weight(self):
        # "multimodal" appears in the title of 2601.01234 and only in the
        # abstract of 2511.06789, so the former must score higher.
        by_id = {p.arxiv_id: p for p in self.papers}
        self.assertGreater(
            rank.score_paper(by_id["2601.01234"], ["multimodal"]),
            rank.score_paper(by_id["2511.06789"], ["multimodal"]),
        )

    def test_date_filter(self):
        recent = rank.filter_by_days(self.papers, 30, today=date(2026, 1, 15))
        ids = {p.arxiv_id for p in recent}
        self.assertIn("2601.01234", ids)       # 2026-01-12
        self.assertIn("2512.05678", ids)       # 2025-12-28, within 30 days
        self.assertNotIn("2511.06789", ids)    # 2025-11-15, too old
        self.assertEqual(len(recent), 5)


class RenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.papers = arxiv_client.parse_feed(get_sample_xml())

    def test_render_contains_titles_and_links(self):
        digest = render.render_digest(self.papers, generated=date(2026, 1, 15))
        self.assertIn("# PaperLens Digest", digest)
        for paper in self.papers:
            self.assertIn(paper.title, digest)
            self.assertIn(f"[{paper.arxiv_id}]({paper.link})", digest)

    def test_render_groups_by_category(self):
        digest = render.render_digest(self.papers, generated=date(2026, 1, 15))
        self.assertIn("## cs.CV", digest)
        self.assertIn("## cs.CL", digest)
        self.assertIn("## math.OC", digest)

    def test_render_keyword_groups(self):
        groups = [
            {"name": "Optimization", "keywords": ["scheduling", "optimization"]},
        ]
        digest = render.render_digest(
            self.papers, generated=date(2026, 1, 15), keyword_groups=groups
        )
        self.assertIn("## Optimization", digest)

    def test_render_empty(self):
        digest = render.render_digest([], generated=date(2026, 1, 15))
        self.assertIn("No papers matched", digest)


class QueryUrlTests(unittest.TestCase):
    def test_build_query_url(self):
        url = arxiv_client.build_query_url(
            keywords=["multimodal"], categories=["cs.LG"], max_results=10
        )
        self.assertIn("export.arxiv.org/api/query", url)
        self.assertIn("max_results=10", url)
        self.assertIn("cs.LG", url)


if __name__ == "__main__":
    unittest.main()
