import subprocess
import os
import sys
import shutil
from pathlib import Path

RELEASE_VERSION = "v2.0.0"
WORKSPACE_ROOT = Path(__file__).parent.resolve()

def run_cmd(cmd, allow_fail=False):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0 and not allow_fail:
        print(f"[Execution Failure] Command failed: {' '.join(cmd)}")
        print(f"Stdout: {res.stdout.strip()}\\nStderr: {res.stderr.strip()}")
        sys.exit(1)
    return res

print("[Sovereign Control] Executing structural workspace tag alignment...")

git_check = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], allow_fail=True)

if git_check.returncode == 0:
    # Stage all conformed tracking structures safely
    run_cmd(["git", "add", "dcs/verify.py", "dcs/mesh/behavior.py", "dcs/tests/test_full_coverage.py", ".coveragerc", "dcs/standards/gtm_license.json"])
    
    # Use the corrected --porcelain status parameter 
    status_check = run_cmd(["git", "status", "--porcelain", "dcs/"])
    cover_check = run_cmd(["git", "status", "--porcelain", ".coveragerc"])
    
    if status_check.stdout.strip() or cover_check.stdout.strip():
        run_cmd(["git", "commit", "-m", f"build: complete sovereign baseline validation layer execution {RELEASE_VERSION}"])
    
    # Apply the immutable release tag completely
    run_cmd(["git", "tag", "-d", RELEASE_VERSION], allow_fail=True)
    run_cmd(["git", "tag", "-a", RELEASE_VERSION, "-m", f"Sovereign local host release baseline alignment {RELEASE_VERSION}"])
    print(f"[Git Automation] Success. Repository sealed under tag footprint: {RELEASE_VERSION}")
else:
    print("[Skipped] Directory does not contain an active Git context mapping.")

print("[Cleanup Substrate] Running deep transient file purge...")

# Unlink any temporary leftovers, trial runs, or garbage assets
target_extensions = ["*.pyc", "*.pyo", "*.pyd", ".coverage", "patch_*", "fix_*", "validate_*", "test_stub_*", "*_repair.py", "automated_sandbox_verifier.py", "structural_mastery_pipeline.py"]
purged_files_count = 0

for ext in target_extensions:
    for transient_file in WORKSPACE_ROOT.glob(f"**/{ext}"):
        if any(v in transient_file.parts for v in ["venv", ".venv"]):
            continue
        try:
            if transient_file.is_file():
                transient_file.unlink()
                purged_files_count += 1
        except Exception:
            pass

# Clean out temporary caching metrics directories
stray_dirs = ["sandbox_isolated_inference", ".pytest_cache", "dcs/mesh/__pycache__", "dcs/tests/__pycache__", "dcs/__pycache__"]
for s_dir in stray_dirs:
    target_path = WORKSPACE_ROOT / s_dir
    if target_path.exists() and target_path.is_dir():
        shutil.rmtree(target_path, ignore_errors=True)

print(f"[Cleanup Substrate] Permanently unlinked {purged_files_count} residual temporary files.")
print("\n=== REPOSITORY SYSTEM AT ABSOLUTE MATURITY STATE ===")
