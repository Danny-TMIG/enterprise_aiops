# Operations Runbook

Generated: 2026-10-01T17:46:39.856814+00:00
Commit: ae8ff24073d649f7130c6d8bbe78f6520ff5acda

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
