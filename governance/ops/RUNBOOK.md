# Operations Runbook

Generated: 2026-10-01T17:44:32.528788+00:00
Commit: 72687806f7047c9422294c2f9c2ecc012dfd9f94

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
