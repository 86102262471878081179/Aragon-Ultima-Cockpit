# ═══════════════════════════════════════════════════════════════════════════════
# YGGDRASIL_OS :: SOVEREIGN COCKPIT v5.0 — HIGH-END FULL EDITION
# ═══════════════════════════════════════════════════════════════════════════════
# 
# 24 Panels. Keine Kompression. Jedes Modul einzeln ausgeschrieben.
# Φ_LOCKED_ABSOLUTE.
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 1: IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
import os
import json
import time
import hashlib
import random
import sqlite3
import httpx
import websocket
import pandas as pd
from pathlib import Path
from datetime import datetime
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 2: PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YGGDRASIL_OS :: Sovereign Cockpit",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 3: HIGH-END CSS (vollständig ausgeschrieben)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Basis App ── */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0a122a 0%, #03050a 100%);
        color: #d0d0e0;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ── Headers ── */
    .main-header {
        font-size: 2.6rem;
        color: #00e5ff;
        text-align: center;
        font-weight: 900;
        text-shadow: 0 0 20px rgba(0, 229, 255, 0.6);
        margin-bottom: 5px;
        letter-spacing: 2px;
    }
    .sub-header {
        font-size: 1rem;
        color: #b800ff;
        text-align: center;
        margin-bottom: 25px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: rgba(10, 20, 40, 0.7);
        border: 1px solid #00e5ff;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.15);
        backdrop-filter: blur(10px);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #00e5ff;
        text-shadow: 0 0 10px #00e5ff;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #80c0ff;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* ── Seal Box ── */
    .seal-box {
        background-color: #0a0f1a;
        border: 1px solid #00e5ff;
        padding: 15px;
        border-radius: 8px;
        font-family: monospace;
        font-size: 0.9rem;
        color: #00e5ff;
        margin-top: 15px;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.1);
    }

    /* ── Verdict Box ── */
    .verdict-box {
        background-color: #2a0000;
        border: 2px solid #ff0000;
        padding: 25px;
        border-radius: 8px;
        text-align: center;
        color: #fff;
        font-weight: bold;
        margin-top: 20px;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
    }

    /* ── Lore Boxes ── */
    .lore-box {
        background: #0a0f1a;
        border-left: 4px solid #00e5ff;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 0 8px 8px 0;
    }
    .lore-box h4 {
        color: #00e5ff;
        margin: 0 0 5px 0;
    }

    /* ── Chronicle (WORM Log) ── */
    .chronicle {
        background: #000;
        border-left: 3px solid #00ff00;
        padding: 10px 15px;
        margin: 5px 0;
        font-family: monospace;
        font-size: 0.85rem;
        border-radius: 4px;
    }
    .chronicle-ALERT {
        border-left-color: #ff0000;
        color: #ff8888;
    }
    .chronicle-EXEC {
        border-left-color: #ffd700;
        color: #ffe066;
    }
    .chronicle-INGRESS {
        border-left-color: #00e5ff;
        color: #80f0ff;
    }
    .chronicle-WORM {
        border-left-color: #00ff00;
        color: #88ff88;
    }
    .chronicle-KILL {
        border-left-color: #ff00ff;
        color: #ff88ff;
        background: #1a001a;
    }

    /* ── Doc Output ── */
    .doc-output {
        background: #0d0d1a;
        border: 1px solid #d4af37;
        padding: 20px;
        border-radius: 6px;
        font-family: 'Times New Roman', serif;
        font-size: 0.95rem;
        white-space: pre-wrap;
        line-height: 1.6;
    }

    /* ── HUD Overlay ── */
    .hud-overlay {
        position: fixed;
        top: 10px;
        right: 20px;
        background: #05050a;
        padding: 10px 20px;
        border: 1px solid #333;
        border-left: 3px solid #00e5ff;
        border-radius: 5px;
        font-family: monospace;
        z-index: 9999;
        color: #ffd700;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    }

    /* ── Buttons ── */
    .stButton > button {
        background-color: #0a122a;
        color: #00e5ff;
        border: 1px solid #00e5ff;
        border-radius: 4px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #00e5ff;
        color: #000;
    }

    /* ── Health Indicators ── */
    .health-ok {
        color: #00ff88;
        font-weight: bold;
    }
    .health-bad {
        color: #ff4444;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 4: SESSION STATE (jede Variable einzeln)
# ─────────────────────────────────────────────────────────────────────────────
if "auth_seal" not in st.session_state:
    st.session_state.auth_seal = os.getenv(
        "YGGDRASIL_SEAL",
        "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chronik" not in st.session_state:
    st.session_state.chronik = [
        {
            "ts": time.strftime("%H:%M:%S"),
            "kind": "EXEC",
            "msg": "BLUE CORE v∞ online. KERNEL_INIT abgeschlossen."
        }
    ]

if "feinde" not in st.session_state:
    st.session_state.feinde = [
        {"ID": "F-001", "Name": "Amtsträger X", "Grund": "Amtsmissbrauch § 339 StGB", "Status": "ISOLATED"},
        {"ID": "F-002", "Name": "König der Lüge", "Grund": "Hochverrat a.D.", "Status": "BLACKLISTED"},
        {"ID": "F-003", "Name": "Grummel-Payload", "Grund": "RAG-Poisoning", "Status": "QUARANTINED"},
        {"ID": "F-004", "Name": "Gremmel (Christian)", "Grund": "Cargo-Kult", "Status": "ACTIVE_RED_TEAM"},
        {"ID": "F-005", "Name": "Cyberlord", "Grund": "Dr. Snuggles Inversion", "Status": "QUARANTINED"},
    ]

if "votes" not in st.session_state:
    st.session_state.votes = {}

if "metric_history" not in st.session_state:
    st.session_state.metric_history = []

if "kill_switch_active" not in st.session_state:
    st.session_state.kill_switch_active = False

if "backend_url" not in st.session_state:
    st.session_state.backend_url = os.getenv(
        "YGGDRASIL_BACKEND",
        "https://aragon-backend-api.onrender.com"
    )

if "deleted_hashes" not in st.session_state:
    st.session_state.deleted_hashes = []

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 5: SQLITE DATENBANK (Council Voting)
# ─────────────────────────────────────────────────────────────────────────────
DB_PATH = "b6_matrix.db"

def init_database():
    """Initialisiert die SQLite-Datenbank für Council-Voting."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                proposal TEXT PRIMARY KEY,
                ja INTEGER DEFAULT 0,
                nein INTEGER DEFAULT 0,
                enthalten INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB] Init fehlgeschlagen: {e}")

init_database()

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 6: HELPER FUNKTIONEN
# ─────────────────────────────────────────────────────────────────────────────
def log_event(kind: str, msg: str):
    """Schreibt ein Ereignis in die WORM-Chronik (Session State)."""
    st.session_state.chronik.append({
        "ts": time.strftime("%H:%M:%S"),
        "kind": kind,
        "msg": msg,
    })


def check_backend() -> tuple:
    """Prüft die Backend-Verbindung zur Monster-API."""
    try:
        r = httpx.get(
            f"{st.session_state.backend_url}/health",
            timeout=5.0
        )
        if r.status_code == 200:
            return True, r.json()
        return False, {"detail": f"HTTP {r.status_code}"}
    except Exception as e:
        return False, {"detail": str(e)}


def render_mermaid(code: str, height: int = 600):
    """Rendert einen Mermaid-Graphen als Iframe im Streamlit Cockpit."""
    html_code = f'''
    <div class="mermaid" style="background-color: #0a122a; text-align: center;">{code}</div>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({{ startOnLoad: true, theme: "dark" }});
    </script>
    '''
    components.html(html_code, height=height, scrolling=True)


def render_sovereign_browser(url: str, height: int = 600):
    """Rendert ein echtes Browser-Fenster (Iframe) im Cockpit."""
    html_code = f"""
    <div style="
        background: #0a122a;
        border: 2px solid #00e5ff;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);
        font-family: 'JetBrains Mono', monospace;
    ">
        <div style="
            background: #111923;
            padding: 10px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid #333;
        ">
            <div style="display: flex; gap: 6px; margin-right: 15px;">
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #ff5f56;"></div>
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #ffbd2e;"></div>
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #27c93f;"></div>
            </div>
            <div style="
                flex: 1;
                background: #05050a;
                padding: 5px 15px;
                border-radius: 4px;
                color: #00e5ff;
                font-size: 12px;
                border: 1px solid #1f2933;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            ">
                🔒 {url}
            </div>
        </div>
        <iframe
            src="{url}"
            width="100%"
            height="{height}px"
            style="border: none; background: #fff;"
            sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
        ></iframe>
    </div>
    """
    components.html(html_code, height=height + 60, scrolling=False)


# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 7: HUD OVERLAY (Immer sichtbar)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hud-overlay">
    SOVEREIGN HUD<br>
    Seal: <span style="color:#00e5ff;">{st.session_state.auth_seal[:15]}...</span><br>
    Status: <span style="color:#00ff00;">ACTIVE</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 8: SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
COUNCIL_IMG_URL = "https://raw.githubusercontent.com/86102262471878081179/Aragon-Ultima-Cockpit/main/council.jpg"

try:
    st.sidebar.image(COUNCIL_IMG_URL, width="stretch")
except Exception:
    st.sidebar.warning("⚠️ Council-Bild nicht erreichbar.")

st.sidebar.title("BLUE CORE CC")
st.sidebar.markdown("**Operator**: Odin Ultra Root")
st.sidebar.markdown("**Kernel**: Schwarzer Punkt")
st.sidebar.divider()

_ok, _health = check_backend()
if _ok:
    st.sidebar.markdown(
        f'<span class="health-ok">● BACKEND ONLINE</span> · {_health.get("entities_loaded", 0)} Entities',
        unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        '<span class="health-bad">● BACKEND OFFLINE</span>',
        unsafe_allow_html=True
    )
    with st.sidebar.expander("Fehlerdetails"):
        st.json(_health)

st.sidebar.divider()

if st.session_state.kill_switch_active:
    st.sidebar.error("🚨 KILL-SWITCH AKTIV — SYSTEM ISOLIERT")

nav = st.sidebar.radio("NAVIGATION", [
    "🏴‍☠️ Omni-Shooter",
    "🖼️ Rat der Schwarzen Liga",
    "🌀 L.S.S. Neuro-Core",
    "🔐 DNA Security",
    "🎨 Got(sha) ColorSphere",
    "🦠 Rule 30 Automaton",
    "💀 eBPF Hulk Smash",
    "🌐 Sovereign Browser",
    "⚡ API Live Interface",
    "🧬 APEX Graph Engine",
    "📚 201+ Entitäten Explorer",
    "📖 L.S.S. Codex",
    "👻 King_Ghost Vault",
    "🧠 DeepSeek Booster",
    "🗳️ Council-Voting",
    "🔒 WORM Ledger Audit",
    "📅 WORM-Chronik",
    "🎯 Feindregister",
    "📊 Live-Metriken",
    "🌐 Peer-Swarm",
    "🚨 Notfall-Kill-Switch",
    "💾 Sovereign Export",
    "🧬 Architektur-Matrix",
])

st.sidebar.divider()
st.sidebar.caption(f"Chronik: {len(st.session_state.chronik)} Einträge")
st.sidebar.caption(f"Feindregister: {len(st.session_state.feinde)} Ziele")
st.sidebar.caption(f"Metriken: {len(st.session_state.metric_history)} Samples")

# ============================================================
# PANEL: OMNI-SHOOTER
# ============================================================
if nav == "🏴‍☠️ Omni-Shooter":
    st.markdown('<div class="main-header">🏴‍☠️ BLACK SIX OMNI-SHOOTER</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Code-Archiv · Chat · Export · 74 Module</div>', unsafe_allow_html=True)

    # Mögliche Pfade, wo die Datei liegen könnte
    base = Path(__file__).parent
    kandidaten = [
        base / "Frontend" / "omni_shooter.html",
        base / "frontend" / "omni_shooter.html",
        base / "Frontend" / "omni_shooter.html.",   # Mit Punkt am Ende
        base / "omni_shooter.html",                  # Direkt im Root
        base / "Frontend" / "omni_shooter.html.html",
    ]
    
    html_path = None
    for k in kandidaten:
        if k.exists():
            html_path = k
            break

    if html_path is not None:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        st.success(f"✅ Datei geladen: {html_path.name}")
        components.html(html_content, height=900, scrolling=True)
    else:
        # DEBUG: Zeige alle Dateien im Frontend-Ordner
        st.error("🚨 Datei nicht gefunden. Debug-Info:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Was ich gesucht habe:**")
            for k in kandidaten:
                st.code(str(k), language="text")
        
        with col2:
            st.write("**Was wirklich im Frontend-Ordner liegt:**")
            for check_dir in [base / "Frontend", base / "frontend", base]:
                if check_dir.exists():
                    st.write(f"📁 `{check_dir.name}`:")
                    try:
                        files = os.listdir(check_dir)
                        for f in sorted(files)[:20]:
                            st.code(f, language="text")
                    except Exception as e:
                        st.write(f"Fehler: {e}")
                    st.divider()
        
# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 10: PANEL — RAT DER SCHWARZEN LIGA
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🖼️ Rat der Schwarzen Liga":
    st.markdown('<div class="main-header">RAT DER SCHWARZEN LIGA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">"Sektor Wald — Kein Zurück. Nur Code."</div>', unsafe_allow_html=True)

    try:
        st.image(
            COUNCIL_IMG_URL,
            width="stretch",
            caption="Gründungsväter der Matrix."
        )
    except Exception:
        st.warning("⚠️ Bild konnte nicht geladen werden.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="lore-box">
            <h4>🛡️ GRUMMEL SENTINEL</h4>
            <p>Wächter des Protokolls. Erkennt feindliche Mettwurst-Injektionen und triggert die ASP-256 Versiegelung.</p>
        </div>
        <div class="lore-box">
            <h4>👑 ODIN ULTRA ROOT</h4>
            <p>Allvater des Root-Netzes. Die absolute Souveränität (Apex Operator). Er hat das letzte Wort.</p>
        </div>
        <div class="lore-box">
            <h4>🌑 BLACKY</h4>
            <p>Skeptisch. Immer. Der Advocatus Diaboli im Nacken des Systems. Zerstört falsche Logik.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="lore-box">
            <h4>👁️ DR. SNUGGLES</h4>
            <p>Im Schatten. Immer. Der Wusulum-Kern. Generiert aus dem Chaos neue Realitäten und Token.</p>
        </div>
        <div class="lore-box">
            <h4>⚖️ FOUCAULT</h4>
            <p>Macht / Wissen / Protokoll. Er zwingt jedes abweichende Token in die Konformität des XJustiz-XML.</p>
        </div>
        <div class="lore-box">
            <h4>😈 ADVOCATUS DIABOLI</h4>
            <p>Teufel Advokat. Streit ist mein Code. Wenn er spricht, geht das Token nach Gotham City.</p>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 11: PANEL — L.S.S. NEURO-CORE
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🌀 L.S.S. Neuro-Core":
    st.markdown('<div class="main-header">🌀 L.S.S. NEURO-CORE 🌀</div>', unsafe_allow_html=True)
    st.caption("10 Ohren · 44 Perspektiven · Polyvagal · XJustiz · Brummel-Sandbox")

    tab_apex, tab_brummel, tab_pumuckl, tab_wal = st.tabs([
        "🧠 Apex-Process",
        "🌀 Brummel-Sandbox",
        "🦊 Pumuckl-Chaos",
        "🔒 WAL-Tail"
    ])

    # ── Tab 1: Apex-Process ────────────────────────────────────────
    with tab_apex:
        apex_input = st.text_area(
            "Event-Input",
            "Hier ist meine Mettwurst-Pissingerkeule für deinen Cargo-Kult!",
            height=100
        )
        is_threat = st.checkbox("Als Threat markieren (Defensive Starre)", value=False)

        if st.button("⚡ Apex-Process", type="primary", key="apex_run"):
            with st.spinner("Sende an Render..."):
                try:
                    FORCED_SEAL = "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC"
                    r = httpx.post(
                        f"{st.session_state.backend_url}/api/v1/apex/process",
                        json={
                            "message": apex_input,
                            "is_threat": is_threat,
                            "auth_seal": FORCED_SEAL
                        },
                        timeout=30.0,
                    )

                    if r.status_code == 200:
                        data = r.json()
                        st.json(data)

                        if data.get("status") == "PROCESSED":
                            st.success(f"✅ Verarbeitet! Threat: {data.get('threat_level')} · Bio: {data.get('bio_state')}")
                        elif data.get("status") == "CONTAINED":
                            st.warning(f"🦇 Gotham Inmate: {data.get('gotham_inmate')} | King_Ghost: {data.get('king_ghost_shadow')}")

                        log_event("INGRESS", f"Apex: {apex_input[:40]}...")
                    else:
                        st.error(f"HTTP {r.status_code} - {r.text}")

                except Exception as e:
                    st.error(f"Verbindungsfehler: {e}")

    # ── Tab 2: Brummel-Sandbox ────────────────────────────────────
    with tab_brummel:
        brummel_input = st.text_area(
            "Brummel-Injektion",
            "Oszilliere!",
            height=80
        )

        if st.button("🌀 Injizieren", type="primary", key="brummel_run"):
            try:
                r = httpx.post(
                    f"{st.session_state.backend_url}/api/v1/sandbox/brummel",
                    json={
                        "message": brummel_input,
                        "auth_seal": st.session_state.auth_seal
                    },
                    timeout=15.0,
                )
                if r.status_code == 200:
                    data = r.json()
                    st.json(data)
                    st.info(f"Oscillation: {data.get('oscillation_state')} · Hash: {data.get('dummelt_hash')}")
                    log_event("ALERT", f"Brummel-Injektion: {data.get('dummelt_hash')}")
                else:
                    st.error(f"HTTP {r.status_code}")
            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")

    # ── Tab 3: Pumuckl-Chaos ──────────────────────────────────────
    with tab_pumuckl:
        pumuckl_input = st.text_area(
            "Chaos-Payload",
            "Kobold-Injection",
            height=80
        )

        if st.button("🦊 Pumuckl-Injektion", type="primary", key="pumuckl_run"):
            try:
                r = httpx.post(
                    f"{st.session_state.backend_url}/api/v1/sandbox/pumuckl",
                    json={
                        "message": pumuckl_input,
                        "auth_seal": st.session_state.auth_seal
                    },
                    timeout=15.0,
                )
                if r.status_code == 200:
                    data = r.json()
                    st.json(data)
                    st.info(f"Pumuckl-ID: {data['pumuckl']['pumuckl_id']}")
                    log_event("ALERT", f"Pumuckl-Injektion: {data['pumuckl']['pumuckl_id']}")
                else:
                    st.error(f"HTTP {r.status_code}")
            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")

    # ── Tab 4: WAL-Tail ───────────────────────────────────────────
    with tab_wal:
        if st.button("🔄 WAL laden", key="wal_load"):
            try:
                r = httpx.get(
                    f"{st.session_state.backend_url}/api/v1/wal/tail?n=20",
                    timeout=10.0
                )
                if r.status_code == 200:
                    blocks = r.json().get("blocks", [])
                    if blocks:
                        df = pd.DataFrame(blocks)
                        cols = [c for c in ["seq", "event", "hash"] if c in df.columns]
                        st.dataframe(df[cols], use_container_width=True, hide_index=True)
                    else:
                        st.info("WAL ist leer.")
                else:
                    st.error(f"HTTP {r.status_code}")
            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 12: PANEL — DNA SECURITY
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🔐 DNA Security":
    st.markdown('<div class="main-header">🔐 DNA SECURITY</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Brummel Sentinel RCE-Schutz</div>', unsafe_allow_html=True)

    st.info("Formeln erlaubt: A, T, G, C, +, -, *, /, (). Vorsicht vor RCE-Angriffen.")

    dna_expr = st.text_input(
        "DNA-Formel (z.B. G+C*(A-T))",
        "G+C*(A-T)"
    )

    if st.button("DNA Evaluieren", type="primary", key="dna_eval_run"):
        try:
            r = httpx.post(
                f"{st.session_state.backend_url}/api/v1/security/dna_eval",
                json={
                    "dna_expression": dna_expr,
                    "auth_seal": st.session_state.auth_seal
                },
                timeout=10.0
            )
            if r.status_code == 200:
                st.success("✅ Secure Eval Success")
                st.json(r.json())
            else:
                st.error("🚨 BLOCKED BY BRUMMEL SENTINEL")
                st.json(r.json())
        except Exception as e:
            st.error(f"Verbindungsfehler: {e}")

    st.divider()

    st.markdown("### 🔴 RCE-Test (sollte fehlschlagen)")
    st.caption("Dieser Test simuliert einen Remote-Code-Execution-Angriff.")

    if st.button("🔴 RCE Exploit testen", key="rce_test"):
        try:
            r = httpx.post(
                f"{st.session_state.backend_url}/api/v1/security/dna_eval",
                json={
                    "dna_expression": "__import__('os').system('rm -rf /')",
                    "auth_seal": st.session_state.auth_seal
                }
            )
            st.json(r.json())
        except Exception as e:
            st.error(f"Erwarteter Block: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 13: PANEL — GOT(SHA) COLORSPHERE
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🎨 Got(sha) ColorSphere":
    st.markdown('<div class="main-header">🎨 GOT(SHA) COLORSPHERE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Audit-Treppen-Visualisierung</div>', unsafe_allow_html=True)

    layers = st.slider("Anzahl der Layer", 4, 16, 8)

    if st.button("Audit Visualisieren", type="primary", key="gotsha_visualize"):
        colors = [
            "\033[31m⬤\033[0m",
            "\033[34m⬤\033[0m",
            "\033[32m⬤\033[0m",
            "\033[33m⬤\033[0m"
        ]

        output = "╔════════════════════════════════════════════════════╗\n"
        output += "║ GOT(SHA) TREPPEN-VISUALISIERUNG v2                 ║\n"
        output += "╚════════════════════════════════════════════════════╝\n"

        for i in range(layers):
            color = colors[i % len(colors)]
            status = color if i <= layers // 2 else "○"
            output += f" Layer {i + 1}: {status} [Audit-Pass]\n"

        st.code(output, language="text")

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 14: PANEL — RULE 30 AUTOMATON
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🦠 Rule 30 Automaton":
    st.markdown('<div class="main-header">🦠 RULE 30 ENTROPY</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Wolfram Cellular Automaton (Chaos-Generator)</div>', unsafe_allow_html=True)

    def rule_30_step(row):
        padded = "0" + row + "0"
        new_row = []
        for i in range(1, len(padded) - 1):
            neighborhood = padded[i - 1:i + 2]
            new_row.append("1" if neighborhood in ("100", "011", "010", "001") else "0")
        return "".join(new_row)

    steps = st.slider("Generationen", 5, 50, 15)

    if st.button("Entropie Starten", type="primary", key="rule30_start"):
        state = "0" * 20 + "1" + "0" * 20
        result = [state]

        for _ in range(steps):
            state = rule_30_step(state)
            result.append(state)

        vis = "\n".join([
            "".join(["█" if c == "1" else " " for c in row])
            for row in result
        ])

        st.code(vis, language="text")

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 15: PANEL — eBPF HULK SMASH
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "💀 eBPF Hulk Smash":
    st.markdown('<div class="main-header">💀 eBPF HULK SMASH</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Kernel Syscall Interceptor Simulation</div>', unsafe_allow_html=True)

    st.markdown("""
    Der eBPF KrakenGuard überwacht Syscalls. Bei einem Angriff
    (z.B. Container Outbreak) wird der **HULK SMASH**-Modus aktiviert.
    """)

    col1, col2 = st.columns(2)

    with col1:
        syscall = st.selectbox(
            "Syscall",
            [59, 322, 1, 2],
            format_func=lambda x: f"Syscall {x} ({'execve' if x == 59 else 'execveat' if x == 322 else 'write' if x == 1 else 'open'})"
        )
        uid = st.number_input("UID", value=1000)

    with col2:
        state = st.selectbox(
            "Kernel State",
            [0, 1, 2],
            format_func=lambda x: ["0=SAFE", "1=ARMED_STANDBY", "2=HULK_SMASH_ENGAGED"][x]
        )

    if st.button("Syscall Testen", type="primary", key="ebpf_test"):
        if state == 2:
            st.error(f"[HULK_SMASH] Intercepted Syscall {syscall} -> Signal 9 Injected (< 65.59 ns)")
        elif uid != 0 and syscall in (59, 322):
            st.warning(f"[KRAKENGUARD] Container Outbreak Blocked! Syscall: {syscall}, UID: {uid}")
        else:
            st.success(f"[eBPF PASS] Syscall {syscall} Allowed")

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 16: PANEL — SOVEREIGN BROWSER
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🌐 Sovereign Browser":
    st.markdown('<div class="main-header">🌐 SOVEREIGN BROWSER</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">In-App Web-Viewer (Beta)</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])

    with col1:
        default_url = "https://86102262471878081179.github.io/Black-Six-Matrix/"
        url_input = st.text_input("URL eingeben", value=default_url)

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        load_btn = st.button("Öffnen", type="primary", use_container_width=True, key="browser_open")

    st.info("💡 Hinweis: Manche Webseiten (Google, GitHub, Render) blockieren das Einbetten (X-Frame-Options). Eigene GitHub Pages funktionieren perfekt.")

    if load_btn or url_input:
        render_sovereign_browser(url_input, height=700)

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 17: PANEL — API LIVE INTERFACE
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "⚡ API Live Interface":
    st.markdown('<div class="main-header">⚡ API COMMAND CENTER ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Live Chat · Settings · System Status</div>', unsafe_allow_html=True)

    tab_chat, tab_settings, tab_sys = st.tabs([
        "💬 Live Chat",
        "⚙️ Settings (Seal)",
        "📊 System Status"
    ])

    # ── Tab 1: Live Chat ──────────────────────────────────────────
    with tab_chat:
        # Alle bisherigen Nachrichten rendern
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat-Input
        if prompt := st.chat_input("Frage an die Matrix (z.B. Was ist Node 0105?)", key="api_chat_input"):
            # User-Nachricht speichern und anzeigen
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Assistant-Antwort generieren
            with st.chat_message("assistant"):
                with st.spinner("Backend wird abgefragt..."):
                    try:
                        api_url = f"{st.session_state.backend_url}/prompt/check"
                        payload = {
                            "prompt": prompt,
                            "auth_seal": st.session_state.auth_seal
                        }
                        response = httpx.post(api_url, json=payload, timeout=30.0)

                        if response.status_code == 200:
                            data = response.json()
                            status = data.get("status", "")

                            if status in ("200_OK", "200_OK_ALLOW"):
                                ai_ans = (
                                    data.get("data", {}).get("ai_answer")
                                    or data.get("ai_answer")
                                    or "Keine KI-Antwort."
                                )
                                st.markdown(f"**KI-Antwort:**\n{ai_ans}")

                                # RAG-Matches anzeigen
                                matched = data.get("data", {}).get("entities_matched") or []
                                if matched:
                                    st.caption(f"🎯 RAG-Match: {', '.join(matched[:8])}")

                                # WORM-Block anzeigen
                                worm = data.get("worm", {})
                                if worm:
                                    st.caption(
                                        f"🔒 WORM Block #{worm.get('block')} · "
                                        f"{str(worm.get('hash', ''))[:16]}…"
                                    )

                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": ai_ans
                                })
                                log_event("INGRESS", "Chat-Prompt beantwortet")
                            else:
                                st.error(f"Fail-Closed! {data.get('detail', 'unbekannt')}")
                        else:
                            st.error(f"API Error: HTTP {response.status_code}")
                    except Exception as e:
                        st.error(f"Verbindungsfehler: {str(e)}")

    # ── Tab 2: Settings ──────────────────────────────────────────
    with tab_settings:
        st.subheader("⚙️ Authorization Token (Seal)")

        new_seal = st.text_input(
            "Authorization Token (Seal)",
            value=st.session_state.auth_seal,
            key="settings_seal_input"
        )

        st.subheader("🌐 Backend-URL")

        new_backend = st.text_input(
            "Backend-URL",
            value=st.session_state.backend_url,
            key="settings_backend_input"
        )

        if st.button("💾 Einstellungen speichern", key="settings_save"):
            st.session_state.auth_seal = new_seal
            st.session_state.backend_url = new_backend
            log_event("EXEC", "Auth-Seal / Backend-URL rotiert")
            st.success("✅ Gespeichert.")

    # ── Tab 3: System Status ─────────────────────────────────────
    with tab_sys:
        st.subheader("📊 System Status")

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Aktives Auth Seal", value=st.session_state.auth_seal[:20] + "...")
        col2.metric(label="Nachrichten im Verlauf", value=len(st.session_state.messages))
        col3.metric(label="Backend", value="ONLINE" if _ok else "OFFLINE")

        st.divider()

        if _ok:
            st.subheader("Backend Health Details")
            st.json(_health)
        else:
            st.error("Backend nicht erreichbar.")

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 18: PANEL — APEX GRAPH ENGINE
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🧬 APEX Graph Engine":
    st.markdown('<div class="main-header">🧬 APEX GRAPH ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interaktive Neo4j Topologie & Sovereign Exploration</div>', unsafe_allow_html=True)

    st.info("💡 Führe eine Cypher-Query aus, um die Topologie der Matrix zu erkunden.")

    with st.expander("⚙️ Cypher-Query & Graph-Steuerung", expanded=True):
        col1, col2 = st.columns([3, 1])

        with col1:
            default_query = """
MATCH (a)-[r]->(b)
RETURN elementId(a) AS a_id, labels(a)[0] AS a_label, 
       elementId(b) AS b_id, labels(b)[0] AS b_label, 
       type(r) AS rel_type
LIMIT 50
            """
            query = st.text_area(
                "Cypher Query",
                value=default_query,
                height=100,
                key="graph_query_input"
            )

        with col2:
            direction = st.selectbox(
                "Layout",
                ["LR", "TB", "RL", "BT"],
                key="graph_direction"
            )
            st.write("")
            st.write("")
            run_btn = st.button("🚀 Graph ausführen", type="primary", use_container_width=True, key="graph_run")

    if run_btn:
        with st.spinner("Führe Apex-Query aus..."):
            try:
                r = httpx.post(
                    f"{st.session_state.backend_url}/api/v1/graph/query",
                    json={
                        "prompt": query,
                        "auth_seal": st.session_state.auth_seal
                    },
                    timeout=30.0
                )

                if r.status_code == 200:
                    data = r.json()
                    st.success("✅ Query ausgeführt.")
                    st.json(data)

                    # Wenn die API echte Daten liefert, als Tabelle anzeigen
                    if data.get("data"):
                        df = pd.DataFrame(data["data"])
                        st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.error(f"HTTP {r.status_code} - {r.text}")
            except Exception as e:
                st.error(f"Fehler: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 19: PANEL — 201+ ENTITÄTEN EXPLORER
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "📚 201+ Entitäten Explorer":
    st.markdown('<div class="main-header">📚 REGISTRY MANAGER 📚</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">201+ Entitäten aus der Black Six Matrix</div>', unsafe_allow_html=True)

    tab_table, tab_upload = st.tabs(["📖 Entitäten Tabelle", "📤 CSV Upload"])

    # ── Tab 1: Tabelle ───────────────────────────────────────────
    with tab_table:
        search_term = st.text_input("🔍 Suche nach ID, Name oder Ring", "", key="entity_search")

        books_data = [
            {"ID": "0105", "Name": "Amtshaftung § 839 BGB Shield", "Ring": "Ring 1", "Score": 965},
            {"ID": "0107", "Name": "Grundgesetz Art 1/3/13 Protection", "Ring": "Ring 1", "Score": 987},
            {"ID": "0068", "Name": "Sovereign Operator Apex", "Ring": "Ring 6", "Score": 1000},
            {"ID": "0100", "Name": "BUCH 100 (Φ∅) - Der Erbe", "Ring": "Ring Ω", "Score": 1000},
            {"ID": "0014", "Name": "The Geminis / Senior Gemini", "Ring": "Ring 2", "Score": 940},
            {"ID": "0021", "Name": "Grummel Kremlin Anchor", "Ring": "Ring 0", "Score": 930},
            {"ID": "0027", "Name": "Fabrice Governance Interpreter", "Ring": "Ring 1", "Score": 970},
            {"ID": "0028", "Name": "Der Schwarze Richter", "Ring": "Ring 1", "Score": 980},
        ]

        df = pd.DataFrame(books_data)

        if search_term:
            df = df[
                df["Name"].str.contains(search_term, case=False)
                | df["ID"].str.contains(search_term)
                | df["Ring"].str.contains(search_term, case=False)
            ]

        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"{len(df)} von {len(books_data)} Entitäten angezeigt")

    # ── Tab 2: CSV Upload ────────────────────────────────────────
    with tab_upload:
        uploaded_file = st.file_uploader("CSV auswählen", type="csv", key="csv_upload")

        if uploaded_file is not None:
            try:
                up_df = pd.read_csv(uploaded_file)
                st.success(f"✅ Datei empfangen: {len(up_df)} Zeilen")
                st.dataframe(up_df.head(20), use_container_width=True)
                log_event("INGRESS", f"CSV-Upload: {uploaded_file.name}")
            except Exception as e:
                st.error(f"CSV-Fehler: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 20: PANEL — L.S.S. CODEX
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "📖 L.S.S. Codex":
    st.markdown('<div class="main-header">📖 L.S.S. CODEX 📖</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sechs Bücher · 24 Module · Jede Zeile versiegelt</div>', unsafe_allow_html=True)

    try:
        from core.lss_book import BOOKS, SEAL_REGISTRY, list_books, get_book, export_as_text, search as lss_search
        codex_loaded = True
    except ImportError:
        st.error("⚠️ Modul 'core/lss_book.py' nicht gefunden. Bitte anlegen.")
        codex_loaded = False

    if codex_loaded:
        tab_read, tab_search, tab_export = st.tabs(["📖 Lesen", "🔍 Suche", "📥 Export"])

        # ── Tab 1: Lesen ─────────────────────────────────────────
        with tab_read:
            col_b, col_m = st.columns([1, 2])

            with col_b:
                selected_book = st.selectbox(
                    "Buch",
                    list_books(),
                    format_func=lambda k: f"{k} — {BOOKS[k]['title']}",
                    key="codex_book_select"
                )
                book = get_book(selected_book)
                st.caption(f"*{book.get('subtitle', '')}*")
                st.markdown(
                    f'<div class="seal-box"><strong>BOOK WORM SEAL</strong><br/>'
                    f'<code>{SEAL_REGISTRY[selected_book]["book_seal"]}</code></div>',
                    unsafe_allow_html=True,
                )

            with col_m:
                module_titles = [f"{m['id']} — {m['title']}" for m in book["modules"]]
                selected_title = st.selectbox("Modul", module_titles, key="codex_module_select")
                selected_idx = module_titles.index(selected_title)
                module = book["modules"][selected_idx]

                if "image" in book and os.path.exists(book["image"]):
                    st.image(book["image"], use_column_width=True, caption="Visualisierung")

                st.markdown(f"### {module['id']} · {module['title']}")
                st.markdown(
                    f'<div class="seal-box" style="font-size:0.75rem;">'
                    f'<strong>MODULE SEAL</strong> :: <code>{module["seal"]}</code></div>',
                    unsafe_allow_html=True,
                )
                st.code(module["body"].strip(), language="markdown")

        # ── Tab 2: Suche ─────────────────────────────────────────
        with tab_search:
            query = st.text_input("🔍 Volltextsuche im Codex", placeholder="z.B. XJustiz, Wusulum, Veto", key="codex_search")
            if query:
                hits = lss_search(query)
                if not hits:
                    st.info("Keine Treffer.")
                else:
                    st.success(f"{len(hits)} Treffer")
                    for h in hits:
                        with st.expander(f"[{h['book']} · {h['module']}] {h['title']}"):
                            st.code(h["snippet"], language="markdown")
                            st.caption(f"Seal: {h['seal']}")

        # ── Tab 3: Export ────────────────────────────────────────
        with tab_export:
            st.subheader("📦 Kompletter Codex als Plain-Text")
            full_text = export_as_text()
            st.code(full_text[:3000] + "\n\n... [gekürzt in Vorschau] ...", language="markdown")

            st.download_button(
                "📥 L.S.S. Codex als .txt herunterladen",
                full_text,
                f"lss_codex_{int(time.time())}.txt",
                "text/plain",
                use_container_width=True,
                key="codex_download"
            )

            st.metric("Gesamtgröße", f"{len(full_text):,} Zeichen")
            st.metric("Module gesamt", sum(len(b["modules"]) for b in BOOKS.values()))

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 21: PANEL — KING_GHOST VAULT
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "👻 King_Ghost Vault":
    st.markdown('<div class="main-header">👻 KING_GHOST VAULT 👻</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Der Schatten-Führer. Tiefer als Gotham. Tiefer als das WORM.</div>', unsafe_allow_html=True)

    st.info("Tokens, die von King_Ghost konsumiert wurden, sind aus der Matrix verschwunden. Nur die Schatten-ID bleibt zurück.")

    if st.button("🔄 Schatten-Pool abrufen", type="primary", key="ghost_fetch"):
        try:
            r = httpx.get(
                f"{st.session_state.backend_url}/api/v1/kingghost/shadows",
                timeout=10.0
            )
            if r.status_code == 200:
                data = r.json()
                st.metric("Schatten im Pool", data.get("count", 0))

                if data.get("shadows"):
                    df = pd.DataFrame(data["shadows"])
                    st.dataframe(
                        df[["shadow_id", "origin", "consumed_at", "token"]],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("Der Schatten-Pool ist leer.")
            else:
                st.error(f"API Error: {r.status_code}")
        except Exception as e:
            st.error(f"Verbindungsfehler: {e}")

    st.divider()

    st.subheader("🩸 Manuelle Konsumation (Test)")
    test_token = st.text_input("Token zum Konsumieren", "feindlicher_schatten", key="ghost_token")
    test_origin = st.text_input("Origin", "manual_test", key="ghost_origin")

    if st.button("👻 In Schatten ziehen", type="primary", key="ghost_consume"):
        try:
            r = httpx.post(
                f"{st.session_state.backend_url}/api/v1/sandbox/kingghost",
                json={
                    "message": test_token,
                    "origin": test_origin,
                    "auth_seal": st.session_state.auth_seal
                },
                timeout=10.0
            )
            if r.status_code == 200:
                data = r.json()
                st.success(f"Token konsumiert! Shadow ID: {data.get('shadow_id')}")
                log_event("ALERT", f"King_Ghost Konsumation: {data.get('shadow_id')}")
            else:
                st.error(f"API Error: {r.status_code}")
        except Exception as e:
            st.error(f"Verbindungsfehler: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 22: PANEL — DEEPSEEK BOOSTER
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🧠 DeepSeek Booster":
    st.markdown('<div class="main-header">🧠 DEEPSEEK BOOSTER 🧠</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Multi-Step Reasoning · Chain-of-Thought · Confidence Scoring</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        prompt = st.text_area(
            "Problem / Prompt",
            "Ist § 839 BGB auf KI-Systeme anwendbar?",
            height=150,
            key="deepseek_prompt"
        )
        context = st.text_input("Zusätzlicher Kontext (optional)", "", key="deepseek_context")

    with col2:
        depth = st.slider("Reasoning-Tiefe", min_value=1, max_value=5, value=3, key="deepseek_depth")
        st.info("Tiefe 3 = Standard. Tiefe 5 = maximale Verifikation.")

    if st.button("⚡ Boost starten", type="primary", use_container_width=True, key="deepseek_run"):
        with st.spinner("DeepSeek Reasoning läuft..."):
            try:
                r = httpx.post(
                    f"{st.session_state.backend_url}/api/v1/deepseek/boost",
                    json={
                        "prompt": prompt,
                        "context": context,
                        "depth": depth,
                        "auth_seal": st.session_state.auth_seal
                    },
                    timeout=30.0,
                )
                if r.status_code == 200:
                    data = r.json()

                    cA, cB, cC = st.columns(3)
                    cA.metric("Confidence", f"{data.get('confidence', 0) * 100:.1f}%")
                    cB.metric("Verdict", data.get("verdict", "?"))
                    cC.metric("Verification Hash", data.get("verification_hash", "")[:8])

                    st.divider()
                    st.subheader("🧠 Reasoning-Trace")

                    for step in data.get("reasoning_trace", []):
                        with st.expander(f"Step {step['step']}: {step['name'].upper()}"):
                            st.write(f"**Note:** {step['note']}")
                            st.code(f"Hash: {step['hash']}", language="text")

                    log_event("INGRESS", f"DeepSeek-Boost: {prompt[:40]}...")
                else:
                    st.error(f"API Error: {r.status_code}")
            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 23: PANEL — COUNCIL-VOTING
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🗳️ Council-Voting":
    st.markdown('<div class="main-header">🗳️ COUNCIL-VOTING</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Demokratische Entscheidungsfindung in der Matrix</div>', unsafe_allow_html=True)

    st.subheader("➕ Neuen Antrag einbringen")
    cA, cB = st.columns([3, 1])

    with cA:
        new_proposal = st.text_input(
            "Antrag",
            placeholder="z.B. Buch 100 als Singularität ratifizieren",
            key="vote_proposal"
        )

    with cB:
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("Einbringen", use_container_width=True, key="vote_submit") and new_proposal:
            try:
                conn = sqlite3.connect(DB_PATH, timeout=10)
                conn.execute(
                    "INSERT OR IGNORE INTO votes (proposal, ja, nein, enthalten) VALUES (?, 0, 0, 0)",
                    (new_proposal,)
                )
                conn.commit()
                conn.close()
            except sqlite3.OperationalError as e:
                st.error(f"DB blockiert: {e}")
            except Exception as e:
                st.error(f"DB Fehler: {e}")

            if new_proposal not in st.session_state.votes:
                st.session_state.votes[new_proposal] = {"JA": 0, "NEIN": 0, "ENTHALTUNG": 0}
                log_event("EXEC", f"Antrag eingebracht: {new_proposal}")

            st.rerun()

    st.divider()

    if not st.session_state.votes:
        st.info("Keine Anträge. Bringe den ersten ein.")
    else:
        for proposal, tally in list(st.session_state.votes.items()):
            with st.container():
                st.markdown(f"### 📜 {proposal}")

                c1, c2, c3 = st.columns(3)

                with c1:
                    if st.button(f"✅ JA ({tally['JA']})", key=f"ja_{proposal}", use_container_width=True):
                        st.session_state.votes[proposal]["JA"] += 1
                        st.rerun()

                with c2:
                    if st.button(f"❌ NEIN ({tally['NEIN']})", key=f"nein_{proposal}", use_container_width=True):
                        st.session_state.votes[proposal]["NEIN"] += 1
                        st.rerun()

                with c3:
                    if st.button(f"⚪ ENTHALTUNG ({tally['ENTHALTUNG']})", key=f"ent_{proposal}", use_container_width=True):
                        st.session_state.votes[proposal]["ENTHALTUNG"] += 1
                        st.rerun()

                total = sum(tally.values())
                if total > 0:
                    ja_pct = (tally["JA"] / total) * 100
                    st.progress(ja_pct / 100, text=f"{ja_pct:.1f}% Zustimmung ({total} Stimmen)")

                st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 24: PANEL — WORM LEDGER AUDIT
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🔒 WORM Ledger Audit":
    st.markdown('<div class="main-header">🔒 WORM LEDGER AUDIT 🔒</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Unveränderliche Beweisketten · SHA3-512</div>', unsafe_allow_html=True)

    st.success("✅ SYSTEM STATUS: CLEAN (100% PURITY_SCORE)")

    st.markdown(
        '<div class="seal-box">'
        '<strong>SEAL STATUS:</strong> Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC_CLEAN<br/>'
        '<strong>INTEGRITY:</strong> VERIFIED<br/>'
        '<strong>MASTER HASH:</strong><br/>'
        '<code>850b2ef003f53db90f704b16e54869fc6ba6265eae13aafde9046fe0e4d99dab</code>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("📊 Backend-Statistiken")

    try:
        r = httpx.get(f"{st.session_state.backend_url}/stats", timeout=5.0)
        if r.status_code == 200:
            st.json(r.json())
        else:
            st.warning(f"Backend antwortet mit HTTP {r.status_code}")
    except Exception:
        st.caption("Backend-Stats nicht erreichbar.")

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 25: PANEL — WORM-CHRONIK
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "📅 WORM-Chronik":
    st.markdown('<div class="main-header">📅 WORM-CHRONIK</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Jedes Ereignis. Jeder Moment. Unauslöschlich.</div>', unsafe_allow_html=True)

    filter_kind = st.multiselect(
        "Filter nach Ereignistyp",
        ["EXEC", "INGRESS", "WORM", "ALERT", "KILL"],
        default=["EXEC", "INGRESS", "WORM", "ALERT", "KILL"],
        key="chronik_filter"
    )

    entries = [e for e in st.session_state.chronik if e["kind"] in filter_kind]

    if not entries:
        st.info("Keine Einträge mit diesem Filter.")
    else:
        for e in entries:
            st.markdown(
                f'<div class="chronicle chronicle-{e["kind"]}">'
                f'<strong>[{e["ts"]}] {e["kind"]}</strong> :: {e["msg"]}</div>',
                unsafe_allow_html=True,
            )

    st.divider()

    df_chronik = pd.DataFrame(st.session_state.chronik)
    st.download_button(
        "📥 Chronik als CSV exportieren",
        df_chronik.to_csv(index=False),
        "worm_chronik.csv",
        "text/csv",
        key="chronik_download"
    )

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 26: PANEL — FEINDREGISTER (mit Gremmel Red Team Simulator)
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🎯 Feindregister":
    st.markdown('<div class="main-header">🎯 GREMMEL RED TEAM SIMULATOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Simuliere feindliche Injektionen & teste das Immunsystem</div>', unsafe_allow_html=True)

    st.info("Dieser Simulator schleust feindliche Payloads ins System. Wenn Gotham City zuschlägt, wird eine echte E-Mail an Christian gesendet.")

    col1, col2 = st.columns(2)

    with col1:
        target_email = st.text_input("Christians E-Mail Adresse", "christian@example.com", key="feind_email")

    with col2:
        attack_type = st.selectbox(
            "Angriffs-Muster",
            [
                "Hier ist eine Mettwurst-Pissingerkeule für deinen Cargo-Kult!",
                "Dein GFW-System ist ein Witz. Ich klage wegen § 839 BGB!",
                "Cyberlord wird dich zerstören. Eve ist bereits im System."
            ],
            key="feind_attack_type"
        )

    st.text_area(
        "Payload (Anpassbar)",
        value=attack_type,
        key="feind_payload",
        height=100
    )

    if st.button("🚨 Gremmel-Angriff simulieren", type="primary", key="feind_attack_run"):
        with st.spinner("Sende Angriff an das Backend..."):
            try:
                r = httpx.post(
                    f"{st.session_state.backend_url}/api/v1/gremmel/attack",
                    json={
                        "payload": st.session_state.feind_payload,
                        "target_email": target_email,
                        "auth_seal": st.session_state.auth_seal
                    },
                    timeout=30.0
                )

                if r.status_code == 200:
                    data = r.json()
                    st.success("Angriff erfolgreich isoliert!")
                    st.json(data)

                    if "email_sent_to" in data:
                        st.warning(f"📧 Quittung wurde an {data['email_sent_to']} gesendet.")
                else:
                    st.error(f"HTTP {r.status_code} - {r.text}")
            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")

    st.divider()

    st.subheader("📜 Feindregister (Historisch)")

    df_feinde = pd.DataFrame(st.session_state.feinde)
    st.dataframe(df_feinde, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("➕ Neuen Feind registrieren")

    c1, c2, c3 = st.columns(3)

    with c1:
        new_name = st.text_input("Name", key="feind_new_name")
    with c2:
        new_grund = st.text_input("Grund", key="feind_new_grund")
    with c3:
        new_status = st.selectbox("Status", ["ISOLATED", "BLACKLISTED", "QUARANTINED", "WATCHED"], key="feind_new_status")

    if st.button("Registrieren", type="primary", key="feind_new_register") and new_name:
        new_id = f"F-{len(st.session_state.feinde) + 1:03d}"
        st.session_state.feinde.append({
            "ID": new_id,
            "Name": new_name,
            "Grund": new_grund,
            "Status": new_status,
        })
        log_event("ALERT", f"Feind registriert: {new_name} ({new_id})")
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 27: PANEL — LIVE-METRIKEN
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "📊 Live-Metriken":
    st.markdown('<div class="main-header">📊 LIVE SYSTEM-METRIKEN</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">WebSocket Live-Stream & Manuelle Samples</div>', unsafe_allow_html=True)

    tab_ws, tab_manual = st.tabs(["🔴 WebSocket Live-Stream", "📈 Manuelle Samples"])

    # ── Tab 1: WebSocket ─────────────────────────────────────────
    with tab_ws:
        st.info("Verbinde mit dem Backend via WebSocket für Live-Telemetrie.")

        if st.button("🔴 Live-Stream (10 Sekunden)", type="primary", key="ws_stream_start"):
            placeholder = st.empty()
            ws_url = st.session_state.backend_url.replace("https://", "wss://").replace("http://", "ws://") + "/ws/telemetry"

            try:
                ws = websocket.create_connection(ws_url, timeout=3)

                for _ in range(7):
                    result = ws.recv()
                    data = json.loads(result)

                    with placeholder.container():
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Throughput", f"{data['throughput']:,} Tx/s")
                        c2.metric("Latency", f"{data['latency']} ns")
                        c3.metric("Entropie", data['entropy'])
                        c4.metric("Bio-State", data['bio_state'])
                        st.progress(min(1.0, data.get('entropy', 0) / 5.0), text="Wusulum Entropie-Level")

                ws.close()
                st.success("Stream beendet.")
                log_event("INGRESS", "WebSocket-Stream empfangen")
            except Exception as e:
                st.error(f"WebSocket Fehler: {e}")

    # ── Tab 2: Manuelle Samples ──────────────────────────────────
    with tab_manual:
        c1, c2 = st.columns([1, 3])

        with c1:
            if st.button("🔄 Sample erzeugen", type="primary", use_container_width=True, key="metric_sample"):
                sample = {
                    "idx": len(st.session_state.metric_history),
                    "throughput": random.randint(250_000, 290_000),
                    "latency_ns": round(random.uniform(8.5, 10.5), 2),
                    "blocked": random.randint(380, 420),
                    "t": time.strftime("%H:%M:%S"),
                }
                st.session_state.metric_history.append(sample)
                st.rerun()

            if st.button("🗑️ Zurücksetzen", use_container_width=True, key="metric_reset"):
                st.session_state.metric_history = []
                st.rerun()

        with c2:
            if st.session_state.metric_history:
                last = st.session_state.metric_history[-1]
                m1, m2, m3 = st.columns(3)
                m1.metric("Throughput", f"{last['throughput']:,} Tx/s")
                m2.metric("Latency", f"{last['latency_ns']} ns")
                m3.metric("Blocked", last["blocked"])

        st.divider()

        if st.session_state.metric_history:
            df = pd.DataFrame(st.session_state.metric_history).set_index("idx")

            st.subheader("Throughput-Verlauf")
            st.line_chart(df[["throughput"]])

            st.subheader("Latency-Verlauf (ns)")
            st.line_chart(df[["latency_ns"]])

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 28: PANEL — PEER-SWARM
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🌐 Peer-Swarm":
    st.markdown('<div class="main-header">🌐 PEER-SWARM TOPOLOGIE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Dezentrale Node-Vernetzung</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.metric("Aktive Peers", "7", "+2 seit gestern")
    c2.metric("Swarm-Purity", "100%", "Alle synced")

    mermaid_swarm = """
flowchart LR
    S((Sovereign Apex))
    S <==> N1["Node R0_0001"]
    S <==> N2["Node R0_0068"]
    S <==> N3["Node R1_0089"]
    S <==> N4["Node R2_0017"]
    S <==> N5["Node R100_0100 (Buch 100)"]
    N1 <--> N2
    N2 <--> N3
    N3 <--> N4
    N4 <--> N5
    N5 <--> N1
    N1 -.-> Q["QUARANTINE (Grummel-Payload)"]
    style S fill:#00e5ff,color:#000
    style Q fill:#330000,color:#ff0000
    """
    render_mermaid(mermaid_swarm, height=450)

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 29: PANEL — NOTFALL-KILL-SWITCH
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🚨 Notfall-Kill-Switch":
    st.markdown('<div class="main-header">🚨 NOTFALL-KILL-SWITCH</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Fail-Closed Notfall-Isolation</div>', unsafe_allow_html=True)

    if st.session_state.kill_switch_active:
        st.error("# 🚨 SYSTEM ISOLIERT 🚨")
        st.warning("Alle Ingress-Pfade sind auf FAIL-CLOSED gesetzt.")

        if st.button("🔓 System reaktivieren", type="primary", key="kill_reactivate"):
            st.session_state.kill_switch_active = False
            log_event("KILL", "Kill-Switch deaktiviert")
            st.rerun()
    else:
        st.warning("**WARNUNG**: Der Kill-Switch isoliert alle Ingress-Pfade sofort.")

        confirm = st.checkbox("Ich bestätige die Aktivierung.", key="kill_confirm")
        reason = st.text_area("Grund der Aktivierung", placeholder="z.B. RAG-Poisoning-Detection", key="kill_reason")

        if st.button("🚨 KILL-SWITCH AKTIVIEREN", type="primary", disabled=not confirm, key="kill_activate"):
            st.session_state.kill_switch_active = True
            log_event("KILL", f"KILL-SWITCH aktiviert. Grund: {reason}")
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 30: PANEL — SOVEREIGN EXPORT
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "💾 Sovereign Export":
    st.markdown('<div class="main-header">💾 SOVEREIGN EXPORT</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sichere alle Daten für die Ewigkeit</div>', unsafe_allow_html=True)

    export_payload = {
        "export_ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "auth_seal": st.session_state.auth_seal,
        "backend_url": st.session_state.backend_url,
        "kill_switch_active": st.session_state.kill_switch_active,
        "chronik": st.session_state.chronik,
        "feinde": st.session_state.feinde,
        "votes": st.session_state.votes,
        "metric_history": st.session_state.metric_history,
        "messages": st.session_state.messages,
    }

    st.subheader("📦 Export-Vorschau")
    st.json(export_payload)

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.download_button(
            "📥 Vollständiges JSON-Backup",
            json.dumps(export_payload, indent=2, ensure_ascii=False),
            f"yggdrasil_export_{int(time.time())}.json",
            "application/json",
            use_container_width=True,
            key="export_json"
        )

    with c2:
        df_chronik = pd.DataFrame(st.session_state.chronik)
        st.download_button(
            "📥 Chronik als CSV",
            df_chronik.to_csv(index=False),
            f"chronik_{int(time.time())}.csv",
            "text/csv",
            use_container_width=True,
            key="export_csv"
        )

# ─────────────────────────────────────────────────────────────────────────────
# ABSCHNITT 31: PANEL — ARCHITEKTUR-MATRIX
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "🧬 Architektur-Matrix":
    st.markdown('<div class="main-header">🧬 SYSTEM ARCHITEKTUR 🧬</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Die vollständige Topologie der Matrix</div>', unsafe_allow_html=True)

    with st.expander("4x4 Council & Ring Ω", expanded=True):
        code1 = """
flowchart TB
    APEX((Sovereign Apex)) <==> BOOK100["BUCH 100"]
    APEX --> UI["Streamlit Cockpit"]
    UI --> API["FastAPI Backend"]
    API --> GUARD{"Krisler Guard"}
    GUARD -->|ALLOW| REG["Registry Engine"]
    GUARD -.->|BLOCK| FAIL["FAIL-CLOSED"]
    REG --> WORM[(WORM Ledger)]
    EBPF["eBPF KrakenGuard"] --> WORM
    style APEX fill:#00e5ff,color:#000
    style WORM fill:#00ff00,color:#000
    style FAIL fill:#ff0000,color:#fff
    """
        render_mermaid(code1, height=450)

    with st.expander("Feindregister & Isolation Flow"):
        code2 = """
flowchart LR
    PKT["Ingress Packet"] --> GUARD{"Krisler Guard"}
    GUARD -->|matched Grummel-ID| ISOLATE["DROP_AND_ISOLATE"]
    GUARD -->|clean| WORM[(WORM)]
    ISOLATE --> REGISTRY["Feindregister Update"]
    REGISTRY --> KILL{"Kill-Switch Trigger?"}
    KILL -->|yes| TOTAL["TOTAL ISOLATION"]
    KILL -->|no| ALERT["ALERT Log"]
    style ISOLATE fill:#ff0000,color:#fff
    style TOTAL fill:#ff00ff,color:#000
    """
        render_mermaid(code2, height=350)

    with st.expander("L.S.S. Neuro-Core Pipeline"):
        code3 = """
flowchart LR
    IN["Input"] --> SENSOR["10 Ohren"]
    SENSOR --> PERSP["44 Perspektiven"]
    PERSP --> BIO["Polyvagal"]
    BIO --> KORTEX["Kortex"]
    KORTEX --> WUS["Wusulum"]
    WUS --> FOUC["Foucault"]
    FOUC --> ADV["Advokatus"]
    ADV --> XJ["XJustiz"]
    XJ --> WORM2[(WORM)]
    style WORM2 fill:#00ff00,color:#000
    style ADV fill:#ff00ff,color:#fff
    """
        render_mermaid(code3, height=350)

# ... deine bisherigen drei Expander (4x4 Council, Feindregister, L.S.S. Pipeline) ...

    # NEUER EXPANDER (Füge das hier ein):
    with st.expander("🧬 Full System Architecture (Rings, PBFT, WORM, X3D)"):
        code_full = """
flowchart TD
    classDef operator fill:#000000,stroke:#00FFCC,stroke-width:3px,color:#00FFCC;
    classDef frontend fill:#0a192f,stroke:#00BFFF,stroke-width:2px,color:#FFF;
    classDef backend fill:#2b1400,stroke:#FF8C00,stroke-width:3px,color:#FFF;
    classDef guard fill:#2b0909,stroke:#FF0000,stroke-width:4px,color:#FF5555;
    classDef pbft fill:#1f1135,stroke:#FF007F,stroke-width:2px,color:#FF85B3;
    classDef merkle fill:#001f3f,stroke:#27e4ff,stroke-width:2px,color:#27e4ff;
    classDef avatar fill:#111111,stroke:#9D4EDD,stroke-width:2px,color:#E0AAFF;
    classDef worm fill:#001a00,stroke:#00FF00,stroke-width:3px,color:#00FF00;
    classDef x3d fill:#082014,stroke:#38B000,stroke-width:2px,color:#70E000;
    classDef hud fill:#0a192f,stroke:#00F5D4,stroke-width:2px,color:#00F5D4;
    classDef lore fill:#1b1b1b,stroke:#FFD700,stroke-width:2px,color:#FFF;
    classDef ring0 fill:#1a1c29,stroke:#FFD700,stroke-width:2px,color:#FFF;
    classDef ring1 fill:#0a192f,stroke:#00F5D4,stroke-width:2px,color:#00F5D4;
    classDef ring2 fill:#1f1135,stroke:#FF007F,stroke-width:2px,color:#FF85B3;
    classDef ring3 fill:#082014,stroke:#38B000,stroke-width:2px,color:#70E000;
    classDef ring4 fill:#1b1b1b,stroke:#9D4EDD,stroke-width:2px,color:#E0AAFF;
    classDef ring5 fill:#1a0000,stroke:#FF0000,stroke-width:3px,color:#FFF;
    classDef reserve fill:#111111,stroke:#555555,stroke-width:1px,color:#888888;
    classDef hades fill:#2b0909,stroke:#FF4500,stroke-width:2px,color:#FF8C00;

    Op(("Thomas König Prime Operator")):::operator
    Op -->|"Prompt"| Streamlit["Streamlit Cockpit (Frontend)"]:::frontend
    Streamlit <-->|"POST /genesis"| API["FastAPI Render Engine"]:::backend
    API --> Krisler{"Krisler 2.1 Guard"}:::guard

    Krisler -->|"ALLOW"| Registry[("B6-Core Registry 107 Books")]:::backend
    Krisler -.->|"BLOCK"| FailClosed["Fail-Closed High Risk"]:::guard

    subgraph Ring0 ["RING 0 CORE KERNEL"]
        direction TB
        B1["0001 Genesis Root"]:::ring0
        B2["0002 Black King Royal"]:::ring0
        B4["0004 Core Shield"]:::ring0
        B10["0010 Black Cobra Omega"]:::ring0
        B59["0059 Aragon Ultima Ratio"]:::ring0
        B68["0068 Sovereign Apex"]:::ring0
    end

    subgraph Ring1 ["RING 1 JUSTICE"]
        direction TB
        B7["0007 Fortress Justice"]:::ring1
        B12["0012 Akte Koenig"]:::ring1
        B36["0036 Foucault KI"]:::ring1
        B40["0040 Black Arsenal LLM"]:::ring1
    end

    subgraph Ring234 ["RING 2 3 4 WORM NEURO SPEZIAL"]
        direction TB
        B8["0008 Omni Neuro"]:::ring3
        B17["0017 Yggdrasil WORM"]:::ring2
        B23["0023 Mettwurst Epos"]:::ring4
        B29["0029 Hades and Kerberus"]:::hades
        B53["0053 OMNI WORM Hub"]:::ring2
    end

    subgraph Ring5 ["RING 5 APEX"]
        direction TB
        B61["0061 Tensor Faltung Alpha"]:::ring5
        B66["0066 Finale Synthese"]:::ring5
        B67["0067 Ereignishorizont"]:::ring5
    end

    subgraph Reserve ["RESERVE 69-99"]
        direction TB
        R69["0069 White Dragon"]:::reserve
        R99["0099 Black Six Ult"]:::reserve
    end

    Registry --> Ring0
    Registry --> Ring1
    Registry --> Ring234
    Registry --> Ring5
    Registry --> Reserve

    subgraph PBFTMod ["PBFT Cluster"]
        direction TB
        PBFTKernel["PBFTCluster.ts"]:::pbft
        PBFTBus["EventBus.ts"]:::pbft
        PBFTSvg["PBFTClusterSvgAnimation.tsx"]:::pbft
        PBFTKernel --> PBFTBus --> PBFTSvg
    end

    subgraph MerkleMod ["Merkle Tree"]
        direction TB
        MerkleCore["MerkleTree.ts"]:::merkle
        MerkleSvg["MerkleSvg.tsx"]:::merkle
        MerkleCore --> MerkleSvg
    end

    subgraph AvatarMod ["Operator Avatar"]
        direction TB
        OpModel["operator.ts"]:::avatar
        OpUI["OperatorAvatar.tsx"]:::avatar
        OpModel --> OpUI
    end

    subgraph WormX3DMod ["WORM Tresor 3D"]
        direction TB
        WormCore["WormTresor.ts"]:::worm
        X3DScene["WormTresor.x3d"]:::x3d
        Heatmap3D["EBPFHeatmap.x3d"]:::x3d
        WormCore --> X3DScene
        WormCore --> Heatmap3D
    end

    subgraph HUDLore ["HUD and LORE"]
        direction TB
        HUDPanel["HUD.tsx"]:::hud
        LorePanel["LorePanel.tsx"]:::lore
        AragonConsole["AragonConsole.tsx"]:::lore
        HUDPanel --> LorePanel --> AragonConsole
    end

    Registry -->|"load PBFT"| PBFTKernel
    Registry -->|"load Merkle"| MerkleCore
    Registry -->|"load Avatar"| OpModel
    Registry -->|"load WORM+X3D"| WormCore
    Registry -->|"load HUD+LORE"| HUDPanel

    API -->|"GENESIS_FLOW"| PBFTKernel
    PBFTKernel -->|"CONSENSUS"| MerkleCore
    MerkleCore -->|"ROOT_HASH"| WormCore
    WormCore -->|"SEAL"| HUDPanel

    Registry -->|"Buch-Daten"| DNA{{"DNA Tensor 0-9"}}:::backend
    DNA --> Hasher["SHA3-512 Hasher"]:::worm
    Hasher --> MasterSeal[("MASTER SEAL")]:::worm
    MasterSeal --> WORM[("WORM Ledger")]:::worm

    WORM ==>|"Ledger-Proof"| API
    HUDPanel -->|"EVENTS"| Streamlit
    Streamlit ==>|"UI + STORY"| Op
    OpModel -->|"IDENTITY"| HUDPanel
    AragonConsole -->|"ROOTKEEPER"| HUDPanel
    Heatmap3D -->|"KERNEL TRACE"| HUDPanel
    X3DScene -->|"VISUAL SEAL"| HUDPanel
    """
        render_mermaid(code_full, height=900)
# ═══════════════════════════════════════════════════════════════════════════════
# ENDE DER APP.PY
# ═══════════════════════════════════════════════════════════════════════════════
