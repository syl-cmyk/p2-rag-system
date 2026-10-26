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

TODO: describe your three systems.

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

TODO: write what the practice-query intervals let you claim.

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

TODO: write your answer choices and your three-answer audit.

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

TODO: describe your corpus and its license basis.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

TODO: describe your gold set and your relevance rule.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.833 | 0.773 | 0.772 |
| dense | 0.975 | 0.879 | 0.898 |
| hybrid | 0.917 | 0.856 | 0.859 |
| rerank | 0.967 | 0.907 | 0.919 |
| ablation/bm25_lab | 0.850 | 0.779 | 0.781 |

60 judged queries; nDCG uses binary labels; a random ranking of the 1,776 documents would get recall@10 near 0.006.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | identifier (n=18) | paraphrase (n=22) | mixed (n=20) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.636 | 0.900 |
| bm25 | MRR@10 | 0.963 | 0.532 | 0.867 |
| bm25 | nDCG@10 | 0.972 | 0.516 | 0.875 |
| dense | Recall@10 | 1.000 | 0.932 | 1.000 |
| dense | MRR@10 | 0.925 | 0.786 | 0.942 |
| dense | nDCG@10 | 0.941 | 0.810 | 0.957 |
| hybrid | Recall@10 | 1.000 | 0.818 | 0.950 |
| hybrid | MRR@10 | 1.000 | 0.712 | 0.883 |
| hybrid | nDCG@10 | 1.000 | 0.706 | 0.899 |
| rerank | Recall@10 | 1.000 | 0.955 | 0.950 |
| rerank | MRR@10 | 0.956 | 0.898 | 0.875 |
| rerank | nDCG@10 | 0.962 | 0.906 | 0.893 |
| ablation/bm25_lab | Recall@10 | 1.000 | 0.682 | 0.900 |
| ablation/bm25_lab | MRR@10 | 0.963 | 0.553 | 0.863 |
| ablation/bm25_lab | nDCG@10 | 0.972 | 0.543 | 0.872 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=12) | claude (n=48) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 0.639 | 0.882 | -0.243 | [-0.493, +0.000] | not distinguishable |
| bm25 | MRR@10 | 0.507 | 0.839 | -0.332 | [-0.583, -0.065] | claude higher |
| bm25 | nDCG@10 | 0.494 | 0.842 | -0.348 | [-0.569, -0.124] | claude higher |
| dense | Recall@10 | 0.958 | 0.979 | -0.021 | [-0.125, +0.062] | not distinguishable |
| dense | MRR@10 | 0.722 | 0.919 | -0.197 | [-0.368, -0.022] | claude higher |
| dense | nDCG@10 | 0.760 | 0.933 | -0.173 | [-0.300, -0.044] | claude higher |
| hybrid | Recall@10 | 0.722 | 0.965 | -0.243 | [-0.472, -0.042] | claude higher |
| hybrid | MRR@10 | 0.583 | 0.924 | -0.340 | [-0.564, -0.111] | claude higher |
| hybrid | nDCG@10 | 0.589 | 0.926 | -0.337 | [-0.548, -0.129] | claude higher |
| rerank | Recall@10 | 0.833 | 1.000 | -0.167 | [-0.417, +0.000] | not distinguishable |
| rerank | MRR@10 | 0.537 | 1.000 | -0.463 | [-0.688, -0.229] | claude higher |
| rerank | nDCG@10 | 0.606 | 0.997 | -0.391 | [-0.600, -0.193] | claude higher |
| ablation/bm25_lab | Recall@10 | 0.639 | 0.903 | -0.264 | [-0.514, -0.021] | claude higher |
| ablation/bm25_lab | MRR@10 | 0.498 | 0.850 | -0.352 | [-0.603, -0.083] | claude higher |
| ablation/bm25_lab | nDCG@10 | 0.486 | 0.855 | -0.370 | [-0.591, -0.147] | claude higher |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | -0.097 | -0.319 | +0.222 | [-0.021, +0.493] | not distinguishable |
| MRR@10 | -0.079 | -0.215 | +0.136 | [-0.158, +0.421] | not distinguishable |
| nDCG@10 | -0.091 | -0.266 | +0.175 | [-0.067, +0.413] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.32 (12 queries), claude 0.76 (48 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 12 hand and 48 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | +0.142 | [+0.061, +0.231] | 0.121 | dense higher |
| dense minus bm25 | MRR@10 | +0.107 | [+0.014, +0.202] | 0.134 | dense higher |
| dense minus bm25 | nDCG@10 | +0.126 | [+0.045, +0.213] | 0.120 | dense higher |
| hybrid minus bm25 | Recall@10 | +0.083 | [+0.017, +0.167] | 0.101 | hybrid higher |
| hybrid minus bm25 | MRR@10 | +0.083 | [+0.019, +0.149] | 0.093 | hybrid higher |
| hybrid minus bm25 | nDCG@10 | +0.086 | [+0.034, +0.142] | 0.078 | hybrid higher |
| hybrid minus dense | Recall@10 | -0.058 | [-0.117, -0.011] | 0.076 | dense higher |
| hybrid minus dense | MRR@10 | -0.024 | [-0.097, +0.048] | 0.105 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.039 | [-0.099, +0.017] | 0.084 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.133 | [+0.058, +0.219] | 0.115 | rerank higher |
| rerank minus bm25 | MRR@10 | +0.135 | [+0.052, +0.224] | 0.122 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.146 | [+0.070, +0.231] | 0.114 | rerank higher |
| rerank minus dense | Recall@10 | -0.008 | [-0.067, +0.050] | 0.085 | not distinguishable |
| rerank minus dense | MRR@10 | +0.028 | [-0.053, +0.112] | 0.120 | not distinguishable |
| rerank minus dense | nDCG@10 | +0.020 | [-0.046, +0.090] | 0.100 | not distinguishable |
| rerank minus hybrid | Recall@10 | +0.050 | [+0.011, +0.100] | 0.065 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.052 | [-0.016, +0.122] | 0.099 | not distinguishable |
| rerank minus hybrid | nDCG@10 | +0.060 | [+0.001, +0.124] | 0.088 | rerank higher |
| ablation/bm25_lab minus bm25 | Recall@10 | +0.017 | [+0.000, +0.050] | 0.047 | not distinguishable |
| ablation/bm25_lab minus bm25 | MRR@10 | +0.006 | [-0.002, +0.017] | 0.014 | not distinguishable |
| ablation/bm25_lab minus bm25 | nDCG@10 | +0.009 | [-0.002, +0.025] | 0.020 | not distinguishable |
| ablation/bm25_lab minus dense | Recall@10 | -0.125 | [-0.219, -0.039] | 0.132 | dense higher |
| ablation/bm25_lab minus dense | MRR@10 | -0.100 | [-0.195, -0.009] | 0.133 | dense higher |
| ablation/bm25_lab minus dense | nDCG@10 | -0.117 | [-0.204, -0.034] | 0.122 | dense higher |
| ablation/bm25_lab minus hybrid | Recall@10 | -0.067 | [-0.150, +0.000] | 0.113 | not distinguishable |
| ablation/bm25_lab minus hybrid | MRR@10 | -0.076 | [-0.139, -0.015] | 0.091 | hybrid higher |
| ablation/bm25_lab minus hybrid | nDCG@10 | -0.078 | [-0.133, -0.024] | 0.079 | hybrid higher |
| ablation/bm25_lab minus rerank | Recall@10 | -0.117 | [-0.197, -0.050] | 0.108 | rerank higher |
| ablation/bm25_lab minus rerank | MRR@10 | -0.128 | [-0.214, -0.050] | 0.116 | rerank higher |
| ablation/bm25_lab minus rerank | nDCG@10 | -0.137 | [-0.217, -0.066] | 0.107 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

TODO: write what your own-corpus intervals let you claim.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/bm25_lab minus bm25 | Recall@10 | +0.017 | [+0.000, +0.050] | 0.047 | not distinguishable |
| ablation/bm25_lab minus bm25 | MRR@10 | +0.006 | [-0.002, +0.017] | 0.014 | not distinguishable |
| ablation/bm25_lab minus bm25 | nDCG@10 | +0.009 | [-0.002, +0.025] | 0.020 | not distinguishable |
| ablation/bm25_lab minus dense | Recall@10 | -0.125 | [-0.219, -0.039] | 0.132 | dense higher |
| ablation/bm25_lab minus dense | MRR@10 | -0.100 | [-0.195, -0.009] | 0.133 | dense higher |
| ablation/bm25_lab minus dense | nDCG@10 | -0.117 | [-0.204, -0.034] | 0.122 | dense higher |
| ablation/bm25_lab minus hybrid | Recall@10 | -0.067 | [-0.150, +0.000] | 0.113 | not distinguishable |
| ablation/bm25_lab minus hybrid | MRR@10 | -0.076 | [-0.139, -0.015] | 0.091 | hybrid higher |
| ablation/bm25_lab minus hybrid | nDCG@10 | -0.078 | [-0.133, -0.024] | 0.079 | hybrid higher |
| ablation/bm25_lab minus rerank | Recall@10 | -0.117 | [-0.197, -0.050] | 0.108 | rerank higher |
| ablation/bm25_lab minus rerank | MRR@10 | -0.128 | [-0.214, -0.050] | 0.116 | rerank higher |
| ablation/bm25_lab minus rerank | nDCG@10 | -0.137 | [-0.217, -0.066] | 0.107 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/bm25_lab against bm25 (BASE = "bm25" in p2/retrievers/bm25_lab.py): it helped 3 queries, hurt 2 and left 55 unchanged.

| Query | Class | Origin | bm25 RR | ablation/bm25_lab RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| c17 | paraphrase | claude | 0.000 | 0.200 | +0.200 | helped |
| c18 | paraphrase | claude | 0.333 | 0.500 | +0.167 | helped |
| c22 | paraphrase | claude | 0.125 | 0.250 | +0.125 | helped |
| h12 | mixed | hand | 0.333 | 0.250 | -0.083 | hurt |
| h10 | paraphrase | hand | 0.167 | 0.143 | -0.024 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

Hypothesis: I expect bm25_lab to lower MRR@10 compared with bm25 on my corpus, because on the identifier queries with hyphenated names (c02, c03, c05, c07, c08, c12, c13, c15) it loses the rare full token like gaco-cad, and the leftover pieces like detr, lora or cad show up in lots of other papers, so the right paper can drop down, while the paraphrase queries have almost no hyphenated words, so they should stay about the same.

TODO: write the ablation: the one change, the hypothesis, the result and the claim.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|

TODO: add one row for each failure you analyzed, and write two or three sentences on the pattern you see across them.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

TODO: write the cross-corpus comparison.

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
| traces/own-own-rerank.jsonl | rerank | 60 | 60 | 0 | 701,018 | 26,398 | 785.9 | 11,684 | 440 | 13.1 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 20 | 233,108 | 6,808 | 212.9 | 11,655 | 340 | 10.6 |
| traces/shared-practice-rerank.r1.jsonl | rerank | 20 | 20 | 0 | 233,086 | 6,860 | 215.0 | 11,654 | 343 | 10.8 |
| traces/shared-practice-rerank.r2.jsonl | rerank | 20 | 20 | 0 | 233,556 | 6,821 | 228.1 | 11,678 | 341 | 11.4 |
| traces/shared-practice-rerank.r3.jsonl | rerank | 20 | 20 | 0 | 227,516 | 6,820 | 232.7 | 11,376 | 341 | 11.6 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 40 | 453,643 | 15,135 | 475.7 | 11,341 | 378 | 11.9 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.268 | [-0.508, -0.026] | 11,655 | 10.6 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.212 | [-0.383, -0.071] | 11,655 | 10.6 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.304 | [-0.481, -0.140] | 11,655 | 10.6 | rerank higher |
| own: bm25 minus rerank | 60 | -0.135 | [-0.224, -0.052] | 11,684 | 13.1 | rerank higher |
| own: dense minus rerank | 60 | -0.028 | [-0.112, +0.053] | 11,684 | 13.1 | not distinguishable |
| own: hybrid minus rerank | 60 | -0.052 | [-0.122, +0.016] | 11,684 | 13.1 | not distinguishable |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-ablation-bm25_lab.jsonl | bm25_lab | 60 | 0.07 | 1.1 |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 60 | 0.07 | 1.1 |
| traces/retrieval/own-own-dense.jsonl | dense | 60 | 0.51 | 8.4 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 60 | 0.61 | 10.1 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.03 | 1.6 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.25 | 12.6 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.28 | 14.0 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.07 | 1.8 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.43 | 10.9 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 0.55 | 13.8 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.

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

598E: write the repeats result here.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

598E: write the claim and its outcome here.
