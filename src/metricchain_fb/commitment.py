"""Salted hash commitments for material that must stay undisclosed until an assessment.

Every branch of the repository is readable by every division, so a held-out list written in
clear text is disclosed the moment it is committed.  A *commitment* publishes only

    c = SHA-256( "metricchain-fb-commitment/1\\n" || salt || "\\n" || payload )

Later the custodian reveals ``salt`` and ``payload``; anyone can recompute ``c`` and see that
the payload was fixed before the reveal and was not changed afterwards.  The salt (32 random
bytes, hex) prevents confirming a guess of the payload from the commitment alone — necessary
here because the payloads are short lists drawn from a public database.

A commitment proves *that* a list was fixed; who has seen the list in the meantime is a
matter of custody and must be recorded separately (who holds the salt and the payload, where,
and since when).  The commitment gives no secrecy to a payload that is stored in the
repository in clear text.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets

__all__ = ["DOMAIN", "commit", "open_commitment", "new_salt"]

DOMAIN = b"metricchain-fb-commitment/1\n"


def new_salt() -> str:
    """256 random bits as lowercase hex."""
    return secrets.token_hex(32)


def commit(payload: bytes, salt_hex: str | None = None):
    """Returns ``(commitment_hex, salt_hex)``.  ``payload`` is committed byte for byte."""
    if not isinstance(payload, (bytes, bytearray)):
        raise TypeError("payload must be bytes (commit to an exact byte string)")
    salt_hex = new_salt() if salt_hex is None else salt_hex
    if len(salt_hex) != 64 or any(c not in "0123456789abcdef" for c in salt_hex):
        raise ValueError("salt must be 64 lowercase hex digits")
    digest = hashlib.sha256(DOMAIN + salt_hex.encode("ascii") + b"\n" + bytes(payload)).hexdigest()
    return digest, salt_hex


def open_commitment(commitment_hex: str, payload: bytes, salt_hex: str) -> bool:
    """True iff ``payload`` and ``salt_hex`` open the commitment."""
    try:
        digest, _ = commit(payload, salt_hex)
    except (TypeError, ValueError):
        return False
    return hmac.compare_digest(digest, commitment_hex)
