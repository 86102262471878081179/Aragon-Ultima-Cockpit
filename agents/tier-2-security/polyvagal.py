class PolyvagalStateRegulator:
    """Polyvagal-Regler mit natürlichem Decay (Stress-Abbau)."""
    
    DECAY = 0.08

    def __init__(self):
        self.state = "VENTRAL_VAGAL"
        self.stress_level = 0.0

    def update(self, threat: float) -> str:
        self.stress_level = max(0.0, self.stress_level - self.DECAY)
        self.stress_level = min(1.0, self.stress_level + threat)
        
        if self.stress_level < 0.4:
            self.state = "VENTRAL_VAGAL"
            return "KREATIV_MODUS (Wusulum aktiv)"
        elif self.stress_level < 0.8:
            self.state = "SYMPATHIKUS"
            return "KAMPF_MODUS (Kortex aktiviert KrakenGuard)"
        
        self.state = "DORSAL_VAGAL"
        return "SHUTDOWN_MODUS (Fail-Closed)"

    def co_regulate(self, amount: float = 0.2) -> None:
        self.stress_level = max(0.0, self.stress_level - amount)
        if self.stress_level < 0.4:
            self.state = "VENTRAL_VAGAL"
