"""Dense retrieval (stage 1): embed every chunk once, embed the query, and rank chunks by cosine similarity.

Ported from the 12 lab's retrieve.py (load_bge, cached_doc_vectors, dense_rankings), but over chunks
instead of whole articles, through the helpers in p2/embed.py.
The embedder is bge-small-en-v1.5 unless p2.toml has a [dense] table with model = "...".
"""

from __future__ import annotations

from p2 import embed
from p2.retrievers import ChunkScorer

NEEDS_CLAUDE = False


class Dense(ChunkScorer):
    def __init__(self, corpus, cfg):
        super().__init__(corpus, cfg)
        self.model = cfg.table("dense").get("model", embed.BGE)
        self.embedder = embed.load(self.model)
        # one unit-length row per chunk, cached in .cache/vectors/ so later runs skip the encoding
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)

    def score_chunks(self, text: str) -> list[float]:
        if not self.chunks:
            return []
        query = embed.unit(self.embedder.encode([text]))[0]
        # every row has length 1, so the dot product is the cosine similarity
        return (self.vectors @ query).tolist()


def build(corpus, cfg):
    return Dense(corpus, cfg)
