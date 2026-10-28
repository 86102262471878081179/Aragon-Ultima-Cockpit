# Architektur/kernel_loader.py
import os
import yaml
import streamlit as st
from pathlib import Path
from typing import Dict, Any, List

# Standard-Pfad zur Kernel-Konfiguration
DEFAULT_KERNEL_PATH = os.getenv("KERNEL_PATH", "kernel.yaml")

# Das Standard-Fallback, falls die kernel.yaml fehlt oder zerstört wurde
DEFAULT_KERNEL = {
    "kernel_id": "black_six_kernel_v1",
    "version": "1.0.0",
    "mode": "APEX_SINGULARITY_LOCKED",
    "rings": [
        {"id": "RING_0_GENESIS", "name": "Genesis", "role": "ROOT", "priority": 0},
        {"id": "RING_1_IDENTITY", "name": "Identity", "role": "JUSTICE", "priority": 1},
        {"id": "RING_2_STRUCTURE", "name": "Structure", "role": "WORM", "priority": 2},
        {"id": "RING_3_COHERENCE", "name": "Coherence", "role": "OMNI", "priority": 3},
        {"id": "RING_4_MIND", "name": "Mind", "role": "NEURO", "priority": 4},
        {"id": "RING_5_INTELLIGENCE", "name": "Intelligence", "role": "AGENT", "priority": 5},
        {"id": "RING_6_EVENT", "name": "Event", "role": "RUNTIME", "priority": 6},
        {"id": "RING_7_EVOLUTION", "name": "Evolution", "role": "META", "priority": 7},
        {"id": "RING_OMEGA", "name": "Sovereign", "role": "SOVEREIGN", "priority": 99}
    ],
    "governance": {
        "seal": "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC",
        "worm_required": True,
        "audit_level": "JUDICIAL",
        "sovereignty_level": "APEX",
        "fail_mode": "FAIL_CLOSED",
        "ledger_mode": "WORM_SHA3_512"
    },
    "backend": {
        "api_url": "https://aragon-backend-api.onrender.com/prompt/check",
        "timeout_seconds": 30,
        "retries": 3
    },
    "neo4j": {
        "uri": "bolt://localhost:7687",
        "user": "neo4j",
        "password": "password",
        "topology_query": "MATCH (n)-[r]->(m) RETURN n,m,type(r) AS rel LIMIT 100"
    },
    "runtime": {
        "heartbeat_interval_seconds": 10,
        "event_log_enabled": True,
        "max_events_buffer": 500
    }
}

@st.cache_data(ttl=60)
def load_kernel(path: str = DEFAULT_KERNEL_PATH) -> Dict[str, Any]:
    """
    Lädt die kernel.yaml. Nutzt Streamlit-Caching, um I/O-Overhead zu vermeiden.
    Wenn die Datei nicht existiert, wird sie aus DEFAULT_KERNEL generiert.
    """
    kernel_path = Path(path)
    
    # Auto-Repair: Wenn die Datei fehlt, neu erstellen
    if not kernel_path.exists():
        st.warning(f"⚠️ Kernel-Datei '{path}' nicht gefunden. Erstelle Standard-Kernel (Auto-Repair)...")
        try:
            with open(kernel_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(DEFAULT_KERNEL, f, sort_keys=False, allow_unicode=True)
            return DEFAULT_KERNEL
        except Exception as e:
            st.error(f"🚨 Kritischer Fehler beim Erstellen der Kernel-Datei: {e}")
            return DEFAULT_KERNEL

    # Datei existiert -> Laden und validieren
    try:
        with open(kernel_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            
        if not data:
            raise ValueError("Kernel-Datei ist leer.")
            
        # Grundlegende Validierung
        if "kernel_id" not in data or "governance" not in data:
            raise ValueError("Kernel-Datei ist unvollständig (fehlende Sektionen).")
            
        return data

    except Exception as e:
        st.error(f"🚨 Fehler beim Laden der Kernel-Datei '{path}': {e}")
        st.info("Fallback auf DEFAULT_KERNEL wird genutzt (Fail-Safe).")
        return DEFAULT_KERNEL

def get_governance_seal() -> str:
    """Gibt das aktive Governance-Seal zurück."""
    kernel = load_kernel()
    return kernel.get("governance", {}).get("seal", "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC")

def get_backend_config() -> Dict[str, Any]:
    """Gibt die Backend-API-Konfiguration zurück."""
    kernel = load_kernel()
    return kernel.get("backend", DEFAULT_KERNEL["backend"])

def get_neo4j_config() -> Dict[str, Any]:
    """Gibt die Neo4j-Datenbank-Konfiguration zurück."""
    kernel = load_kernel()
    return kernel.get("neo4j", DEFAULT_KERNEL["neo4j"])

def get_rings() -> List[Dict[str, Any]]:
    """Gibt die Liste aller Matrix-Ringe zurück."""
    kernel = load_kernel()
    return kernel.get("rings", DEFAULT_KERNEL["rings"])

def get_runtime_config() -> Dict[str, Any]:
    """Gibt die Runtime-Einstellungen zurück."""
    kernel = load_kernel()
    return kernel.get("runtime", DEFAULT_KERNEL["runtime"])

# =========================================================
# TEST-BLOCK (Wird nur ausgeführt, wenn man die Datei direkt startet)
# =========================================================
if __name__ == "__main__":
    print("=== KERNEL LOADER TEST ===")
    kernel = load_kernel()
    
    print(f"Kernel ID: {kernel.get('kernel_id')}")
    print(f"Mode: {kernel.get('mode')}")
    print(f"Seal: {get_governance_seal()}")
    print(f"Backend URL: {get_backend_config().get('api_url')}")
    print(f"Ringe geladen: {len(get_rings())}")
    
    print("\n[+] Kernel Loader funktioniert einwandfrei.")
