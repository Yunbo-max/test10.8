# B09 reproduction

Run under the preserved Simple .3 command supervisor with one process and
numeric threads1.  Inputs are the author Landmark matrix
`29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b`,
B07/B08 native512 array
`d0de6bb598161e85557321a309e9d720cb1c398b722140725e47d8365e3ec68a`,
and B07 semantic reference
`b8c4f5278fa58c96c485d6f547acdd927a5cd5153528219ebc1fd6ada4744fa5`.

1. Initialize with `config.json`.
2. Submit `plan_calibration.json`, then `plan_repeats.json`.
3. Freeze `B09_RUN_MANIFEST.json` and run the V1 audit.  It must retain the
   loss-trajectory failure.
4. Submit `plan_v2.json`.
5. Freeze `B09_V2_RUN_MANIFEST.json` and submit `plan_v2_audit.json`.

All raw JSON/NPZ, task contracts, stdout/stderr, receipts, runner database,
preflight reviews and failure records are retained in the evidence archive.
The 1024 command is calibration only; do not cite it as continuous-policy or
5000-row performance.
