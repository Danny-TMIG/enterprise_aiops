// verify.dcs.dev — public in-toto envelope verifier.
//
// POST /verify        body: JSON envelope
// GET  /health
//
// Returns { valid, subject, digest, keyid, error? }.
// No storage. No logging. No cost beyond Workers free tier.

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/health") {
      return json({ ok: true, service: "dcs-verify", version: "1.0.0" });
    }

    if (url.pathname === "/verify" || url.pathname === "/") {
      if (request.method !== "POST") {
        return json({ error: "POST required" }, 405);
      }
      let env;
      try {
        env = await request.json();
      } catch (e) {
        return json({ valid: false, error: "invalid JSON: " + e.message }, 400);
      }
      return await verify(env);
    }

    return json({ error: "not found" }, 404);
  },
};

async function verify(env) {
  if (env.payloadType !== "application/vnd.in-toto+json") {
    return json({ valid: false, error: "wrong payloadType" }, 400);
  }
  const sigs = env.signatures || [];
  if (!sigs.length) {
    return json({ valid: false, error: "no signatures" }, 400);
  }

  let payload;
  try {
    payload = Uint8Array.from(atob(env.payload), (c) => c.charCodeAt(0));
  } catch (e) {
    return json({ valid: false, error: "payload not base64" }, 400);
  }

  let stmt;
  try {
    stmt = JSON.parse(new TextDecoder().decode(payload));
  } catch (e) {
    return json({ valid: false, error: "payload not JSON" }, 400);
  }

  const results = [];
  for (const sig of sigs) {
    if (!sig.public || !sig.sig) {
      results.push({ keyid: sig.keyid, valid: false, error: "missing public or sig" });
      continue;
    }
    try {
      const raw = hexToBytes(sig.public);
      const key = await crypto.subtle.importKey(
        "raw", raw, { name: "Ed25519" }, false, ["verify"]
      );
      const sigBytes = Uint8Array.from(atob(sig.sig), (c) => c.charCodeAt(0));
      const ok = await crypto.subtle.verify("Ed25519", key, sigBytes, payload);
      results.push({ keyid: sig.keyid, valid: ok });
    } catch (e) {
      results.push({ keyid: sig.keyid, valid: false, error: String(e) });
    }
  }

  const allValid = results.every((r) => r.valid);
  return json({
    valid: allValid,
    subject: stmt.subject?.[0]?.name,
    digest: stmt.subject?.[0]?.digest?.sha256,
    predicate: stmt.predicateType,
    signatures: results,
  });
}

function hexToBytes(hex) {
  const out = new Uint8Array(hex.length / 2);
  for (let i = 0; i < out.length; i++) {
    out[i] = parseInt(hex.substr(i * 2, 2), 16);
  }
  return out;
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "content-type": "application/json",
      "access-control-allow-origin": "*",
    },
  });
}
