# Operations Runbook

Generated: 2026-10-01T17:44:48.814502+00:00
Commit: 4e87c94a4fb1bec2c6d9b03102e0891b38b4e70a

## Deploy
pip install dist/dcs-0.5.0-py3-none-any.whl

## Verify
python -c "from dcs.self import MANIFESTS; print(len(MANIFESTS))"

## Rollback
pip install dcs==<previous>

## Incident
1. Freeze CT log
2. Rotate key
3. Republish manifest
4. Notify
