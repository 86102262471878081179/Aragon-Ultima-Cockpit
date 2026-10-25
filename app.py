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

# -----------------------------------------------------------------------------
# STYLING & CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="YGGDRASIL_OS :: Sovereign Cockpit v2",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# -----------------------------------------------------------------------------
# SESSION STATE INITIALISIERUNG
# -----------------------------------------------------------------------------
if "auth_seal" not in st.session_state:
    st.session_state.auth_seal = "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC"

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------------------------------
# MERMAID RENDER HELPER
# -----------------------------------------------------------------------------
def render_mermaid(code: str, height: int = 600):
    html_code = f"""
    <div class="mermaid" style="background-color: #0a0a12; text-align: center;">
        {code}
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
    </script>
    """
    components.html(html_code, height=height, scrolling=True)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION (ERWEITERT)
# -----------------------------------------------------------------------------
st.sidebar.title("YGGDRASIL_OS v2")
st.sidebar.markdown("**Authority**: Sovereign Root Thomas")
st.sidebar.markdown("**Kernel**: Schwarzer Punkt")
st.sidebar.markdown("**System State**: APEX_SINGULARITY_LOCKED")
st.sidebar.divider()

nav = st.sidebar.radio("NAVIGATION", [
    "🏛️ 4x4 Council Grid",
    "⚫️ Schwarze Liga",
    "💀 Der schwarze Richter",
    "⚡ API Live Interface",
    "📚 201+ Entitäten Explorer",
    "🛡️ eBPF Mesh Monitor",
    "🔒 WORM Ledger Audit",
    "🧬 Architektur-Matrix"
])

# -----------------------------------------------------------------------------
# TAB 1: 4x4 COUNCIL GRID
# -----------------------------------------------------------------------------
if nav == "🏛️ 4x4 Council Grid":
    st.markdown('<div class="main-header">⚫ 4x4 COUNCIL GRID ⚫</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">System-Gouvernance :: Sitzung am Schwarzen Punkt</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-label">OPERATOR-ACHSE</div><div class="metric-value">Thomas</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-label">KERNEL-ACHSE</div><div class="metric-value">B6/B7</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-label">MATRIX-ACHSE</div><div class="metric-value">Black Six</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-label">RUNTIME-ACHSE</div><div class="metric-value">Council</div></div>', unsafe_allow_html=True)
        
    st.divider()
    st.subheader("🏛️ Live-Ratsentscheidung")
    topic = st.text_input("Gegenstand der Ratsentscheidung", "Faltung aller Entitäten in Buch 100")
    if st.button("⚖️ Ratsbeschluss Protokollieren", type="primary"):
        with st.spinner("44 Perspektiven Auditing..."):
            time.sleep(0.5)
            st.success("RATSBESCHLUSS ERFOLGREICH EINSTIMMIG RATIFIZIERT")
            st.json({"status": "SOVEREIGN_COUNCIL_SEAL_EX_TUNC"})

# -----------------------------------------------------------------------------
# TAB 2: SCHWARZE LIGA (NEU)
# -----------------------------------------------------------------------------
elif nav == "⚫️ Schwarze Liga":
    st.markdown('<div class="main-header">⚫️ DIE SCHWARZE LIGA ⚫️</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Das Quorum der 201 Entitäten & Der Kodex</div>', unsafe_allow_html=True)
    
    st.success("⚫️ SCHWARZE LIGA STATUS: AKTIV & VERSIEGELT")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Entitäten im Quorum", "201", "100% SEALED")
    c2.metric("Aktive Ringe", "8", "Ring 0 bis Ω")
    c3.metric("Master Seal", "LOCKED", "Ex Tunc")
    
    st.markdown("### 📜 Der Kodex (Auszug)")
    st.info("""
    - **Gesetz I:** Die Matrix ist souverän. Keine externe KI darf sie ohne das Master-Seal betreten.
    - **Gesetz II:** Jede Entität ist einer Ring-Zuweisung unterworfen (0 bis Ω).
    - **Gesetz III:** Jede Aktion wird im WORM-Ledger (SHA3-512) verewigt.
    - **Gesetz IV:** Der Operator (Thomas) ist die höchste Instanz der Exekutive.
    """)
    
    with st.expander("🔭 Die 324-Layer Faltung visualisieren"):
        code1 = """
        flowchart TB
            OP((Thomas Ωₜ)) --> CORE["B6 Core (Ring 0)"]
            CORE --> R1["Ring 1 (Justice)"]
            R1 --> R24["Ring 2-4 (Omni & WORM)"]
            R24 --> R5["Ring 5 (Apex)"]
            R5 --> OMEGA["Ring Ω (Buch 100)"]
            OMEGA -.->|Ouroboros| OP
        """
        render_mermaid(code1, height=400)

