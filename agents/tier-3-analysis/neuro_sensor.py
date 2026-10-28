import hashlib
import json

class TenEarsNeuroSensor:
    EARS = {
        "Sache":             ["fakt", "daten", "code", "beweis", "zahl"],
        "Beziehung":         ["du", "ihr", "macht", "hierarchie", "gegen"],
        "Appell":            ["muss", "sollte", "fordere", "tue", "verlange"],
        "Selbstoffenbarung": ["ich", "fühle", "denke", "mein", "habe"],
        "Trauma":            ["angst", "panik", "gefahr", "schmerz", "schock"],
        "Macht (Foucault)":  ["autorität", "herrschaft", "disziplin", "überwachen"],
        "Scham":             ["peinlich", "fehler", "versagen", "schlecht", "unwürdig"],
        "Ohnmacht":          ["hilflos", "ausgeliefert", "kontrolle", "ohnmächtig"],
        "System (Luhmann)":  ["struktur", "prozess", "regel", "system", "netzwerk"],
        "Haftung (BGB)":     ["klage", "schaden", "urteil", "gesetz", "recht", "vertrag"],
    }

    def scan_input(self, text: str) -> dict:
        t = text.lower()
        scores = {}
        for ear, kws in self.EARS.items():
            hits = sum(1 for kw in kws if kw in t)
            scores[ear] = min(1.0, hits / max(1, len(kws) * 0.5))
        return scores

class NeuroScanModul:
    def __init__(self):
        self.sensor = TenEarsNeuroSensor()

    def execute_scan(self, signal: str) -> dict:
        ears = self.sensor.scan_input(signal)
        scan_hash = hashlib.sha3_512(json.dumps(ears, sort_keys=True).encode()).hexdigest()[:16]
        return {
            "scan_id": f"NEURO_SCAN_{scan_hash}",
            "ear_data": ears,
            "dominant_ear": max(ears, key=ears.get) if ears else "None",
            "sensory_threat_level": round(ears.get("Trauma", 0) + ears.get("Macht (Foucault)", 0), 3),
        }
