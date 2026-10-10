import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
for script in ("solver_regression_v2.py", "landmark128_repair_v3.py"):
    completed = subprocess.run([sys.executable, script], cwd=HERE, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
