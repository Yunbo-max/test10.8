# Prospective random baseline matrix: developmental descriptive results

Evidence boundary: this report summarizes the independently accepted archive
at remote commit `99de82eefb87be6f7e9da66f6b924fb35b801349`, tree
`1699dcadf286c7b39051b3ab037be8b10dac0db0`.  The archive blob is
`8f0595f7fa9a85b0eb6fb7616d404bfb1409fe6d`, SHA-256
`af9b40bfb131570d1d5868006d0f4193550ba087f6679bb250a65554bab1bb8e`.
It contains one prospectively frozen, unscaled 3000-by-4 integer stream with
seed 20261009 and rank 1.  It is not a reconstruction of the paper's unseeded
Figure 3 stream.

All loss ratios use `||A_t(I-P_t)||_F^2 / OPT_t`; prefix 1 is excluded because
`OPT_t` is near zero, leaving 2999 defined ratios for every arm.  Recourse is
the steady-state sum of `||P_t-P_{t-1}||_F^2`, excluding initialization from
zero.  Timings are single-run engineering observations, not benchmarks.

| Arm | Mean defined ratio | Max defined ratio | Steady recourse | Update s | Score s | Pipeline s |
|---|---:|---:|---:|---:|---:|---:|
| fresh SVD | 1.000000 | 1.000000 | 0.157747 | 0.201518 | 0.140885 | 0.596945 |
| fixed | 1.611537 | 1.772724 | 0.000000 | 0.003619 | 0.126875 | 0.374209 |
| periodic 10 | 1.001522 | 1.725019 | 0.193526 | 0.024487 | 0.120314 | 0.399097 |
| periodic 100 | 1.019954 | 1.725019 | 0.277278 | 0.006617 | 0.116962 | 0.368230 |
| Algorithm 4, c=1.1 | 1.000092 | 1.007444 | 0.158103 | 0.010662 | 0.112793 | 0.385192 |
| Algorithm 4, c=2 | 1.001002 | 1.152063 | 0.120433 | 0.008179 | 0.111770 | 0.330170 |
| Algorithm 4, c=2.5 | 1.001541 | 1.725019 | 0.159667 | 0.007735 | 0.114487 | 0.330169 |
| Algorithm 4, c=5 | 1.004344 | 1.725019 | 0.196733 | 0.007853 | 0.113797 | 0.330329 |
| Algorithm 4, c=10 | 1.007756 | 1.725019 | 0.204793 | 0.007851 | 0.115581 | 0.338213 |
| Algorithm 4, c=100 | 1.038948 | 1.725019 | 0.290683 | 0.008651 | 0.120836 | 0.352963 |
| qualified FD, ell=2 | 1.000039 | 1.000542 | 0.177757 | 0.097918 | 0.137593 | 0.509977 |
| qualified FD, ell=4 | 1.000000 | 1.000000 | 0.157747 | 0.103331 | 0.128621 | 0.493265 |
| author FD diagnostic, ell=2 | 1.000002 | 1.000072 | 0.160961 | 0.130654 | 0.129599 | 0.526388 |

## What this one stream says

- Algorithm 4 at `c=2` has the lowest nonzero recourse in this matrix:
  0.120433, 23.65% below fresh SVD, while its mean ratio is 1.001002 and its
  maximum is 1.152063.  This is a descriptive single-instance trade-off, not a
  superiority or theorem claim.
- `c=1.1` stays close to fresh SVD in loss (mean 1.000092, maximum 1.007444)
  but does not reduce recourse on this stream.  Larger `c` values do not form a
  monotone empirical improvement: their worst defined ratio reaches 1.725019
  and recourse eventually rises above fresh SVD.
- Periodic updating is not a low-recourse surrogate here.  Intervals 10 and
  100 both have more projector recourse than fresh SVD because less frequent
  but larger projector moves still contribute their squared distance.
- Qualified FD with `ell=2` and the author-FD diagnostic have very small loss
  inflation but slightly more recourse than fresh SVD.  `ell=4` matches fresh
  SVD because the sketch dimension equals the ambient dimension; it is a
  control, not evidence of compressed-memory performance.
- The fixed projector exposes the opposite endpoint: zero recourse with mean
  ratio 1.611537.  It prevents interpreting low recourse alone as success.

## What remains unqualified

No uncertainty estimate is possible from one seed.  The generator identity,
normalization and scorer are not authenticated as the paper's released Figure
3 evaluation.  These data do not cover Landmark, a prospective confirmation
split, a new candidate method, four-family G01, Gate A, originality, theorem
transfer or paper eligibility.  Parameter selection using this stream is
developmental; this same stream cannot later be relabelled as confirmation.
