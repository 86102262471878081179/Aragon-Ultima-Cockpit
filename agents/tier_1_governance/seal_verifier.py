import hmac
import os

EXPECTED_SEAL = os.getenv("EXPECTED_SEAL", "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC")

def verify_seal(provided_seal: str) -> bool:
    """Timing-sichere Prüfung des Auth-Seals."""
    if not provided_seal or not isinstance(provided_seal, str):
        return False
    try:
        return hmac.compare_digest(provided_seal, EXPECTED_SEAL)
    except (TypeError, AttributeError):
        return False
