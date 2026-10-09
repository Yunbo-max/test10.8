# Independent source review: matrix publication repair

Reviewer: `/root/baseline_audit`  
Initial pinned commit: `b769760490492468061c6d0514d6a77a51dacee3`  
Initial pinned tree: `2b27b5f5458d0be80b18f884caa9c77f6b3b92b2`  
Initial verdict: **needs correction**.

No method, scorer, dataset, arm or parameter change was found. The initial
publication repair nevertheless had three evidence-integrity defects:

1. `os.replace(partial, output)` could overwrite a final path created after the
   initial absence check. Exclusive partial creation did not make final
   publication non-clobbering.
2. The final publication observations rehashed retained files but did not
   compare every fresh digest with the cohort archive and member digests
   computed earlier. An archive changed after its first verification could
   therefore be recorded in a zero-exit manifest with conflicting hashes.
3. The manifest partial path was absent from preflight, and staging was absent
   from the path-alias set. An aliased output could perform all arms before
   failing at publication.

The correction replaces rename with atomic hard-link publication that fails if
the final exists, then removes the partial only after the link succeeds. It
preflights every final, partial and staging path as a distinct unoccupied path,
and compares the complete final 81-file observation inventory (three archives,
39 raw files and 39 summaries) against all expected hashes before publishing
the manifest. Independent rereview is required before plan construction or
execution.

## Correction rereview

Final reviewed remote commit: `86bdfa7378d21bc239cf976f99a77b29b01007a7`

Final reviewed tree: `d4aabd418c2da2d424b87837dbac5f5c8d62fe0d`

Verdict: **accepted for source and publication contract only**.

The reviewer recomputed runner SHA-256
`e09d9d68d021433d691e74044b4cfe56d7f880a8bd3af04c077285e97df128c7`
and repair-record SHA-256
`984d83424a61e5a2fabfe55e3012ebdd0e417a99a59af99c8bb622eac21e9005`.
The no-clobber publication, 81-file pre-manifest inventory equality and full
path preflight close the three initial blockers. Archive rereading, fsync,
member rehashing and failure retention remain present; cohort enumeration,
parameters, scorer and loader are unchanged. A new plan may enumerate 82
successful outputs, but must still be independently reviewed, and collector
rehashing remains mandatory.
