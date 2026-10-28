import hashlib
import time

class WusulumCore:
    MAX_ENTROPY = 5.0

    def __init__(self):
        self.state = "GENESIS_WAHRHEIT"
        self.memory = []
        self.entropy_pool = 0.0

    def run_cycle(self) -> dict:
        self.entropy_pool = min(self.MAX_ENTROPY, self.entropy_pool + 0.1)
        # Simulierter Token-Fluss
        raw_token = f"TOKEN_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]}"
        self.memory.append(raw_token)
        self.state = raw_token
        
        return {
            "state": self.state,
            "entropy": round(self.entropy_pool, 2),
            "memory_size": len(self.memory)
        }
