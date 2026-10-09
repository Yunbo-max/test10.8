# Independent review record: integer-input density extension

## Reviewed immutable inputs

- Reviewer: `/root/integer_density_review`
- Candidate commit: `8f35727ad9e096e58936d30437285d01321793ee`
- Candidate Git blob: `7f8ec76f897d1d6e3364cae6c7939be03f745111`
- Candidate SHA256: `23888855caa586065d61070a46115c8968496b38bf8b009ae719d489b0e7232f`
- Assignment commit: `d8552ad0318b088b636559ecb6815c0bfa8f4352`
- Base SHA256 independently verified:
  `0cbf0413e49df6f81e135219f0cb6ea994129167d2f900dfc5594bdb0d90d477`

## First verdict: `needs_correction`

The reviewer accepted the fixed-`k` integer existence proof:

1. the two covariance maps are continuous;
2. the positive cutoff gaps persist jointly and the Riesz projectors are
   continuous;
3. strict `F>8` plus rational density gives a rational pair preserving
   uniqueness and the inequality; and
4. one common denominator preserves the row-arrival relation, both projectors,
   gap signs and recourse.

The reviewer rejected the first draft's dynamic inference.  That draft fixed
only `k=2^210` and retained only `F>8`.  Repetition of one fixed pair remains
`O(L)` with a fixed constant, so it does not exclude every rank-independent
linear constant.

## Required correction

For every `k`, integerize the v2 pair in a neighborhood retaining
`F_k>H_k/18`.  With `N=2k` and `N^2` alternating insert/delete updates, retain

$$
\operatorname{Recourse}/L
>\frac{N}{N+1}\frac{H_k}{18}
>H_k/36\to\infty.
$$

State conditioning over the same separately integerized family by intersecting
the finitely many relevant open neighborhoods.  Common scaling preserves
condition ratios, but there is no polynomial bound on denominator, integer
magnitude or bit length.

## Official-source scope checked by the reviewer

The official Theorem 2.2 is stated for exact-optimal maintenance under row
insertions/deletions with total recourse `O(n)` and no entry-magnitude,
bit-complexity or condition parameter; its proof is presented as an immediate
use of Lemma 2.1's explicit constant 8.  Theorem 1.3 is separately approximate
and explicitly has a bounded-integer-magnitude parameter.  Therefore the
corrected arbitrary-`k` integer family may target the rank/dimension-uniform
reading of Theorem 2.2, but it does not target Theorem 1.3.

## Re-review status

`accepted`.

- Corrected candidate commit:
  `e6ca030dae13084a116659a78d8f1e680e862b95`
- Candidate Git blob: `d4a368b87c97dc7e3ba4f6c4f66356f15fdf373a`
- Candidate SHA256:
  `ef0fed96c2db6bfd22f26325d3a97d8c25e7228daf8ae42a751270a1df3a6c86`
- Assignment commit: `b3e203a9473492c937bf3418bfab7864dba81a89`
- Assignment blob: `2bd9a22da296cc3f4d35b701a0e625ea3166ce5f`
- Assignment SHA256:
  `07a04387b4cf3185c16c9a6b6cf8bc82657a0403d88d6fb628c8ca32e1908c88`

The reviewer verified the arbitrary-`k` continuity/density quantifier, common
denominator scaling, `N^2`-toggle averaging and family-level conditioning.  For
the full augmented rectangular block, the reviewer noted that
`sigma_min([B;v]) >= sigma_min(B)` supplies direct control.  The record retains
the lack of any polynomial `q_k`, `M_k` or bit-length bound and the explicit
non-implication for Theorem 1.3.  No files or numerical experiments were
created by the reviewer.  The initial `needs_correction` verdict above remains
part of the history.
