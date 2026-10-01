# Operations Runbook

Generated: 2026-10-01T17:46:00.526587+00:00
Commit: 4e0d7f8721dd894fe264dc7acaea1e9e82e4d84b

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
