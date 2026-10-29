import streamlit.components.v1 as components
from pathlib import Path
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

# ============================================================
# 1. PAGE CONFIG + HIGH-END CSS (Blue Core / Deluxe)
# ============================================================
st.set_page_config(
    page_title="YGGDRASIL_OS :: Sovereign Cockpit CC",
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
    .verdict-box { background-color: #2a0000; border: 2px solid #ff0000; padding: 25px; border-radius: 8px; text-align: center; color: #fff; font-weight: bold; margin-top: 20px; box-shadow: 0 0 20px rgba(255,0,0,0.3); }
    .lore-box { background: #0a0f1a; border-left: 4px solid #00e5ff; padding: 15px; margin-bottom: 12px; border-radius: 0 8px 8px 0; }
    .lore-box h4 { color: #00e5ff; margin: 0 0 5px 0; }
    .chronicle { background: #000; border-left: 3px solid #00ff00; padding: 10px 15px; margin: 5px 0; font-family: monospace; font-size: 0.85rem; border-radius: 4px; }
    .chronicle-ALERT { border-left-color: #ff0000; color: #ff8888; }
    .chronicle-EXEC { border-left-color: #ffd700; color: #ffe066; }
    .chronicle-INGRESS { border-left-color: #00e5ff; color: #80f0ff; }
    .chronicle-WORM { border-left-color: #00ff00; color: #88ff88; }
    .chronicle-KILL { border-left-color: #ff00ff; color: #ff88ff; background: #1a001a; }
    .hud-overlay { position: fixed; top: 10px; right: 20px; background: #05050a; padding: 10px 20px; border: 1px solid #333; border-left: 3px solid #00e5ff; border-radius: 5px; font-family: monospace; z-index: 9999; color: #ffd700; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    .stButton>button { background-color: #0a122a; color: #00e5ff; border: 1px solid #00e5ff; border-radius: 4px; transition: all 0.3s; }
    .stButton>button:hover { background-color: #00e5ff; color: #000; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. SESSION STATE & KONFIGURATION
# ============================================================
if "auth_seal" not in st.session_state:
    st.session_state.auth_seal = "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC"
if "messages" not in st.session_state: st.session_state.messages = []
if "chronik" not in st.session_state: st.session_state.chronik = [{"ts": time.strftime("%H:%M:%S"), "kind": "EXEC", "msg": "BLUE CORE v∞ online."}]
if "kill_switch_active" not in st.session_state: st.session_state.kill_switch_active = False
if "backend_url" not in st.session_state: st.session_state.backend_url = "https://aragon-backend-api.onrender.com"
if "votes" not in st.session_state: st.session_state.votes = {}
if "metric_history" not in st.session_state: st.session_state.metric_history = []

# SQLite Setup
DB_PATH = "b6_matrix.db"
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        conn.execute("CREATE TABLE IF NOT EXISTS votes (proposal TEXT PRIMARY KEY, ja INTEGER, nein INTEGER, enthalten INTEGER)")
        conn.commit()
        conn.close()
    except Exception as e:
        pass # Fail-safe für Cloud-Umgebungen
init_db()

# ============================================================
# 3. HELPER FUNKTIONEN
# ============================================================
def log_event(kind: str, msg: str):
    st.session_state.chronik.append({"ts": time.strftime("%H:%M:%S"), "kind": kind, "msg": msg})

def render_mermaid(code: str, height: int = 600):
    html_code = f'''
    <div class="mermaid" style="background-color: #0a122a; text-align: center;">{code}</div>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({{ startOnLoad: true, theme: "dark" }});
    </script>
    '''
    components.html(html_code, height=height, scrolling=True)

def check_backend():
    try:
        r = httpx.get(f"{st.session_state.backend_url}/health", timeout=5.0)
        return (r.status_code == 200), r.json()
    except Exception as e:
        return False, {"detail": str(e)}

def render_sovereign_browser(url: str, height: int = 600):
    html_code = f"""
    <div style="background: #0a122a; border: 2px solid #00e5ff; border-radius: 8px; overflow: hidden; box-shadow: 0 0 20px rgba(0, 229, 255, 0.2); font-family: 'JetBrains Mono', monospace;">
        <div style="background: #111923; padding: 10px; display: flex; align-items: center; border-bottom: 1px solid #333;">
            <div style="display: flex; gap: 6px; margin-right: 15px;">
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #ff5f56;"></div>
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #ffbd2e;"></div>
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #27c93f;"></div>
            </div>
            <div style="flex: 1; background: #05050a; padding: 5px 15px; border-radius: 4px; color: #00e5ff; font-size: 12px; border: 1px solid #1f2933; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">🔒 {url}</div>
        </div>
        <iframe src="{url}" width="100%" height="{height}px" style="border: none; background: #fff;" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>
    </div>
    """
    components.html(html_code, height=height + 60, scrolling=False)

# ============================================================
# 4. SIDEBAR & HUD
# ============================================================
COUNCIL_IMG_URL = "https://raw.githubusercontent.com/86102262471878081179/Aragon-Ultima-Cockpit/main/council.jpg"

st.markdown(f"""
<div class="hud-overlay">
    SOVEREIGN HUD<br>
    Seal: <span style="color:#00e5ff;">{st.session_state.auth_seal[:15]}...</span><br>
    Status: <span style="color:#00ff00;">ACTIVE</span>
</div>
""", unsafe_allow_html=True)

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
    "🚨 Notfall-Kill-Switch"
])

# ============================================================
# 5. PANELS
# ============================================================
if nav == "🖼️ Rat der Schwarzen Liga":
    st.markdown('<div class="main-header">RAT DER SCHWARZEN LIGA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">"Sektor Wald — Kein Zurück. Nur Code."</div>', unsafe_allow_html=True)
    try:
        st.image(COUNCIL_IMG_URL, width="stretch", caption="Gründungsväter der Matrix.")
    except:
        st.warning("Bild konnte nicht geladen werden.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="lore-box"><h4>🛡️ GREMEL SENTINEL</h4><p>Wächter des Protokolls. Erkennt feindliche Mettwurst-Injektionen.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="lore-box"><h4>👑 ODIN ULTRA ROOT</h4><p>Allvater des Root-Netzes. Die absolute Souveränität.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="lore-box"><h4>👁️ DR. SNUGGLES</h4><p>Im Schatten. Der Wusulum-Kern. Generiert neue Realitäten.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="lore-box"><h4>😈 ADVOCATUS DIABOLI</h4><p>Streit ist mein Code. Wenn er spricht, geht das Token nach Gotham.</p></div>', unsafe_allow_html=True)

elif nav == "🌀 L.S.S. Neuro-Core":
    st.markdown('<div class="main-header">🌀 L.S.S. NEURO-CORE 🌀</div>', unsafe_allow_html=True)
    tab_apex, tab_brummel, tab_pumuckl, tab_wal = st.tabs(["🧠 Apex-Process", "🌀 Brummel-Sandbox", "🦊 Pumuckl-Chaos", "🔒 WAL-Tail"])

    with tab_apex:
        apex_input = st.text_area("Event-Input", "Hier ist meine Mettwurst-Pissingerkeule für deinen Cargo-Kult!", height=100)
        is_threat = st.checkbox("Als Threat markieren", value=False)
        
        if st.button("⚡ Apex-Process", type="primary", key="apex_run"):
            with st.spinner("Sende an Render..."):
                try:
                    FORCED_SEAL = "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC" # Hard-Bypass
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

    with tab_brummel:
        b_msg = st.text_area("Brummel Injektion", "Oszilliere!")
        if st.button("Injizieren"):
            try:
                r = httpx.post(f"{st.session_state.backend_url}/api/v1/sandbox/brummel", json={"message": b_msg, "auth_seal": st.session_state.auth_seal})
                st.json(r.json())
            except Exception as e: st.error(e)

    with tab_wal:
        if st.button("WAL laden"):
            try:
                r = httpx.get(f"{st.session_state.backend_url}/api/v1/wal/tail?n=15")
                st.json(r.json())
            except Exception as e: st.error(e)

elif nav == "🔐 DNA Security":
    st.markdown('<div class="main-header">🔐 DNA SECURITY</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Brummel Sentinel RCE-Schutz</div>', unsafe_allow_html=True)
    dna_expr = st.text_input("DNA-Formel (z.B. G+C*(A-T))", "G+C*(A-T)")
    
    if st.button("Evaluieren", type="primary"):
        try:
            r = httpx.post(
                f"{st.session_state.backend_url}/api/v1/security/dna_eval",
                json={"dna_expression": dna_expr, "auth_seal": st.session_state.auth_seal}, timeout=10.0
            )
            if r.status_code == 200:
                st.success("Evaluiert"); st.json(r.json())
            else:
                st.error("BLOCKIERT"); st.json(r.json())
        except Exception as e: st.error(e)
        
    st.divider()
    if st.button("🔴 RCE Exploit testen"):
        try:
            r = httpx.post(f"{st.session_state.backend_url}/api/v1/security/dna_eval", json={"dna_expression": "__import__('os').system('rm -rf /')", "auth_seal": st.session_state.auth_seal})
            st.json(r.json())
        except Exception as e: st.error(f"Blockiert: {e}")

elif nav == "🎨 Got(sha) ColorSphere":
    st.markdown('<div class="main-header">🎨 GOT(SHA) COLORSPHERE</div>', unsafe_allow_html=True)
    layers = st.slider("Anzahl der Layer", 4, 16, 8)
    if st.button("Audit Visualisieren", type="primary"):
        colors = ["\033[31m⬤\033[0m", "\033[34m⬤\033[0m", "\033[32m⬤\033[0m", "\033[33m⬤\033[0m"]
        output = "╔════════════════════════════════════════════════════╗\n"
        output += "║ GOT(SHA) TREPPEN-VISUALISIERUNG v2                 ║\n"
        output += "╚════════════════════════════════════════════════════╝\n"
        for i in range(layers):
            color = colors[i % len(colors)]
            status = color if i <= layers // 2 else "○"
            output += f" Layer {i+1}: {status} [Audit-Pass]\n"
        st.code(output, language="text")

elif nav == "🦠 Rule 30 Automaton":
    st.markdown('<div class="main-header">🦠 RULE 30 ENTROPY</div>', unsafe_allow_html=True)
    def rule_30_step(row):
        padded = "0" + row + "0"
        new_row = []
        for i in range(1, len(padded) - 1):
            neighborhood = padded[i-1:i+2]
            new_row.append("1" if neighborhood in ("100", "011", "010", "001") else "0")
        return "".join(new_row)

    steps = st.slider("Generationen", 5, 50, 15)
    if st.button("Entropie Starten", type="primary"):
        state = "0" * 20 + "1" + "0" * 20
        result = [state]
        for _ in range(steps):
            state = rule_30_step(state)
            result.append(state)
        vis = "\n".join(["".join(["█" if c == "1" else " " for c in row]) for row in result])
        st.code(vis, language="text")

elif nav == "💀 eBPF Hulk Smash":
    st.markdown('<div class="main-header">💀 eBPF HULK SMASH</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        syscall = st.selectbox("Syscall", [59, 322, 1, 2], format_func=lambda x: f"Syscall {x}")
        uid = st.number_input("UID", value=1000)
    with col2:
        state = st.selectbox("Kernel State", [0, 1, 2], format_func=lambda x: ["0=SAFE", "1=ARMED", "2=HULK_SMASH_ENGAGED"][x])
        
    if st.button("Syscall Testen", type="primary"):
        if state == 2: st.error(f"[HULK_SMASH] Intercepted {syscall} -> Signal 9 (< 65.59 ns)")
        elif uid != 0 and syscall in (59, 322): st.warning(f"[KRAKENGUARD] Container Outbreak Blocked! Syscall: {syscall}")
        else: st.success(f"[eBPF PASS] Syscall {syscall} Allowed")

elif nav == "🌐 Sovereign Browser":
    st.markdown('<div class="main-header">🌐 SOVEREIGN BROWSER</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        default_url = "https://86102262471878081179.github.io/Black-Six-Matrix/"
        url_input = st.text_input("URL eingeben", value=default_url)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        load_btn = st.button("Öffnen", type="primary", use_container_width=True)
    st.info("💡 Hinweis: Google/GitHub blockieren oft das Einbetten. Eigene GitHub Pages funktionieren perfekt.")
    if load_btn or url_input: render_sovereign_browser(url_input, height=700)

elif nav == "⚡ API Live Interface":
    st.markdown('<div class="main-header">⚡ API COMMAND CENTER ⚡</div>', unsafe_allow_html=True)
    tab_chat, tab_settings, tab_sys = st.tabs(["💬 Live Chat", "⚙️ Settings (Seal)", "📊 System Status"])
    
    with tab_chat:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        if prompt := st.chat_input("Frage an die Matrix..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Backend wird abgefragt..."):
                    try:
                        r = httpx.post(f"{st.session_state.backend_url}/prompt/check", json={"prompt": prompt, "auth_seal": st.session_state.auth_seal}, timeout=30.0)
                        if r.status_code == 200:
                            ans = r.json().get("data", {}).get("ai_answer", "Keine Antwort.")
                            st.markdown(ans)
                            st.session_state.messages.append({"role": "assistant", "content": ans})
                        else: st.error(f"HTTP {r.status_code}")
                    except Exception as e: st.error(e)
                    
    with tab_settings:
        new_seal = st.text_input("Authorization Token (Seal)", value=st.session_state.auth_seal)
        new_backend = st.text_input("Backend-URL", value=st.session_state.backend_url)
        if st.button("Einstellungen speichern"):
            st.session_state.auth_seal = new_seal
            st.session_state.backend_url = new_backend
            st.success("Gespeichert.")
            
    with tab_sys:
        st.metric("Aktives Seal", st.session_state.auth_seal)
        st.metric("Backend", st.session_state.backend_url)

elif nav == "🧬 APEX Graph Engine":
    st.markdown('<div class="main-header">🕸️ APEX GRAPH ENGINE</div>', unsafe_allow_html=True)
    st.caption("Neo4j Query Console (Simuliert im Cockpit)")
    st.code("MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50", language="cypher")
    if st.button("Graph visualisieren", type="primary"):
        try:
            r = httpx.post(f"{st.session_state.backend_url}/api/v1/graph/query", json={"prompt": "MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 10", "auth_seal": st.session_state.auth_seal})
            st.json(r.json())
        except Exception as e: st.error(e)

elif nav == "📚 201+ Entitäten Explorer":
    st.markdown('<div class="main-header">📚 REGISTRY MANAGER 📚</div>', unsafe_allow_html=True)
    search = st.text_input("🔍 Suche nach ID, Name oder Ring", "")
    books = [
        {"ID": "0105", "Name": "Amtshaftung § 839 BGB Shield", "Ring": "Ring 1", "Score": 965},
        {"ID": "0107", "Name": "Grundgesetz Protection", "Ring": "Ring 1", "Score": 987},
        {"ID": "0068", "Name": "Sovereign Operator Apex", "Ring": "Ring 6", "Score": 1000},
        {"ID": "0100", "Name": "BUCH 100 (Φ∅) - Der Erbe", "Ring": "Ring Ω", "Score": 1000}
    ]
    df = pd.DataFrame(books)
    if search: df = df[df["Name"].str.contains(search, case=False) | df["ID"].str.contains(search)]
    st.dataframe(df, use_container_width=True, hide_index=True)

elif nav == "📖 L.S.S. Codex":
    st.markdown('<div class="main-header">📖 L.S.S. CODEX 📖</div>', unsafe_allow_html=True)
    st.markdown('<div class="seal-box"><strong>L.S.S. Codex (The Labyrinth)</strong><br/>Buch 0: Das Council<br/>Buch 1: Genesis<br/>...</div>', unsafe_allow_html=True)
    st.info("Modul 'core.lss_book' geladen. (Simulation)")

elif nav == "👻 King_Ghost Vault":
    st.markdown('<div class="main-header">👻 KING_GHOST VAULT 👻</div>', unsafe_allow_html=True)
    if st.button("Schatten-Pool abrufen", type="primary"):
        try:
            r = httpx.get(f"{st.session_state.backend_url}/api/v1/kingghost/shadows")
            st.json(r.json())
        except Exception as e: st.error(e)

elif nav == "🧠 DeepSeek Booster":
    st.markdown('<div class="main-header">🧠 DEEPSEEK BOOSTER</div>', unsafe_allow_html=True)
    prompt = st.text_area("Problem / Prompt", "Ist § 839 BGB anwendbar?", height=100)
    depth = st.slider("Reasoning-Tiefe", 1, 5, 3)
    if st.button("⚡ Boost starten", type="primary"):
        try:
            r = httpx.post(f"{st.session_state.backend_url}/api/v1/deepseek/boost", json={"prompt": prompt, "depth": depth, "auth_seal": st.session_state.auth_seal})
            if r.status_code == 200: st.json(r.json())
            else: st.error(r.text)
        except Exception as e: st.error(e)

elif nav == "🗳️ Council-Voting":
    st.markdown('<div class="main-header">🗳️ COUNCIL-VOTING</div>', unsafe_allow_html=True)
    new_proposal = st.text_input("Antrag", placeholder="z.B. Buch 100 ratifizieren")
    if st.button("Einbringen") and new_proposal:
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10)
            conn.execute("INSERT OR IGNORE INTO votes (proposal, ja, nein, enthalten) VALUES (?, 0, 0, 0)", (new_proposal,))
            conn.commit(); conn.close()
            st.session_state.votes[new_proposal] = {"JA": 0, "NEIN": 0, "ENTHALTUNG": 0}
            st.rerun()
        except Exception as e: st.error(f"DB Fehler: {e}")
        
    for p, tally in st.session_state.votes.items():
        st.markdown(f"### 📜 {p}")
        c1, c2, c3 = st.columns(3)
        if c1.button(f"✅ JA ({tally['JA']})", key=f"ja_{p}"): st.session_state.votes[p]["JA"] += 1; st.rerun()
        if c2.button(f"❌ NEIN ({tally['NEIN']})", key=f"nein_{p}"): st.session_state.votes[p]["NEIN"] += 1; st.rerun()
        if c3.button(f"⚪ ENTHALTUNG ({tally['ENTHALTUNG']})", key=f"ent_{p}"): st.session_state.votes[p]["ENTHALTUNG"] += 1; st.rerun()

elif nav == "🔒 WORM Ledger Audit":
    st.markdown('<div class="main-header">🔒 WORM LEDGER AUDIT</div>', unsafe_allow_html=True)
    st.success("✅ SYSTEM STATUS: CLEAN (100% PURITY_SCORE)")
    st.markdown('<div class="seal-box"><strong>SEAL STATUS:</strong> Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC_CLEAN<br/><strong>INTEGRITY:</strong> VERIFIED<br/><strong>MASTER HASH:</strong><br/><code>850b2ef0...</code></div>', unsafe_allow_html=True)

elif nav == "📅 WORM-Chronik":
    st.markdown('<div class="main-header">📅 WORM-CHRONIK</div>', unsafe_allow_html=True)
    for e in st.session_state.chronik:
        st.markdown(f'<div class="chronicle chronicle-{e["kind"]}"><strong>[{e["ts"]}] {e["kind"]}</strong> :: {e["msg"]}</div>', unsafe_allow_html=True)

elif nav == "🎯 Feindregister":
    st.markdown('<div class="main-header">🎯 FEINDREGISTER</div>', unsafe_allow_html=True)
    feinde = pd.DataFrame([
        {"ID": "F-001", "Name": "Amtsträger X", "Status": "ISOLATED"},
        {"ID": "F-002", "Name": "König der Lüge", "Status": "BLACKLISTED"},
        {"ID": "F-003", "Name": "Grummel-Payload", "Status": "QUARANTINED"}
    ])
    st.dataframe(feinde, use_container_width=True, hide_index=True)

elif nav == "🚨 Notfall-Kill-Switch":
    st.markdown('<div class="main-header">🚨 NOTFALL-KILL-SWITCH</div>', unsafe_allow_html=True)
    if st.session_state.kill_switch_active:
        st.error("# 🚨 SYSTEM ISOLIERT 🚨")
        if st.button("🔓 System reaktivieren", type="primary"):
            st.session_state.kill_switch_active = False
            log_event("KILL", "Kill-Switch deaktiviert")
            st.rerun()
            
elif nav == "🏴‍☠️ Omni-Shooter":
    st.markdown('<div class="main-header">🏴‍☠️ BLACK SIX OMNI-SHOOTER</div>', unsafe_allow_html=True)
    
    # Pfad zur HTML-Datei
    html_path = Path(__file__).parent / "frontend" / "omni_shooter.html"
    
    if html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        # Rendert das HTML in einem Iframe
        components.html(html_content, height=900, scrolling=True)
    else:
elif nav == "🚨 Notfall-Kill-Switch":
    if st.session_state.kill_switch_active:
        st.error("🚨 SYSTEM ISOLIERT 🚨")
        if st.button("🔓 System reaktivieren", type="primary"):
            st.session_state.kill_switch_active = False
            log_event("KILL", "Kill-Switch deaktiviert")
            st.rerun()
    else:
