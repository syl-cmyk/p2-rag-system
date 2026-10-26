"""Hybrid retrieval (stage 1): reciprocal rank fusion of bm25 and dense.

Ported from rrf() in the 13 lab's pipeline.py: each document scores the sum of 1 / (k + rank) over
the two rankings, with k = 60. Both rankings are full (every document, or every chunk), so a
document that is 11th in both lists can still reach the fused top 10.
"""

from __future__ import annotations

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False

RRF_K = 60
PARTS = ("bm25", "dense")


def rrf(rankings, k=RRF_K):
    """Fuse rankings of (id, score) pairs, best first, into one list of (id, fused score)."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, (item, _) in enumerate(ranking, 1):
            scores[item] = scores.get(item, 0.0) + 1 / (k + rank)
    return order(scores.items())


class Hybrid:
    def __init__(self, corpus, cfg):
        self.parts = [retrievers.build(name, corpus, cfg) for name in PARTS]
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(corpus.chunks(cfg.chunk_words, cfg.chunk_overlap))

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        return rrf([p.search(text, self.n_docs) for p in self.parts])[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        return rrf([p.search_chunks(text, self.n_chunks) for p in self.parts])[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
