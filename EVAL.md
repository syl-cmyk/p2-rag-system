# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

dense uses bge-small-en-v1.5. it cuts each document into 300-word chunks, ranks them by cosine similarity (how close the meaning is), and a document's score is the score of its best chunk. lab 12 ranked whole documents, and here I changed it to rank chunks.

hybrid merges the bm25 and dense rankings with RRF (k = 60). each document gets 1/(60 + rank) from each of the two rankings and the two are added up. it merges the full rankings, not only the top 10.

rerank takes the top 20 from hybrid and gives them to Claude to reorder, with only the first 600 characters of each document. Claude has to return each number from 1 to 20 exactly once (this limit is something I added on top of the lab version). if the reply is in the wrong format, the hybrid order is kept.

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.592 | 0.471 | 0.444 |
| rerank | 0.758 | 0.775 | 0.721 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 0.500 | 0.405 | 0.917 |
| hybrid | MRR@10 | 0.514 | 0.154 | 0.792 |
| hybrid | nDCG@10 | 0.397 | 0.203 | 0.779 |
| rerank | Recall@10 | 0.714 | 0.595 | 1.000 |
| rerank | MRR@10 | 0.714 | 0.714 | 0.917 |
| rerank | nDCG@10 | 0.667 | 0.626 | 0.897 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | -0.033 | [-0.250, +0.192] | 0.324 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.036 | [-0.178, +0.084] | 0.193 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.075 | [-0.238, +0.075] | 0.228 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.033 | [-0.125, +0.192] | 0.231 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.091 | [-0.305, +0.110] | 0.300 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.036 | [-0.199, +0.113] | 0.227 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.133 | [-0.100, +0.358] | 0.340 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.268 | [+0.026, +0.508] | 0.349 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.203 | [-0.024, +0.429] | 0.328 | not distinguishable |
| rerank minus dense | Recall@10 | +0.200 | [+0.050, +0.367] | 0.224 | rerank higher |
| rerank minus dense | MRR@10 | +0.212 | [+0.071, +0.383] | 0.231 | rerank higher |
| rerank minus dense | nDCG@10 | +0.242 | [+0.109, +0.394] | 0.209 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | 0.166 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.304 | [+0.140, +0.481] | 0.249 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.278 | [+0.149, +0.413] | 0.192 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

only the rerank comparisons can be told apart. rerank is higher than the other three, but against bm25 the lower end of the interval is only +0.026, so it barely counts. dense vs bm25, hybrid vs bm25 and hybrid vs dense are all not distinguishable.

a gap has to be about 0.19 to 0.41 before 20 queries can see it. anything smaller is invisible here, but that doesn't mean the two systems are the same.

"a reranker helps" is supported: against its own first stage, hybrid, rerank is +0.304 [+0.140, +0.481], and that interval is far from zero; only the pair against bm25 barely counts. "fusing beats both alone" is not supported: hybrid has the lowest average, but its gaps are not distinguishable either, so it is left open. bm25 and dense clearly complement each other (bm25 got 0.000 on the paraphrase queries and 0.810 on identifiers, dense got 0.714 and 0.333), but RRF didn't turn that into an advantage.

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 10 of 10 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.

I answered with rerank, because on the stage 1 practice queries it was the only system that clearly beat the other three, and the other systems could not be told apart from each other. I didn't change prompts/answer.txt.

a01: mostly supported. the 15 minutes and the death are both in the quote, but in the quote the 15 minutes start from when the operator "knows or should know", and the claim says "after an accident", so it drops that condition.

a05: claim 1 is supported. claim 2 is partly supported. the 8 hours is in the quote, but the quote says the conditions should duplicate underground conditions "as closely as practicable", and the claim drops "as practicable", so it makes the rule sound stricter than the quote.

a07: claim 1 is supported. claim 2 is not supported. the two quotes only show that the same sentence appears in both 56 and 57, and neither says "metal and nonmetal". you need outside knowledge to know what parts 56 and 57 cover, and the difference between them is surface vs underground, not metal vs nonmetal.

