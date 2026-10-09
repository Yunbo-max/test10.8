# Sampling-source qualification and conservative recourse fallback

Status: accepted after correction re-review at immutable candidate commit
`b8651edf183ff8103aa97823c044d79a9b9cef99`; **not** an implementation,
native run, complete theorem repair certificate, or paper claim.

## Frozen primary sources

1. Vladimir Braverman, Petros Drineas, Cameron Musco, Christopher Musco,
   Jalaj Upadhyay, David P. Woodruff, Samson Zhou, *Near Optimal Linear Algebra
   in the Online and Sliding Window Models*, arXiv:1805.03765v6 (11 April
   2023), <https://arxiv.org/html/1805.03765v6>.
2. David Woodruff and Samson Zhou, *Consistent Low-Rank Approximation*, official
   ICLR 2026 PDF, paper identifier b14d76c7266be21b338527cd25deac45,
   <https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf>.

The arXiv version is recorded explicitly.  It must not be silently represented
as byte-identical to an earlier conference version.

## What the PCP source actually supplies

Braverman et al. define the online condition number of a row stream as the
maximum condition number over its prefixes.  Their online rank-`k` projection-
cost preserving (PCP) result has weighted sampled rows and size

\[
  s=O\!\left(k\eta^{-2}\log n\,\log^2\kappa\right),
\]

with high probability.  The source also states the online, all-prefix use of
the coreset: for every prefix, the sampled prefix is a PCP for the corresponding
input prefix.  This is the property needed for a consistent online algorithm;
a guarantee only for the final matrix would not suffice.

The target paper reproduces this result as its Theorem 2.4 (attributed there to
Braverman et al., Theorem 3.1), then specializes to polynomial online condition
number, so `log^2 kappa = O(log^2 n)` and

\[
  s=O\!\left(k\eta^{-2}\log^3 n\right).
\]

The already-reviewed consecutive-row condition supplement is stronger than
the online-prefix condition needed for this particular source theorem.  That
supplement therefore admits the alternating construction to this assumption;
it is not evidence about the random sampler's implementation or success event.

## Loss transfer and parameter calibration

Write `cost_A(P)=||A(I-P)||_F^2` for a rank-`k` projector `P`.  A multiplicative
PCP with parameter `eta` gives, simultaneously for relevant `P`,

\[
 (1-\eta)\,\operatorname{cost}_A(P)
 \leq \operatorname{cost}_C(P)
 \leq (1+\eta)\,\operatorname{cost}_A(P).
\]

If `P_C` minimizes the coreset cost and `P_A` minimizes the input cost, then

\[
 \operatorname{cost}_A(P_C)
 \leq \frac{1+\eta}{1-\eta}\operatorname{cost}_A(P_A).
\]

Choosing `eta = epsilon/(2+epsilon)` makes the ratio exactly `1+epsilon`.
Thus `eta^{-2}=Theta(epsilon^{-2})` for the usual bounded-accuracy regime.  A
claim using the same symbol without this calibration would hide a constant-
factor accuracy mismatch.

## Conservative recourse fallback after failure of the constant-eight lemma

For any two rank-`k` orthogonal projectors,

\[
 \|P-Q\|_F^2
 =2k-2\operatorname{tr}(PQ)
 \leq 2k.
\]

For one run of the theoretical sampler, define the joint high-probability event

\[
 \mathcal E=\{\text{every sampled prefix is a PCP for its input prefix}\}
 \cap\{|M_n|\leq s\}.
\]

Algorithm 5 in Braverman et al. appends an accepted row to `M` once and never
deletes, replaces or resamples an existing row.  If the output projector is a
fixed deterministic function of the current coreset, rejected rows do not
change it.  Consequently the number of output-changing events is at most the
number of accepted rows, and on `E` it is at most `s`.  Summing the universal
projector diameter over those events gives, on `E`,

\[
  \operatorname{Recourse}
  =\sum_t\|P_t-P_{t-1}\|_F^2
  \leq 2ks
  =O\!\left(k^2\epsilon^{-2}\log^3 n\right)
\]

under polynomial online condition number and the calibrated PCP accuracy.

This is not an unconditional deterministic asymptotic bound: both simultaneous
all-prefix PCP validity and `|M_n|<=s` are components of the high-probability
event `E`.  The event accounting is source-qualified for the *theoretical*
append-only Algorithm 5; the project's executable implementation, its random
choices and exact correspondence to that pseudocode remain separate admission
items.  For a general streaming coreset, a space bound alone does not bound the
number of replacements or resampling events.

## Claim boundary

- Qualified at source/statement level: the online-condition definition, the
  all-prefix PCP guarantee, the asymptotic coreset size, and the target paper's
  use of these facts.
- Qualified algebraically on the explicitly stated joint high-probability event:
  the
  `O(k^2 epsilon^-2 log^3 n)` universal-diameter fallback.
- Not qualified here: executable sampler code, probability constants, random
  seed handling, native scoring parity, or an empirical result.
- Not claimed: that the target Theorem 1.2 existence statement is false.  The
  finite and dynamic counterexamples invalidate its displayed rank-independent
  constant-eight proof route.  A different rank-linear construction is not
  ruled out.
- Not novel: the quadratic-in-`k` fallback is the immediate projector-diameter
  argument and is treated only as a repaired baseline.

## Independent-review questions

1. Do the cited version and statements really provide a simultaneous
   all-prefix PCP guarantee and the stated online condition definition?
2. Is the target paper's Theorem 2.4-to-Theorem 1.2 dependency represented
   without strengthening either source?
3. Is the PCP loss-transfer calibration exact?
4. Does theoretical Algorithm 5 support the append-only event count, is the
   joint high-probability event stated correctly, and is executable parity
   still kept pending?
5. Does the claim boundary avoid converting a proof failure into a refutation
   of the theorem's existence statement?
