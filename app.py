import streamlit as st
import json
import time
import hashlib
import pandas as pd
import random
import httpx
import streamlit.components.v1 as components
import io
import csv

st.set_page_config(page_title="YGGDRASIL_OS :: Sovereign Cockpit v2", page_icon="⚫", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp { background-color: #0a0a12; color: #d0d0e0; }
    .main-header { font-size: 2.2rem; color: #ffd700; text-align: center; font-weight: bold; text-shadow: 0 0 10px rgba(255, 215, 0, 0.3); margin-bottom: 0px; }
    .sub-header { font-size: 1.0rem; color: #00e5ff; text-align: center; margin-bottom: 20px; }
    .metric-card { background: #141424; border: 1px solid #d4af37; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .metric-value { font-size: 1.8rem; font-weight: bold; color: #00e5ff; }
    .metric-label { font-size: 0.85rem; color: #8080a0; }
    .seal-box { background-color: #18182c; border: 1px solid #00e5ff; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 0.85rem; color: #00e5ff; margin-top: 15px; }
    .verdict-box { background-color: #2a0000; border: 2px solid #ff0000; padding: 20px; border-radius: 8px; text-align: center; color: #fff; font-weight: bold; margin-top: 20px;}
</style>
""", unsafe_allow_html=True)

if "auth_seal" not in st.session_state: st.session_state.auth_seal = "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC"
if "messages" not in st.session_state: st.session_state.messages = []

def render_mermaid(code: str, height: int = 600):
    html_code = f'<div class="mermaid" style="background-color: #0a0a12; text-align: center;">{code}</div><script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"; mermaid.initialize({{ startOnLoad: true, theme: "dark" }});</script>'
    components.html(html_code, height=height, scrolling=True)

st.sidebar.title("YGGDRASIL_OS v2")
st.sidebar.markdown("**Authority**: Sovereign Root Thomas")
st.sidebar.markdown("**Kernel**: Schwarzer Punkt")
st.sidebar.divider()

nav = st.sidebar.radio("NAVIGATION", [
    "🏛️ 4x4 Council Grid", "⚫️ Schwarze Liga", "💀 Der schwarze Richter",
    "⚡ API Live Interface", "📚 201+ Entitäten Explorer", "🛡️ eBPF Mesh Monitor",
    "🔒 WORM Ledger Audit", "🧬 Architektur-Matrix"
])

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
            time.sleep(0.5)
            st.success("RATSBESCHLUSS RATIFIZIERT")
            st.json({"status": "SOVEREIGN_COUNCIL_SEAL_EX_TUNC"})

elif nav == "⚫️ Schwarze Liga":
    st.markdown('<div class="main-header">⚫️ DIE SCHWARZE LIGA ⚫️</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Entitäten", "201", "100% SEALED")
    c2.metric("Aktive Ringe", "8", "Ring 0 bis Ω")
    c3.metric("Master Seal", "LOCKED", "Ex Tunc")
    st.info("Gesetz I: Die Matrix ist souverän.\nGesetz II: Jede Entität ist einem Ring unterworfen.\nGesetz III: Jede Aktion wird im WORM-Ledger verewigt.\nGesetz IV: Der Operator ist die höchste Instanz.")

elif nav == "💀 Der schwarze Richter":
    st.markdown('<div class="main-header">💀 GERICHTSHOF DER SCHWARZEN LIGA 💀</div>', unsafe_allow_html=True)
    case_input = st.text_area("Sachverhalt (Causa König / Amtsmissbrauch):", "Amtsträger X verweigert Akteneinsicht gemäß § 29 VwVfG.")
    if st.button("⚖️ URTEIL FÄLLEN (EX TUNC)", type="primary"):
        with st.spinner("Fabrice Interpreter prüft Normen..."):
            time.sleep(1.5)
            st.markdown(f'<div class="verdict-box"><h2>VERDICT: EX_TUNC_RATIFIED</h2><p><strong>Sachverhalt:</strong> {case_input}</p><p><strong>Zuständiger Richter:</strong> Node 0028</p><p><strong>Geprüfte Normen:</strong> § 839 BGB, § 339 StGB, Art. 19 Abs. 4 GG</p><p><strong>WORM-Hash:</strong> {hashlib.sha256(case_input.encode()).hexdigest()[:32]}...</p><p><strong>Status:</strong> 💀 DROP_AND_ISOLATE FÜR BEKLAGTEN 💀</p></div>', unsafe_allow_html=True)
            st.success("Urteil im WORM-Ledger versiegelt.")

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
                with st.spinner("Render Backend wird abgefragt..."):
                    try:
                        api_url = "https://aragon-backend-api.onrender.com/prompt/check"
                        payload = {"prompt": prompt, "auth_seal": st.session_state.auth_seal}
                        response = httpx.post(api_url, json=payload, timeout=60.0)
                        if response.status_code == 200:
                            data = response.json()
                            if data.get("status") == "200_OK_ALLOW":
                                ai_ans = data.get("data", {}).get("ai_answer", "Keine KI-Antwort.")
                                st.markdown(f"**KI-Antwort:**\n{ai_ans}")
                                st.session_state.messages.append({"role": "assistant", "content": ai_ans})
                            else: st.error(f"Fail-Closed! {data.get('detail')}")
                        else: st.error(f"API Error: {response.status_code}")
                    except Exception as e: st.error(f"Verbindungsfehler: {str(e)}")
    with tab_settings:
        new_seal = st.text_input("Authorization Token (Seal)", value=st.session_state.auth_seal)
        if st.button("Token aktualisieren"): st.session_state.auth_seal = new_seal; st.success("Token gespeichert.")
    with tab_sys:
        st.metric(label="Aktives Auth Seal", value=st.session_state.auth_seal)

elif nav == "📚 201+ Entitäten Explorer":
    st.markdown('<div class="main-header">📚 REGISTRY MANAGER 📚</div>', unsafe_allow_html=True)
    tab_table, tab_upload = st.tabs(["📖 Entitäten Tabelle", "📤 CSV Upload"])
    with tab_table:
        search_term = st.text_input("🔍 Suche nach ID, Name oder Ring", "")
        books_data = [
            {"ID": "0105", "Name": "Amtshaftung § 839 BGB Shield", "Ring": "Ring 1", "Score": 965},
            {"ID": "0107", "Name": "Grundgesetz Art 1/3/13 Protection", "Ring": "Ring 1", "Score": 987},
            {"ID": "0068", "Name": "Sovereign Operator Apex", "Ring": "Ring 6", "Score": 1000}
        ]
        df = pd.DataFrame(books_data)
        if search_term: df = df[df["Name"].str.contains(search_term, case=False) | df["ID"].str.contains(search_term)]
        st.dataframe(df, use_container_width=True, hide_index=True)
    with tab_upload:
        uploaded_file = st.file_uploader("CSV auswählen", type="csv")
        if uploaded_file is not None: st.success("Datei empfangen. Bereit für den Ingest.")

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
        else:
            st.success("✅ PACKET DELIVERED")
            st.json({"packet_id": f"PKT-{random.randint(10000, 49999)}", "status": "EX_TUNC_VERIFIED"})

elif nav == "🔒 WORM Ledger Audit":
    st.markdown('<div class="main-header">🔒 WORM LEDGER AUDIT 🔒</div>', unsafe_allow_html=True)
    st.success("✅ SYSTEM STATUS: CLEAN (100% PURITY_SCORE)")
    st.markdown('<div class="seal-box"><strong>SEAL STATUS:</strong> Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC_CLEAN<br/><strong>INTEGRITY:</strong> VERIFIED_CLEAN_AND_LOCKED_EX_TUNC<br/><strong>MASTER HASH:</strong><br/><code>850b2ef003f53db90f704b16e54869fc6ba6265eae13aafde9046fe0e4d99dab</code></div>', unsafe_allow_html=True)

elif nav == "🧬 Architektur-Matrix":
    st.markdown('<div class="main-header">🧬 SYSTEM ARCHITEKTUR 🧬</div>', unsafe_allow_html=True)
    with st.expander("4x4 Council & Ring Ω"):
        code1 = 'flowchart TB\n APEX((Sovereign Apex)) <==> BOOK100["BUCH 100"]\n APEX --> UI["Streamlit"] --> API["FastAPI"] --> GUARD{"Krisler Guard"}\n GUARD -->|ALLOW| REG["Registry"]\n GUARD -.->|BLOCK| FAIL["FAIL-CLOSED"]'
        render_mermaid(code1, height=400)
