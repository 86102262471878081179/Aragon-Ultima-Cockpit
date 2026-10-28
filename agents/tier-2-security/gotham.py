import time
import logging

logger = logging.getLogger("TIER-2-GOTHAM")

class GothamCitySandbox:
    """Arkham Cache für zerstörte Tokens."""
    
    def __init__(self):
        self.inmates = []

    def incarcerate(self, token: str, reason: str) -> str:
        inmate_id = hash(token) # Platzhalter, wird in main.py durch blake2b ersetzt
        inmate_id_str = f"{inmate_id:08x}"
        self.inmates.append({
            "id": inmate_id_str, "token": token, "reason": reason, "ts": time.time()
        })
        logger.warning(f"[GOTHAM] Inmate {inmate_id_str} eingesperrt: {reason[:60]}")
        return inmate_id_str
