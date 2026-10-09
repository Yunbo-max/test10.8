"""Collect terminal harness receipts and two output readbacks, without score replay."""
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timezone

run_id, batch_id, prefix_name, output_dir, collection_name, reservation_key = sys.argv[1:]
def identity(path):
    data = path.read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
receipt_path = Path('runs/attempts')/run_id/'receipt.json'
receipt = json.loads(receipt_path.read_text())
assert len(receipt['attempts']) == 1
attempt = receipt['attempts'][0]
attempt_path = Path(attempt['attempt_path'])
workspace = attempt_path/'workspace'
out = workspace/output_dir
files = []
for base in (Path('runs/attempts')/run_id, Path('runs/harness')/batch_id):
    for path in base.rglob('*'):
        if path.is_file() and 'workspace' not in path.parts:
            files.append(path)
if out.exists():
    files.extend(path for path in out.rglob('*') if path.is_file())
prefix = Path('evidence/dispatch')/prefix_name
files.extend(prefix.with_suffix(suffix) for suffix in ('.json', '.stdout.log', '.stderr.log'))
files = sorted(set(files))
usage = json.loads(prefix.with_suffix('.json').read_text())
assert attempt['status'] in ('completed', 'failed', 'timeout', 'interrupted')
expected_outputs = [out/'projector-certificate.jsonl', out/'projector-summary.json']
boundaries = []
if attempt['status'] == 'completed':
    assert all(path.is_file() for path in expected_outputs)
    boundaries = [[identity(path) for path in expected_outputs] for _ in range(2)]
    assert boundaries[0] == boundaries[1]
summary = json.loads(expected_outputs[1].read_text()) if expected_outputs[1].is_file() else None
collection = dict(format='exact-integer-projector-collection-v1', attempt_id=attempt['attempt_id'],
    status=attempt['status'], attempt_exit_code=attempt['exit_code'],
    launcher_usage=usage, output_readback_boundaries=boundaries,
    summary=summary, files=[identity(path) for path in files],
    scientific_gate_advanced=False, native_evaluator_qualified=False)
target = Path(collection_name)
with target.open('x') as stream:
    stream.write(json.dumps(collection, indent=2)+'\n')
budget_path = Path('BUDGET_OBSERVATION.json')
budget = json.loads(budget_path.read_text())
reservation = budget[reservation_key]
assert reservation['attempts_launched'] == 1 and not reservation['released']
reservation.update(attempt_id=attempt['attempt_id'], attempts_completed=1,
    released=True, release_basis='terminalnestedreceipt and postexit outputreadbacks; independent process reconciliation pending',
    execution_status=attempt['status']+'_pending_independent_evidence_review',
    waited_process_tree_cpu_seconds=usage['waited_process_tree_cpu_seconds'],
    actual_harness_wall_seconds=usage['wall_seconds'], maximum_child_rss_kib=usage['maximum_child_rss_kib'])
budget['observed_process_cpu_seconds'] += usage['waited_process_tree_cpu_seconds']
now = datetime.now(timezone.utc)
budget['observed_at'] = now.isoformat()
budget['remaining_wall_seconds_at_observation'] = (datetime.fromisoformat(budget['deadline_utc'].replace('Z', '+00:00'))-now).total_seconds()
budget_path.write_text(json.dumps(budget, indent=2)+'\n')
names = [str(path) for path in files]+[str(target), str(budget_path), 'evidence/dispatch/collect-integer-projector.py']
Path('/tmp/integer-projector-packet-files.json').write_text(json.dumps(names))
print(json.dumps(dict(status=attempt['status'], attempt_id=attempt['attempt_id'],
    packet_files=len(names), usage=usage, summary=summary)))
