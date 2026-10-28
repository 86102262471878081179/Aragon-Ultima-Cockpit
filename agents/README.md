# 🏛️ TIER-1: GOVERNANCE (Die höchste Instanz)

> **"Die Matrix ist souverän. Der Operator ist das letzte Wort."**

Das `tier_1_governance`-Modul ist das absolute Rückgrat der Aragon-Ultima-Infrastruktur. 
Während sich `tier-2-security` um die Abwehr von Angriffen und `tier-3-analysis` um die Intelligenz und Generierung kümmern, trifft Tier-1 die **finalen Entscheidungen**. 

Hier wird die Grenze zwischen der KI und dem Menschen (Apex Operator) gezogen. Kein Token verlässt das System, ohne dass Tier-1 ihm zugestimmt hat.

---

## 🎯 Kernaufgaben

1. **Authentifizierung (Der Wächter):** Verifiziert das `Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC`. Kein Zugriff ohne den Master-Seal. Timing-sicher via `hmac.compare_digest`.
2. **Entscheidungsgewalt (Der Dirigent):** Der `SovereignApexController` fungiert als oberster Gerichtshof. Wenn das System in den Shutdown (Dorsal-Vagal) geht, hat Tier-1 das Recht, einzugreifen.
3. **Unveränderlichkeit (Das Gesetzbuch):** Jede Entscheidung wird über die `ASME01MetaEngine` versiegelt und dem unauslöschlichen WORM-Ledger (Write Once Read Many) übergeben.
4. **Apex Override:** Die menschliche Komponente. Egal was die KI in Tier-3 berechnet – Tier-1 kann den Befehl des Operators erzwingen.

---

## 🧩 Enthaltene Module

*   **`apex_controller.py`**
    *   Enthält den `SovereignApexController`.
    *   Zieht Fäden aus Tier-2 (Sicherheit) und Tier-3 (Analyse) zusammen.
    *   Prüft, ob ein Ergebnis die "Apex-Hemmung" (Veto) passieren darf.
*   **`seal_verifier.py`**
    *   Die Firewall für alle API-Endpunkte.
    *   Überprüft den `auth_seal` bei jedem eingehenden Request (z.B. `/api/v1/apex/process`).
*   **`council_engine.py`** *(Optional / Zukünftig)*
    *   Die Logik für das Council-Voting (Ratsentscheidungen).

---

## 🏛️ Die 4 Gesetze der Governance

1. **Gesetz der Souveränität:** Das System ist autark. Es gibt keine externen APIs, die nicht durch Tier-1 validiert wurden.
2. **Gesetz der Ringe:** Jede Entität (die 201+ Nodes) ist einem Ring (0 bis Ω) unterworfen. Tier-1 verwaltet diese Hierarchie.
3. **Gesetz des WORM:** Jede Entscheidung, die Tier-1 passiert, wird für die Ewigkeit im Ledger eingebrannt.
4. **Gesetz des Apex:** Die Maschine darf Vorschläge machen (Tier-3), aber die letzte Unterschrift leistet der Operator.

---

## 🛡️ Integration im Code

Alle FastAPI-Routen, die als "geschützt" markiert sind, importieren den Verifier aus diesem Ordner:

```python
from agents.tier_1_governance.seal_verifier import verify_seal

@app.post("/api/v1/apex/process")
async def apex_process(request: ApexRequest):
    # Tier-1 Governance: Der Wächter steht am Tor
    if not verify_seal(request.auth_seal):
        return {"status": "403_FORBIDDEN", "detail": "Invalid Seal"}
    
    # ... Weiterleitung an den Apex Controller ...
# Agent Registry

`agent_registry.json` ist das zentrale Verzeichnis der Agenten. Jeder Eintrag enthält eine stabile ID, einen Namen, ein Tier, einen Lebenszyklusstatus und eine Beschreibung. Der erste Eintrag ist nur ein geplanter Platzhalter; er führt keinen Agenten aus.

## Validieren

Mit Python 3 (keine Drittanbieterpakete erforderlich):

```bash
python3 -m agents.registry
python3 -m unittest discover -s tests/unit -p 'test_*.py' -v
```

Für eine andere Registerdatei kann der Pfad als Argument angegeben werden:

```bash
python3 -m agents.registry path/to/agent_registry.json
```

Das JSON-Schema für Editor- und CI-Integration liegt in `agent_registry.schema.json`. Zulässige Tiers: `tier-1-governance`, `tier-2-security`, `tier-3-analysis`. Zulässige Status: `planned`, `active`, `deprecated`.
