# Final low-dimensional matrix repair execution

Status: **completed; numerical evidence pending independent review**.

The independently admitted repair-ordinal-2 plan ran exactly once. The native
attempt and harness exited 0. This document records collection and integrity;
it does not accept any score, ranking or scientific claim.

## Frozen execution

- admission commit: `303de52dee43131f60be5e1c1d61b85712ca733b`
- source commit: `a328a4d836c498bd2c0eb036e48ac9e622107254`
- native plan digest: `d30ea8255bb5b1c7f3eef43389b9399b63092f7ac782959dac8859d7bb863582`
- harness plan digest: `280abf635dfb5662bce6a15ffb63977c72d72a320f44ef22f1554d9ec5b9e6cf`
- attempt: `rice-skin-lowdim-existing-baseline-matrix-final-repair-a1-f1b61a189db048988917b37c2626a74f`
- retry count: 0
- receipt SHA-256: `4f22ba4f5f9537a4cbb04852e5f3e7ded9aa6fb3caeaabf8056eb1936001846e`
- attempt SHA-256: `55e5019310160efa0557affbea2eb2e80d0cae01408259d43148602e11dc7742`
- process-guard SHA-256: `e066b8b81ac0718687bcd7fa08033db4eb4cfe7f7c9f876a7fc2ff826c7dc607`
- stdout SHA-256: `a17bd4175f8da32dcbe3cf66823c2e7c15e6621d2756af08de63124c04768379`
- stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- manifest SHA-256: `87cca1fdb04f84c34504858d7e9bbfc462ea796a2227abfd3fec332b1cba6f7a`

The producer reports 22.415467461 wall seconds, 22.408896 process CPU seconds
and 158252 KiB maximum RSS. The enclosing receipt reports 23.842787581 seconds
and the harness reports 24.196666240 seconds. The five numerical thread
variables were all `1`; one CPU and no GPU were used.

## Post-exit collection

The receipt declares 82 unique outputs: one v3 manifest, three archives, 39 raw
JSONL files and 39 summaries. Two complete post-exit rehash passes found zero
mismatches across all 82. Independently rechecking the manifest's 81
pre-manifest `publication_observations` also found zero mismatches. Each archive
is readable, has 26 unique members, and every extracted member hash equals its
corresponding final raw or summary hash.

| Cohort archive | SHA-256 | Git blob | Members |
| --- | --- | --- | ---: |
| Rice k=1 | `e959e370355baf4d2a173c84f34a4596843696c90b8ed5a7bc4d50dd6a848197` | `074bfdd1263f9410e217a41f6b9243e68395a975` | 26 |
| Skin k=1 | `6f7985f7ae1f4f87844585d857986e1119413673d61343dffbe266fe364e1cea` | `597f616a235b8fa1843c9d1de49c7f30d9c40a41` | 26 |
| Skin k=2 | `95a9e652597ccb85d0842eb24ec3ff31551069d7e42cd6f3013fcb1c5538816a` | `b25bd2ba617ae5300a4c38386e9e3ba814f867bd` | 26 |

The surrounding workspace layer recreated eight hidden raw partial names and
two archive partial names after publication. Every recreated partial is a
different `(device,inode)` pair from its corresponding final. The finals remain
byte-identical to the receipt; the explicit inventory excluded all partials.
This is direct evidence that v3 isolated replayed progressive paths without
corrupting published evidence.

## Scope

The reservation is released. Executable/preparation attempts increase to 12;
scientific attempts and scientific failures remain zero. The cumulative
observed process CPU lower bound becomes 66.562782 seconds and peak preparation
RSS becomes 158252 KiB. No method comparison, parameter preference, Gate A,
G01/E04 decision, confirmation result or paper claim is admitted until an
independent reviewer verifies the exact committed receipt, manifest, archives,
logs and resource accounting.
