import streamlit as st
import os
import json
import time
import hashlib
import pandas as pd
import random
import httpx
import streamlit.components.v1 as components
import io
import csv

# ============================================================
# 1. PAGE CONFIG + CSS
# ============================================================
st.set_page_config(
    page_title="YGGDRASIL_OS :: Sovereign Cockpit v3",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background-color: #0a0a12; color: #d0d0e0; }
    .main-header { font-size: 2.2rem; color: #ffd700; text-align: center; font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.3); margin-bottom: 0px; }
    .sub-header { font-size: 1.0rem; color: #00e5ff; text-align: center; margin-bottom: 20px; }
    .metric-card { background: #141424; border: 1px solid #d4af37; padding: 15px;
        border-radius: 8px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .metric-value { font-size: 1.8rem; font-weight: bold; color: #00e5ff; }
    .metric-label { font-size: 0.85rem; color: #8080a0; }
    .seal-box { background-color: #18182c; border: 1px solid #00e5ff; padding: 12px;
        border-radius: 6px; font-family: monospace; font-size: 0.85rem; color: #00e5ff; margin-top: 15px; }
    .verdict-box { background-color: #2a0000; border: 2px solid #ff0000; padding: 20px;
        border-radius: 8px; text-align: center; color: #fff; font-weight: bold; margin-top: 20px;}
    .chronicle { background: #000; border-left: 3px solid #00ff00; padding: 8px 12px;
        margin: 3px 0; font-family: monospace; font-size: 0.85rem; border-radius: 3px; }
    .chronicle-ALERT { border-left-color: #ff0000; color: #ff8888; }
    .chronicle-EXEC  { border-left-color: #ffd700; color: #ffe066; }
    .chronicle-INGRESS { border-left-color: #00e5ff; color: #80f0ff; }
    .chronicle-WORM  { border-left-color: #00ff00; color: #88ff88; }
    .chronicle-KILL  { border-left-color: #ff00ff; color: #ff88ff; background: #1a001a; }
    .doc-output { background: #0d0d1a; border: 1px solid #d4af37; padding: 20px;
        border-radius: 6px; font-family: 'Times New Roman', serif; font-size: 0.95rem;
        white-space: pre-wrap; line-height: 1.6; }
    .health-ok  { color: #00ff88; font-weight: bold; }
    .health-bad { color: #ff4444; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. SESSION STATE
# ============================================================
if "auth_seal" not in st.session_state:
    st.session_state.auth_seal = os.getenv(
        "YGGDRASIL_SEAL", "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC"
    )
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chronik" not in st.session_state:
    st.session_state.chronik = [
        {"ts": time.strftime("%H:%M:%S"), "kind": "EXEC",
         "msg": "KERNEL_INIT :: YGGDRASIL_OS v3 online"}
    ]
if "feinde" not in st.session_state:
    st.session_state.feinde = [
        {"ID": "F-001", "Name": "Amtsträger X", "Grund": "Amtsmissbrauch § 339 StGB", "Status": "ISOLATED"},
        {"ID": "F-002", "Name": "König der Lüge", "Grund": "Hochverrat a.D.", "Status": "BLACKLISTED"},
        {"ID": "F-003", "Name": "Grummel-Payload", "Grund": "RAG-Poisoning", "Status": "QUARANTINED"},
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
        "https://aragon-backend-api.onrender.com",
    )

# ============================================================
# 3. HELPERS
# ============================================================
def log_event(kind: str, msg: str):
    """Schreibt ein Ereignis in die WORM-Chronik."""
    st.session_state.chronik.append({
        "ts": time.strftime("%H:%M:%S"), "kind": kind, "msg": msg,
    })


def render_mermaid(code: str, height: int = 600):
    """Rendert einen Mermaid-Graphen."""
    html_code = f'''
    <div class="mermaid" style="background-color: #0a0a12; text-align: center;">{code}</div>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({{ startOnLoad: true, theme: "dark" }});
    </script>
    '''
    components.html(html_code, height=height, scrolling=True)


def check_backend():
    """Pingt den Backend-Health-Endpoint."""
    try:
        r = httpx.get(f"{st.session_state.backend_url}/health", timeout=5.0)
        if r.status_code == 200:
            return True, r.json()
        return False, {"detail": f"HTTP {r.status_code}"}
    except Exception as e:
        return False, {"detail": str(e)}

# ============================================================
# 4. SIDEBAR NAVIGATION
# ============================================================
st.sidebar.title("YGGDRASIL_OS v3")
st.sidebar.markdown("**Authority**: Sovereign Root Thomas")
st.sidebar.markdown("**Kernel**: Schwarzer Punkt")
st.sidebar.divider()

# Backend-Health
_ok, _health = check_backend()
if _ok:
    st.sidebar.markdown(
        f'<span class="health-ok">● BACKEND ONLINE</span> · {_health.get("entities_loaded", 0)} Entities',
        unsafe_allow_html=True,
    )
else:
    st.sidebar.markdown(
        f'<span class="health-bad">● BACKEND OFFLINE</span>',
        unsafe_allow_html=True,
    )
    with st.sidebar.expander("Fehlerdetails"):
        st.json(_health)

st.sidebar.divider()

if st.session_state.kill_switch_active:
    st.sidebar.error("🚨 KILL-SWITCH AKTIV — SYSTEM ISOLIERT")

nav = st.sidebar.radio("NAVIGATION", [
    "🏛️ 4x4 Council Grid",
    "⚫️ Schwarze Liga",
    "💀 Der schwarze Richter",
    "⚖️ Normen-Engine",
    "⚡ API Live Interface",
    "📚 201+ Entitäten Explorer",
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
    "🧬 Architektur-Matrix",
])

st.sidebar.divider()
st.sidebar.caption(f"Chronik: {len(st.session_state.chronik)} Einträge")
st.sidebar.caption(f"Feindregister: {len(st.session_state.feinde)} Ziele")
st.sidebar.caption(f"Metriken: {len(st.session_state.metric_history)} Samples")

# ============================================================
# PANEL 1: 4x4 COUNCIL GRID
# ============================================================
if nav == "🏛️ 4x4 Council Grid":
    st.markdown('<div class="main-header">⚫ 4x4 COUNCIL GRID ⚫</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown('<div class="metric-card"><div class="metric-label">OPERATOR</div><div class="metric-value">Thomas</div></div>', unsafe_allow_html=True)
    col2.markdown('<div class="metric-card"><div class="metric-label">KERNEL</div><div class="metric-value">B6/B7</div></div>', unsafe_allow_html=True)
    col3.markdown('<div class="metric-card"><div class="metric-label">MATRIX</div><div class="metric-value">Black Six</div></div>', unsafe_allow_html=True)
    col4.markdown('<div class="metric-card"><div class="metric-label">RUNTIME</div><div class="metric-value">Council</div></div>', unsafe_allow_html=True)
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
    c1, c2, c3 = st.columns(3)
    c1.metric("Entitäten", "201", "100% SEALED")
    c2.metric("Aktive Ringe", "8", "Ring 0 bis Ω")
    c3.metric("Master Seal", "LOCKED", "Ex Tunc")
    st.info(
        "**Gesetz I**: Die Matrix ist souverän.\n\n"
        "**Gesetz II**: Jede Entität ist einem Ring unterworfen.\n\n"
        "**Gesetz III**: Jede Aktion wird im WORM-Ledger verewigt.\n\n"
        "**Gesetz IV**: Der Operator ist die höchste Instanz."
    )

# ============================================================
# PANEL 3: SCHWARZER RICHTER
# ============================================================
elif nav == "💀 Der schwarze Richter":
    st.markdown('<div class="main-header">💀 GERICHTSHOF DER SCHWARZEN LIGA 💀</div>', unsafe_allow_html=True)
    case_input = st.text_area("Sachverhalt (Causa König / Amtsmissbrauch):",
                              "Amtsträger X verweigert Akteneinsicht gemäß § 29 VwVfG.")
    if st.button("⚖️ URTEIL FÄLLEN (EX TUNC)", type="primary"):
        with st.spinner("Fabrice Interpreter prüft Normen..."):
            time.sleep(1.2)
            st.markdown(
                f'<div class="verdict-box">'
                f'<h2>VERDICT: EX_TUNC_RATIFIED</h2>'
                f'<p><strong>Sachverhalt:</strong> {case_input}</p>'
                f'<p><strong>Zuständiger Richter:</strong> Node 0028</p>'
                f'<p><strong>Geprüfte Normen:</strong> § 839 BGB, § 339 StGB, Art. 19 Abs. 4 GG</p>'
                f'<p><strong>WORM-Hash:</strong> {hashlib.sha3_512(case_input.encode()).hexdigest()[:32]}...</p>'
                f'<p><strong>Status:</strong> 💀 DROP_AND_ISOLATE FÜR BEKLAGTEN 💀</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.success("Urteil im WORM-Ledger versiegelt.")
            log_event("ALERT", f"Urteil gefällt: {case_input[:60]}...")

# ============================================================
# PANEL 4: NORMEN-ENGINE
# ============================================================
elif nav == "⚖️ Normen-Engine":
    st.markdown('<div class="main-header">⚖️ NORMEN-ENGINE & SCHADENSRECHNER</div>', unsafe_allow_html=True)
    tab_norm, tab_calc = st.tabs(["📖 Normen-Register", "💰 Schadensersatz-Rechner"])

    with tab_norm:
        normen = {
            "BGB": {"§ 823": "Schadensersatzpflicht", "§ 826": "Sittenwidrige Schädigung", "§ 839": "Amtspflichtverletzung", "§ 249": "Umfang des Schadensersatzes"},
            "StGB": {"§ 339": "Rechtsbeugung", "§ 340": "Körperverletzung im Amt", "§ 353d": "Verbotene Mitteilungen", "§ 142": "Unerlaubtes Entfernen vom Unfallort"},
            "GG": {"Art. 1": "Menschenwürde", "Art. 3": "Gleichheit", "Art. 19 Abs. 4": "Rechtsweggarantie", "Art. 20 Abs. 3": "Bindung an Gesetz und Recht"},
            "VwVfG": {"§ 28": "Anhörung", "§ 29": "Akteneinsicht", "§ 48": "Rücknahme", "§ 51": "Wiederaufgreifen"},
        }
        col_g, col_p = st.columns(2)
        with col_g:
            gesetz = st.selectbox("Gesetzbuch", list(normen.keys()))
        with col_p:
            paragraph = st.selectbox("Paragraph", list(normen[gesetz].keys()))
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
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Frage an die Matrix (z.B. Was ist Node 0105?)"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Backend wird abgefragt..."):
                    try:
                        api_url = f"{st.session_state.backend_url}/prompt/check"
                        payload = {"prompt": prompt, "auth_seal": st.session_state.auth_seal}
                        response = httpx.post(api_url, json=payload, timeout=30.0)

                        if response.status_code == 200:
                            data = response.json()
                            status = data.get("status", "")

                            # Akzeptiert altes UND neues Format
                            if status in ("200_OK", "200_OK_ALLOW"):
                                ai_ans = (
                                    data.get("data", {}).get("ai_answer")
                                    or data.get("ai_answer")
                                    or "Keine KI-Antwort."
                                )
                                st.markdown(f"**KI-Antwort:**\n{ai_ans}")

                                matched = data.get("data", {}).get("entities_matched") or []
                                if matched:
                                    st.caption(f"🎯 RAG-Match: {', '.join(matched[:8])}")

                                worm = data.get("worm", {})
                                if worm:
                                    st.caption(
                                        f"🔒 WORM Block #{worm.get('block')} · "
                                        f"{str(worm.get('hash', ''))[:16]}…"
                                    )

                                st.session_state.messages.append(
                                    {"role": "assistant", "content": ai_ans}
                                )
                                log_event("INGRESS", "Chat-Prompt beantwortet")
                            else:
                                st.error(f"Fail-Closed! {data.get('detail', 'unbekannt')}")
                        else:
                            st.error(f"API Error: HTTP {response.status_code}")
                    except Exception as e:
                        st.error(f"Verbindungsfehler: {str(e)}")

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
        if search_term:
            df = df[
                df["Name"].str.contains(search_term, case=False)
                | df["ID"].str.contains(search_term)
                | df["Ring"].str.contains(search_term, case=False)
            ]
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
            except Exception as e:
                st.error(f"CSV-Fehler: {e}")

# ============================================================
# PANEL 7: URKUNDEN-FORGE
# ============================================================
elif nav == "📜 Urkunden-Forge":
    st.markdown('<div class="main-header">📜 URKUNDEN-FORGE</div>', unsafe_allow_html=True)
    st.caption("Generiert rechtssichere Schriftstücke mit WORM-Siegel.")
    template = st.selectbox("Vorlage", [
        "Widerspruch gegen Verwaltungsakt", "Klage vor dem Verwaltungsgericht",
        "Strafanzeige § 339 StGB", "Fachaufsichtsbeschwerde", "Antrag auf Akteneinsicht § 29 VwVfG"
    ])
    c1, c2 = st.columns(2)
    with c1:
        absender = st.text_input("Absender", "Thomas, Sovereign Operator (Ring 6)")
        aktenzeichen = st.text_input("Aktenzeichen", "AZ-2025-001")
    with c2:
        empfaenger = st.text_input("Empfänger", "Landratsamt XY, Sachbearbeiter Müller")
        datum = st.date_input("Datum")
    begruendung = st.text_area("Begründung / Sachverhalt", "Der Bescheid vom 01.01.2025 ist rechtswidrig...", height=150)

    if st.button("📜 Urkunde generieren", type="primary"):
        doc = f"""
{absender}
{datum.strftime('%d.%m.%Y')}

An: {empfaenger}
Aktenzeichen: {aktenzeichen}
Betreff: {template}

Sehr geehrte Damen und Herren,
hiermit erhebe ich form- und fristgerecht: {template.upper()}
Begründung: {begruendung}

Rechtsgrundlage: § 839 BGB, Art. 34 GG, § 29 VwVfG, Art. 19 Abs. 4 GG
Mit freundlichen Grüßen
{absender}

--- WORM-Siegel ---
SHA3-512: {hashlib.sha3_512((absender + empfaenger + begruendung).encode()).hexdigest()}
"""
        st.markdown(f'<div class="doc-output">{doc}</div>', unsafe_allow_html=True)
        st.download_button(
            "📥 Urkunde als .txt herunterladen",
            doc,
            file_name=f"urkunde_{aktenzeichen}.txt",
            mime="text/plain",
        )
        log_event("WORM", f"Urkunde generiert: {template} ({aktenzeichen})")

# ============================================================
# PANEL 8: KRYPTO-SCHMIEDE
# ============================================================
elif nav == "🔐 Krypto-Schmiede":
    st.markdown('<div class="main-header">🔐 KRYPTO-SCHMIEDE</div>', unsafe_allow_html=True)
    text = st.text_area("Eingabe", "Sovereign Text — Ex Tunc", height=100)
    algs = st.multiselect(
        "Hash-Algorithmen",
        ["SHA3-512", "SHA-256", "BLAKE2b", "MD5"],
        default=["SHA3-512", "SHA-256"],
    )
    if st.button("🔨 Hashen", type="primary") and text:
        result = {}
        data = text.encode()
        for alg in algs:
            if alg == "SHA3-512": result[alg] = hashlib.sha3_512(data).hexdigest()
            elif alg == "SHA-256": result[alg] = hashlib.sha256(data).hexdigest()
            elif alg == "BLAKE2b": result[alg] = hashlib.blake2b(data).hexdigest()
            elif alg == "MD5": result[alg] = hashlib.md5(data).hexdigest()
        for alg, h in result.items():
            st.code(f"{alg}: {h}", language="text")
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
    st.markdown(
        '<div class="seal-box">'
        '<strong>SEAL STATUS:</strong> Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC_CLEAN<br/>'
        '<strong>INTEGRITY:</strong> VERIFIED<br/>'
        '<strong>MASTER HASH:</strong><br/>'
        '<code>850b2ef003f53db90f704b16e54869fc6ba6265eae13aafde9046fe0e4d99dab</code>'
        '</div>',
        unsafe_allow_html=True,
    )
    # Backend-Ledger live abrufen
    try:
        r = httpx.get(f"{st.session_state.backend_url}/stats", timeout=5.0)
        if r.status_code == 200:
            st.json(r.json())
    except Exception:
        st.caption("Backend-Stats nicht erreichbar.")

# ============================================================
# PANEL 11: WORM-CHRONIK
# ============================================================
elif nav == "📅 WORM-Chronik":
    st.markdown('<div class="main-header">📅 WORM-CHRONIK</div>', unsafe_allow_html=True)
    filter_kind = st.multiselect(
        "Filter nach Ereignistyp",
        ["EXEC", "INGRESS", "WORM", "ALERT", "KILL"],
        default=["EXEC", "INGRESS", "WORM", "ALERT", "KILL"],
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
    )

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
        st.session_state.feinde.append({
            "ID": new_id, "Name": new_name, "Grund": new_grund, "Status": new_status,
        })
        log_event("ALERT", f"Feind registriert: {new_name} ({new_id})")
        st.rerun()

# ============================================================
# PANEL 13: COUNCIL-VOTING
# ============================================================
elif nav == "🗳️ Council-Voting":
    st.markdown('<div class="main-header">🗳️ COUNCIL-VOTING</div>', unsafe_allow_html=True)
    st.subheader("➕ Neuen Antrag einbringen")
    cA, cB = st.columns([3, 1])
    with cA:
        new_proposal = st.text_input("Antrag", placeholder="z.B. Buch 100 als Singularität ratifizieren")
    with cB:
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("Einbringen", use_container_width=True) and new_proposal:
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

# ============================================================
# PANEL 14: LIVE-METRIKEN
# ============================================================
elif nav == "📊 Live-Metriken":
    st.markdown('<div class="main-header">📊 LIVE SYSTEM-METRIKEN</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("🔄 Sample erzeugen", type="primary", use_container_width=True):
            sample = {
                "idx": len(st.session_state.metric_history),
                "throughput": random.randint(250_000, 290_000),
                "latency_ns": round(random.uniform(8.5, 10.5), 2),
                "blocked": random.randint(380, 420),
                "t": time.strftime("%H:%M:%S"),
            }
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
    style S fill:#ffd700,color:#000
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
        )
    with c2:
        df_chronik = pd.DataFrame(st.session_state.chronik)
        st.download_button(
            "📥 Chronik als CSV",
            df_chronik.to_csv(index=False),
            f"chronik_{int(time.time())}.csv",
            "text/csv",
            use_container_width=True,
        )

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
    style APEX fill:#ffd700,color:#000
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
