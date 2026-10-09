import datetime, json, resource, subprocess, time
from pathlib import Path
command = ["python3", "vendor/rsi/scripts/run_harness.py", "plans/harness-formal-geometric-target61-02.json", "--root", str(Path.cwd()), "--execute", "--approved-plan-digest", "34deb544034d52ad591e6f1be2de2e7fe2e8e915be085fc7abe5cd6a36f362f9"]
prefix = Path("evidence/dispatch/formal-geometric-target61-02")
started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
start = time.monotonic()
before = resource.getrusage(resource.RUSAGE_CHILDREN)
with prefix.with_suffix(".stdout.log").open("xb") as out, prefix.with_suffix(".stderr.log").open("xb") as err:
    result = subprocess.run(command, stdout=out, stderr=err, check=False)
after = resource.getrusage(resource.RUSAGE_CHILDREN)
record = {"command":command,"cwd":str(Path.cwd()),"started_at":started_at,"completed_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"exit_code":result.returncode,"wall_seconds":time.monotonic()-start,"waited_process_tree_cpu_seconds":after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,"maximum_child_rss_kib":after.ru_maxrss,"cpu_semantics":"RUSAGE_CHILDREN delta for waited harness and reaped descendants; failed/unreaped processes could undercount", "scientific_gate_advanced":False}
with prefix.with_suffix(".json").open("x") as stream: stream.write(json.dumps(record,indent=2)+"\n")
print(json.dumps(record))
raise SystemExit(result.returncode)
