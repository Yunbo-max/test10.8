# Independent review: native protocol / G01 design v2

Reviewer: `/root/rice_skin_plan_review`  
Initially reviewed commit: `956fc9837576eb5bcce31d2859cc8aef9b73791e`  
Initially reviewed tree: `4a614f97585e0efaba3019f0c6e95f1fb2a3830f`  
Initially reviewed SHA-256: `4cb31710b4b2d70df5e77663ddbc9c82c7dfd415b69f1b190da57068f00d7a34`

Initial verdict: **NEEDS_CORRECTION; documentation/design only**.

Four-family coverage, comparators/controls, development-confirmation boundary,
accepted counts/costs, Landmark represented-column wording and all non-pass
boundaries were accepted. Two G01 fields were incomplete: literal immutable
execution bindings were absent, and the scoring tolerance, observed
denominators and unresolved Landmark caption/code endpoint join were not
operationally frozen.

Repair 1 adds only those command bindings and denominator semantics. It does
not change raw evidence, admit Landmark execution, pass G01/Gate A, or start a
scientific experiment.

## Correction rereview

Rereviewed commit: `39641db14c9999929f70ad26a08c5f70cb7c1120`
Rereviewed tree: `ec68df6efcaf39addf8571282b7cfcdc2d8bfeee`
Corrected protocol SHA-256: `dc19834b84e118c5a80ba0cd2f89ee2eb28526a595621cf6d0b920959265631d`

Final verdict: **ACCEPT; documentation/design only**.

The reviewer independently resolved the full native/harness plan hashes and
digests, execution-record hashes, resource limits and literal dispatch
commands for both accepted matrices.  They match the frozen plans.  Landmark
acquisition matches the reviewed partial checkout, and the document explicitly
admits no Landmark numerical command or queue.

The ratio predicate exactly matches the repaired scorer.  Accepted
defined/excluded/positive-loss-near-zero counts are Rice k1 `2999/1/0`, Skin
k1 `2999/1/0`, Skin k2 `2986/14/0`, and prospective random k1 `2999/1/0`.
Landmark has no accepted denominator; author prefixes 1..4999, a future
repaired 1..5000 set, and the separately labelled inclusive project slice
150..5000 (4851 prefixes) are not conflated.

This acceptance closes the two design-document defects.  It is not execution
permission, a G01 or Gate A pass, or Landmark/scientific admission.
