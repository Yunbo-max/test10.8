# B07 source and mathematical audit

Scope: existing mechanism audit and attributed comparator qualification. Not a complete novelty adjudication. Primary source cutoff2026-10-10; incomplete search coverage and modern baseline inventory remain open.

## Primary sources actually inspected

1. Woodruff/Zhou, Consistent Low-Rank Approximation, arXiv2603.02148v1: Section1.2.2 (FD/online ridge leverage sampling and SVD strawmen), Theorem1.5, Algorithm1, Section5.1 raw Landmark first5000,d2704,k25 and Section5.2/5.3 native Skin/Rice. Formal recourse is squared projector Frobenius change. The experimental method is energy/additive-triggered, not our strict multiplicative certified_full benchmark comparator.
2. Ghashami/Liberty/Phillips/Woodruff, arXiv1501.01711, Section2, Algorithm2.1, Properties1--3 and subsequent relative projection-error derivation. Covariance Loewner/error bounds and cumulative shrink Delta are prior work. Section3 batched compression is distinct from unbatched trace equality.
3. Liberty, arXiv2202.01780v1, complete one-page Algorithm1 and Lemma1: covariance compression proof and low-memory representation. Used for alternate proof, not novelty.
4. Independent verifier additionally read Ghashami/Phillips arXiv1307.7454 Algorithm2.1/Lemmas2.3--2.4, which explicitly documents exact ell Delta trace loss. Verifier's artifact states its narrower scope and limits.

Paper URLs: https://arxiv.org/html/2603.02148v1 ; https://arxiv.org/pdf/1501.01711 ; https://arxiv.org/pdf/2202.01780 ; https://arxiv.org/pdf/1307.7454 . Source static reads are not reproduction receipts.

## Actual author implementation at pinned commit

samsonzhou/consistent-LRA@d607c4f6467216c470d1e3b93989d44d5fcdec97. Both full source files captured in ../sources. Landmark source blob4c63060bbefcb38e0c705cea1f883d2fb7121f2c and SHA25629fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b reused, not redownloaded. Native A bytes are restored from audited B04/B06 parent;128 rows are development only.

consistent-fd.py/FrequentDirections._shrink_and_replace uses ell+1 stacked rows and delta=s[ell]^2, retaining ell nonzero modes. Consequently exact trace loss is (ell+1)delta; a classic ell delta identity would be incorrect on this implementation. Its main loop uses capacity25, returns raw25-row sketch and measures count_rows_not_in_span instead of rank25 orthogonal projector distance. V_old is assigned directly to B, and append can mutate that array in place: earlier old/current references alias between compressions. These static observations make published-code recourse counters non-interchangeable with our mathematical metric; no recomputed correction to published numerical figures is claimed.

consistent-lra-landmark.py uses squared-energy trigger sq_norm_At>c*count, randomized_svd(n_iter=7), and prefix1..4999. true_cost is computed from V retained at the last refresh; it is not a fresh exact prefix SVD at each step. r and kcurr are also initialized outside the c loop and updated in the refresh branch, which warrants dedicated author-protocol reproduction before interpreting early prefixes or cross-c results. Here these are source-level evidence obligations, not claims that the theorem or all paper results are wrong.

Our qualified direct singular-value-tail scorer and squared projector metric must therefore be described as verified mathematical evaluators, not the author's official scorer. Author-protocol emulation and same-metric strong baseline comparisons require separate columns and artifacts.

## Consequential derivation and constraint

Let C=A'A,S=B'B,0<=C-S<=Delta I. For every rankk projector P, tr(PC)<=sum_topk(S)+kDelta. Therefore OPT>=trC-sum_topk(S)-kDelta. For classic ell-row unbatched shrink from zero, traceC-traceS=ellDelta, yielding L=tail(B)+(ell-k)Delta. The author augmented implementation instead gives L=tail(B)+(ell+1-k)Delta. Both are attributed consequences of FD covariance control. No new-method claim.

Insertion makes OPT nondecreasing: each fixed projector residual adds nonnegative energy, hence the minimum cannot decrease. Historical exact OPT is a valid lower bound. If a safe bound is ONLY a gate and refresh is confirmed by exact OPT with the same deterministic update map, every true violation must query. False queries do not change Q. By induction any such gate gives the same Q/refresh/recourse sequence. Stronger pointwise bounds remove only false queries. They do not reduce necessary refreshes or solve the stability tradeoff.

This invalidates a broad planned claim that a tighter lower bound alone reduces refresh count. Remaining useful investigation: does attributed FD qualification remove enough false queries to pay for maintaining its sketch? Break-even needs sum(saved oracle CPU)>FD maintenance CPU, plus paired full-runtime repeats on eligible data. A positive query count alone cannot establish this.32/128/512 checkpoints are not independent statistical samples.

## Decision before results

Qualify the existing FD corollary and source-sensitive trace factor on the unchanged Landmark128 development prefix. Independently review mathematics and source, then live-audit saved arrays with Gram spectra/covariance loss. No new candidate code, pool reset, Newton repair, Landmark5000 completion, paper PASS or originality PASS. If there are no false query savings, preserve that negative result and investigate certified approximate refresh or updated objective only through proper renewed discovery; do not rename the FD gate as a new method.

## RFD first-pass primary collision check
Luo etal2019, Robust Frequent Directions with Application in Online Learning, https://www.jmlr.org/papers/v20/17-773.html (paperAlgorithm2,Theorems2/3,AppendixD read). RFD maintains an isotropic regularization with the sketch. For identicalB, addingalphaI changes eigenvalues but not topk eigenspaces with the same deterministic tie rule; this covariance approximation improvement alone does not establish outputrecourse improvement. No RFD code executed here.
