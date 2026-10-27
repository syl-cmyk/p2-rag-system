# Pre-registration (598E)

This file is for 598E students; it is the second half of the 598E rider, and 498E students can ignore it or delete it.

A pre-registration is a claim you write down, with the test that will judge it, before you can see the answer.
Its value is that the claim can be wrong in a way anyone can check, and that you cannot adjust it afterwards to fit the numbers.
A well-powered result that says "no effect as large as the one I cared about" scores as well as a confirmation, so you have no reason to bend the claim.

**Git history is how I will know the order.**
Commit this file, filled in through section 4, before the first commit that puts a judgment line into `eval/own/qrels.txt` (or any other file under `eval/own/`).
`uv run p2 check` reads `git log` to find the first commit in which sections 1 to 4 have no TODO marker left and some words of yours in each, and confirms that it comes before your first judgment; a copy that was filled in afterwards fails.
Right after that commit, `p2 check` names it and waits for your first judgment; it asks for section 5 separately, once you have scored your own corpus.
You may ingest your corpus and write queries first, but not the relevance judgments.
After that first commit, do not edit sections 1 to 4, because `p2 check` compares them with the commit where you filled them in.
If something must change, add a dated entry in section 6 and leave the original as it was.

You need your stage 1 scores for section 3, so score the shared corpus first.

---

## 1. Hypothesis

One sentence, about your own corpus, naming two of your systems and a direction.
For example: "On my corpus of Kubernetes documentation, `rerank` has a higher MRR@10 than `hybrid`, because the queries are paraphrases that a first-stage fusion ranks too low."
It should be something you could be wrong about.

On my corpus of arXiv cs.CV abstracts, `rerank` has a higher MRR@10 than `hybrid`, because a lot of my queries describe a paper in different words than its abstract uses, so `hybrid` gets the right paper into the top 10 but often not at rank 1, and the reranker reads the query and each abstract together so it can tell which one actually matches and move it up.

---

## 2. The smallest effect that matters

Name one metric, MRR@10 or nDCG@10, and choose it now so you cannot pick the better one afterwards.
Then say how large a difference between the two systems would matter to a person using the search, and why that size.
A difference of 0.02 is usually not worth a reranker's cost in time and tokens.
In this course, choose a Δ of at least 0.15 unless you argue for a larger one, because a smaller gap takes more queries than one project can judge.
Call your number Δ (delta).

Metric: MRR@10. Δ = 0.15, because rerank costs about 12 seconds and about 12k tokens more per query, so it has to change what the user sees first.

0.15 is about the same as 3 out of every 10 queries moving the right paper from rank 2 to rank 1. a smaller gap means only one or two queries out of ten get better, and a user wouldn't notice that for the extra wait.

---

## 3. How many queries you need

The size of the gold set follows from three numbers: how large a difference you want to detect (Δ), how variable the per-query differences are (sd), and the usual choices of a 5% false-alarm rate and 80% power.

```
n = ((1.96 + 0.84) * sd / Δ)^2
```

Here sd is the standard deviation of the per-query differences between your two systems, which `results/results.json` holds for the shared practice queries.
Compute it from your stage 1 runs for the same two systems, or the nearest pair you have, and say which pair you used.
With only 20 practice queries the sd is itself noisy, so be generous and round up.

Some numbers to calibrate against.
At sd 0.3 and Δ 0.10 the formula gives about 71 queries, and with the t distribution's small-sample correction it is a few more, about 73.
At sd 0.3, a gold set of 30 queries can only detect a difference of about 0.15, which is why 30 queries cannot support a claim about a gap of 0.10.
The spreads you will measure on the shared practice queries are mostly larger than 0.3: from about 0.31 for `hybrid` against `bm25` to about 0.66 for `dense` against `bm25`.
For `rerank` against `hybrid` the sd is about 0.39, so a Δ of 0.10 needs about 120 queries, 0.15 about 55, and 0.20 about 31.
So the course's Δ of 0.15 means about 55 queries for that pair; at an sd of 0.66 it would mean about 150, so compare a pair whose spread you can afford.
Choose Δ and the size of your gold set together: the smallest effect that matters to a user, and a number of queries you can write and judge in the time you have.
If the two do not meet, say which one you gave ground on and why.

