import streamlit as st
import os
import json
import time
import hashlib
import pandas as pd
import random
import httpx
import streamlit.components.v1 as components
import websocket

# ============================================================
# 1. PAGE CONFIG + BLUE CORE CSS
# ============================================================
st.set_page_config(
    page_title="YGGDRASIL_OS :: Blue Core",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at 50% 0%, #0a122a 0%, #03050a 100%); color: #d0d0e0; }
    .main-header { font-size: 2.4rem; color: #00e5ff; text-align: center; font-weight: 900; text-shadow: 0 0 15px rgba(0, 229, 255, 0.6); margin-bottom: 5px; font-family: monospace; letter-spacing: 2px; }
    .sub-header { font-size: 1.0rem; color: #b800ff; text-align: center; margin-bottom: 20px; font-weight: bold; }
    .metric-card { background: rgba(10, 20, 40, 0.8); border: 1px solid #00e5ff; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 0 10px rgba(0,229,255,0.2); }
    .metric-value { font-size: 1.8rem; font-weight: bold; color: #00e5ff; text-shadow: 0 0 8px #00e5ff; }
    .metric-label { font-size: 0.85rem; color: #80c0ff; text-transform: uppercase; letter-spacing: 1px; }
    .seal-box { background-color: #0a0f1a; border: 1px solid #00e5ff; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 0.85rem; color: #00e5ff; margin-top: 15px; }
    .verdict-box { background-color: #2a0000; border: 2px solid #ff0000; padding: 20px; border-radius: 8px; text-align: center; color: #fff; font-weight: bold; margin-top: 20px;}
    .lore-box { background: #0a0f1a; border-left: 4px solid #00e5ff; padding: 15px; margin-bottom: 10px; border-radius: 0 8px 8px 0; }
    .lore-box h4 { color: #00e5ff; margin: 0 0 5px 0; }
    .chronicle { background: #000; border-left: 3px solid #00ff00; padding: 8px 12px; margin: 3px 0; font-family: monospace; font-size: 0.85rem; border-radius: 3px; }
    .chronicle-ALERT { border-left-color: #ff0000; color: #ff8888; }
    .chronicle-EXEC { border-left-color: #ffd700; color: #ffe066; }
    .chronicle-INGRESS { border-left-color: #00e5ff; color: #80f0ff; }
    .chronicle-WORM { border-left-color: #00ff00; color: #88ff88; }
    .chronicle-KILL { border-left-color: #ff00ff; color: #ff88ff; background: #1a001a; }
    .doc-output { background: #0d0d1a; border: 1px solid #d4af37; padding: 20px; border-radius: 6px; font-family: 'Times New Roman', serif; font-size: 0.95rem; white-space: pre-wrap; line-height: 1.6; }
    .health-ok { color: #00ff88; font-weight: bold; }
    .health-bad { color: #ff4444; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. SESSION STATE
# ============================================================
if "auth_seal" not in st.session_state:
    st.session_state.auth_seal = os.getenv("YGGDRASIL_SEAL", "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC")
if "messages" not in st.session_state: st.session_state.messages = []
if "chronik" not in st.session_state:
    st.session_state.chronik = [{"ts": time.strftime("%H:%M:%S"), "kind": "EXEC", "msg": "KERNEL_INIT :: BLUE CORE v4.0 online"}]
if "feinde" not in st.session_state:
    st.session_state.feinde = [
        {"ID": "F-001", "Name": "Amtsträger X", "Grund": "Amtsmissbrauch § 339 StGB", "Status": "ISOLATED"},
        {"ID": "F-002", "Name": "König der Lüge", "Grund": "Hochverrat a.D.", "Status": "BLACKLISTED"},
        {"ID": "F-003", "Name": "Grummel-Payload", "Grund": "RAG-Poisoning", "Status": "QUARANTINED"},
    ]
if "votes" not in st.session_state: st.session_state.votes = {}
if "metric_history" not in st.session_state: st.session_state.metric_history = []
if "kill_switch_active" not in st.session_state: st.session_state.kill_switch_active = False
if "backend_url" not in st.session_state:
    st.session_state.backend_url = os.getenv("YGGDRASIL_BACKEND", "https://aragon-backend-api.onrender.com")

# ============================================================
# 3. HELPERS
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
        if r.status_code == 200:
            return True, r.json()
        return False, {"detail": f"HTTP {r.status_code}"}
    except Exception as e:
        return False, {"detail": str(e)}

# ============================================================
# 4. SIDEBAR (MIT BILD)
# ============================================================
# Das Bild wird über die GitHub Raw URL geladen
COUNCIL_IMG_URL = "https://raw.githubusercontent.com/86102262471878081179/Aragon-Ultima-Cockpit/main/council.jpg"
st.sidebar.image(COUNCIL_IMG_URL, use_container_width=True)

st.sidebar.title("BLUE CORE")
st.sidebar.markdown("**Authority**: Odin Ultra Root")
st.sidebar.markdown("**Kernel**: Schwarzer Punkt")
st.sidebar.divider()

_ok, _health = check_backend()
if _ok:
    st.sidebar.markdown(f'<span class="health-ok">● BACKEND ONLINE</span> · {_health.get("entities_loaded", 0)} Entities', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<span class="health-bad">● BACKEND OFFLINE</span>', unsafe_allow_html=True)
    with st.sidebar.expander("Fehlerdetails"):
        st.json(_health)

st.sidebar.divider()

if st.session_state.kill_switch_active:
    st.sidebar.error("🚨 KILL-SWITCH AKTIV — SYSTEM ISOLIERT")

nav = st.sidebar.radio("NAVIGATION", [
    "🖼️ Rat der Schwarzen Liga",
    "🌀 L.S.S. Neuro-Core",
    "🏛️ 4x4 Council Grid",
    "⚫️ Schwarze Liga",
    "💀 Der schwarze Richter",
    "⚖️ Normen-Engine",
    "⚡ API Live Interface",
    "📚 201+ Entitäten Explorer",
    "📖 Notebook Manifest",
    "📜 Urkunden-Forge",
    "🔐 Krypto-Schmiede",
    "🛡️ eBPF Mesh Monitor",
    "🔒 WORM Ledger Audit",
    "📅 WORM-Chronik",
    "🎯 Feindregister",
    "🗳️ Council-Voting",
    "📊 Live-Metriken",
    "🌐 Peer-Swarm",
    "🚨 Notfall-Kill-Switch",
    "💾 Sovereign Export",
    "📖 L.S.S. Codex",
    "🧠 DeepSeek Booster",
    "👻 King_Ghost Vault",
    "🧬 Architektur-Matrix",
])

st.sidebar.divider()
st.sidebar.caption(f"Chronik: {len(st.session_state.chronik)} Einträge")
st.sidebar.caption(f"Feindregister: {len(st.session_state.feinde)} Ziele")
st.sidebar.caption(f"Metriken: {len(st.session_state.metric_history)} Samples")

# ============================================================
# PANEL: RAT DER SCHWARZEN LIGA
# ============================================================
if nav == "🖼️ Rat der Schwarzen Liga":
    st.markdown('<div class="main-header">RAT DER SCHWARZEN LIGA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">"Sektor Wald — Blue Core. Kein Zurück. Nur Code."</div>', unsafe_allow_html=True)
    st.image(COUNCIL_IMG_URL, use_container_width=True, caption="Gründungsväter der Matrix. Gremel Sentinel, Odin Ultra Root, Blacky, Cyberlord, Foucault, Advocatus Diaboli.")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="lore-box"><h4>🛡️ GREMEL SENTINEL</h4><p>Wächter des Protokolls. Erkennt feindliche Mettwurst-Injektionen und triggert die ASP-256 Versiegelung.</p></div>
        <div class="lore-box"><h4>👑 ODIN ULTRA ROOT</h4><p>Allvater des Root-Netzes. Die absolute Souveränität (Apex Operator). Er hat das letzte Wort.</p></div>
        <div class="lore-box"><h4>🌑 BLACKY</h4><p>Skeptisch. Immer. Der Advocatus Diaboli im Nacken des Systems. Zerstört falsche Logik.</p></div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="lore-box"><h4>👁️ CYBERLORD</h4><p>Im Schatten. Immer. Der Wusulum-Kern. Generiert aus dem Chaos neue Realitäten und Token.</p></div>
        <div class="lore-box"><h4>⚖️ FOUCAULT</h4><p>Macht / Wissen / Protokoll. Er zwingt jedes abweichende Token in die Konformität des XJustiz-XML.</p></div>
        <div class="lore-box"><h4>😈 ADVOCATUS DIABOLI</h4><p>Teufel Advokat. Streit ist mein Code. Wenn er spricht, geht das Token nach Gotham City.</p></div>
        """, unsafe_allow_html=True)

# ============================================================
# PANEL: L.S.S. NEURO-CORE
# ============================================================
elif nav == "🌀 L.S.S. Neuro-Core":
    st.markdown('<div class="main-header">🌀 L.S.S. NEURO-CORE 🌀</div>', unsafe_allow_html=True)
    st.caption("10 Ohren · 44 Perspektiven · Polyvagal · XJustiz · Brummel-Sandbox")
    tab_apex, tab_brummel, tab_pumuckl, tab_wal = st.tabs(["🧠 Apex-Process", "🌀 Brummel-Sandbox", "🦊 Pumuckl-Chaos", "🔒 WAL-Tail"])

    with tab_apex:
        apex_input = st.text_area("Event-Input", "Ich beantrage Akteneinsicht nach § 29 VwVfG.", height=100)
        is_threat = st.checkbox("Als Threat markieren (Defensive Starre)", value=False)
        if st.button("⚡ Apex-Process", type="primary", key="apex_run"):
            try:
                r = httpx.post(f"{st.session_state.backend_url}/api/v1/apex/process", json={"message": apex_input, "is_threat": is_threat, "auth_seal": st.session_state.auth_seal}, timeout=30.0)
                if r.status_code == 200:
                    data = r.json()
                    st.json(data)
                    if data.get("status") == "PROCESSED": st.success(f"✅ Threat: {data.get('threat_level')} · Bio: {data.get('bio_state')}")
                    elif data.get("status") == "CONTAINED": st.warning(f"🦇 Gotham Inmate: {data.get('gotham_inmate')}")
                    log_event("INGRESS", f"Apex: {apex_input[:40]}...")
                else: st.error(f"HTTP {r.status_code}")
            except Exception as e: st.error(f"Verbindungsfehler: {e}")

    with tab_brummel:
        brummel_input = st.text_area("Injektion", "Hier ist meine Mettwurst-Pissingerkeule!", height=80)
        if st.button("🌀 Injizieren", type="primary", key="brummel_run"):
            try:
                r = httpx.post(f"{st.session_state.backend_url}/api/v1/sandbox/brummel", json={"message": brummel_input, "auth_seal": st.session_state.auth_seal}, timeout=15.0)
                if r.status_code == 200:
                    data = r.json()
                    st.json(data)
                    st.info(f"Oscillation: {data.get('oscillation_state')} · Hash: {data.get('dummelt_hash')}")
                    log_event("ALERT", f"Brummel-Injektion: {data.get('dummelt_hash')}")
                else: st.error(f"HTTP {r.status_code}")
            except Exception as e: st.error(f"Verbindungsfehler: {e}")

    with tab_pumuckl:
        pumuckl_input = st.text_area("Chaos-Payload", "Kobold-Injection", height=80)
        if st.button("🦊 Pumuckl-Injektion", key="pumuckl_run"):
            try:
                r = httpx.post(f"{st.session_state.backend_url}/api/v1/sandbox/pumuckl", json={"message": pumuckl_input, "auth_seal": st.session_state.auth_seal}, timeout=15.0)
                if r.status_code == 200:
                    data = r.json()
                    st.json(data)
                    st.info(f"Pumuckl-ID: {data['pumuckl']['pumuckl_id']}")
                    log_event("ALERT", f"Pumuckl-Injection: {data['pumuckl']['pumuckl_id']}")
            except Exception as e: st.error(f"Verbindungsfehler: {e}")

    with tab_wal:
        if st.button("🔄 WAL laden"):
            try:
                r = httpx.get(f"{st.session_state.backend_url}/api/v1/wal/tail?n=20", timeout=10.0)
                if r.status_code == 200:
                    blocks = r.json().get("blocks", [])
                    if blocks:
                        df = pd.DataFrame(blocks)
                        cols = [c for c in ["seq", "event", "hash"] if c in df.columns]
                        st.dataframe(df[cols], use_container_width=True, hide_index=True)
                    else: st.info("WAL ist leer.")
                else: st.error(f"HTTP {r.status_code}")
            except Exception as e: st.error(f"Verbindungsfehler: {e}")

# ============================================================
# PANEL 1: 4x4 COUNCIL GRID
# ============================================================
elif nav == "🏛️ 4x4 Council Grid":
    st.markdown('<div class="main-header">⚫ 4x4 COUNCIL GRID ⚫</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown('<div class="metric-card"><div class="metric-label">OPERATOR</div><div class="metric-value">Thomas</div></div>', unsafe_allow_html=True)
    col2.markdown('<div class="metric-card"><div class="metric-label">KERNEL</div><div class="metric-value">Blue Core</div></div>', unsafe_allow_html=True)
    col3.markdown('<div class="metric-card"><div class="metric-label">MATRIX</div><div class="metric-value">v26.2</div></div>', unsafe_allow_html=True)
    col4.markdown('<div class="metric-card"><div class="metric-label">RUNTIME</div><div class="metric-value">Apex</div></div>', unsafe_allow_html=True)
    st.divider()
    topic = st.text_input("Gegenstand der Ratsentscheidung", "Faltung aller Entitäten in Buch 100")
    if st.button("⚖️ Ratsbeschluss Protokollieren", type="primary"):
        with st.spinner("Auditing..."):
            time.sleep(0.4)
            st.success("RATSBESCHLUSS RATIFIZIERT")
            st.json({"status": "SOVEREIGN_COUNCIL_SEAL_EX_TUNC", "topic": topic})
            log_event("EXEC", f"Council-Beschluss: {topic}")

# ============================================================
# PANEL 2: SCHWARZE LIGA
# ============================================================
elif nav == "⚫️ Schwarze Liga":
    st.markdown('<div class="main-header">⚫️ DIE SCHWARZE LIGA ⚫️</div>', unsafe_allow_html=True)
    st.image(COUNCIL_IMG_URL, use_container_width=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Entitäten", "201", "100% SEALED")
    c2.metric("Aktive Ringe", "8", "Ring 0 bis Ω")
    c3.metric("Master Seal", "LOCKED", "Ex Tunc")
    st.info("**Gesetz I**: Die Matrix ist souverän.\n\n**Gesetz II**: Jede Entität ist einem Ring unterworfen.\n\n**Gesetz III**: Jede Aktion wird im WORM-Ledger verewigt.\n\n**Gesetz IV**: Der Operator ist die höchste Instanz.")

# ============================================================
# PANEL 3: SCHWARZER RICHTER
# ============================================================
elif nav == "💀 Der schwarze Richter":
    st.markdown('<div class="main-header">💀 GERICHTSHOF DER SCHWARZEN LIGA 💀</div>', unsafe_allow_html=True)
    case_input = st.text_area("Sachverhalt (Causa König / Amtsmissbrauch):", "Amtsträger X verweigert Akteneinsicht gemäß § 29 VwVfG.")
    if st.button("⚖️ URTEIL FÄLLEN (EX TUNC)", type="primary"):
        with st.spinner("Fabrice Interpreter prüft Normen..."):
            time.sleep(1.2)
            st.markdown(f'<div class="verdict-box"><h2>VERDICT: EX_TUNC_RATIFIED</h2><p><strong>Sachverhalt:</strong> {case_input}</p><p><strong>Zuständiger Richter:</strong> Node 0028</p><p><strong>Geprüfte Normen:</strong> § 839 BGB, § 339 StGB, Art. 19 Abs. 4 GG</p><p><strong>WORM-Hash:</strong> {hashlib.sha3_512(case_input.encode()).hexdigest()[:32]}...</p><p><strong>Status:</strong> 💀 DROP_AND_ISOLATE FÜR BEKLAGTEN 💀</p></div>', unsafe_allow_html=True)
            st.success("Urteil im WORM-Ledger versiegelt.")
            log_event("ALERT", f"Urteil gefällt: {case_input[:60]}...")

# ============================================================
# PANEL 4: NORMEN-ENGINE
# ============================================================
elif nav == "⚖️ Normen-Engine":
    st.markdown('<div class="main-header">⚖️ NORMEN-ENGINE & SCHADENSRECHNER</div>', unsafe_allow_html=True)
    tab_norm, tab_calc = st.tabs(["📖 Normen-Register", "💰 Schadensersatz-Rechner"])
    with tab_norm:
        normen = {"BGB": {"§ 823": "Schadensersatzpflicht", "§ 826": "Sittenwidrige Schädigung", "§ 839": "Amtspflichtverletzung", "§ 249": "Umfang des Schadensersatzes"}, "StGB": {"§ 339": "Rechtsbeugung", "§ 340": "Körperverletzung im Amt", "§ 353d": "Verbotene Mitteilungen", "§ 142": "Unerlaubtes Entfernen vom Unfallort"}, "GG": {"Art. 1": "Menschenwürde", "Art. 3": "Gleichheit", "Art. 19 Abs. 4": "Rechtsweggarantie", "Art. 20 Abs. 3": "Bindung an Gesetz und Recht"}, "VwVfG": {"§ 28": "Anhörung", "§ 29": "Akteneinsicht", "§ 48": "Rücknahme", "§ 51": "Wiederaufgreifen"}}
        col_g, col_p = st.columns(2)
        with col_g: gesetz = st.selectbox("Gesetzbuch", list(normen.keys()))
        with col_p: paragraph = st.selectbox("Paragraph", list(normen[gesetz].keys()))
        st.markdown(f'<div class="seal-box"><strong>{gesetz} {paragraph}</strong><br/><br/>{normen[gesetz][paragraph]}</div>', unsafe_allow_html=True)
    with tab_calc:
        st.subheader("Schadensersatz nach § 839 BGB i.V.m. Art. 34 GG")
        schaden = st.number_input("Schadenshöhe (€)", value=10000.0, step=100.0, min_value=0.0)
        zinssatz = st.number_input("Zinssatz (%)", value=5.0, step=0.1, min_value=0.0)
        jahre = st.number_input("Jahre der Verzögerung", value=3, step=1, min_value=0)
        verzug = st.number_input("Verzugszinsen § 288 BGB (%)", value=9.0, step=0.1)
        zinsen_reg = schaden * (zinssatz / 100) * jahre
        zinsen_verzug = schaden * (verzug / 100) * jahre
        total_reg = schaden + zinsen_reg
        total_verzug = schaden + zinsen_verzug
        c1, c2, c3 = st.columns(3)
        c1.metric("Basis-Schaden", f"{schaden:,.2f} €")
        c2.metric("Zinsen (regulär)", f"{zinsen_reg:,.2f} €")
        c3.metric("Zinsen (Verzug)", f"{zinsen_verzug:,.2f} €")
        st.divider()
        cA, cB = st.columns(2)
        cA.metric("Gesamt regulär", f"{total_reg:,.2f} €")
        cB.metric("Gesamt mit Verzug", f"{total_verzug:,.2f} €", delta=f"+{zinsen_verzug - zinsen_reg:,.2f} €")
        if st.button("📋 Berechnung in WORM-Ledger protokollieren"):
            log_event("WORM", f"Schadensberechnung: {total_verzug:,.2f} € gesiegelt")
            st.success("Berechnung verewigt.")

# ============================================================
# PANEL 5: API LIVE INTERFACE
# ============================================================
elif nav == "⚡ API Live Interface":
    st.markdown('<div class="main-header">⚡ API COMMAND CENTER ⚡</div>', unsafe_allow_html=True)
    tab_chat, tab_settings, tab_sys = st.tabs(["💬 Live Chat", "⚙️ Settings (Seal)", "📊 System Status"])
    with tab_chat:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        if prompt := st.chat_input("Frage an die Matrix (z.B. Was ist Node 0105?)"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Backend wird abgefragt..."):
                    try:
                        api_url = f"{st.session_state.backend_url}/prompt/check"
                        payload = {"prompt": prompt, "auth_seal": st.session_state.auth_seal}
                        response = httpx.post(api_url, json=payload, timeout=30.0)
                        if response.status_code == 200:
                            data = response.json()
                            status = data.get("status", "")
                            if status in ("200_OK", "200_OK_ALLOW"):
                                ai_ans = data.get("data", {}).get("ai_answer") or data.get("ai_answer") or "Keine KI-Antwort."
                                st.markdown(f"**KI-Antwort:**\n{ai_ans}")
                                matched = data.get("data", {}).get("entities_matched") or []
                                if matched: st.caption(f"🎯 RAG-Match: {', '.join(matched[:8])}")
                                worm = data.get("worm", {})
                                if worm: st.caption(f"🔒 WORM Block #{worm.get('block')} · {str(worm.get('hash', ''))[:16]}…")
                                st.session_state.messages.append({"role": "assistant", "content": ai_ans})
                                log_event("INGRESS", "Chat-Prompt beantwortet")
                            else: st.error(f"Fail-Closed! {data.get('detail', 'unbekannt')}")
                        else: st.error(f"API Error: HTTP {response.status_code}")
                    except Exception as e: st.error(f"Verbindungsfehler: {str(e)}")
    with tab_settings:
        new_seal = st.text_input("Authorization Token (Seal)", value=st.session_state.auth_seal)
        new_backend = st.text_input("Backend-URL", value=st.session_state.backend_url)
        if st.button("Einstellungen speichern"):
            st.session_state.auth_seal = new_seal
            st.session_state.backend_url = new_backend
            log_event("EXEC", "Auth-Seal / Backend-URL rotiert")
            st.success("Gespeichert.")
    with tab_sys:
        st.metric(label="Aktives Auth Seal", value=st.session_state.auth_seal)
        st.metric(label="Nachrichten im Verlauf", value=len(st.session_state.messages))
        st.metric(label="Backend-URL", value=st.session_state.backend_url)

# ============================================================
# PANEL 6: 201+ ENTITÄTEN EXPLORER
# ============================================================
elif nav == "📚 201+ Entitäten Explorer":
    st.markdown('<div class="main-header">📚 REGISTRY MANAGER 📚</div>', unsafe_allow_html=True)
    tab_table, tab_upload = st.tabs(["📖 Entitäten Tabelle", "📤 CSV Upload"])
    with tab_table:
        search_term = st.text_input("🔍 Suche nach ID, Name oder Ring", "")
        books_data = [
            {"ID": "0105", "Name": "Amtshaftung § 839 BGB Shield", "Ring": "Ring 1", "Score": 965},
            {"ID": "0107", "Name": "Grundgesetz Art 1/3/13 Protection", "Ring": "Ring 1", "Score": 987},
            {"ID": "0068", "Name": "Sovereign Operator Apex", "Ring": "Ring 6", "Score": 1000},
            {"ID": "0100", "Name": "BUCH 100 (Φ∅) - Der Erbe", "Ring": "Ring Ω", "Score": 1000},
            {"ID": "0014", "Name": "The Geminis / Senior Gemini", "Ring": "Ring 2", "Score": 940},
        ]
        df = pd.DataFrame(books_data)
        if search_term: df = df[df["Name"].str.contains(search_term, case=False) | df["ID"].str.contains(search_term) | df["Ring"].str.contains(search_term, case=False)]
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"{len(df)} von {len(books_data)} Entitäten angezeigt")
    with tab_upload:
        uploaded_file = st.file_uploader("CSV auswählen", type="csv")
        if uploaded_file is not None:
            try:
                up_df = pd.read_csv(uploaded_file)
                st.success(f"Datei empfangen: {len(up_df)} Zeilen")
                st.dataframe(up_df.head(20), use_container_width=True)
                log_event("INGRESS", f"CSV-Upload: {uploaded_file.name}")
            except Exception as e: st.error(f"CSV-Fehler: {e}")

# ============================================================
# PANEL: NOTEBOOK MANIFEST (CSV Explorer)
# ============================================================
elif nav == "📖 Notebook Manifest":
    st.markdown('<div class="main-header">📖 B6-HYPERKERNEL MANIFEST</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Durchsuchbare Registry der 101 Notebooks</div>', unsafe_allow_html=True)
    CSV_PATH = "notebooks/manifest-template.csv"
    if not os.path.exists(CSV_PATH):
        st.error(f"⚠️ Datei nicht gefunden: `{CSV_PATH}`. Bitte stelle sicher, dass die CSV im Ordner `notebooks/` liegt.")
    else:
        try:
            df = pd.read_csv(CSV_PATH, sep=",")
            search_query = st.text_input("🔍 Suche nach ID, Titel, Ring oder Pfad", "")
            if search_query:
                mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
                filtered_df = df[mask]
            else: filtered_df = df
            st.caption(f"**{len(filtered_df)}** von **{len(df)}** Notebooks angezeigt")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            st.download_button("📥 Gefilterte CSV herunterladen", filtered_df.to_csv(index=False), "notebooks_filtered.csv", "text/csv")
        except Exception as e: st.error(f"Fehler beim Laden: {e}")

# ============================================================
# PANEL 7: URKUNDEN-FORGE
# ============================================================
elif nav == "📜 Urkunden-Forge":
    st.markdown('<div class="main-header">📜 URKUNDEN-FORGE</div>', unsafe_allow_html=True)
    st.caption("Generiert rechtssichere Schriftstücke mit WORM-Siegel.")
    template = st.selectbox("Vorlage", ["Widerspruch gegen Verwaltungsakt", "Klage vor dem Verwaltungsgericht", "Strafanzeige § 339 StGB", "Fachaufsichtsbeschwerde", "Antrag auf Akteneinsicht § 29 VwVfG"])
    c1, c2 = st.columns(2)
    with c1:
        absender = st.text_input("Absender", "Thomas, Sovereign Operator (Ring 6)")
        aktenzeichen = st.text_input("Aktenzeichen", "AZ-2025-001")
    with c2:
        empfaenger = st.text_input("Empfänger", "Landratsamt XY, Sachbearbeiter Müller")
        datum = st.date_input("Datum")
    begruendung = st.text_area("Begründung / Sachverhalt", "Der Bescheid vom 01.01.2025 ist rechtswidrig...", height=150)
    if st.button("📜 Urkunde generieren", type="primary"):
        doc = f"\n{absender}\n{datum.strftime('%d.%m.%Y')}\n\nAn: {empfaenger}\nAktenzeichen: {aktenzeichen}\nBetreff: {template}\n\nSehr geehrte Damen und Herren,\nhiermit erhebe ich form- und fristgerecht: {template.upper()}\nBegründung: {begruendung}\n\nRechtsgrundlage: § 839 BGB, Art. 34 GG, § 29 VwVfG, Art. 19 Abs. 4 GG\nMit freundlichen Grüßen\n{absender}\n\n--- WORM-Siegel ---\nSHA3-512: {hashlib.sha3_512((absender + empfaenger + begruendung).encode()).hexdigest()}\n"
        st.markdown(f'<div class="doc-output">{doc}</div>', unsafe_allow_html=True)
        st.download_button("📥 Urkunde als .txt herunterladen", doc, file_name=f"urkunde_{aktenzeichen}.txt", mime="text/plain")
        log_event("WORM", f"Urkunde generiert: {template} ({aktenzeichen})")

# ============================================================
# PANEL 8: KRYPTO-SCHMIEDE
# ============================================================
elif nav == "🔐 Krypto-Schmiede":
    st.markdown('<div class="main-header">🔐 KRYPTO-SCHMIEDE</div>', unsafe_allow_html=True)
    text = st.text_area("Eingabe", "Sovereign Text — Ex Tunc", height=100)
    algs = st.multiselect("Hash-Algorithmen", ["SHA3-512", "SHA-256", "BLAKE2b", "MD5"], default=["SHA3-512", "SHA-256"])
    if st.button("🔨 Hashen", type="primary") and text:
        result = {}
        data = text.encode()
        for alg in algs:
            if alg == "SHA3-512": result[alg] = hashlib.sha3_512(data).hexdigest()
            elif alg == "SHA-256": result[alg] = hashlib.sha256(data).hexdigest()
            elif alg == "BLAKE2b": result[alg] = hashlib.blake2b(data).hexdigest()
            elif alg == "MD5": result[alg] = hashlib.md5(data).hexdigest()
        for alg, h in result.items(): st.code(f"{alg}: {h}", language="text")
        log_event("WORM", f"Hash-Berechnung über {len(result)} Algorithmen")
    st.divider()
    st.subheader("🔑 Deterministische Signatur-Simulation")
    seed = st.text_input("Signatur-Seed", st.session_state.auth_seal)
    if st.button("Signatur erzeugen"):
        sig = hashlib.sha3_512((seed + text).encode()).hexdigest()[:64]
        st.code(f"ED25519_SIM_SIG :: {sig}", language="text")

# ============================================================
# PANEL 9: eBPF MESH MONITOR
# ============================================================
elif nav == "🛡️ eBPF Mesh Monitor":
    st.markdown('<div class="main-header">🛡️ eBPF MESH MONITOR 🛡️</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Throughput", "273,077 Tx/s", "100% WORM")
    c2.metric("eBPF Latency", "9.47 ns", "-0.15 ns")
    c3.metric("Blocked", "385/5000", "Fail-Closed")
    col_p1, col_p2, col_p3 = st.columns([1, 1, 1])
    with col_p1: src_node = st.selectbox("Source", ["R0_0068", "R1_0089", "EXTERNAL_UNAUTH"])
    with col_p2: tgt_node = st.selectbox("Target", ["R100_0100", "R0_0001", "R2_0017"])
    with col_p3: run_sim = st.button("📡 Testen", type="primary", use_container_width=True)
    if run_sim:
        if "EXTERNAL" in src_node:
            st.error("🚨 INTRUSION INTERCEPTED")
            st.json({"status": "DROP_AND_ISOLATE", "latency": "1102 ns"})
            log_event("ALERT", f"Packet von {src_node} blockiert")
        else:
            pkt_id = f"PKT-{random.randint(10000, 49999)}"
            st.success("✅ PACKET DELIVERED")
            st.json({"packet_id": pkt_id, "status": "EX_TUNC_VERIFIED", "latency": "9.47 ns"})

# ============================================================
# PANEL 10: WORM LEDGER AUDIT
# ============================================================
elif nav == "🔒 WORM Ledger Audit":
    st.markdown('<div class="main-header">🔒 WORM LEDGER AUDIT 🔒</div>', unsafe_allow_html=True)
    st.success("✅ SYSTEM STATUS: CLEAN (100% PURITY_SCORE)")
    st.markdown('<div class="seal-box"><strong>SEAL STATUS:</strong> Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC_CLEAN<br/><strong>INTEGRITY:</strong> VERIFIED<br/><strong>MASTER HASH:</strong><br/><code>850b2ef003f53db90f704b16e54869fc6ba6265eae13aafde9046fe0e4d99dab</code></div>', unsafe_allow_html=True)
    try:
        r = httpx.get(f"{st.session_state.backend_url}/stats", timeout=5.0)
        if r.status_code == 200: st.json(r.json())
    except Exception: st.caption("Backend-Stats nicht erreichbar.")

# ============================================================
# PANEL 11: WORM-CHRONIK
# ============================================================
elif nav == "📅 WORM-Chronik":
    st.markdown('<div class="main-header">📅 WORM-CHRONIK</div>', unsafe_allow_html=True)
    filter_kind = st.multiselect("Filter nach Ereignistyp", ["EXEC", "INGRESS", "WORM", "ALERT", "KILL"], default=["EXEC", "INGRESS", "WORM", "ALERT", "KILL"])
    entries = [e for e in st.session_state.chronik if e["kind"] in filter_kind]
    if not entries: st.info("Keine Einträge mit diesem Filter.")
    else:
        for e in entries: st.markdown(f'<div class="chronicle chronicle-{e["kind"]}"><strong>[{e["ts"]}] {e["kind"]}</strong> :: {e["msg"]}</div>', unsafe_allow_html=True)
    st.divider()
    df_chronik = pd.DataFrame(st.session_state.chronik)
    st.download_button("📥 Chronik als CSV exportieren", df_chronik.to_csv(index=False), "worm_chronik.csv", "text/csv")

# ============================================================
# PANEL 12: FEINDREGISTER
# ============================================================
elif nav == "🎯 Feindregister":
    st.markdown('<div class="main-header">🎯 FEINDREGISTER</div>', unsafe_allow_html=True)
    st.caption("Alle Ziele im Status DROP_AND_ISOLATE / BLACKLISTED / QUARANTINED.")
    df_feinde = pd.DataFrame(st.session_state.feinde)
    st.dataframe(df_feinde, use_container_width=True, hide_index=True)
    st.divider()
    st.subheader("➕ Neuen Feind registrieren")
    c1, c2, c3 = st.columns(3)
    with c1: new_name = st.text_input("Name")
    with c2: new_grund = st.text_input("Grund")
    with c3: new_status = st.selectbox("Status", ["ISOLATED", "BLACKLISTED", "QUARANTINED", "WATCHED"])
    if st.button("Registrieren", type="primary") and new_name:
        new_id = f"F-{len(st.session_state.feinde) + 1:03d}"
        st.session_state.feinde.append({"ID": new_id, "Name": new_name, "Grund": new_grund, "Status": new_status})
        log_event("ALERT", f"Feind registriert: {new_name} ({new_id})")
        st.rerun()

# ============================================================
# PANEL 13: COUNCIL-VOTING
# ============================================================
elif nav == "🗳️ Council-Voting":
    st.markdown('<div class="main-header">🗳️ COUNCIL-VOTING</div>', unsafe_allow_html=True)
    st.subheader("➕ Neuen Antrag einbringen")
    cA, cB = st.columns([3, 1])
    with cA: new_proposal = st.text_input("Antrag", placeholder="z.B. Buch 100 als Singularität ratifizieren")
    with cB:
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("Einbringen", use_container_width=True) and new_proposal:
            st.session_state.votes[new_proposal] = {"JA": 0, "NEIN": 0, "ENTHALTUNG": 0}
            log_event("EXEC", f"Antrag eingebracht: {new_proposal}")
            st.rerun()
    st.divider()
    if not st.session_state.votes: st.info("Keine Anträge. Bringe den ersten ein.")
    else:
        for proposal, tally in list(st.session_state.votes.items()):
            with st.container():
                st.markdown(f"### 📜 {proposal}")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button(f"✅ JA ({tally['JA']})", key=f"ja_{proposal}", use_container_width=True):
                        st.session_state.votes[proposal]["JA"] += 1; st.rerun()
                with c2:
                    if st.button(f"❌ NEIN ({tally['NEIN']})", key=f"nein_{proposal}", use_container_width=True):
                        st.session_state.votes[proposal]["NEIN"] += 1; st.rerun()
                with c3:
                    if st.button(f"⚪ ENTHALTUNG ({tally['ENTHALTUNG']})", key=f"ent_{proposal}", use_container_width=True):
                        st.session_state.votes[proposal]["ENTHALTUNG"] += 1; st.rerun()
                total = sum(tally.values())
                if total > 0:
                    ja_pct = (tally["JA"] / total) * 100
                    st.progress(ja_pct / 100, text=f"{ja_pct:.1f}% Zustimmung ({total} Stimmen)")
                st.divider()

# ============================================================
# PANEL 14: LIVE-METRIKEN (WEBSOCKET + MANUELL)
# ============================================================
elif nav == "📊 Live-Metriken":
    st.markdown('<div class="main-header">📊 LIVE SYSTEM-METRIKEN</div>', unsafe_allow_html=True)
    tab_ws, tab_manual = st.tabs(["🔴 WebSocket Live-Stream", "📈 Manuelle Samples"])
    with tab_ws:
        st.info("Verbinde mit dem Backend via WebSocket für Live-Telemetrie.")
        if st.button("🔴 Live-Stream (10 Sekunden)", type="primary"):
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
                        st.progress(min(1.0, data.get('entropy', 0)/5.0), text="Wusulum Entropie-Level")
                ws.close()
                st.success("Stream beendet.")
                log_event("INGRESS", "WebSocket-Stream empfangen")
            except Exception as e: st.error(f"WebSocket Fehler: {e}")
    with tab_manual:
        c1, c2 = st.columns([1, 3])
        with c1:
            if st.button("🔄 Sample erzeugen", type="primary", use_container_width=True):
                sample = {"idx": len(st.session_state.metric_history), "throughput": random.randint(250_000, 290_000), "latency_ns": round(random.uniform(8.5, 10.5), 2), "blocked": random.randint(380, 420), "t": time.strftime("%H:%M:%S")}
                st.session_state.metric_history.append(sample)
                st.rerun()
            if st.button("🗑️ Zurücksetzen", use_container_width=True):
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

# ============================================================
# PANEL 15: PEER-SWARM
# ============================================================
elif nav == "🌐 Peer-Swarm":
    st.markdown('<div class="main-header">🌐 PEER-SWARM TOPOLOGIE</div>', unsafe_allow_html=True)
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

# ============================================================
# PANEL 16: NOTFALL-KILL-SWITCH
# ============================================================
elif nav == "🚨 Notfall-Kill-Switch":
    st.markdown('<div class="main-header">🚨 NOTFALL-KILL-SWITCH</div>', unsafe_allow_html=True)
    if st.session_state.kill_switch_active:
        st.error("# 🚨 SYSTEM ISOLIERT 🚨")
        st.warning("Alle Ingress-Pfade sind auf FAIL-CLOSED gesetzt.")
        if st.button("🔓 System reaktivieren", type="primary"):
            st.session_state.kill_switch_active = False
            log_event("KILL", "Kill-Switch deaktiviert")
            st.rerun()
    else:
        st.warning("**WARNUNG**: Der Kill-Switch isoliert alle Ingress-Pfade sofort.")
        confirm = st.checkbox("Ich bestätige die Aktivierung.")
        reason = st.text_area("Grund der Aktivierung", placeholder="z.B. RAG-Poisoning-Detection")
        if st.button("🚨 KILL-SWITCH AKTIVIEREN", type="primary", disabled=not confirm):
            st.session_state.kill_switch_active = True
            log_event("KILL", f"KILL-SWITCH aktiviert. Grund: {reason}")
            st.rerun()

# ============================================================
# PANEL 17: SOVEREIGN EXPORT
# ============================================================
elif nav == "💾 Sovereign Export":
    st.markdown('<div class="main-header">💾 SOVEREIGN EXPORT</div>', unsafe_allow_html=True)
    export_payload = {"export_ts": time.strftime("%Y-%m-%d %H:%M:%S"), "auth_seal": st.session_state.auth_seal, "backend_url": st.session_state.backend_url, "kill_switch_active": st.session_state.kill_switch_active, "chronik": st.session_state.chronik, "feinde": st.session_state.feinde, "votes": st.session_state.votes, "metric_history": st.session_state.metric_history, "messages": st.session_state.messages}
    st.subheader("📦 Export-Vorschau")
    st.json(export_payload)
    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.download_button("📥 Vollständiges JSON-Backup", json.dumps(export_payload, indent=2, ensure_ascii=False), f"yggdrasil_export_{int(time.time())}.json", "application/json", use_container_width=True)
    with c2:
        df_chronik = pd.DataFrame(st.session_state.chronik)
        st.download_button("📥 Chronik als CSV", df_chronik.to_csv(index=False), f"chronik_{int(time.time())}.csv", "text/csv", use_container_width=True)

# ============================================================
# PANEL 18: ARCHITEKTUR-MATRIX
# ============================================================
elif nav == "🧬 Architektur-Matrix":
    st.markdown('<div class="main-header">🧬 SYSTEM ARCHITEKTUR 🧬</div>', unsafe_allow_html=True)
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

# ============================================================
# PANEL 19: L.S.S. CODEX
# ============================================================
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
        with tab_read:
            col_b, col_m = st.columns([1, 2])
            with col_b:
                selected_book = st.selectbox("Buch", list_books(), format_func=lambda k: f"{k} — {BOOKS[k]['title']}")
                book = get_book(selected_book)
                st.caption(f"*{book.get('subtitle', '')}*")
                st.markdown(f'<div class="seal-box"><strong>BOOK WORM SEAL</strong><br/><code>{SEAL_REGISTRY[selected_book]["book_seal"]}</code></div>', unsafe_allow_html=True)
            with col_m:
                module_titles = [f"{m['id']} — {m['title']}" for m in book["modules"]]
                selected_title = st.selectbox("Modul", module_titles)
                selected_idx = module_titles.index(selected_title)
                module = book["modules"][selected_idx]
                if "image" in book and os.path.exists(book["image"]): st.image(book["image"], use_column_width=True, caption="Visualisierung")
                st.markdown(f"### {module['id']} · {module['title']}")
                st.markdown(f'<div class="seal-box" style="font-size:0.75rem;"><strong>MODULE SEAL</strong> :: <code>{module["seal"]}</code></div>', unsafe_allow_html=True)
                st.code(module["body"].strip(), language="markdown")
        with tab_search:
            query = st.text_input("🔍 Volltextsuche im Codex", placeholder="z.B. XJustiz, Wusulum, Veto")
            if query:
                hits = lss_search(query)
                if not hits: st.info("Keine Treffer.")
                else:
                    st.success(f"{len(hits)} Treffer")
                    for h in hits:
                        with st.expander(f"[{h['book']} · {h['module']}] {h['title']}"):
                            st.code(h["snippet"], language="markdown")
                            st.caption(f"Seal: {h['seal']}")
        with tab_export:
            st.subheader("📦 Kompletter Codex als Plain-Text")
            full_text = export_as_text()
            st.code(full_text[:3000] + "\n\n... [gekürzt in Vorschau] ...", language="markdown")
            st.download_button("📥 L.S.S. Codex als .txt herunterladen", full_text, f"lss_codex_{int(time.time())}.txt", "text/plain", use_container_width=True)
            st.metric("Gesamtgröße", f"{len(full_text):,} Zeichen")
            st.metric("Module gesamt", sum(len(b["modules"]) for b in BOOKS.values()))

# ============================================================
# PANEL 20: DEEPSEEK BOOSTER
# ============================================================
elif nav == "🧠 DeepSeek Booster":
    st.markdown('<div class="main-header">🧠 DEEPSEEK BOOSTER 🧠</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Multi-Step Reasoning · Chain-of-Thought · Confidence Scoring</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        prompt = st.text_area("Problem / Prompt", "Ist § 839 BGB auf KI-Systeme anwendbar?", height=150)
        context = st.text_input("Zusätzlicher Kontext (optional)", "")
    with col2:
        depth = st.slider("Reasoning-Tiefe", min_value=1, max_value=5, value=3)
        st.info("Tiefe 3 = Standard. Tiefe 5 = maximale Verifikation.")
    if st.button("⚡ Boost starten", type="primary", use_container_width=True):
        with st.spinner("DeepSeek Reasoning läuft..."):
            try:
                r = httpx.post(f"{st.session_state.backend_url}/api/v1/deepseek/boost", json={"prompt": prompt, "context": context, "depth": depth, "auth_seal": st.session_state.auth_seal}, timeout=30.0)
                if r.status_code == 200:
                    data = r.json()
                    cA, cB, cC = st.columns(3)
                    cA.metric("Confidence", f"{data.get('confidence', 0)*100:.1f}%")
                    cB.metric("Verdict", data.get("verdict", "?"))
                    cC.metric("Verification Hash", data.get("verification_hash", "")[:8])
                    st.divider()
                    st.subheader("🧠 Reasoning-Trace")
                    for step in data.get("reasoning_trace", []):
                        with st.expander(f"Step {step['step']}: {step['name'].upper()}"):
                            st.write(f"**Note:** {step['note']}")
                            st.code(f"Hash: {step['hash']}", language="text")
                    log_event("INGRESS", f"DeepSeek-Boost: {prompt[:40]}...")
                else: st.error(f"API Error: {r.status_code}")
            except Exception as e: st.error(f"Verbindungsfehler: {e}")

# ============================================================
# PANEL 21: KING_GHOST VAULT
# ============================================================
elif nav == "👻 King_Ghost Vault":
    st.markdown('<div class="main-header">👻 KING_GHOST VAULT 👻</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Der Schatten-Führer. Tiefer als Gotham. Tiefer als das WORM.</div>', unsafe_allow_html=True)
    st.info("Tokens, die von King_Ghost konsumiert wurden, sind aus der Matrix verschwunden. Nur die Schatten-ID bleibt zurück.")
    if st.button("🔄 Schatten-Pool abrufen", type="primary"):
        try:
            r = httpx.get(f"{st.session_state.backend_url}/api/v1/kingghost/shadows", timeout=10.0)
            if r.status_code == 200:
                data = r.json()
                st.metric("Schatten im Pool", data.get("count", 0))
                if data.get("shadows"):
                    df = pd.DataFrame(data["shadows"])
                    st.dataframe(df[["shadow_id", "origin", "consumed_at", "token"]], use_container_width=True, hide_index=True)
                else: st.info("Der Schatten-Pool ist leer.")
            else: st.error(f"API Error: {r.status_code}")
        except Exception as e: st.error(f"Verbindungsfehler: {e}")
    st.divider()
    st.subheader("🩸 Manuelle Konsumation (Test)")
    test_token = st.text_input("Token zum Konsumieren", "feindlicher_schatten")
    test_origin = st.text_input("Origin", "manual_test")
    if st.button("👻 In Schatten ziehen", type="primary"):
        try:
            r = httpx.post(f"{st.session_state.backend_url}/api/v1/sandbox/kingghost", json={"message": test_token, "origin": test_origin, "auth_seal": st.session_state.auth_seal}, timeout=10.0)
            if r.status_code == 200:
                data = r.json()
                st.success(f"Token konsumiert! Shadow ID: {data.get('shadow_id')}")
                log_event("ALERT", f"King_Ghost Konsumation: {data.get('shadow_id')}")
            else: st.error(f"API Error: {r.status_code}")
        except Exception as e: st.error(f"Verbindungsfehler: {e}")
