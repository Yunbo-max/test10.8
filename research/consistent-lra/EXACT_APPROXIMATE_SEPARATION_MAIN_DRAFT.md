# Exact recourse and approximate loss separate on the accepted witness

Status: new analytic clarification of the existing formal correction lineage;
independent review pending. Author: /root. No workload, matrix scoring, new
method, discovery admission, originality or paper-eligibility claim.

## Question and fixed inputs

Does the accepted large exact-projector movement force a comparable movement
when the final update only requires a 1% relative reconstruction guarantee?
The existing v5/v7 witnesses answer the exact question, not this approximate one.
We now derive an explicit upper bound for the simplest alternative: keep the
unique exact top-k projector from the immediately preceding matrix.

Use the accepted v5 real construction and v7 integerization at historical
project commit b62528927acd3a8771fb5269fc1fc945b717eed1. v5 SHA256
de008df475aba17eb4557fdeb5e7ed57d7843f79dd107ecbed686e40ef717ef5;
v7 SHA256 d0f56dbf1ec12c302ad2b42e8ae608a06c9c6c2da63b50da2ee11f6ec8fede79;
v7 review SHA256 bc239b1819de5657b481bd776a17bc949b4fdf305e9f69d742b92bf23fd9d003.
The paper's Frobenius residual/projector definitions and the distinction between
exact Lemma2.1 and approximate Theorem1.2 were re-read in the ICLR2026 PDF,
pp3/5, on 2026-10-09. Primary URL:
https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf
This reading is not a full proof verification or a new novelty search.

Moves: exact trace decomposition, geometric upper bound, scale normalization,
and perturbation bounds carried from the independently accepted parent.
All matrices and projectors below are exact mathematical objects. No float64
measurement or native benchmark is used.

## 1. Real parent: a zero-change final update is already near optimal

Let a_i=16^i, a=16^k and T_k=sum_i a_i. The old covariance is
C_0=2aI+diag(-a_i,+a_i), and C_1=C_0+uu^T has eigenvalues
2a-a_i/2 and 2a+2a_i. Define F_k(C) as the sum of its top k
eigenvalues. The unique old projector P_0 selects the positive coordinates.
For any rank-k projector P, loss_C(P)=tr(C)-tr(PC) and
OPT_C=tr(C)-F_k(C).

Therefore

    F_k(C_0)=2ka+T_k,
    F_k(C_1)=2ka+2T_k,
    OPT_1=2ka-T_k/2.

The last equality follows from the bottom k eigenvalues of C_1.
By the exact positive rank-one append identity,

    loss_1(P_0)-OPT_1
      =F_k(C_1)-F_k(C_0)-u^T P_0 u
      =T_k-sum_{lambda>0}rho_lambda.

Optimality gives the nonnegative lower bound; positivity gives the upper bound
T_k. Because T_k=(16/15)(a-1)<16a/15, OPT_1>a(2k-8/15)>0. Hence

    1 <= loss_1(P_0)/OPT_1 < 1 + 8/(15k-4).

At k=61 this is strictly less than 1+8/911<1.01. Keeping P_0 on this
single final append incurs recourse exactly zero, while the two unique exact
optimizers have squared projector distance greater than122/15>8 by the
accepted v5 proof. These statements are compatible: the relative loss and
projector displacement measure different consequences.

## 2. Integer witness: the same distinction survives rounding

Let Z_0 be v7's integer diagonal matrix, Z_1=[Z_0;h^T], and S=128k4^k.
Set B_j=Z_j^T Z_j/S^2. The accepted v7 proof supplies
||B_j-C_j||_op <= ||B_j-C_j||_F < tau_k=1/(30sqrt(k)) for j=0,1.
Let Q_0 be B_0's unique exact top-k projector. Scaling by S^2 changes neither
Q_0 nor a loss/OPT ratio. The rounded append remains exact:
B_1=B_0+(h/S)(h/S)^T.

Using Ky Fan sums and nonnegative captured appended energy,

    loss_{B_1}(Q_0)-OPT_{B_1}
      =F_k(B_1)-F_k(B_0)-(h/S)^T Q_0(h/S)
      <=F_k(B_1)-F_k(B_0)
      <=T_k+2k tau_k.

Weyl's bound on each of the bottom k eigenvalues gives

    OPT_{B_1} >= OPT_1-k tau_k
              > a(2k-8/15)-k tau_k.

For all integer k>=1, sqrt(k)<=16^(k-1). This follows from
k<=256^(k-1): true at1 and preserved because k+1<=256k.
Consequently k tau_k/a=sqrt(k)/(30*16^k)<=1/480.
The denominator above is positive. Combining the strict geometric bound with
these inequalities gives the convenient uniform estimate

    1 <= loss_{Z_1}(Q_0)/OPT_{Z_1}
       < 1 + (16/15+1/240)/(2k-8/15-1/480)
       = 1 + 514/(960k-257).

At k=61, 100*514=51400<58303=960*61-257, so this ratio is
strictly below1.01. Nevertheless the accepted v7 proof gives the two exact
integer optimizers recourse greater than122/15-1/100>8, and every nonempty
consecutive row block has positive-singular condition below4. No matrix
eigenvalue or condition number has been numerically computed here.

## Interpretation, falsifiers and limits

This quantitatively closes an overclaim risk: the particular accepted final
append cannot refute a 1.01 approximate guarantee merely by its exact-optimal
movement. The old exact projector is an explicit feasible zero-change choice
for that update, in both real and integer witnesses. A full arrival algorithm
would still have to satisfy every earlier prefix; no full-stream algorithm,
recourse guarantee, lower bound or repair of Theorem1.2 is established.

The threshold is a sufficient upper bound, not a tight necessary epsilon. The
argument discards positive captured rank-one energy, so the actual excess may
be smaller. It depends on this shifted geometric family; it is not a universal
claim that large exact motion is always harmless. General loss-sensitive
subspace stability, inverse secular constructions and perturbation machinery
are established concepts; no originality is asserted.

Falsifiers: wrong old/new top or bottom spectra; a failure of positive append;
an invalid carried v7 covariance bound; a negative estimated OPT denominator;
incorrect scale invariance, Ky Fan perturbation factors or the geometric
arithmetic. Independent review must check the exact source-bound draft rather
than infer validity from the parent acceptance.

Next discriminating source/proof work: determine which approximate recourse
arguments constrain spectral loss rather than exact optimizer distance, and
which legitimate residual question remains after this strongest zero-change
alternative. This formal clarification advances no empirical/native gate and
does not count as another candidate or paper.
