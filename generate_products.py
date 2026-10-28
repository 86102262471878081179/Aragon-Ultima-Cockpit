import os

PRODUCTS = {
    "ai-governance-platform": ("P01", "RING 1", "Die zentrale Verwaltungsoberfläche für KI-Modelle (EU AI Act Konformität)."),
    "compliance-engine": ("P02", "RING 1", "Überwacht die 125+ deterministischen Gesetze und Regeln."),
    "cybersecurity-suite": ("P03", "RING 2", "Enthält den Krisler Guard, eBPF-Metriken und Fail-Closed-Logik."),
    "data-fabric": ("P04", "RING 3", "Daten-Schnittstelle zwischen Streamlit, Registry und WORM."),
    "evidence-fabric": ("P05", "RING 1", "Der forensische Beweis-Tresor für Hash-Ketten (WORM)."),
    "legal-tech-suite": ("P06", "RING 1", "XJustiz, Fabrice, Der schwarze Richter (Justiz-Module)."),
    "orchestration-fabric": ("P07", "RING 5", "Die Steuerung für Docker, Go, Python und den Hypervisor."),
    "policy-fabric": ("P08", "RING 1", "Fabrice-Interpreter-Regeln und Policy-Engines."),
    "quantum-orchestrator": ("P09", "RING 2", "Zero-Knowledge-Proofs (Poseidon) und Post-Quantum Sicherheit."),
    "regulatory-fabric": ("P10", "RING 1", "Schnittstellen zu Behörden (z.B. BezReg Münster, Datenschutz)."),
    "sovereign-cloud": ("P11", "RING 0", "Container- und Kubernetes-Deployments der Infrastruktur."),
    "threat-intelligence": ("P12", "RING 5", "Grummel-Scanner, Gotham City, King_Ghost und Biene Maja.")
}

BASE_DIR = "products"

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

for folder, (pid, ring, desc) in PRODUCTS.items():
    path = os.path.join(BASE_DIR, folder)
    os.makedirs(path, exist_ok=True)
    
    # 1. __init__.py erstellen
    init_file = os.path.join(path, "__init__.py")
    with open(init_file, "w", encoding="utf-8") as f:
        f.write(f"# {pid} - {folder}\n")
        
    # 2. README.md erstellen
    readme_file = os.path.join(path, "README.md")
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(f"# {pid} :: {folder.upper()}\n\n")
        f.write(f"**Status:** ACTIVE\n")
        f.write(f"**Ring:** {ring}\n")
        f.write(f"**Seal:** Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC\n\n")
        f.write(f"## Beschreibung\n{desc}\n\n")
        f.write(f"## Integration\nDieses Modul wird über `product_index.py` im Streamlit-Cockpit geladen.\n")

print("✅ Alle 12 Produkt-Ordner wurden erfolgreich mit __init__.py und README.md befüllt.")
