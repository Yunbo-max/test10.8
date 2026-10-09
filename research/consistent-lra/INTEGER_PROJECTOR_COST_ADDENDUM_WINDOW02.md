# Actual142 predetermined representative cost calibration addendum

Existing actual140/141 math and acceptance thresholds unchanged. This addendum
resolves actual141's cost gap before source generation. Actual143 independent
review is required; no source or executable attempt now.

Implement two fixed modes, with no adaptive root/precision selection:

- calibration: complete top-root inventory for ranks1,2 and precisely root indices
  j=61 and j=121 for rank61 (first and last new top roots). These use the actual
  full122-coordinate, up-to258-bit integer witness. Rank61 slice is explicitly
  incomplete: no full-R lower-bound target verdict, no claim that it certifies >8.
- full: complete rank61 indices j=61..121, unchanged12 bisections/32-bit floors.

Fractions use reduced numerator/denominator serialized as hexadecimal strings
in a JSON object; hash canonical sorted compact UTF-8 JSON. Negative numerators
include the canonical Python hex sign; denominator is positive. Large temporary
fractions are hashed but actual input integers and every interval/decision remain
available for independent reconstruction. Record actual wall/CPU by root and
whole process; serialization/publication costs are separate and retained.

Calibration is one CPU task, stdlib only, 256MiB reservation not OS-enforced,
inner90/outer120 seconds, one attempt, zero retry. Root61 slice must actually
complete and independent evidence review must reconstruct both roots and costs
before full61 admission. Small-rank timings are not the admission basis.

Full proposed inner300/outer360 remains conditional. Prospective heuristic cost
envelope = 61 * 4 * max(observed rank61-slice per-root wall) + 30 seconds
serialization/harness allowance. Require this envelope <=300, observed peak RSS
<=128MiB, one CPU resource/ownership check, and >=660 seconds remaining before
the hard deadline (360 execution +300 closeout). This is a conservative measured
planning heuristic, not a proven complexity or worst-case guarantee: sampled
roots can differ, Fraction arithmetic/host speed can vary. The enforced timeout
bounds actual work. If the threshold fails, retain calibration and leave full
pending; no blind retry or post-result threshold weakening. Independent plan
review may reject this finite proposal even if the heuristic passes.

All source/plan/output reviews remain separate. No scientific native/evaluator
authority or originality is supplied. The fixed calibration slice never becomes
a substitute full61 projector certificate.
