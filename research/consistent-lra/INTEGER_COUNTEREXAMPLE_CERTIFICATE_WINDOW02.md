# A reproducible integer certificate for the constant-eight lemma audit

This is a research evidence note. Originality and manuscript eligibility remain
pending; no baseline winner, optimized approximate method or multiple papers.

The frozen construction has k=61, d=122. Its old data matrix is diagonal with
122 positive integer entries; append one positive integer row to form123x122.
There are244 stored nonzero integer entries; maximum actual entry bitlength258.
The old and new top61 projectors are unique. Complete independent exact-rational
replay certifies

\[
\|P_{\mathrm{new}}-P_{\mathrm{old}}\|_F^2
\ge\frac{2290438555}{134217728}>8.
\]

The relevant conference Lemma2.1 claims a constant8 for a single row arrival.
This existing-paper correction now has a concrete integer input and an accepted
complete certificate. The all-consecutive-block condition<4 remains an analytic
v7 result; no per-block numerical experiment was run. Near-optimal outputs and
the paper's approximate-existence theorems have separate proof obligations.

Construction parameters are a=16^k and S=128k4^k. Ordered parent poles are
lambda=sorted(-16^i,+16^i) and parent roots mu=sorted(-16^i/2,+2*16^i), i=1..k.
Positive residues are -prod(lambda_i-mu_j)/prod_(j!=i)(lambda_i-lambda_j).
Nearest-half-up integer rounding of S*sqrt(2a+lambda_i) and S*sqrt(residue_i)
gives diagonal and appended entries. The integer generator uses isqrt and exact
brackets; no floating square root is needed. Existing secular/inverse-spectrum
machinery is attributed in the collision review, not claimed as new.

For actual rounded integers, poles d_i=m_i^2 and weights h_i^2 define
f(x)=1+sum h_i^2/(d_i-x). Positivity/strict poles give simple interlacing roots.
The complete new top61 inventory uses pole indices61..121. Twelve frozen rational
bisections per root and endpoint-distance bounds produce conservative old-bottom
coordinate mass. A 32-bit downward dyadic floor per root gives the retained lower
bound; all732 decisions were independently reconstructed from the actual input.

Evidence and source:

- [Actual integer witness and independent construction review](INTEGER_WITNESS_EVIDENCE_REVIEW_WINDOW02.md)
- [Complete root raw/receipts collection](evidence/integer-projector-target61-02-collection.json)
- [Independent complete certificate review](INTEGER_PROJECTOR_TARGET61_EVIDENCE_REVIEW_WINDOW02.md)
- [Producer source](integer_projector_certificate_window02.py) and [independent source review](INTEGER_PROJECTOR_SOURCE_REVIEW_WINDOW02.md)
- [Unchanged independent replay source](evidence/reviews/actual154-independent-replay.py)
- [Prospective complete plan and cancellation bounds](plans/native-integer-projector-target61-02.json) / [harness](plans/harness-integer-projector-target61-02.json)
- [Primary collision/correction scope](INTEGER_CORRECTION_INDEPENDENT_COLLISION_REVIEW_WINDOW02.md)
- [Approximate-proof dependencies and qualified known fallback](APPROXIMATE_PROOF_DEPENDENCY_REVIEW_WINDOW02.md)

Full original attempt wall13.090105889s,CPU12.213068s,RSS25392KiB;
separate independent replay wall11.894702007s,CPU11.891034659s,RSS21512KiB.
Both are charged in the monotonic budget. The replay retains its exact historical
repository location and immutable evidence commit; it is read-only and never
imports the producer. Restore that commit before verification; no completed run
needs to be relaunched on the next continuation.

Remaining: conjunction priority, native faithful-evaluator/live parity authority,
full fair benchmark matrix, meaningful residual failures and new-method discovery
prerequisites, future prospective confirmation. Formal v5/v6/v7 strengthen one
lineage; parameter/seed variations are not separate paper contributions.
