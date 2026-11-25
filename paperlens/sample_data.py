"""A small sample arXiv Atom feed, bundled for offline demo mode and tests.

The entries are fictional, but the XML follows the real arXiv API Atom
format (including the ``arxiv`` extension namespace) so the parser is
exercised exactly as it would be against the live API.
"""

SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <title>ArXiv Query: search_query=all:"multimodal" OR all:"optimization"</title>
  <id>http://arxiv.org/api/sample-feed</id>
  <updated>2026-01-15T00:00:00Z</updated>

  <entry>
    <id>http://arxiv.org/abs/2601.01234v1</id>
    <updated>2026-01-12T09:30:00Z</updated>
    <published>2026-01-12T09:30:00Z</published>
    <title>Evidence-Driven Multimodal Fusion for Medical Image Diagnosis</title>
    <summary>Multimodal models that combine imaging, laboratory values, and clinical
notes often fail silently when one modality is missing or contradictory. We propose
an evidence-driven fusion framework that gathers modality-specific evidence before
committing to a diagnosis, and explicitly reports which evidence supports each
candidate condition. On two public benchmarks the method improves diagnostic
accuracy under missing-modality conditions by a large margin, while producing
auditable evidence trails that clinicians can inspect.</summary>
    <author><name>Haoran Li</name></author>
    <author><name>Mei Chen</name></author>
    <author><name>Jonas Weber</name></author>
    <link href="http://arxiv.org/abs/2601.01234v1" rel="alternate" type="text/html"/>
    <link href="http://arxiv.org/pdf/2601.01234v1" rel="related" type="application/pdf" title="pdf"/>
    <category term="cs.CV" scheme="http://arxiv.org/schemas/atom"/>
    <category term="cs.AI" scheme="http://arxiv.org/schemas/atom"/>
    <arxiv:primary_category term="cs.CV"/>
  </entry>

  <entry>
    <id>http://arxiv.org/abs/2601.02345v1</id>
    <updated>2026-01-10T14:05:00Z</updated>
    <published>2026-01-10T14:05:00Z</published>
    <title>Reinforcement Learning Assisted Evolutionary Optimization for Production Scheduling</title>
    <summary>We present a hybrid framework in which a reinforcement learning agent
guides the variation operators of an evolutionary algorithm for flexible job-shop
scheduling. The agent learns, from instance features, when to favour exploration
over exploitation, which substantially reduces the number of generations needed
to reach high-quality schedules. Experiments on standard benchmarks show consistent
improvements over both pure evolutionary optimization and recent learning-based
schedulers, especially on large instances with tight due dates.</summary>
    <author><name>Xiaoyu Wang</name></author>
    <author><name>Priya Nair</name></author>
    <link href="http://arxiv.org/abs/2601.02345v1" rel="alternate" type="text/html"/>
    <link href="http://arxiv.org/pdf/2601.02345v1" rel="related" type="application/pdf" title="pdf"/>
    <category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
    <category term="math.OC" scheme="http://arxiv.org/schemas/atom"/>
    <arxiv:primary_category term="cs.LG"/>
  </entry>

  <entry>
    <id>http://arxiv.org/abs/2601.03456v2</id>
    <updated>2026-01-09T11:20:00Z</updated>
    <published>2026-01-08T08:15:00Z</published>
    <title>Graph Neural Networks for Engineering Design Change Propagation</title>
    <summary>Engineering design changes rarely stay local: modifying one component
can force adjustments across an entire product structure. We model the product
as a heterogeneous graph and train a graph neural network to predict change
propagation paths and their coordination cost. The model supports engineers in
choosing change plans that minimise ripple effects, and it outperforms
rule-based propagation analysis on two industrial case studies.</summary>
    <author><name>Tomás Silva</name></author>
    <author><name>Yuki Tanaka</name></author>
    <author><name>Haoran Li</name></author>
    <link href="http://arxiv.org/abs/2601.03456v2" rel="alternate" type="text/html"/>
    <link href="http://arxiv.org/pdf/2601.03456v2" rel="related" type="application/pdf" title="pdf"/>
    <category term="cs.AI" scheme="http://arxiv.org/schemas/atom"/>
    <category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
    <arxiv:primary_category term="cs.AI"/>
  </entry>

  <entry>
    <id>http://arxiv.org/abs/2601.04567v1</id>
    <updated>2026-01-05T16:40:00Z</updated>
    <published>2026-01-05T16:40:00Z</published>
    <title>Efficient Attention Mechanisms for Long-Context Language Models</title>
    <summary>We study attention mechanisms that scale to contexts of one million
