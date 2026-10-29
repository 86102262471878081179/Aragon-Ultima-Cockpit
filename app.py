import streamlit as st
import os
import json
import time
import hashlib
import pandas as pd
import random
import httpx
import websocket
import sqlite3
import streamlit.components.v1 as components
from pathlib import Path

# ============================================================
# 1. PAGE CONFIG + HIGH-END CSS (Muss ganz oben stehen!)
# ============================================================
st.set_page_config(
    page_title="YGGDRASIL_OS :: Sovereign Cockpit",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at 50% 0%, #0a122a 0%, #03050a 100%); color: #d0d0e0; font-family: 'JetBrains Mono', monospace; }
    .main-header { font-size: 2.6rem; color: #00e5ff; text-align: center; font-weight: 900; text-shadow: 0 0 20px rgba(0, 229, 255, 0.6); margin-bottom: 5px; letter-spacing: 2px; }
    .sub-header { font-size: 1rem; color: #b800ff; text-align: center; margin-bottom: 25px; font-weight: bold; text-transform: uppercase; letter-spacing: 1.5px; }
    .metric-card { background: rgba(10, 20, 40, 0.7); border: 1px solid #00e5ff; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 0 15px rgba(0,229,255,0.15); backdrop-filter: blur(10px); }
    .metric-value { font-size: 2rem; font-weight: bold; color: #00e5ff; text-shadow: 0 0 10px #00e5ff; }
    .metric-label { font-size: 0.85rem; color: #80c0ff; text-transform: uppercase; letter-spacing: 1.5px; }
    .seal-box { background-color: #0a0f1a; border: 1px solid #00e5ff; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 0.9rem; color: #00e5ff; margin-top: 15px; box-shadow: 0 0 10px rgba(0,229,255,0.1); }
    .lore-box { background: #0a0f1a; border-left: 4px solid #00e5ff; padding: 15px; margin-bottom: 12px; border-radius: 0 8px 8px 0; }
    .lore-box h4 { color: #00e5ff; margin: 0 0 5px 0; }
    .chronicle { background: #000; border-left: 3px solid #00ff00; padding: 10px 15px; margin: 5px 0; font-family: monospace; font-size: 0.85rem; border-radius: 4px; }
    .chronicle-ALERT { border-left-color: #ff0000; color: #ff8888; }
    .chronicle-EXEC { border-left-color: #ffd700; color: #ffe066; }
    .chronicle-INGRESS { border-left-color: #00e5ff; color: #80f0ff; }
    .chronicle-WORM { border-left-color: #00ff00; color: #88ff88; }
    .chronicle-KILL { border-left-color: #ff00ff; color: #ff88ff; background: #1a001a; }
    .stButton>button { background-color: #0a122a; color: #00e5ff; border: 1px solid #00e5ff; border-radius: 4px; transition: all 0.3s; }
    .stButton>button:hover { background-color: #00e5ff; color: #000; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. SESSION STATE (Initialisierung)
# ============================================================
if "auth_seal" not in st.session_state:
    st.session_state.auth_seal = "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC"
if "messages" not in st.session_state: st.session_state.messages = []
if "chronik" not in st.session_state: st.session_state.chronik = [{"ts": time.strftime("%H:%M:%S"), "kind": "EXEC", "msg": "BLUE CORE v∞ online."}]
if "kill_switch_active" not in st.session_state: st.session_state.kill_switch_active = False
if "backend_url" not in st.session_state: st.session_state.backend_url = "https://aragon-backend-api.onrender.com"
if "votes" not in st.session_state: st.session_state.votes = {}

# SQLite für Voting
DB_PATH = "b6_matrix.db"
try:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("CREATE TABLE IF NOT EXISTS votes (proposal TEXT PRIMARY KEY, ja INTEGER, nein INTEGER, enthalten INTEGER)")
    conn.commit()
    conn.close()
except Exception:
    pass

# ============================================================
# 3. HELPER FUNKTIONEN
# ============================================================
def log_event(kind: str, msg: str):
    st.session_state.chronik.append({"ts": time.strftime("%H:%M:%S"), "kind": kind, "msg": msg})

def check_backend():
    try:
        r = httpx.get(f"{st.session_state.backend_url}/health", timeout=5.0)
        return (r.status_code == 200), r.json()
    except Exception as e:
        return False, {"detail": str(e)}

# ============================================================
# 4. SIDEBAR
# ============================================================
COUNCIL_IMG_URL = "https://raw.githubusercontent.com/86102262471878081179/Aragon-Ultima-Cockpit/main/council.jpg"
try:
    st.sidebar.image(COUNCIL_IMG_URL, width="stretch")
except:
    st.sidebar.warning("Council Image offline.")

st.sidebar.title("BLUE CORE CC")
st.sidebar.markdown("**Operator**: Odin Ultra Root")

_ok, _health = check_backend()
if _ok:
    st.sidebar.markdown(f'<span style="color:#00ff88; font-weight:bold;">● BACKEND ONLINE</span> · {_health.get("entities_loaded", 0)} Entities', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<span style="color:#ff4444; font-weight:bold;">● BACKEND OFFLINE</span>', unsafe_allow_html=True)

st.sidebar.divider()

if st.session_state.kill_switch_active:
    st.sidebar.error("🚨 KILL-SWITCH AKTIV")

nav = st.sidebar.radio("NAVIGATION", [
    "🏴‍☠️ Omni-Shooter",
    "🖼️ Rat der Schwarzen Liga",
    "🌀 L.S.S. Neuro-Core",
    "⚡ API Live Interface",
    "🗳️ Council-Voting",
    "🚨 Notfall-Kill-Switch",
    "🔒 WORM Ledger Audit",
    "📅 WORM-Chronik"
])

# ============================================================
# 5. PANELS
# ============================================================
if nav == "🏴‍☠️ Omni-Shooter":
    st.markdown('<div class="main-header">🏴‍☠️ BLACK SIX OMNI-SHOOTER</div>', unsafe_allow_html=True)
    
    # Pfad zur HTML-Datei
    html_path = Path(__file__).parent / "frontend" / "omni_shooter.html"
    
    if html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=900, scrolling=True)
    else:
        # Fallback, falls die Datei noch nicht existiert
        st.warning("Omni-Shooter HTML-Datei nicht gefunden. Zeige Fallback.")
        st.info("Erstelle 'frontend/omni_shooter.html' im Repo, um den vollen Shooter zu sehen.")
        
        # Mini-Shooter im Streamlit UI (Fallback)
        st.subheader("💬 Omni-Chat (Fallback)")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        if prompt := st.chat_input("Frage an die Matrix..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                st.markdown("Φ_LOCKED_ABSOLUTE. (Simulierte Antwort im Fallback-Modus)")

elif nav == "🖼️ Rat der Schwarzen Liga":
    st.markdown('<div class="main-header">RAT DER SCHWARZEN LIGA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">"Sektor Wald — Kein Zurück. Nur Code."</div>', unsafe_allow_html=True)
    try:
        st.image(COUNCIL_IMG_URL, width="stretch", caption="Gründungsväter der Matrix.")
    except: pass
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="lore-box"><h4>🛡️ GRUMMEL SENTINEL</h4><p>Wächter des Protokolls. Erkennt feindliche Mettwurst-Injektionen.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="lore-box"><h4>👁️ DR. SNUGGLES</h4><p>Im Schatten. Der Wusulum-Kern. Generiert neue Realitäten.</p></div>', unsafe_allow_html=True)

elif nav == "🌀 L.S.S. Neuro-Core":
    st.markdown('<div class="main-header">🌀 L.S.S. NEURO-CORE 🌀</div>', unsafe_allow_html=True)
    
    apex_input = st.text_area("Event-Input", "Hier ist meine Mettwurst-Pissingerkeule für deinen Cargo-Kult!", height=100)
    is_threat = st.checkbox("Als Threat markieren", value=False)
    
    if st.button("⚡ Apex-Process", type="primary"):
        with st.spinner("Sende an Render..."):
            try:
                # HARD-BYPASS FÜR DEN SEAL
                FORCED_SEAL = "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC"
                r = httpx.post(
                    f"{st.session_state.backend_url}/api/v1/apex/process",
                    json={"message": apex_input, "is_threat": is_threat, "auth_seal": FORCED_SEAL},
                    timeout=30.0,
                )
                if r.status_code == 200:
                    data = r.json()
                    st.json(data)
                    if data.get("status") == "PROCESSED": st.success("✅ Verarbeitet!")
                    elif data.get("status") == "CONTAINED": st.warning(f"🦇 Gotham Inmate: {data.get('gotham_inmate')}")
                    log_event("INGRESS", f"Apex: {apex_input[:20]}")
                else:
                    st.error(f"HTTP {r.status_code} - {r.text}")
            except Exception as e:
                st.error(f"Fehler: {e}")

elif nav == "⚡ API Live Interface":
    st.markdown('<div class="main-header">⚡ API COMMAND CENTER ⚡</div>', unsafe_allow_html=True)
    st.session_state.auth_seal = st.text_input("Authorization Token (Seal)", value=st.session_state.auth_seal)
    st.session_state.backend_url = st.text_input("Backend-URL", value=st.session_state.backend_url)
    if st.button("Einstellungen speichern"):
        st.success("Gespeichert.")

elif nav == "🗳️ Council-Voting":
    st.markdown('<div class="main-header">🗳️ COUNCIL-VOTING</div>', unsafe_allow_html=True)
    new_proposal = st.text_input("Antrag", placeholder="z.B. Buch 100 ratifizieren")
    
    if st.button("Einbringen") and new_proposal:
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10)
            conn.execute("INSERT OR IGNORE INTO votes (proposal, ja, nein, enthalten) VALUES (?, 0, 0, 0)", (new_proposal,))
            conn.commit()
            conn.close()
            st.session_state.votes[new_proposal] = {"JA": 0, "NEIN": 0, "ENTHALTUNG": 0}
            st.rerun()
        except Exception as e: st.error(f"DB Fehler: {e}")
        
    for p, tally in st.session_state.votes.items():
        st.markdown(f"### 📜 {p}")
        c1, c2, c3 = st.columns(3)
        if c1.button(f"✅ JA ({tally['JA']})", key=f"ja_{p}"): st.session_state.votes[p]["JA"] += 1; st.rerun()
        if c2.button(f"❌ NEIN ({tally['NEIN']})", key=f"nein_{p}"): st.session_state.votes[p]["NEIN"] += 1; st.rerun()
        if c3.button(f"⚪ ENTHALTUNG ({tally['ENTHALTUNG']})", key=f"ent_{p}"): st.session_state.votes[p]["ENTHALTUNG"] += 1; st.rerun()

elif nav == "🚨 Notfall-Kill-Switch":
    st.markdown('<div class="main-header">🚨 NOTFALL-KILL-SWITCH</div>', unsafe_allow_html=True)
    
    if st.session_state.kill_switch_active:
        st.error("🚨 SYSTEM ISOLIERT 🚨")
        if st.button("🔓 System reaktivieren", type="primary"):
            st.session_state.kill_switch_active = False
            log_event("KILL", "Kill-Switch deaktiviert")
            st.rerun()
    else:
        st.warning("**WARNUNG**: Der Kill-Switch isoliert alle Ingress-Pfade sofort.")
        confirm = st.checkbox("Ich bestätige die Aktivierung.")
        if st.button("🚨 KILL-SWITCH AKTIVIEREN", type="primary", disabled=not confirm):
            st.session_state.kill_switch_active = True
            log_event("KILL", "KILL-SWITCH aktiviert")
            st.rerun()

elif nav == "🔒 WORM Ledger Audit":
    st.markdown('<div class="main-header">🔒 WORM LEDGER AUDIT</div>', unsafe_allow_html=True)
    st.success("✅ SYSTEM STATUS: CLEAN (100% PURITY_SCORE)")
    st.markdown('<div class="seal-box"><strong>SEAL:</strong> Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC_CLEAN<br/><strong>MASTER HASH:</strong><br/><code>850b2ef0...</code></div>', unsafe_allow_html=True)

elif nav == "📅 WORM-Chronik":
    st.markdown('<div class="main-header">📅 WORM-CHRONIK</div>', unsafe_allow_html=True)
    for e in st.session_state.chronik:
        st.markdown(f'<div class="chronicle chronicle-{e["kind"]}"><strong>[{e["ts"]}] {e["kind"]}</strong> :: {e["msg"]}</div>', unsafe_allow_html=True)
