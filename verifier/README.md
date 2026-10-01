# dcs-verify

Public in-toto DSSE envelope verifier.

    curl -X POST https://verify.dcs.dev/verify \
         -H 'content-type: application/json' \
         --data-binary @envelope.intoto.json

Response:

    {
      "valid": true,
      "subject": "dcs-self-...",
      "digest": "sha256:...",
      "predicate": "https://dcs.dannylabs.example/attestation/v1",
      "signatures": [{ "keyid": "...", "valid": true }]
    }

Deploy:

    cd verifier && npx wrangler deploy

Free tier handles 100k requests/day.
