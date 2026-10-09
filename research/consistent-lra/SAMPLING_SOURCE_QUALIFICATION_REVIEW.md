# Independent review record: sampling-source qualification

## Reviewed immutable inputs

- Reviewer: `/root/sampling_source_review`
- Candidate commit: `77429350ae1513ae0f6825b7d07c4b0825288b43`
- Candidate Git blob: `1f6079de91e5dd5802d82c2db75a96d7277f69da`
- Candidate SHA256:
  `99a8c1c99fe56e31e702f181740b87f100be0517a08c9631ab32a1bd99191091`
- Assignment commit: `b3e203a9473492c937bf3418bfab7864dba81a89`
- Assignment Git blob: `cd2dc034d23d7af087364a77ec29781a711e64d5`
- Assignment SHA256:
  `fdf5833ebbe164dc5670709fe710848620016f9277d56398cb4eca8462a2e917`

## First verdict: `needs_correction`

Accepted components:

1. Braverman et al. v6 defines online condition number as the maximum over
   prefix condition numbers and establishes simultaneous PCP validity for all
   prefixes.
2. The target paper's Theorem 2.4 statement and its Lemma 2.1-dependent route
   to Theorem 1.2 were represented accurately.
3. The PCP loss transfer and `eta=epsilon/(2+epsilon)` calibration are exact.
4. The target-theorem boundary correctly avoids claiming that Theorem 1.2's
   existence statement itself is false.

Required corrections:

- arXiv v6 is dated 11 April 2023, not 13 March 2023;
- the simultaneous-prefix PCP and sample-size statements are high probability.
  The fallback must be stated on the joint event
  `E={all-prefix PCP} intersect {|M_n|<=s}`, not as an unconditional bound.

The reviewer additionally confirmed that theoretical Algorithm 5 is
append-only: an accepted row is added once, with no deletion, replacement or
resampling.  Hence its accepted-row event count equals final sample count, but
an executable implementation still requires separate parity qualification.

## Correction re-review status

`accepted`.

- Corrected candidate commit:
  `b8651edf183ff8103aa97823c044d79a9b9cef99`
- Candidate Git blob: `1c0a3763b667f6bd9f11f08c088a822c0d1079e9`
- Candidate SHA256:
  `c54da47a0a3e7aad71a6851225f73e9f8ff95dd0305b305d4ad823408f5a82c9`
- Assignment commit: `5a11100ecf1eadb60485096f7972515f7e1bd6c8`
- Assignment Git blob: `2492f003941fcb49f948053f9ba71e40f384c9cf`
- Assignment SHA256:
  `e1154fbabed4e24695330b0f9c831e2a7f5323a512b45cd82f1c7a38b7912854`

The reviewer accepted the corrected 11 April 2023 version date, the explicit
joint high-probability event and the theoretical Algorithm 5 append-only event
accounting.  Executable sampler parity remains pending.  No source reading,
algebra or first verdict is overwritten, and the reviewer performed no
numerical experiment.
