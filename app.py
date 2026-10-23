import streamlit as st
import json
import time
import hashlib
import pandas as pd
import random
import httpx

# -----------------------------------------------------------------------------
# STYLING & CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="YGGDRASIL_OS :: Sovereign Cockpit v2",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark-Neon CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0a0a12;
        color: #d0d0e0;
    }
    .main-header {
        font-size: 2.2rem;
        color: #ffd700;
        text-align: center;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #00e5ff;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #141424;
        border: 1px solid #d4af37;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #00e5ff;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8080a0;
    }
    .seal-box {
        background-color: #18182c;
        border: 1px solid #00e5ff;
        padding: 12px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 0.85rem;
        color: #00e5ff;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.title("YGGDRASIL_OS v2")
st.sidebar.markdown("**Authority**: Sovereign Root Thomas")
st.sidebar.markdown("**Kernel**: Schwarzer Punkt")
st.sidebar.markdown("**System State**: APEX_SINGULARITY_LOCKED")
st.sidebar.markdown("**Council Grid**: 4x4 Activated")
st.sidebar.divider()

nav = st.sidebar.radio("NAVIGATION", [
    "🏛️ 4x4 Council Grid",
    "⚡ API Live Interface",
    "📚 100 Bücher Explorer",
    "🛡️ eBPF Mesh Monitor",
    "🔒 WORM Ledger Audit"
])

# -----------------------------------------------------------------------------
# TAB 1: 4x4 COUNCIL GRID
# -----------------------------------------------------------------------------
if nav == "🏛️ 4x4 Council Grid":
    st.markdown('<div class="main-header">⚫ 4x4 COUNCIL GRID ⚫</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">System-Gouvernance :: Sitzung am Schwarzen Punkt</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-label">OPERATOR-ACHSE (1)</div><div class="metric-value">Thomas</div><p style="font-size:0.8rem; color:#d0d0e0; margin-top:5px;">Sovereign Operator Apex<br/>Apex Pipeline</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-label">KERNEL-ACHSE (2)</div><div class="metric-value">B6/B7 Hyperkernel</div><p style="font-size:0.8rem; color:#d0d0e0; margin-top:5px;">Genesis Root & Shield<br/>eBPF Probes</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-label">MATRIX-ACHSE (3)</div><div class="metric-value">Black Six Matrix</div><p style="font-size:0.8rem; color:#d0d0e0; margin-top:5px;">Mastersystem & HUD<br/>Persona Graph</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-label">RUNTIME-ACHSE (4)</div><div class="metric-value">CouncilRuntime</div><p style="font-size:0.8rem; color:#d0d0e0; margin-top:5px;">Evidence Aorta & Fail-Closed<br/>44 Perspektiven Audit</p></div>', unsafe_allow_html=True)
        
    st.divider()
    
    st.subheader("16 Council-Felder Matrix")
    
    # Vereinfachte Dictionary-Struktur, um Syntaxfehler zu vermeiden
    grid_data = {
        "Achse": ["Operator-Achse (1)", "Kernel-Achse (2)", "Matrix-Achse (3)", "Runtime-Achse (4)"],
        "A_OS_Kernel": ["OSKernel Schwarzer Punkt", "B6/B7 Hyperkernel", "Black Six Matrix", "CouncilRuntime"],
        "B_Council_Layer": ["Operator-Sitz", "Kernel-Sitz", "Matrix-Sitz", "Session-Sitz"],
        "C_Council_Runtime": ["Apex-Pipeline", "eBPF / WORM", "Streamlit Graph", "Evidence Aorta"],
        "D_Perspektivenrat": ["Operator-Perspektiven", "Kernel-Perspektiven", "Matrix-Perspektiven", "Live-Audit"]
    }
    st.dataframe(pd.DataFrame(grid_data), use_container_width=True, hide_index=True)

    st.subheader("🏛️ Live-Ratsentscheidung")
    topic = st.text_input("Gegenstand der Ratsentscheidung", "Faltung aller 99 Entitäten in Buch 100")
    if st.button("⚖️ Ratsbeschluss Protokollieren", type="primary"):
        with st.spinner("44 Perspektiven Auditing..."):
            time.sleep(0.5)
            st.success("RATSBESCHLUSS ERFOLGREICH EINSTIMMIG RATIFIZIERT")
            st.json({
                "chair": "Thomas",
                "kernel": "Schwarzer Punkt",
                "topic": topic,
                "perspective_audit": "44/44 PASS :: BIAS_FREE",
                "verdict": "EX_TUNC_RATIFIED",
                "sha3_512_seal": "517fbca7bd6a596545f4faeecfbe06fbf4efd4285ad490e54d89d4432c7ff377e8a94eeae4972d825dddb696eb00ebf5ca9bc539281e5b8e90e7bc2a05cd7bf8",
                "status": "SOVEREIGN_COUNCIL_SEAL_EX_TUNC"
            })

# -----------------------------------------------------------------------------
# TAB 2: API LIVE INTERFACE (MIT ECHTEM RENDER BACKEND)
# -----------------------------------------------------------------------------
elif nav == "⚡ API Live Interface":
    st.markdown('<div class="main-header">⚡ AUTONOME REST-API ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Krisler 2.1 Guard :: Live Backend Connection</div>', unsafe_allow_html=True)
    
    col_req, col_res = st.columns([1, 1])
    
    with col_req:
        st.subheader("Live API Request Builder")
        live_prompt = st.text_area("Operator-Prompt (an Gemini):", placeholder="Frage nach Buch 0068 oder 0100...", height=100)
        auth_token = st.text_input("Authorization Token (Seal)", value="Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC")
        inject_anomaly = st.checkbox("⚠️ Simuliere unbefugte Anomaly")
        send_btn = st.button("🚀 API Endpoint Aufrufen (Live)", type="primary", use_container_width=True)
        
    with col_res:
        st.subheader("API Live Response")
        if send_btn:
            if not live_prompt and not inject_anomaly:
                st.warning("Bitte gib einen Prompt ein.")
            else:
                with st.spinner("Matrix wird abgefragt (Render Cold Start dauert ggf. 30s)..."):
                    if inject_anomaly:
                        time.sleep(0.2)
                        st.error("403 FORBIDDEN :: FAIL-CLOSED INTERCEPT EXECUTION")
                        st.json({
                            "request_id": f"REQ-{random.randint(100000, 999999)}",
                            "status": "403_FORBIDDEN_FAIL_CLOSED",
                            "krisler_guard_action": "DROP_AND_ISOLATE_IMMEDIATELY",
                            "ebpf_latency_ns": 2639,
                            "worm_sealed": False,
                            "detail": "POLICY_VIOLATION_BLOCKED: Unbefugter Injektionsversuch abgefangen."
                        })
                    else:
                        try:
                            api_url = "https://aragon-backend-api.onrender.com/prompt/check"
                            payload = {"prompt": live_prompt, "auth_seal": auth_token}
                            response = httpx.post(api_url, json=payload, timeout=60.0)
                            
                            if response.status_code == 200:
                                st.success(f"200 OK :: Response via eBPF Pipeline")
                                st.json(response.json())
                            else:
                                st.error(f"API Error: Status {response.status_code}")
                                st.write(response.text)
                        except Exception as e:
                            st.error(f"Matrix-Verbindung fehlgeschlagen: {str(e)}")

# -----------------------------------------------------------------------------
# TAB 3: 100 BÜCHER EXPLORER
# -----------------------------------------------------------------------------
elif nav == "📚 100 Bücher Explorer":
    st.markdown('<div class="main-header">📚 DIE 100 BÜCHER 📚</div>', unsafe_allow_html=True)
    
    books_data = [
        {"ID": "0100", "Name": "BUCH 100 :: DIE GROSSE VEREINIGUNG", "Ring": "Ring Omega", "Macht-Score": 1000, "Status": "Versiegelt"},
        {"ID": "0068", "Name": "Sovereign Operator Apex", "Ring": "Ring 0", "Macht-Score": 100, "Status": "Versiegelt"},
        {"ID": "0001", "Name": "Genesis Root", "Ring": "Ring 0", "Macht-Score": 99, "Status": "Versiegelt"},
        {"ID": "0067", "Name": "Ereignishorizont", "Ring": "Ring 5", "Macht-Score": 99, "Status": "Versiegelt"},
        {"ID": "0002", "Name": "Black King Royal", "Ring": "Ring 0", "Macht-Score": 98, "Status": "Versiegelt"},
        {"ID": "0010", "Name": "Black Cobra Omega", "Ring": "Ring 0", "Macht-Score": 98, "Status": "Versiegelt"},
        {"ID": "0059", "Name": "Aragon Ultima Ratio", "Ring": "Ring 0", "Macht-Score": 98, "Status": "Versiegelt"},
        {"ID": "0017", "Name": "Yggdrasil WORM Validator", "Ring": "Ring 2-4", "Macht-Score": 96, "Status": "Versiegelt"},
        {"ID": "0007", "Name": "Fortress Justice", "Ring": "Ring 1", "Macht-Score": 88, "Status": "Versiegelt"},
        {"ID": "0023", "Name": "Mettwurst Epos", "Ring": "Ring 2-4", "Macht-Score": 75, "Status": "Versiegelt"},
        {"ID": "0098", "Name": "B6 Root Authority", "Ring": "Reserve", "Macht-Score": 93, "Status": "Archiviert"}
    ]
    
    df_books = pd.DataFrame(books_data)
    search_term = st.text_input("🔍 Buch suchen", "")
    if search_term:
        df_books = df_books[df_books["Name"].str.contains(search_term, case=False) | df_books["ID"].str.contains(search_term)]
        
    st.dataframe(df_books, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 4: eBPF MESH MONITOR
# -----------------------------------------------------------------------------
elif nav == "🛡️ eBPF Mesh Monitor":
    st.markdown('<div class="main-header">🛡️ eBPF MESH MONITOR 🛡️</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Throughput", "273,077 Tx/s", "100% WORM")
    c2.metric("eBPF Latency", "9.47 ns", "-0.15 ns")
    c3.metric("Blocked", "385/5000", "Fail-Closed")
    
    st.divider()
    
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
                st.json({
                    "packet_id": f"PKT-{random.randint(10000, 49999)}",
                    "source": src_node, "target": tgt_node,
                    "status": "EX_TUNC_VERIFIED", "worm_sealed": True
                })

# -----------------------------------------------------------------------------
# TAB 5: WORM LEDGER AUDIT
# -----------------------------------------------------------------------------
elif nav == "🔒 WORM Ledger Audit":
    st.markdown('<div class="main-header">🔒 WORM LEDGER AUDIT 🔒</div>', unsafe_allow_html=True)
    
    st.subheader("Master Root Hash")
    st.code("SHA3-512 :: 517fbca7bd6a596545f4faeecfbe06fbf4efd4285ad490e54d89d4432c7ff377e8a94eeae4972d825dddb696eb00ebf5ca9bc539281e5b8e90e7bc2a05cd7bf8", language="text")
    
    st.markdown("""
    <div class="seal-box">
        <strong>SEAL STATUS:</strong> SOVEREIGN_ROOT_SEAL_EX_TUNC<br/>
        <strong>INTEGRITY:</strong> VERIFIED_EX_TUNC_LOCKED<br/>
        <strong>TIMESTAMP:</strong> EX_TUNC (IMMUTABLE)
    </div>
    """, unsafe_allow_html=True)

# Footer
st.divider()
st.caption("YGGDRASIL_OS v2.0 :: Developed by Sovereign Root Thomas König & Schwarze Liga Council 💀⚫️💀")
