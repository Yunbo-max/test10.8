# B14 source and collision record

## Primary/theorem lineage retained from B13

- Wang et al., *Improved Analyses of the Randomized Power Method and Block
  Lanczos Method* (arXiv:1508.06429): gap-dependent and gap-independent analyses
  already cover the core relation between spectral separation and iteration
  complexity. B14 does not claim this relation as new.
- Musco and Musco, *Randomized Block Krylov Methods for Stronger and Faster
  Approximate Singular Value Decomposition* (NeurIPS 2015): block Krylov already
  improves over ordinary simultaneous iteration. It is a required comparator,
  not a B14 invention.
- Garber et al., *Faster Eigenvector Computation via Shift-and-Invert
  Preconditioning* (ICML 2016): alternative gap-sensitive acceleration exists.

## Actual implementation inspection

1. SciPy `lobpcg.py` at repository commit
   `95e01a4004e2781c91a26d9836d82c103dd8513c`, blob
   `500db09374082fd24944fbcf936ffc492c28004c`:
   the public implementation takes a mandatory initial block `X`,
   orthonormalizes it, computes initial Ritz vectors, and stops from residual
   norms. Supplying a retained subspace as `X` is therefore an existing
   warm-start comparator, not by itself a novel mechanism.
2. mlpack randomized block Krylov SVD at commit
   `3c26615acfcc89b3c8fdee0c11a69e4df4c1223b`, interface blob
   `ad32145c06b2e432676e5716ae47b2c4ef0dbac3` and implementation blob
   `04c45c8e03e7ec2f73b81b92a6291aa1fc2da239`:
   the implementation uses a random block, repeated `A(A^T block)` products,
   QR orthonormalization, then Rayleigh--Ritz/SVD. Its iteration parameter and
   block size expose a stronger existing scalable endpoint comparator.

## Collision decision

B14 is a diagnostic round, not a candidate-method round. A future proposal that
only feeds the previous endpoint into block power, LOBPCG, Lanczos, or block
Krylov is classified as an attributed comparator/engineering policy unless it
adds a separately proved certificate or refresh-count consequence that survives
operation-level collision review. The current finite AUROC analysis cannot
establish such a consequence.
