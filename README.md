# PaperLens

> Turn arXiv search results into clean, readable Markdown literature digests — from the command line, with zero dependencies.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](pyproject.toml)
[![Tests](https://img.shields.io/badge/tests-unittest-lightgrey.svg)](tests/)

PaperLens is a small command-line tool for researchers who track a fast-moving
literature. It queries the [arXiv API](https://arxiv.org/help/api), deduplicates
and ranks the results by keyword relevance, and renders them as a tidy Markdown
digest grouped by topic — ready to paste into your notes, a lab wiki, or a
weekly reading list.

It is built entirely on the Python standard library (`urllib`,
`xml.etree.ElementTree`, `argparse`). No `pip install` of third-party packages,
no API keys, no accounts.

## Features

- **Live arXiv search** by keyword, category, and date range via the public arXiv API.
- **Offline demo mode** — generate a digest from the bundled sample feed, no network required.
- **Deduplication** by arXiv ID, so overlapping queries never produce repeats.
- **Relevance ranking** — configurable keyword scoring with separate weights for titles and abstracts.
- **Topic grouping** — group papers by arXiv primary category, or by your own keyword groups.
- **Date filtering** — keep only papers from the last *N* days.
- **JSON configuration** — keyword groups and scoring weights live in one small config file.
- **Zero dependencies** — pure standard library, runs anywhere Python 3.9+ runs.

## Installation

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/zhengas2o3/paperlens.git
cd paperlens
pip install -e .
```

Or just run it straight from the source tree, no installation needed:

```bash
python -m paperlens --help
```

## Quickstart

Search arXiv and print a digest to the terminal:

```bash
paperlens search --query "multimodal, large language model" --days 14 --max 20
```

Save the digest to a file:

```bash
paperlens search --query "production scheduling, evolutionary optimization" \
    --days 30 --max 30 --out digest.md
```

Try the offline demo (uses the bundled sample feed):

```bash
paperlens demo --out examples/sample-digest.md
```

Example digest output:

```markdown
# PaperLens Digest

Generated: 2026-01-15 · 5 papers

## cs.CL

### Efficient Attention Mechanisms for Long-Context Language Models
**Authors:** Sofia Rossi, Ken Watanabe · **Published:** 2026-01-05 · **arXiv:** [2601.04567](https://arxiv.org/abs/2601.04567)

We study attention mechanisms that scale to contexts of one million tokens
and beyond. By combining sliding-window attention with a small set of global
landmark tokens, our method reduces the memory footprint of the key–value
cache by an order of magnitude while matching the perplexity of full
attention on standard benchmarks…
```

## Configuration

Pass `--config config.json` to either subcommand. All fields are optional:

```json
{
  "keywords": ["multimodal", "vision-language"],
  "weights": { "title": 3.0, "abstract": 1.0 },
  "keyword_groups": [
    { "name": "Multimodal LLMs", "keywords": ["multimodal", "vision-language"] },
    { "name": "Optimization", "keywords": ["scheduling", "evolutionary"] }
  ]
}
```

| Field            | Meaning                                                                 |
| ---------------- | ----------------------------------------------------------------------- |
| `keywords`       | Extra keywords merged with `--query`; used for ranking and the query.   |
| `weights.title`  | Score weight for a keyword hit in the title (default `3.0`).            |
| `weights.abstract` | Score weight for a keyword hit in the abstract (default `1.0`).       |
| `keyword_groups` | Topic groups for the digest. A paper joins the first group whose keyword appears in its title or abstract; unmatched papers fall back to their arXiv primary category. |

## Project structure

```
paperlens/
├── paperlens/
│   ├── __init__.py        # package metadata
│   ├── __main__.py        # python -m paperlens entry point
│   ├── arxiv_client.py    # arXiv API query building, fetching, Atom parsing
│   ├── rank.py            # deduplication, relevance scoring, date filtering
│   ├── render.py          # Markdown digest rendering and topic grouping
│   ├── sample_data.py     # bundled sample Atom feed for demo mode and tests
│   └── cli.py             # argument parsing and subcommands
├── tests/
│   └── test_paperlens.py  # unittest suite (parsing, ranking, rendering)
├── examples/
│   └── sample-digest.md   # example output produced by demo mode
├── pyproject.toml
└── README.md
```

## Roadmap

- [ ] Scheduled digest generation (weekly cron-friendly mode)
- [ ] Additional sources: Semantic Scholar and OpenAlex APIs
- [ ] BibTeX export alongside the Markdown digest
- [ ] HTML output theme for publishing digests as web pages
- [ ] Saved "watchlists" with per-topic config files

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Ruizhao Zheng.
