# Independent analytic review: exact motion versus approximate loss

Assignment: main-exact-vs-approximate-bound-independent-review, registered in main a990a23fb2336c9684b1b86f616d44a64dcaf296 (aggregate assignment count144). Reviewer /root/exact_approximate_review, independent of draft author /root. Date2026-10-09. No matrix generator, project code, evaluator or native workload was imported or run. Root remains the sole integration/publication writer.

Verdict: ACCEPT the scoped final-update analytic claims. No blocking mathematical correction. This does not independently reprove the parent's complete recourse/conditioning results, confer novelty, admit experiments or establish a full-stream algorithm.

## Fixed source identities

GitHub connector fetched the exact draft at a990a23fb2336c9684b1b86f616d44a64dcaf296, Git blob c457f84d73fbc72232d6b3c24cab114ef4480051. Local git hash-object independently matched that blob. Draft SHA25665a373607d880e4bf81fb8ac3c729af8543a29c43e9c4652a31120956c95d670. Local HEADb62528927acd3a8771fb5269fc1fc945b717eed1 did not yet contain the remote candidate object; this was resolved by immutable connector read, not by confusing local HEAD with publication.

Read and SHA256-checked parents:

| Artifact | SHA256 |
|---|---|
| v5 draft | de008df475aba17eb4557fdeb5e7ed57d7843f79dd107ecbed686e40ef717ef5 |
| v5 review | d13f5faa8ce4ebcc75af96b21ee74671fe98da3bb723d32ab91e5740be744f8a |
| v7 draft | d0f56dbf1ec12c302ad2b42e8ae608a06c9c6c2da63b50da2ee11f6ec8fede79 |
| v7 review | bc239b1819de5657b481bd776a17bc949b4fdf305e9f69d742b92bf23fd9d003 |

The new loss inequalities below were derived independently from the spectra and perturbation contract; parent acceptance alone was not used to accept them. Prior reviews remain the basis for carried exact-recourse and consecutive-conditioning assertions.

## Real witness: trace and strictly positive OPT

Projector means symmetric orthogonal rank-k projector, as in reconstruction. Since (I-P)^2=I-P, ||A(I-P)||_F^2=tr(C)-tr(PC). Maximum captured trace is the top-k eigenvalue sumF_k. All positive centered eigenvalues lie above all negative ones in both spectra. Thus captured sums are2ka+T and2ka+2T, while the new bottom-k sum is2ka-T/2. No common-shift or dimension term is missing.

Independently expanding for the old optimizer gives

    loss_1(P_0)-OPT_1
      =F_k(C_1)-tr(P_0 C_1)
      =F_k(C_1)-F_k(C_0)-u^T P_0 u
      =T-u^T P_0 u.

Its lower bound0 follows from optimality; its upper boundT follows from nonnegative captured energy. The positive-coordinate residue sum is exactly u^T P_0 u. Summing i=1,...,k givesT=16(a-1)/15<16a/15. ThereforeOPT_1>a(2k-8/15)>0 for everyk>=1, and

    1 <= loss_1(P_0)/OPT_1 < 1+8/(15k-4).

At61,8/911<1/100 because800<911. KeepingP_0 on the final append has recourse0. The parent exact optimizer pair hasR>122/15>8. These are compatible, and the latter is not an approximate-recourse lower bound.

## Integer witness: scale, Ky Fan and Weyl

The parent rounding bound applies toB_j=Z_j^T Z_j/S^2 withS=128k4^k and operator/Frobenius error<tau=1/(30sqrt(k)). The draft uses that normalized absolute error, not unnormalized integer error. Multiplication byS^2 preserves projectors and scales both loss andOPT equally. The ratio is invariant.

Q_0 exactly optimizesB_0, andB_1=B_0+vv^T wherev=h/S. Hence excess equalsF_k(B_1)-F_k(B_0)-v^TQ_0v. The last term is nonnegative. Weyl bounds each ordered eigenvalue error bytau, so |F_k(B_j)-F_k(C_j)|<=k tau. Using two covariances gives the numerator boundT+2k tau. No ambient-dimension multiplier is needed. Summing bottomk eigenvalues of onlyB_1 givesOPT_B1>=OPT_1-k tau. The denominator factor is thereforek, not2k.

Puteta=k tau/a=sqrt(k)/(30*16^k). Inductionk<=256^(k-1) starts at1 and usesk+1<=256k, provingeta<=1/480. The estimated normalized denominator2k-8/15-1/480=2k-257/480 is positive, includingk1 where it is703/480. Thus

    (loss_Z1(Q_0)-OPT_Z1)/OPT_Z1
       < (16/15+2eta)/(2k-8/15-eta)
       <= (16/15+1/240)/(2k-8/15-1/480)
       = (257/240)/((960k-257)/480)
       = 514/(960k-257).

Strictness survives fromT<16a/15 and the strict geometricOPT bound. At61 the denominator is58303 and100*514=51400<58303, proving a final-update ratio below1.01. The lower ratio1 follows from optimality. Zero movement ofQ_0 is feasible on this update.

Uniqueness, exact integer recourseR_Z>122/15-.01>8 and ordered consecutive-block positive-singular condition<4 are carried from acceptedv7, not freshly inferred from this loss argument. No float64 spectral certificate or condition measurement was made.

## Scope and rejected implications

The conclusion supplies one approximate feasible projector on one final append, starting from the immediately preceding exact optimizer. It supplies neither a prefix-by-prefix algorithm nor an efficient method of maintaining that old exact optimum, nor a total-stream recourse guarantee. It neither validates nor repairs the separate approximate-existence theorem; a dependency issue in an exact-motion lemma is distinct from refuting the theorem's conclusion.

The sufficient bounds discard captured energy and are deliberately loose. They do not give a tight epsilon, a universal rule that large motion is harmless, a new method/candidate/paper, or novelty. These exclusions agree with the draft. Optional editorial precision would explicitly call generic projectors orthogonal; context already establishes that convention, so no blocking change is required.

No scientific admission, official/native scorer parity or empirical claim follows from this acceptance. Next proof analysis should identify loss-dependent assumptions controlling approximation across prefixes rather than infer approximate lower bounds solely from exact optimizer distance.
