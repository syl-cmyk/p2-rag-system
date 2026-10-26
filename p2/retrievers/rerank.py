"""Listwise reranking (stage 1): Claude reorders hybrid's top 20.

Ported from rerank_one() in the 13 lab's pipeline.py: the top 20 go to Claude as numbered passages
(each cut to 600 characters), the reply is forced into {"order": [20 numbers]}, a reply that is not
each of 1 to 20 once keeps the first-stage order, and everything below the 20 keeps its order
underneath. The schema's items also carry minimum 1 and maximum 20, so no number can name a missing
passage.
"""

from __future__ import annotations

import sys

from p2 import claude, retrievers

NEEDS_CLAUDE = True

FIRST_STAGE = "hybrid"
CANDIDATES = 20
PASSAGE_CHARS = 600

PROMPT = """Below are {n} passages from a document collection, numbered 1 to {n}, and a search query.
Order the passages from the most useful for answering the query to the least useful.
Reply with all {n} passage numbers, each exactly once, best first.

Query: {query}

{passages}"""


def schema(n: int) -> dict:
    item = {"type": "integer", "minimum": 1, "maximum": n}
    return {
        "type": "object",
        "properties": {"order": {"type": "array", "items": item, "minItems": n, "maxItems": n}},
        "required": ["order"],
    }


class Rerank:
    model: str | None = None

    def __init__(self, corpus, cfg):
        self.cfg = cfg
        self.model = cfg.model
        self.first = retrievers.build(FIRST_STAGE, corpus, cfg)
        self.doc_texts = {d: doc.text for d, doc in corpus.docs.items()}
        self.chunk_texts = corpus.chunk_texts(cfg.chunk_words, cfg.chunk_overlap)

    def rerank(self, query: str, ids: list[str], texts: dict[str, str]) -> list[str]:
        """The candidate ids in Claude's order, or in their own order if the reply is not usable."""
        passages = "\n\n".join(f"[{i}] {texts[x][:PASSAGE_CHARS]}" for i, x in enumerate(ids, 1))
        prompt = PROMPT.format(n=len(ids), query=query, passages=passages)
        reply = claude.call(prompt, schema(len(ids)), model=self.cfg.model, cache_dir=claude.cache_folder(self.cfg))
        if reply.error:
            print(f"WARNING: {reply.error}; kept the {FIRST_STAGE} order for {query[:60]!r}", file=sys.stderr)
            return ids
        order = reply.output.get("order")
        if not isinstance(order, list) or sorted(order) != list(range(1, len(ids) + 1)):
            print(f"WARNING: reply was not each of 1 to {len(ids)} once: {order}; kept the {FIRST_STAGE} order", file=sys.stderr)
            return ids
        return [ids[i - 1] for i in order]

    def reranked(self, query: str, hits: list[tuple[str, float]], texts: dict[str, str], k: int) -> list[tuple[str, float]]:
        ids = [x for x, _ in hits]
        ids = self.rerank(query, ids[:CANDIDATES], texts) + ids[CANDIDATES:]
        # scores from the new rank, so they fall as the rank rises and never tie
        return [(x, float(len(ids) - i)) for i, x in enumerate(ids)][:k]

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        return self.reranked(text, self.first.search(text, max(k, CANDIDATES)), self.doc_texts, k)

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        return self.reranked(text, self.first.search_chunks(text, max(k, CANDIDATES)), self.chunk_texts, k)


def build(corpus, cfg):
    return Rerank(corpus, cfg)
