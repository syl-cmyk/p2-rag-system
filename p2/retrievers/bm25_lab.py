"""Ablation of bm25: the 12 lab's tokenizer instead of "codes", everything else the same.

"codes" keeps a hyphenated name such as GACO-CAD whole (gaco-cad) as well as its parts (gaco, cad);
"lab" keeps only the parts. Same chunks, same k1 and b, same index.
"""

from __future__ import annotations

from p2.retrievers.bm25 import BM25

NEEDS_CLAUDE = False
BASE = "bm25"


def build(corpus, cfg):
    return BM25(corpus, cfg.replace(tokenizer="lab"))
