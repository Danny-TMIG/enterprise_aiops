# Operations Runbook

Generated: 2026-10-01T17:45:07.948548+00:00
Commit: e409d2fffa90fc04ff8542dde049d21672509acd

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