tokens and beyond. By combining sliding-window attention with a small set of
global landmark tokens, our method reduces the memory footprint of the key-value
cache by an order of magnitude while matching the perplexity of full attention
on standard benchmarks. We release an open implementation and an evaluation
suite covering retrieval, summarisation, and code completion at long contexts.</summary>
    <author><name>Sofia Rossi</name></author>
    <author><name>Ken Watanabe</name></author>
    <link href="http://arxiv.org/abs/2601.04567v1" rel="alternate" type="text/html"/>
    <link href="http://arxiv.org/pdf/2601.04567v1" rel="related" type="application/pdf" title="pdf"/>
    <category term="cs.CL" scheme="http://arxiv.org/schemas/atom"/>
    <category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
    <arxiv:primary_category term="cs.CL"/>
  </entry>

  <entry>
    <id>http://arxiv.org/abs/2512.05678v1</id>
    <updated>2025-12-28T10:00:00Z</updated>
    <published>2025-12-28T10:00:00Z</published>
    <title>Uncertainty Quantification for Multiobjective Optimization under Noisy Evaluations</title>
    <summary>Multiobjective optimization with expensive, noisy evaluations needs
principled ways to reason about uncertainty on the Pareto front. We propose a
Bayesian framework that maintains a probabilistic model of the objective space
and selects new evaluations by expected hypervolume improvement adjusted for
estimation risk. The approach is evaluated on engineering design problems where
each evaluation is a costly simulation, and it reaches reliable fronts with
far fewer evaluations than deterministic baselines.</summary>
    <author><name>Priya Nair</name></author>
    <author><name>Marco Bianchi</name></author>
    <link href="http://arxiv.org/abs/2512.05678v1" rel="alternate" type="text/html"/>
    <link href="http://arxiv.org/pdf/2512.05678v1" rel="related" type="application/pdf" title="pdf"/>
    <category term="math.OC" scheme="http://arxiv.org/schemas/atom"/>
    <category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
    <arxiv:primary_category term="math.OC"/>
  </entry>

  <entry>
    <id>http://arxiv.org/abs/2511.06789v1</id>
    <updated>2025-11-15T13:25:00Z</updated>
    <published>2025-11-15T13:25:00Z</published>
    <title>A Survey of Vision-Language Models for Clinical Decision Support</title>
    <summary>Vision-language models are increasingly proposed as assistants for
clinical decision support, yet their evaluation remains fragmented across tasks,
datasets, and safety criteria. This survey organises the recent literature by
clinical workflow stage, compares evaluation protocols, and identifies open
problems in calibration, evidence grounding, and deployment monitoring. We argue
that multimodal systems should be judged not only on answer accuracy but also
on the quality and traceability of the evidence they cite.</summary>
    <author><name>Mei Chen</name></author>
    <author><name>David Okafor</name></author>
    <link href="http://arxiv.org/abs/2511.06789v1" rel="alternate" type="text/html"/>
    <link href="http://arxiv.org/pdf/2511.06789v1" rel="related" type="application/pdf" title="pdf"/>
    <category term="cs.CL" scheme="http://arxiv.org/schemas/atom"/>
    <category term="cs.CV" scheme="http://arxiv.org/schemas/atom"/>
    <arxiv:primary_category term="cs.CL"/>
  </entry>
</feed>
"""


def get_sample_xml() -> str:
    """Return the bundled sample Atom feed as an XML string."""
    return SAMPLE_XML
