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
scientific experiment. Independent rereview is pending.
