# Independent review of the HEAVY multi-refresh potential candidate

Verdict: **ACCEPT_PARTIAL_MATH**.

Assignment: **184**.  Reviewed object:
`HEAVY_MULTI_REFRESH_POTENTIAL_CANDIDATE.md` at SHA-256
`f8acb0f76ef95150497bcef66463b2638ac8ea7f22733c205045d2e0ce3c0b39`,
from the stated base commit
`914f176611d04c0d077cf511ea48a3d8bab3658c`.

The verdict accepts only the displayed ledger, gap-weighted inequality, and
limitation example.  It is not acceptance of an unweighted recourse bound, a
repeatable large-motion construction, a theorem refutation, originality, an
experiment design, native-evaluation admission, or a completed research
cycle.

## 1. OPT ledger and telescoping charge

For each interval, write \(C_j=C_{j-1}+D_j\) and use that \(P_j\) is an exact
rank-\(k\) minimizer for \(C_j\).  Then

\[
\begin{aligned}
\operatorname{OPT}(C_j)
 &=L_{C_j}(P_j)\\
 &=L_{C_{j-1}}(P_j)+L_{D_j}(P_j)\\
 &=\operatorname{OPT}(C_{j-1})+G_j+U_j.
\end{aligned}
\]

Thus candidate equation (1), lines 48--63, is exact.  Moreover,
\(G_j\geq0\) because \(P_{j-1}\) minimizes \(L_{C_{j-1}}\), and \(U_j\geq0\)
because \(D_j\succeq0\) and \(I-P_j\succeq0\).  Summing the equality gives

\[
\operatorname{OPT}(C_J)-\operatorname{OPT}(C_0)
  =\sum_jG_j+\sum_jU_j,
\]

so candidate equation (2), lines 66--77, follows by discarding the
nonnegative \(U_j\) sum.  The term that telescopes is the full old-covariance
regret \(G_j\), not missed old-head mass by itself.

## 2. Equal-rank identity and factor of two

Let the old top-\(k\) eigenspace projector be
\(P_{j-1}=\sum_{i\leq k}e_ie_i^{\mathsf T}\), and set

\[
\alpha_i=1-e_i^{\mathsf T}P_je_i\quad(i\leq k),
\qquad
\beta_i=e_i^{\mathsf T}P_je_i\quad(i>k).
\]

Since both projectors have rank \(k\),

\[
\sum_{i\leq k}\alpha_i
 =k-\operatorname{tr}(P_{j-1}P_j)
 =\sum_{i>k}\beta_i.
\]

Also

\[
R_j=\|P_j-P_{j-1}\|_F^2
   =2k-2\operatorname{tr}(P_{j-1}P_j),
\]

hence each of the two preceding sums equals \(R_j/2\), exactly as stated on
lines 94--100.  Expanding \(G_j\) in the same eigenbasis gives

\[
G_j=\sum_{i\leq k}\lambda_i\alpha_i
       -\sum_{i>k}\lambda_i\beta_i
   \geq
   \bigl(\lambda_k-\lambda_{k+1}\bigr)R_j/2.
\]

Therefore the factor \(1/2\) in equation (3) is correct, and equations (2)
and (3) imply

\[
\sum_j\gamma_{j-1}R_j
 \leq2\bigl(\operatorname{OPT}(C_J)-\operatorname{OPT}(C_0)\bigr),
\]

with the factor \(2\) in equation (4) also correct.

## 3. Near-tie obstruction

For lines 124--147,

\[
C_1=C_0+D_1
 =\operatorname{diag}((1+\delta)I_k,(1+2\delta)I_k).
\]

Because \(\delta>0\), the old top-\(k\) subspace is uniquely the first block
and the new top-\(k\) subspace is uniquely the second block.  Their projectors
are orthogonal, so \(R_1=k+k=2k\).  Direct evaluation gives

\[
\operatorname{OPT}(C_0)=k,
\quad L_{C_0}(P_1)=k(1+\delta),
\quad G_1=\delta k,
\]

\[
U_1=L_{D_1}(P_1)=0,
\quad \operatorname{OPT}(C_1)=k(1+\delta),
\]

and hence
\(\operatorname{OPT}(C_1)-\operatorname{OPT}(C_0)=\delta k\).
Furthermore,
\(D_1=\sum_{i=1}^k(\sqrt{2\delta}\,e_{k+i})
(\sqrt{2\delta}\,e_{k+i})^{\mathsf T}\), so it is indeed a sum of \(k\)
rank-one row updates.  The old gap is \(\gamma_0=\delta\), and equation (3)
is tight: \(G_1=\gamma_0R_1/2\).

The quantifiers behind lines 143--145 are valid when read over the two-parameter
family: for any desired motion threshold \(M\) and charge tolerance
\(\eta>0\), choose \(k>M/2\), then choose
\(0<\delta<\min(1,\eta/k)\).  This gives \(R_1>M\) and
\(\delta k<\eta\).  For fixed \(k\), sending \(\delta\downarrow0\) makes the
charge arbitrarily small while the motion remains \(2k\); it does not by
itself make that fixed motion grow.  No candidate correction is required,
but this explicit quantifier is the safe interpretation.

## 4. Boundary and source-claim check

The candidate stays within the proved boundary.  Lines 118--120 explicitly
deny an unweighted bound; lines 142--147 identify the obstruction as a PSD
limitation example rather than a source-faithful integer stream; lines
151--163 leave both required repair ingredients open; and lines 178--180 and
184--188 deny a theorem proof, repeatable-event construction, experiment
admission, originality, and completed-cycle status.

Accordingly, the only accepted new claim is a gap-weighted amortization: old
regret cannot be charged twice in the sum, but unweighted projector motion may
still concentrate in near-degenerate spectral bands.  The candidate neither
proves nor disproves the paper's advertised aggregate theorem.
