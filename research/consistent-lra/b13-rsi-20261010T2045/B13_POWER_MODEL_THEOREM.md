# B13 frozen-model theorem: warm-start power work needs spectral information

## Status and purpose

This is a project-specific mathematical diagnostic.  It freezes one explicit
endpoint-construction model and asks whether the B12 geometry tuple
`(Delta, D, k, r)` controls construction work.  It is not claimed as a new
algorithm, a novel theorem, or a model of every eigensolver.

## Frozen computational model

Let `G` be a real symmetric positive semidefinite matrix with eigenpairs
`(lambda_i,u_i)`, ordered so that

```
lambda_1 > lambda_2 >= ... >= lambda_d >= 0.
```

The retained state is one unit vector `q`.  The algorithm may access `G` only
through exact matrix-vector products and performs ordinary warm-start power
iteration

```
y_m = G^m q,                 q_m = y_m / ||y_m||_2,
P_m = q_m q_m^T.
```

One matrix-vector product is one unit of work, so `W=m`.  Arithmetic is exact.
The required output is the explicit rank-one projector `P_m`.  The target is
`P=u_1 u_1^T`, and output error is projection recourse

```
E_m = r(P,P_m) = 1 - (u_1^T q_m)^2.
```

Assume `c_1=u_1^T q != 0`.  Write `c_i=u_i^T q`,
`r=1-c_1^2`, and `rho=lambda_2/lambda_1 < 1`.

## Theorem 1: exact work law and gap-dependent envelope

For every integer `m>=0`,

```
E_m = [sum_{i>=2} lambda_i^(2m) c_i^2]
      /[lambda_1^(2m)c_1^2 + sum_{i>=2}lambda_i^(2m)c_i^2].
```

Consequently,

```
E_m <= rho^(2m) r / [(1-r)+rho^(2m)r].                 (1)
```

Equality holds when every off-top component of `q` lies in the
`lambda_2`-eigenspace.  When `0<lambda_2<lambda_1` and
`0<epsilon<r<1`, it is sufficient that

```
m >= log( r(1-epsilon)/(epsilon(1-r)) )
     / [2 log(lambda_1/lambda_2)].                      (2)
```

The positive part and ceiling are understood.  Under the equality condition,
this is also the exact smallest integer work, up to taking the ceiling.
If `lambda_2=0` and `0<epsilon<r`, every off-top eigenvalue is zero, so the
smallest work is instead exactly `m=1`; formula (2) is not used at this
endpoint.

### Proof

Expand `G^m q=sum_i lambda_i^m c_i u_i`.  Squaring the top coordinate after
normalization gives the displayed identity.  Bound each off-top eigenvalue by
`lambda_2`, use `c_1^2=1-r`, and divide numerator and denominator by
`lambda_1^(2m)`.  For `lambda_2>0`, solving the resulting rational inequality
for `m` gives (2).  If `lambda_2=0`, the initial error is `r>epsilon`, while one
application of `G` removes all off-top components, proving the separate
one-matvec endpoint statement.
The bound is tight exactly when all non-top mass experiences the same ratio
`lambda_2/lambda_1`.

## Theorem 2: fixed B12 geometry permits unbounded power work

Fix constants `0 < delta < r_0 < 1`, and choose a target tolerance

```
0 < epsilon < (r_0-delta)/(1-delta).
```

For every `gamma` in `(0,delta/r_0)`, define

```
G_gamma = diag(1, 0, 1-gamma),
P       = e_1 e_1^T,
a_gamma = (delta-gamma r_0)/(1-gamma),
q_gamma = sqrt(1-r_0)e_1 + sqrt(a_gamma)e_2
          + sqrt(r_0-a_gamma)e_3,
Q_gamma = q_gamma q_gamma^T.
```

Let `L_G(R)=tr((I-R)G)` and set the feasibility threshold
`T_gamma=L_{G_gamma}(P)`.  Then, for every such `gamma`,

```
D_gamma = lambda_max(G_gamma)-lambda_min(G_gamma) = 1,
k = 1,
r(P,Q_gamma) = r_0,
Delta_gamma = [L(Q_gamma)-T_gamma]_+ = delta.
```

Thus the complete B12 tuple `(Delta,D,k,r)` equals
`(delta,1,1,r_0)` for the entire family.  Nevertheless the smallest number of
power matvecs needed for `r(P,P_m)<=epsilon` tends to infinity as
`gamma -> 0+`.

### Proof

The interval for `gamma` gives `0<a_gamma<r_0`, so `q_gamma` is a unit vector.
Direct substitution yields

```
tr(PG_gamma)-tr(Q_gamma G_gamma)
  = a_gamma + gamma(r_0-a_gamma) = delta,
```

which proves the fixed deficit because `T_gamma=L(P)`.  The diameter and
recourse identities are immediate.  For `m>=1`, the zero-eigenvalue component
is eliminated and

```
G_gamma^m q_gamma
  = sqrt(1-r_0)e_1
    +(1-gamma)^m sqrt(r_0-a_gamma)e_3.
```

Hence

```
E_m = (1-gamma)^(2m)(r_0-a_gamma)
      /[(1-r_0)+(1-gamma)^(2m)(r_0-a_gamma)].           (3)
```

The exact smallest integer work is

```
ceil( log((r_0-a_gamma)(1-epsilon)
          /(epsilon(1-r_0)))
      /(-2 log(1-gamma)) ).                             (4)
```

For the stated epsilon, the numerator tends to the positive constant
`log((r_0-delta)(1-epsilon)/(epsilon(1-r_0)))`, whereas
`-log(1-gamma) -> 0+`.  Therefore (4) diverges.

## Consequence for the consistent-LRA project

The B12 geometry tuple controls mandatory endpoint movement but not even the
work of this narrowly frozen warm-start solver.  A work theorem must additionally
carry solver-relevant spectral information: at minimum an internal eigengap or,
more sharply, the distribution of retained-state mass across near-top
eigenspaces.  Replacing that information by global diameter `D` is invalid.

This does **not** establish a lower bound for every Krylov, shift-and-invert,
direct, cached, or randomized solver.  It does **not** justify a new method.
Primary literature already contains warm-start and gap-dependent/gap-independent
power/Krylov analyses; the exact formula and counterexample here are retained as
a project decision boundary pending a complete collision audit.