p2 verify can only prove that the quoted text really exists, not that it supports the claim next to it. all three passed, but one claim is not supported and two are only partly supported, so verify alone is not enough, and a person still has to check that the quote and the claim match.

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

my corpus is the titles and abstracts of arXiv cs.CV papers. I picked it because I'm taking a computer vision class, so I know a bit about the field and have a lot of questions about it. I fetched them with arXiv's OAI-PMH interface (scripts/fetch_arxiv.py), for papers updated between 2025-09-01 and 2025-10-22, and only kept papers whose primary category is cs.CV and whose own license is CC BY 4.0 (1,670 papers) or CC BY-SA 4.0 (106 papers). so it comes from the arXiv option in the brief, and the license basis is each paper's own CC license.

it has 1,776 documents, about 353,000 words and 2.7 MB of text. uv run p2 license shows 0 failing and 0 flagged, and uv run p2 license --online matches all 1,776 with the license arXiv publishes. I planned about 600 papers but got 1,776, because OAI-PMH filters by the last-modified date, so older papers that were updated in that window came in too.

the one I was least sure about was 2509.17993 (StableGuard). "Copyright" is in its title, so the license check flagged it. I looked at its arXiv page, the license is CC BY 4.0, and "copyright" is just the research topic of the paper, so I kept it and marked it reviewed in the manifest.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

the gold set has 59 queries: 11 hand and 48 claude. I used the same three classes as stage 1, identifier, paraphrase and mixed, so the two corpora can be compared class by class. there are 63 judgments, and the labels are binary.

my relevance rule: a paper is relevant only if it can directly answer the query. a paper that is only related to the topic doesn't count. for example, h06 asks about face swap videos, and 2505.08437 fakes whole bodies, so I didn't label it.

the candidates for each query were the top 5 of all four systems plus the paper a claude query was drafted from, merged and sorted by docid, without showing which system found which. for h12 and h14 to h16, which I added later, the candidates were the top 5 of bm25, dense and hybrid plus a keyword search. I read the title of every candidate, and when several of them were close to the query, I read the key sentences of their abstracts to decide. I judged the gold set twice, and PREREG.md section 6 says why and what changed.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.839 | 0.737 | 0.756 |
| dense | 0.958 | 0.854 | 0.876 |
| hybrid | 0.915 | 0.836 | 0.848 |
| rerank | 0.983 | 0.935 | 0.940 |
| ablation/bm25_lab | 0.856 | 0.749 | 0.769 |