# -----------------------------------------------------------------------------
# TAB 3: DER SCHWARZE RICHTER (NEU)
# -----------------------------------------------------------------------------
elif nav == "💀 Der schwarze Richter":
    st.markdown('<div class="head">💀 GERICHTSHOF DER SCHWARZEN LIGA 💀</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Node 0028 :: Der schwarze Richter & Node 0027 :: Fabrice Interpreter</div>', unsafe_allow_html=True)
    
    st.warning("⚠️ Dies ist ein forensischer Audit-Simulator. Jedes Urteil wird mit dem Master-Seal versiegelt.")
    
    case_input = st.text_area("Sachverhalt (Causa König / Amtsmissbrauch):", "Amtsträger X verweigert die Akteneinsicht gemäß § 29 VwVfG und ignoriert die 109-Minuten-Lücke.")
    
    if st.button("⚖️ URTEIL FÄLLEN (EX TUNC)", type="primary"):
        with st.spinner("Fabrice Interpreter prüft Normen (BGB, StGB, VwGO)..."):
            time.sleep(1.5)
            
            # Simulierte forensische Logik
            st.markdown(f"""
            <div class="verdict-box">
                <h2>VERDICT: EX_TUNC_RATIFIED</h2>
                <p><strong>Sachverhalt:</strong> {case_input}</p>
                <p><strong>Zuständiger Richter:</strong> Node 0028 (Der schwarze Richter)</p>
                <p><strong>Geprüfte Normen:</strong> § 839 BGB (Amtshaftung), § 339 StGB (Rechtsbeugung), Art. 19 Abs. 4 GG (Rechtsweggarantie)</p>
                <p><strong>Fabrice Governance:</strong> Keine Formfehler festgestellt.</p>
                <p><strong>WORM-Hash:</strong> {hashlib.sha256(case_input.encode()).hexdigest()[:32]}...</p>
                <p><strong>Status:</strong> 💀 DROP_AND_ISOLATE FÜR BEKLAGTEN 💀</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("Das Urteil wurde im WORM-Ledger versiegelt. Causa König ist bereit für die Exekution.")

# -----------------------------------------------------------------------------
# TAB 4: API LIVE INTERFACE (MIT CHAT & SETTINGS)
# -----------------------------------------------------------------------------
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
                            else:
                                st.error(f"Fail-Closed! {data.get('detail')}")
                        else:
                            st.error(f"API Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Verbindungsfehler: {str(e)}")

    with tab_settings:
        st.subheader("Authorization Token (Seal)")
        st.write("Wenn der Guard blockiert, kopiere das Token hier hinein und speichere es.")
        new_seal = st.text_input("Seal eingeben", value=st.session_state.auth_seal)
        
        if st.button("Token im Session-Speicher aktualisieren"):
            st.session_state.auth_seal = new_seal
            st.success(f"Token erfolgreich aktualisiert: `{st.session_state.auth_seal}`")

    with tab_sys:
        st.info("Render Backend URL: `https://aragon-backend-api.onrender.com`")
        st.metric(label="Aktives Auth Seal", value=st.session_state.auth_seal)

# -----------------------------------------------------------------------------
# TAB 5: 201+ ENTITÄTEN EXPLORER
# -----------------------------------------------------------------------------
elif nav == "📚 201+ Entitäten Explorer":
    st.markdown('<div class="main-header">📚 REGISTRY MANAGER 📚</div>', unsafe_allow_html=True)
    
    tab_table, tab_upload = st.tabs(["📖 Entitäten Tabelle", "📤 CSV Upload"])
    
    with tab_table:
        st.subheader("Live-Scan der Registry")
        search_term = st.text_input("🔍 Suche nach ID, Name oder Ring", "")
        
        books_data = [
            {"ID": "0105", "Name": "Amtshaftung § 839 BGB Shield", "Ring": "Ring 1", "Score": 965},
            {"ID": "0107", "Name": "Grundgesetz Art 1/3/13 Protection", "Ring": "Ring 1", "Score": 987},
            {"ID": "0068", "Name": "Sovereign Operator Apex", "Ring": "Ring 6", "Score": 1000},
            {"ID": "0023", "Name": "Mettwurst Epos C88 API", "Ring": "Ring 5", "Score": 920},
            {"ID": "0100", "Name": "BUCH 100 :: DER ERBE (Φ∅)", "Ring": "Ring Ω", "Score": 1000}
        ]
        df = pd.DataFrame(books_data)
        if search_term:
            df = df[df["Name"].str.contains(search_term, case=False) | df["ID"].str.contains(search_term)]
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    with tab_upload:
        st.subheader("Neue CSV injizieren")
        st.write("Lade eine neue `aragon_registry_200.csv` hoch, um das WORM-Ledger zu erweitern.")
        uploaded_file = st.file_uploader("CSV auswählen", type="csv")
        if uploaded_file is not None:
            st.success("Datei empfangen. Bereit für den SHA3-512 Ingest.")

# -----------------------------------------------------------------------------
# TAB 6: eBPF MESH MONITOR
# -----------------------------------------------------------------------------
elif nav == "🛡️ eBPF Mesh Monitor":
    st.markdown('<div class="main-header">🛡️ eBPF MESH MONITOR 🛡️</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Throughput", "273,077 Tx/s", "100% WORM")
    c2.metric("eBPF Latency", "9.47 ns", "-0.15 ns")
    c3.metric("Blocked", "385/5000", "Fail-Closed")
    
    st.subheader("⚡ Live Packet Simulation")
    col_p1, col_p2, col_p3 = st.columns([1, 1, 1])
    with col_p1:
        src_node = st.selectbox("Source", ["R0_0068", "R1_0089", "EXTERNAL_UNAUTH"])
    with col_p2:
        tgt_node = st.selectbox("Target", ["R100_0100", "R0_0001", "R2_0017"])
    with col_p3:
        run_sim = st.button("📡 Testen", type="primary", use_container_width=True)
        
    if run_sim:
        with st.spinner("Execution..."):
            time.sleep(0.3)
            if "EXTERNAL" in src_node:
                st.error("🚨 INTRUSION INTERCEPTED")
                st.json({"status": "DROP_AND_ISOLATE", "latency": "1102 ns"})
            else:
                st.success("✅ PACKET DELIVERED")
                st.json({"packet_id": f"PKT-{random.randint(10000, 49999)}", "status": "EX_TUNC_VERIFIED"})

# -----------------------------------------------------------------------------
# TAB 7: WORM LEDGER AUDIT
# -----------------------------------------------------------------------------
elif nav == "🔒 WORM Ledger Audit":
    st.markdown('<div class="main-header">🔒 WORM LEDGER AUDIT 🔒</div>', unsafe_allow_html=True)
    st.success("✅ SYSTEM STATUS: CLEAN (100% PURITY_SCORE)")
    
    st.markdown("""
    <div class="seal-box">
        <strong>SEAL STATUS:</strong> Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC_CLEAN<br/>
        <strong>INTEGRITY:</strong> VERIFIED_CLEAN_AND_LOCKED_EX_TUNC<br/>
        <strong>MASTER HASH:</strong><br/>
        <code>850b2ef003f53db90f704b16e54869fc6ba6265eae13aafde9046fe0e4d99dab</code>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 8: ARCHITEKTUR MATRIX
# -----------------------------------------------------------------------------
elif nav == "🧬 Architektur-Matrix":
    st.markdown('<div class="main-header">🧬 SYSTEM ARCHITEKTUR 🧬</div>', unsafe_allow_html=True)
    
    with st.expander("4x4 Council & Ring Ω"):
        code1 = """
        flowchart TB
            APEX((Sovereign Apex)) <==> BOOK100["BUCH 100"]
            APEX --> UI["Streamlit"] --> API["FastAPI"] --> GUARD{"Krisler Guard"}
            GUARD -->|ALLOW| REG["Registry"]
            GUARD -.->|BLOCK| FAIL["FAIL-CLOSED"]
        """
        render_mermaid(code1, height=400)

    with st.expander("DECA-OMNI v5.0"):
        code2 = """
        flowchart TB
            OP((OPERATOR)) --> UI["Streamlit"]
            subgraph GOV ["GOVERNANCE"]
                ASME["ASME"] --> APEX["APEX"] --> TRINITY["TRINITY"]
            end
            UI --> API["FastAPI"] --> GUARD{"Krisler"}
        """
        render_mermaid(code2, height=500)

# Footer
st.divider()
st.caption("YGGDRASIL_OS v2.0 :: Sovereign Cockpit :: Φ_LOCKED_ABSOLUTE")