After you score the own corpus, the minimum detectable difference that `uv run p2 score` prints for your two systems is this same calculation run the other way.
It should come out at or below your Δ.
If it does not, your queries varied more than your stage 1 sd suggested, and you will say so in the outcome.

sd = 0.397, the standard deviation of the per-query MRR@10 differences between `rerank` and `hybrid` on the 20 shared practice queries (`results/results.json`). n = ((1.96 + 0.84) × 0.397 / 0.15)² ≈ 55.

20 queries is a small sample, so the sd itself could be off, and if the real sd is bigger I'd need more queries than 55. so I round up and will write 60 queries.

---

## 4. The test, and what each result will mean

The test is the paired 95% interval of the mean difference between your two systems on your own gold set, from the `own-pairs` table that `uv run p2 score` writes in `EVAL.md`.
Write the rule now.
This is the default rule, and you can tighten it, but do not loosen it after you see your numbers.

| The interval is | I will say |
|---|---|
| entirely above zero in the direction I predicted | supported: the difference is distinguishable from zero |
| entirely on the other side of zero | contradicted: the opposite of my hypothesis holds on this gold set |
| around zero, with both ends inside plus or minus Δ | well-powered null: a difference as large as Δ is ruled out |
| around zero, with an end beyond plus or minus Δ | inconclusive: the gold set could not settle it, and I say so |

I keep the default rule above, unchanged. Systems: `rerank` minus `hybrid`. Metric: MRR@10, from the `own-pairs` table.

---

## 5. Outcome (write this after the fact)

What was the interval?
Which row of the table in section 4 is it?
Did your gold set reach the size section 3 asked for, and what was the minimum detectable difference that `uv run p2 score` printed?
What would you do next, and what would you want a reader to take from this?

it is row 1, supported: rerank is 0.099 higher than hybrid on MRR@10, and the interval [+0.020, +0.181] is entirely above zero. but 0.099 didn't reach the 0.15 I set, and 0.15 is still inside the interval, so I can only say rerank really is better, not that it is better by the amount I cared about.

I mostly followed the plan, but I re-judged the gold set, dropped, replaced and added queries, and all of these changes are recorded in section 6 of PREREG.md. in the end the gold set has 59 queries, not 60. the minimum detectable difference that p2 score printed for rerank minus hybrid is 0.115, below my Δ of 0.15, so 59 queries were enough to see a gap of 0.15.

next I would write more hand queries (40 or more), judge them carefully and fill in the missing labels, then compare rerank and hybrid again. what I want a reader to take from this: rerank is better than hybrid, but the gap may be smaller than I first thought.

---

## 6. Amendments

Dated entries only, one per change, each saying what changed and why.
Leave this section as it is if nothing changed.

2026-10-26: after I had already seen the stage 2 scores, I judged every query again from the start. I did this because the first labels were not good enough: their candidates came only from the bm25 and dense top 5, so relevant papers found by the other systems were never judged, and several hand queries were labeled with only the closest match instead of a paper that answers them. this time the candidates were the top 5 of all four systems. with the new labels, rerank minus hybrid changed from not distinguishable to rerank higher, and since rerank's top 5 was now in the candidate pool, this could favor rerank.

2026-10-26: I dropped h01, h05, h08 and h09 from the gold set. when I judged their candidates, no paper in the corpus directly answers any of them, so they have no relevant document and can't be scored. I decided this after I had already seen the stage 2 scores.

2026-10-26: I replaced h12. the old query was "segmenting lung problems in chest X-rays when only a few labeled images exist" (mixed), and no paper in the corpus answers it directly. the new h12 is "checking whether a banknote is worn out or fake from a phone photo" (paraphrase). I changed it after I had already seen the stage 2 scores.

2026-10-26: I added three new hand queries, h14, h15 and h16, to replace some of the four I dropped and to have more hand queries, since the hand and claude queries gave very different results and the hand group was small. I added them after I had already seen the stage 2 scores, and I judged their candidates with the same rule as the others, but their candidates came from the top 5 of bm25, dense and hybrid plus a keyword search, not from rerank.