59 judged queries; nDCG uses binary labels; a random ranking of the 1,776 documents would get recall@10 near 0.006.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | identifier (n=17) | paraphrase (n=23) | mixed (n=19) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.630 | 0.947 |
| bm25 | MRR@10 | 0.971 | 0.427 | 0.905 |
| bm25 | nDCG@10 | 0.977 | 0.461 | 0.915 |
| dense | Recall@10 | 1.000 | 0.913 | 0.974 |
| dense | MRR@10 | 0.950 | 0.757 | 0.885 |
| dense | nDCG@10 | 0.954 | 0.794 | 0.905 |
| hybrid | Recall@10 | 1.000 | 0.804 | 0.974 |
| hybrid | MRR@10 | 1.000 | 0.638 | 0.929 |
| hybrid | nDCG@10 | 0.991 | 0.668 | 0.939 |
| rerank | Recall@10 | 1.000 | 0.957 | 1.000 |
| rerank | MRR@10 | 0.971 | 0.855 | 1.000 |
| rerank | nDCG@10 | 0.975 | 0.869 | 0.996 |
| ablation/bm25_lab | Recall@10 | 1.000 | 0.674 | 0.947 |
| ablation/bm25_lab | MRR@10 | 0.971 | 0.456 | 0.905 |
| ablation/bm25_lab | nDCG@10 | 0.977 | 0.496 | 0.915 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=11) | claude (n=48) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 0.727 | 0.865 | -0.137 | [-0.431, +0.125] | not distinguishable |
| bm25 | MRR@10 | 0.323 | 0.832 | -0.509 | [-0.728, -0.259] | claude higher |
| bm25 | nDCG@10 | 0.413 | 0.835 | -0.421 | [-0.638, -0.183] | claude higher |
| dense | Recall@10 | 0.955 | 0.958 | -0.004 | [-0.116, +0.083] | not distinguishable |
| dense | MRR@10 | 0.599 | 0.912 | -0.312 | [-0.547, -0.076] | claude higher |
| dense | nDCG@10 | 0.671 | 0.922 | -0.251 | [-0.440, -0.062] | claude higher |
| hybrid | Recall@10 | 0.773 | 0.948 | -0.175 | [-0.427, +0.042] | not distinguishable |
| hybrid | MRR@10 | 0.543 | 0.903 | -0.359 | [-0.593, -0.124] | claude higher |
| hybrid | nDCG@10 | 0.586 | 0.908 | -0.322 | [-0.549, -0.109] | claude higher |
| rerank | Recall@10 | 0.909 | 1.000 | -0.091 | [-0.273, +0.000] | not distinguishable |
| rerank | MRR@10 | 0.720 | 0.984 | -0.265 | [-0.508, -0.053] | claude higher |
| rerank | nDCG@10 | 0.753 | 0.983 | -0.230 | [-0.445, -0.047] | claude higher |
| ablation/bm25_lab | Recall@10 | 0.727 | 0.885 | -0.158 | [-0.452, +0.097] | not distinguishable |
| ablation/bm25_lab | MRR@10 | 0.339 | 0.843 | -0.503 | [-0.719, -0.259] | claude higher |
| ablation/bm25_lab | nDCG@10 | 0.427 | 0.848 | -0.420 | [-0.635, -0.186] | claude higher |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | -0.094 | -0.227 | +0.134 | [-0.094, +0.396] | not distinguishable |
| MRR@10 | -0.079 | -0.276 | +0.197 | [-0.134, +0.510] | not distinguishable |
| nDCG@10 | -0.088 | -0.258 | +0.170 | [-0.116, +0.454] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.36 (11 queries), claude 0.76 (48 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 11 hand and 48 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | +0.119 | [+0.042, +0.203] | 0.114 | dense higher |
| dense minus bm25 | MRR@10 | +0.116 | [+0.022, +0.213] | 0.139 | dense higher |
| dense minus bm25 | nDCG@10 | +0.120 | [+0.036, +0.208] | 0.125 | dense higher |
| hybrid minus bm25 | Recall@10 | +0.076 | [+0.017, +0.144] | 0.095 | hybrid higher |
| hybrid minus bm25 | MRR@10 | +0.098 | [+0.042, +0.161] | 0.085 | hybrid higher |
| hybrid minus bm25 | nDCG@10 | +0.092 | [+0.044, +0.146] | 0.074 | hybrid higher |
| hybrid minus dense | Recall@10 | -0.042 | [-0.093, +0.000] | 0.070 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.018 | [-0.093, +0.054] | 0.108 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.027 | [-0.094, +0.036] | 0.095 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.144 | [+0.059, +0.237] | 0.127 | rerank higher |
| rerank minus bm25 | MRR@10 | +0.198 | [+0.104, +0.298] | 0.140 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.184 | [+0.098, +0.278] | 0.130 | rerank higher |
| rerank minus dense | Recall@10 | +0.025 | [-0.034, +0.085] | 0.086 | not distinguishable |
| rerank minus dense | MRR@10 | +0.081 | [+0.001, +0.166] | 0.119 | rerank higher |
| rerank minus dense | nDCG@10 | +0.065 | [-0.006, +0.137] | 0.103 | not distinguishable |
| rerank minus hybrid | Recall@10 | +0.068 | [+0.017, +0.136] | 0.086 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.099 | [+0.020, +0.181] | 0.115 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.092 | [+0.026, +0.163] | 0.099 | rerank higher |
| ablation/bm25_lab minus bm25 | Recall@10 | +0.017 | [+0.000, +0.051] | 0.047 | not distinguishable |
| ablation/bm25_lab minus bm25 | MRR@10 | +0.011 | [+0.002, +0.023] | 0.016 | ablation/bm25_lab higher |
| ablation/bm25_lab minus bm25 | nDCG@10 | +0.013 | [+0.002, +0.030] | 0.021 | ablation/bm25_lab higher |
| ablation/bm25_lab minus dense | Recall@10 | -0.102 | [-0.186, -0.017] | 0.126 | dense higher |
| ablation/bm25_lab minus dense | MRR@10 | -0.105 | [-0.199, -0.013] | 0.135 | dense higher |
| ablation/bm25_lab minus dense | nDCG@10 | -0.106 | [-0.194, -0.023] | 0.124 | dense higher |
| ablation/bm25_lab minus hybrid | Recall@10 | -0.059 | [-0.136, +0.008] | 0.108 | not distinguishable |
| ablation/bm25_lab minus hybrid | MRR@10 | -0.087 | [-0.144, -0.035] | 0.078 | hybrid higher |
| ablation/bm25_lab minus hybrid | nDCG@10 | -0.079 | [-0.130, -0.031] | 0.072 | hybrid higher |
| ablation/bm25_lab minus rerank | Recall@10 | -0.127 | [-0.212, -0.051] | 0.120 | rerank higher |
| ablation/bm25_lab minus rerank | MRR@10 | -0.186 | [-0.282, -0.097] | 0.133 | rerank higher |
| ablation/bm25_lab minus rerank | nDCG@10 | -0.171 | [-0.259, -0.089] | 0.123 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

on 59 queries, every pair except hybrid vs dense can be told apart. rerank is higher than the other three, and bm25 is lower than the other three. but the lower end of rerank vs dense is only +0.001, almost touching zero, so that pair barely counts.

the hand and claude queries rank the systems in the same order: rerank > dense > hybrid > bm25 in both groups. but the scores are very different: every system is 0.26 to 0.51 higher on the claude queries, and bm25 has the biggest gap (0.323 vs 0.832). the reason is that Claude drafted each query from a paper, so its words overlap the paper by 0.76, against 0.36 for my hand queries (most of the words in a claude query come straight from the paper). so the claude queries are easy for every system.

my prediction in DECISIONS.md was right. rerank has the highest average and can be told apart from the other three, and bm25 is the lowest and can be told apart from the other three as well.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/bm25_lab minus bm25 | Recall@10 | +0.017 | [+0.000, +0.051] | 0.047 | not distinguishable |
| ablation/bm25_lab minus bm25 | MRR@10 | +0.011 | [+0.002, +0.023] | 0.016 | ablation/bm25_lab higher |
| ablation/bm25_lab minus bm25 | nDCG@10 | +0.013 | [+0.002, +0.030] | 0.021 | ablation/bm25_lab higher |
| ablation/bm25_lab minus dense | Recall@10 | -0.102 | [-0.186, -0.017] | 0.126 | dense higher |
| ablation/bm25_lab minus dense | MRR@10 | -0.105 | [-0.199, -0.013] | 0.135 | dense higher |
| ablation/bm25_lab minus dense | nDCG@10 | -0.106 | [-0.194, -0.023] | 0.124 | dense higher |
| ablation/bm25_lab minus hybrid | Recall@10 | -0.059 | [-0.136, +0.008] | 0.108 | not distinguishable |
| ablation/bm25_lab minus hybrid | MRR@10 | -0.087 | [-0.144, -0.035] | 0.078 | hybrid higher |
| ablation/bm25_lab minus hybrid | nDCG@10 | -0.079 | [-0.130, -0.031] | 0.072 | hybrid higher |
| ablation/bm25_lab minus rerank | Recall@10 | -0.127 | [-0.212, -0.051] | 0.120 | rerank higher |
| ablation/bm25_lab minus rerank | MRR@10 | -0.186 | [-0.282, -0.097] | 0.133 | rerank higher |
| ablation/bm25_lab minus rerank | nDCG@10 | -0.171 | [-0.259, -0.089] | 0.123 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/bm25_lab against bm25 (BASE = "bm25" in p2/retrievers/bm25_lab.py): it helped 4 queries, hurt 1 and left 54 unchanged.

| Query | Class | Origin | bm25 RR | ablation/bm25_lab RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| c17 | paraphrase | claude | 0.000 | 0.200 | +0.200 | helped |
| h16 | paraphrase | hand | 0.143 | 0.333 | +0.190 | helped |
| c18 | paraphrase | claude | 0.333 | 0.500 | +0.167 | helped |
| c22 | paraphrase | claude | 0.125 | 0.250 | +0.125 | helped |
| h02 | paraphrase | hand | 0.111 | 0.100 | -0.011 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

Hypothesis: I expect bm25_lab to lower MRR@10 compared with bm25 on my corpus, because on the identifier queries with hyphenated names (c02, c03, c05, c07, c08, c12, c13, c15) it loses the rare full token like gaco-cad, and the leftover pieces like detr, lora or cad show up in lots of other papers, so the right paper can drop down, while the paraphrase queries have almost no hyphenated words, so they should stay about the same.

the one change was the bm25 tokenizer: bm25 keeps a hyphenated word as one extra whole token as well as its pieces (gaco-cad, gaco, cad), and bm25_lab keeps only the pieces. everything else stayed the same.

my hypothesis was wrong. I guessed it would get worse, but it got a little better: bm25_lab minus bm25 is +0.011 MRR@10 [+0.002, +0.023], with an MDD of 0.014, so the gain is distinguishable but very small.

the identifier queries didn't change at all (0.971 for both). after a name is split, for 7 of the 8 hyphenated names at least one piece still appears only in that one paper (gaco, mindi, cut3r and jarvis each appear in a single document), so the right paper is still found. WAVE-DETR is the exception: wave appears in 4 papers and detr in 10, but c12 still stayed at rank 1, so the other words in the query must have been enough.

the four queries it helped (c17, h16, c18, c22) are all paraphrase queries, and it hurt one (h02). the whole hyphenated word in the query, like vision-language, does not appear in the right paper at all, but it does appear in unrelated papers, which got extra points from it and moved to the top. once it is split, that whole word is gone, the unrelated papers lose those points, and the right paper moves up.

h02 has no hyphenated word, so both tokenizers split the query the same way. it moved only because the documents were tokenized differently too, which changed their lengths and how rare each word is, so my change explains it only indirectly.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|
| c32 | 2509.07049, classifying streaming image data with image distillation | 2505.03113, a survey of online lightweight vision transformers (rank 4) | label was wrong: 2509.07049 answers the query and I missed it, and 2505.03113 is a survey that doesn't answer it either | if I judged again, label 2509.07049 and drop 2505.03113 |
| h02 | 2510.04231, image registration: aligning two images so corresponding points land in the same place | 2510.16438, LightGlueStick, joint point and line matching (rank 4) | label was missing: 2510.04231 is exactly about finding corresponding points in two images and aligning them | if I judged again, label 2510.04231 as relevant too |
| h06 | 2504.04827, general face deepfake detection | 2412.12278 and 2508.08765, deepfake video detection (rank 2) | label was missing: it does detect face swaps, it just isn't specifically about video | if I judged again, label 2504.04827 as relevant too |
| h11 | 2510.09343, thermal infrared image enhancement | 2302.02030, deblurring telescope images of the night sky (rank 6) | label was wrong: the paper I labeled is not about brightening night photos, and rerank's first result isn't either, it's about infrared images | label SPICE (2510.08358), which brightens dark photos, and put "low-light" in the query |
| h14 | 2510.13316, whether GPT-4o finds the same images interesting as humans | 2509.12248, whether multimodal models understand humor in comics (not in the top 10) | ambiguous query: "GPT" and "people" in my query match the paper about interestingness (GPT 4 times, human 5 times), while the humor paper has no GPT and mentions human only once | rewrite the query to ask one thing, like "can multimodal models get the jokes in comics" |

most of these 5 failures are not the system's fault but the gold set's: for 3 of them (c32, h02, h06), rerank's first result is actually right and I just didn't label it.

also, 4 of the 5 are hand queries, so the labels for the hand queries are the least reliable, maybe because their words don't match the papers and I was more likely to miss things when judging them.

so rerank's score is probably underestimated. as a check, without changing qrels.txt, I recomputed MRR@10 with the fixes above for c32, h02 and h06: rerank goes from 0.935 to 0.969, hybrid from 0.836 to 0.856, dense from 0.854 to 0.859 and bm25 from 0.737 to 0.754, so rerank's lead over hybrid would grow from 0.099 to 0.113.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

I copied the MRR@10 numbers from the tables in sections 1 and 4 into this table.

| | stage 1, regulations, 20 queries | stage 2, my corpus, 59 queries |
|---|---|---|
| bm25 | 0.507 | 0.737 |
| dense | 0.562 | 0.854 |
| hybrid | 0.471 | 0.836 |
| rerank | 0.775 | 0.935 |
| rerank minus hybrid | +0.304 [+0.140, +0.481], distinguishable | +0.099 [+0.020, +0.181], distinguishable |

the winner didn't change. rerank wins on both, and on both it can be told apart, but its lead over hybrid shrank from 0.304 to 0.099.

the main reason every system scores higher on my corpus is that 48 of the 59 queries were written by Claude from the papers, so the queries share a lot of words with the papers and every system finds them easily. also, the abstracts are short, almost every one fits in one chunk, and there are no section numbers like in the regulations, which may make retrieval easier too.

what I tested: the difference between the hand and claude queries (the own-origins table) and the effect of the tokenizer (the ablation). what I only guessed and never tested: that short documents help dense, and that the section numbers in the regulations make retrieval harder.

20 queries can't see a gap below about 0.19 to 0.41, so the stage 1 systems that are "not distinguishable" could still be very different. on my side, only 11 of the 59 queries are hand queries, and the failure analysis found missing and wrong labels in the gold set, so it can't support the claim that rerank is also better on real users' questions.

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 199,889 | 6,440 | 205.2 | 16,657 | 537 | 17.1 |
| traces/answers-rerank.r1.jsonl | rerank | 12 | 24 | 0 | 198,490 | 6,932 | 222.5 | 16,541 | 578 | 18.5 |
| traces/answers-rerank.r2.jsonl | rerank | 12 | 24 | 0 | 202,565 | 7,032 | 222.6 | 16,880 | 586 | 18.5 |
| traces/answers-rerank.r3.jsonl | rerank | 12 | 24 | 0 | 198,686 | 6,748 | 218.9 | 16,557 | 562 | 18.2 |
| traces/own-own-rerank.jsonl | rerank | 59 | 59 | 55 | 683,453 | 25,807 | 767.6 | 11,584 | 437 | 13.0 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 20 | 233,108 | 6,808 | 212.7 | 11,655 | 340 | 10.6 |
| traces/shared-practice-rerank.r1.jsonl | rerank | 20 | 20 | 0 | 233,086 | 6,860 | 215.0 | 11,654 | 343 | 10.8 |
| traces/shared-practice-rerank.r2.jsonl | rerank | 20 | 20 | 0 | 233,556 | 6,821 | 228.1 | 11,678 | 341 | 11.4 |
| traces/shared-practice-rerank.r3.jsonl | rerank | 20 | 20 | 0 | 227,516 | 6,820 | 232.7 | 11,376 | 341 | 11.6 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 40 | 453,643 | 15,135 | 475.6 | 11,341 | 378 | 11.9 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.268 | [-0.508, -0.026] | 11,655 | 10.6 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.212 | [-0.383, -0.071] | 11,655 | 10.6 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.304 | [-0.481, -0.140] | 11,655 | 10.6 | rerank higher |
| own: bm25 minus rerank | 59 | -0.198 | [-0.298, -0.104] | 11,584 | 13.0 | rerank higher |
| own: dense minus rerank | 59 | -0.081 | [-0.166, -0.001] | 11,584 | 13.0 | rerank higher |
| own: hybrid minus rerank | 59 | -0.099 | [-0.181, -0.020] | 11,584 | 13.0 | rerank higher |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-ablation-bm25_lab.jsonl | bm25_lab | 59 | 0.07 | 1.1 |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 59 | 0.07 | 1.1 |
| traces/retrieval/own-own-dense.jsonl | dense | 59 | 0.56 | 9.4 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 59 | 0.65 | 11.0 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.03 | 1.6 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.32 | 16.0 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.26 | 13.1 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.07 | 1.8 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.47 | 11.9 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 0.57 | 14.2 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.

rider

1. the 598E rider.
2. I ran rerank three times on the shared practice queries and answered the 12 shared questions three times, asking Claude again each time, and I wrote and committed PREREG.md before judging my gold set. the files are runs/shared/rerank.practice.r1.trec to r3, answers/shared/rerank.r1.json to r3, and PREREG.md.
3. the table is repeats, in section 9.
4. the repeats show that rerank's gain over hybrid holds up across runs, but with so few questions, a perfect score on the answers doesn't mean they are really reliable (see section 9).
5. next I would write more hand queries (40 or more), judge them carefully and fill in the missing labels, then compare rerank and hybrid again. if rerank minus hybrid on the hand queries also has an interval entirely above zero, that would show rerank really helps on real users' paraphrased questions.

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
Repeated runs of rerank on shared/practice:

| Run | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| rerank.r1 | 0.733 | 0.775 | 0.711 |
| rerank.r2 | 0.746 | 0.775 | 0.713 |
| rerank.r3 | 0.758 | 0.775 | 0.722 |
| range (max minus min) | 0.025 | 0.000 | 0.011 |

| Comparison | Metric | Mean difference | 95% interval | Reading |
| --- | --- | ---: | ---: | --- |
| rerank.r1 minus hybrid | Recall@10 | +0.142 | [+0.050, +0.258] | rerank.r1 higher |
| rerank.r2 minus hybrid | Recall@10 | +0.154 | [+0.037, +0.283] | rerank.r2 higher |
| rerank.r3 minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | rerank.r3 higher |
| rerank.r1 minus hybrid | MRR@10 | +0.304 | [+0.140, +0.481] | rerank.r1 higher |
| rerank.r2 minus hybrid | MRR@10 | +0.304 | [+0.140, +0.481] | rerank.r2 higher |
| rerank.r3 minus hybrid | MRR@10 | +0.304 | [+0.140, +0.481] | rerank.r3 higher |
| rerank.r1 minus hybrid | nDCG@10 | +0.267 | [+0.136, +0.406] | rerank.r1 higher |
| rerank.r2 minus hybrid | nDCG@10 | +0.269 | [+0.134, +0.410] | rerank.r2 higher |
| rerank.r3 minus hybrid | nDCG@10 | +0.279 | [+0.150, +0.415] | rerank.r3 higher |

Repeated answers shared/rerank:

| File | Verified (in) | 95% interval | Declined (out) | 95% interval |
| --- | ---: | ---: | ---: | ---: |
| rerank.r1 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r2 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r3 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| range (max minus min) | 0.000 |  | 0.000 |  |

Each repeat answers the same questions, so the repeats are not independent trials and their counts are not pooled into one interval.
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

it holds up. across the three runs MRR@10 didn't change at all (a spread of 0.000), while the gain over hybrid is 0.304, and all three runs have intervals above zero.

there are too few questions, so a perfect score doesn't mean the answers are really reliable. 8 of 8 verified only says the verified rate is probably above about 68% [0.676, 1.000], and 4 of 4 declined only says the declined rate is probably above about 51% [0.510, 1.000]. the three repeats answer the same questions, so they are not independent and can't be pooled into 24.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

my pre-registered claim was that on my arXiv cs.CV corpus rerank has a higher MRR@10 than hybrid, with Δ = 0.15. it is row 1, supported: rerank is 0.099 higher than hybrid on MRR@10, and the interval [+0.020, +0.181] is entirely above zero. but 0.099 didn't reach the 0.15 I set, and 0.15 is still inside the interval, so I can only say rerank really is better, not that it is better by the amount I cared about.

I mostly followed the plan, but I re-judged the gold set, dropped, replaced and added queries, and all of these changes are recorded in section 6 of PREREG.md. in the end the gold set has 59 queries, not 60.

what I want a reader to take from this: rerank is better than hybrid, but the gap may be smaller than I first thought.
