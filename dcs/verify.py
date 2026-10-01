import hashlib
import inspect
import json
__version__ = "2.0.0"
try:
    import nacl.signing
    _NACL = True
    _HAS_NACL = True
except ImportError:
    _NACL = False
    _HAS_NACL = False
def digest_of(payload: str) -> str:
    return hashlib.sha256(payload.encode()).hexdigest()
