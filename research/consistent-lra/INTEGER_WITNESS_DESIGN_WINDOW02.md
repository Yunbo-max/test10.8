# Exact integer witness generation contract — existing lemma audit only

Assignment129 root design; assignment130 independent /root/window02_consecutive_condition_review.
Source-only proposed extension of independently accepted v7 analytic construction,
not newmethod/discovery/nativebenchmark or novelty. Keep realparentcertificate
and allfailurehistory unchanged. No generator/code/qualificationrun yet.

## Object and complete construction
For each fixed k in [1,2,61], a=16**k, S=128*k*4**k. Lambda ascending
[-16**i,+16**i:i=1..k], Mu ascending[-16**i/2,2*16**i:i=1..k],
negativehalf computed exactinteger division. For each lambda retain exact signed
product numerator=-product(lambda-mu), denominator=product(lambda-nu fornu!=lambda),
normalize as positive reduced Fraction. Diagonal radicand2*a+lambda.
Use only stdlib integers/Fraction/isqrt; never floats/numpy/projectmodules.
For positive r=N/D, q=(4*S*S*N)//D,n=isqrt(q),m=(n+1)//2.
Certificate n*n<=q<(n+1)*(n+1), and for m>0
(2*m-1)**2*D<=4*S*S*N<(2*m+1)**2*D, with lower0 if m==0.
Keep exact numerator/denominator/q/n/m and both inequality residuals, plus
original product identities. m is upward-half-tie rounded Ssqrt(r).

## Declared output and predicates
Two outputs: integer-witnesses.jsonl and integer-witnesses-summary.json.
Exactly3 rankrecords, each ordered2k diagonalm values +2k appendedrow values
(sparse reconstruction A=diag(diagonal), T=[A;h^T], both actual integers).
Each entry<=257*k*16**k and bitlength<=4*k+ceil(log2k)+9, ceil(log2k)
implemented (k-1).bit_length(). All generated diagonal and h entries positive.
All exact products, square brackets/rounding/entrybounds checked before success.
The k61record dimension122, bitbound259. Exact append hhT is an algebraic
rankone identity; no explicit densecovariance/projector/eigenvalue computation.
Retain source/inputhashes, argv, timing/RSS and data-byte manifests. Exclusive
partial+fsync/readback/noreplacepublication; failure partialrecords and diagnostic
reason nonzero, no successsummary. Do not suppress failed costs/results.

## Claim boundaries and independent acceptance
An executed witness confirms specified integer construction/rounding/size only.
R_Z>8/allorderedblockcondition<4 remain claims of accepted analytic v7 theorem,
not measured by generator. No empirical projectorrecourse/floatstable gap/native
benchmark/priority/approximate-existence refutation or paperacceptance.
Independent source/semantic review and complete finite plan review before launch,
then independent output reconstruction/rounding/products/hash/receipt verification.
Read accepted v7 draft/review and relevant v5/v6 parents as unchanged inputs.

## Finite prospective resource proposal
OneCPU,256MiB reservation(notOSenforced),stdlib only; fixed ranks1,2,61.
Single task, max1attempt0retry0confirmation;60sinner90souter, same hostpool and
sharedexclusivekey; remainingwindow/reservations recheck before launch. Small
finite exact products polynomial in k; no scientifictime-sized matrixqueue.
If cost cannot fit or source/plan review fails, keep generatedunexecuted and
block only this child. No budget/scientificfailure reset, no vendorchange.
