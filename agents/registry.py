# registry.py
"""
Lädt agent_registry.json, validiert gegen Schema, liefert Dict an main.py.
Wird beim Start der FastAPI-App aufgerufen (via lifespan).
"""
import json
import os
import hashlib
from typing import Dict, List, Any

REGISTRY_PATH = os.getenv("AGENT_REGISTRY_PATH", "agent_registry.json")
SCHEMA_PATH = os.getenv("AGENT_SCHEMA_PATH", "agent_registry.schema.json")


class RegistryLoader:
    def __init__(self, path: str = REGISTRY_PATH):
        self.path = path
        self.entities: Dict[str, dict] = {}
        self.master_seal: str = ""
        self.version: str = ""

    def load(self) -> Dict[str, dict]:
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Registry nicht gefunden: {self.path}")

        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.version = data.get("version", "unknown")
        self.master_seal = data.get("master_seal", "")

        self.entities = {}
        for e in data.get("entities", []):
            eid = e.get("id")
            if eid:
                self.entities[eid] = {
                    "name": e.get("name", "UNKNOWN"),
                    "ring": e.get("ring", "UNKNOWN"),
                    "talents": ", ".join(e.get("talents", [])),
                    "modules": ", ".join(e.get("modules", [])),
                    "status": e.get("status", "UNKNOWN"),
                    "seal": e.get("seal", ""),
                }
        return self.entities

    def verify_seals(self) -> bool:
        """Prüft, ob alle Entity-Seals zum Master-Seal passen."""
        for eid, e in self.entities.items():
            expected = hashlib.sha3_512(
                f"{eid}{e['name']}{e['ring']}".encode()
            ).hexdigest()[:32]
            if e["seal"] and not e["seal"].startswith(expected[:8]):
                return False
        return True

    def by_ring(self, ring: str) -> List[dict]:
        return [{"id": k, **v} for k, v in self.entities.items() if v["ring"] == ring]

    def by_module(self, module: str) -> List[dict]:
        return [{"id": k, **v} for k, v in self.entities.items() if module in v["modules"]]


# Singleton für Import
registry = RegistryLoader()
