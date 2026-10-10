# Projector-distance numerical audit: literature and derivation

Edelman, Arias and Smith (1998, SIAM J. Matrix Anal. Appl., DOI
10.1137/S0895479895290954) define principal angles by the singular values of
`Q.T @ V` and give the projection Frobenius distance as the Euclidean norm of
the sines of those angles, equivalently `2**(-1/2) * ||QQ.T - VV.T||_F`.
They explicitly distinguish points on the Grassmann manifold from their
non-unique orthonormal bases.  Primary PDF:
https://math.mit.edu/~edelman/publications/geometry_of_algorithms.pdf , section
4.3, pp. 336--338.

For equal-rank orthonormal `Q,V` and projectors `P=QQ.T`, `R=VV.T`,

`||P-R||_F^2 = tr(P)+tr(R)-2tr(PR) = 2k-2||Q.T@V||_F^2`.

This algebraic identity does not imply that the rightmost scalar subtraction is
a stable floating-point algorithm.  When the true distance is near zero, both
terms are order `k`; an absolute dot-product/summation error of order `k*eps`
becomes an apparent distance of order `sqrt(k*eps)` after clipping and square
rooting.  For float64 and `k=25`, `sqrt(k*eps)=7.45e-8`, matching B05's false
`1e-7`-scale discrepancies.  The clipping also creates false zeros when the
rounded squared value is negative.

Using `PV=Q(Q.T@V)` and `RQ=V(V.T@Q)` avoids the scalar subtraction:

`||(I-P)V||_F^2 + ||(I-R)Q||_F^2 = 2k-2||Q.T@V||_F^2 = ||P-R||_F^2`.

Reduced QR is applied first so that the computation depends on the represented
subspaces rather than small orthogonality defects in their stored bases.  This
costs `O(d k^2)` time and `O(d k)` memory rather than forming `d x d`
projectors.  It is the frozen metric for future parity checks; it does not alter
the paper's recourse definition or any method trajectory.
