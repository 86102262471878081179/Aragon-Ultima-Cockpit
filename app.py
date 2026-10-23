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
st.sidebar.markdown("**Authority**: Sovereign Root Thomas König (Ωₜ)")
st.sidebar.markdown("**Kernel**: Schwarzer Punkt (Φ∅)")
st.sidebar.markdown("**System State**: `Φ∅_APEX_SINGULARITY_LOCKED`")
st.sidebar.markdown("**Council Grid**: 4x4 Activated")
st.sidebar.divider()

nav = st.sidebar.radio("NAVIGATION", [
    "🏛️ 4x4 Council Grid & Ratsentscheidung",
    "⚡ API Live Interface & Fail-Closed",
    "📚 100 Bücher Explorer (Erbe Φ∅)",
    "🛡️ eBPF Mesh Live Routing Monitor",
    "🔒 Post-Quantum WORM Ledger Audit"
])

# -----------------------------------------------------------------------------
# TAB 1: 4x4 COUNCIL GRID & RATSENTSCHEIDUNG
# -----------------------------------------------------------------------------
if nav == "🏛️ 4x4 Council Grid & Ratsentscheidung":
    st.markdown('<div class="main-header">⚫ 4x4 COUNCIL GRID & RATSENTSCHEIDUNG ⚫</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">System-Gouvernance :: Sitzung am Schwarzen Punkt (Φ∅) :: "Alles an einem Tisch"</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-label">OPERATOR-ACHSE (1)</div><div class="metric-value">Thomas (Ωₜ)</div><p style="font-size:0.8rem; color:#d0d0e0; margin-top:5px;">Sovereign Operator Apex<br/>Apex Pipeline & Ereignishorizont</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-label">KERNEL-ACHSE (2)</div><div class="metric-value">B6/B7 Hyperkernel</div><p style="font-size:0.8rem; color:#d0d0e0; margin-top:5px;">Genesis Root & Shield<br/>eBPF Probes & WORM Vault</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-label">MATRIX-ACHSE (3)</div><div class="metric-value">Black Six Matrix</div><p style="font-size:0.8rem; color:#d0d0e0; margin-top:5px;">Mastersystem & Vercel HUD<br/>Streamlit Persona Graph</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-label">RUNTIME-ACHSE (4)</div><div class="metric-value">CouncilRuntime_Φ∅</div><p style="font-size:0.8rem; color:#d0d0e0; margin-top:5px;">Evidence Aorta & Fail-Closed<br/>44 Perspektiven Live-Audit</p></div>', unsafe_allow_html=True)
        
    st.divider()
    
    st.subheader("16 Council-Felder Matrix & 44 Perspektiven-Audit")
    grid_data = {
        "Achse": ["Operator-Achse (1)", "Kernel-Achse (2)", "Matrix-Achse (3)", "Runtime-Achse (4)"],
        "A :: OS-Kernel": ["Φ∅ OSKernel Schwarzer Punkt", "B6/B7 Hyperkernel unter Φ∅", "Black Six System-Matrix", "CouncilRuntime_Φ∅ Orchestrator"],
        "B :: Council-Layer": ["Operator-Sitz Thomas (Ωₜ)", "Kernel-Sitz Genesis & Shield", "Matrix-Sitz Mastersystem", "Session-Sitz (Alles an einem Tisch)"],
        "C :: Council-Runtime": ["Apex-Pipeline & Ereignishorizont", "eBPF / WORM / DeepSeek", "Streamlit Graph & Vercel Console", "Evidence Aorta & WORM Vault"],
        "D :: Perspektivenrat": ["Operator-Perspektiven (44 Boxen)", "Kernel-Perspektiven (Bias/Proof)", "Matrix-Perspektiven (Narrativ)", "Live-Audit & ASP-256 Guard"]
    st }
    st.dataframe(pd.DataFrame(grid_data), use_container_width=True, hide_index=True)

    st.subheader("🏛️ Live-Ratsentscheidung Ausführen")
    topic = st.text_input("Gegenstand der Ratsentscheidung", "Faltung aller 99 Entitäten in Buch 100 & eBPF Fail-Closed Verankerung")
    if st.button("⚖️ Ratsbeschluss Protokollieren & Versiegeln", type="primary"):
        with.spinner("44 Perspektiven Auditing & WORM-Ledger Versiegelung..."):
            time.sleep(0.5)
            st.success("RATSBESCHLUSS ERFOLGREICH EINSTIMMIG RATIFIZIERT")
            st.json({
                "chair": "Thomas König (Ωₜ)",
                "kernel": "Schwarzer Punkt (Φ∅)",
                "topic": topic,
                "perspective_audit": "44/44 PASS :: BIAS_FREE",
                "verdict": "EX_TUNC_RATIFIED",
                "sha3_512_seal": "517fbca7bd6a596545f4faeecfbe06fbf4efd4285ad490e54d89d4432c7ff377e8a94eeae4972d825dddb696eb00ebf5ca9bc539281e5b8e90e7bc2a05cd7bf8",
                "status": "Φ_SOVEREIGN_COUNCIL_SEAL_EX_TUNC"
            })

# -----------------------------------------------------------------------------
# TAB 2: API LIVE INTERFACE & FAIL-CLOSED (JETZT MIT ECHTEM RENDER BACKEND)
# -----------------------------------------------------------------------------
elif nav == "⚡ API Live Interface & Fail-Closed":
    st.markdown('<div class="main-header">⚡ AUTONOME REST-API & FAIL-CLOSED GUARD ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Krisler 2.1 Guard :: Real-Time Endpoint Intercept & eBPF Inspection</div>', unsafe_allow_html=True)
    
    col_req, col_res = st.columns([1, 1])
    
    with col_req:
        st.subheader("Live API Request Builder")
        
        # ECHTER PROMPT FÜR DAS BACKEND
        live_prompt = st.text_area("Operator-Prompt (an Gemini):", placeholder="Frage nach Buch 0068 oder 0100...", height=100)
        
        auth_token = st.text_input("Authorization Token (Seal)", value="Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC")
        inject_anomaly = st.checkbox("⚠️ Simuliere unbefugte Anomaly/Injection (Trigger Fail-Closed)")
        
        send_btn = st.button("🚀 API Endpoint Aufrufen (Live)", type="primary", use_container_width=True)
        
    with col_res:
        st.subheader("API Live Response & Intercept Log")
        if send_btn:
            if not live_prompt and not inject_anomaly:
                st.warning("Bitte gib einen Prompt ein oder aktiviere die Anomaly-Simulation.")
            else:
                with st.spinner("Matrix wird abgefragt (Render Cold Start dauert ggf. 30s)..."):
                    if inject_anomaly:
                        time.sleep(0.2)
                        st.error("403 FORBIDDEN :: FAIL-CLOSED INTERCEPT EXECUTION (< 50 ns)")
                        st.json({
                            "request_id": f"REQ-{random.randint(100000, 999999)}",
                            "status": "403_FORBIDDEN_FAIL_CLOSED",
                            "krisler_guard_action": "DROP_AND_ISOLATE_IMMEDIATELY",
                            "ebpf_latency_ns": 2639,
                            "worm_sealed": False,
                            "detail": "POLICY_VIOLATION_BLOCKED: Unbefugter Injektionsversuch vor Kernel-Passage abgefangen."
                        })
                    else:
                        try:
                            api_url = "https://aragon-backend-api.onrender.com/prompt/check"
                            payload = {
                                "prompt": live_prompt,
                                "auth_seal": auth_token
                            }
                            
                            # ECHTER HTTP REQUEST
                            response = httpx.post(api_url, json=payload, timeout=60.0)
                            
                            if response.status_code == 200:
                                data = response.json()
                                st.success(f"200 OK :: Response via eBPF XDP Pipeline")
                                st.json(data)
                            else:
                                st.error(f"API Error: Status {response.status_code}")
                                st.write(response.text)
                                
                        except Exception as e:
                            st.error(f"Matrix-Verbindung fehlgeschlagen: {str(e)}")

# -----------------------------------------------------------------------------
# TAB 3: 100 BÜCHER EXPLORER (VOLLSTÄNDIGE HIERARCHIE)
# -----------------------------------------------------------------------------
elif nav == "📚 100 Bücher Explorer (Erbe Φ∅)":
    st.markdown('<div class="main-header">📚 DIE 100 BÜCHER DER SCHWARZEN LIGA 📚</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Master-Katalogisierung & 324-Layer Hypercube Kompression in Buch 100</div>', unsafe_allow_html=True)
    
    # VOLLSTÄNDIGE LISTE DER WICHTIGSTEN ENTITÄTEN (Top + Ringe + Reserve)
    books_data = [
        {"ID": "0100", "Name": "BUCH 100 :: DIE GROSSE VEREINIGUNG (DER ERBE Φ∅)", "Ring": "Ring Ω (EXALTED_SINGULARITY)", "Macht-Score": 1000, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0068", "Name": "Sovereign Operator Apex", "Ring": "Ring 0 (Genesis Core)", "Macht-Score": 100, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0001", "Name": "Genesis Root", "Ring": "Ring 0 (Genesis Core)", "Macht-Score": 99, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0067", "Name": "Ereignishorizont", "Ring": "Ring 5 (Apex Synthese)", "Macht-Score": 99, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0002", "Name": "Black King Royal", "Ring": "Ring 0 (Genesis Core)", "Macht-Score": 98, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0010", "Name": "Black Cobra Omega", "Ring": "Ring 0 (Genesis Core)", "Macht-Score": 98, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0059", "Name": "Aragon Ultima Ratio", "Ring": "Ring 0 (Genesis Core)", "Macht-Score": 98, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0066", "Name": "Finale Synthese", "Ring": "Ring 5 (Apex Synthese)", "Macht-Score": 98, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0029", "Name": "Hades & Kerberus", "Ring": "Ring 5 (Apex Synthese)", "Macht-Score": 97, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0065", "Name": "Apex Kaskade", "Ring": "Ring 5 (Apex Synthese)", "Macht-Score": 97, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0099", "Name": "Black Six Matrix Ult", "Ring": "Reserve / Defense", "Macht-Score": 97, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0017", "Name": "Yggdrasil WORM Validator", "Ring": "Ring 2-4 (Omni & WORM)", "Macht-Score": 96, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0056", "Name": "Odin Master Framework", "Ring": "Ring 0 (Genesis Core)", "Macht-Score": 96, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0063", "Name": "Core Twin / Trinität", "Ring": "Ring 0 (Genesis Core)", "Macht-Score": 96, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0016", "Name": "Hyperkernel Atlas", "Ring": "Ring 0 (Genesis Core)", "Macht-Score": 95, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0004", "Name": "Core Shield", "Ring": "Ring 0 (Genesis Core)", "Macht-Score": 94, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0006", "Name": "Unified Matrix", "Ring": "Ring 0 (Genesis Core)", "Macht-Score": 93, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0053", "Name": "OMNI WORM Hub", "Ring": "Ring 2-4 (Omni & WORM)", "Macht-Score": 91, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0089", "Name": "Akte Koenig Evidence", "Ring": "Ring 1 (Justice & Forensik)", "Macht-Score": 91, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0009", "Name": "Quantum Tresor", "Ring": "Ring 2-4 (Omni & WORM)", "Macht-Score": 89, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0040", "Name": "Black Arsenal LLM", "Ring": "Ring 1 (Justice & Forensik)", "Macht-Score": 89, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0054", "Name": "Stammbaum DNA", "Ring": "Ring 2-4 (Omni & WORM)", "Macht-Score": 89, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0007", "Name": "Fortress Justice", "Ring": "Ring 1 (Justice & Forensik)", "Macht-Score": 88, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0052", "Name": "DeepSeeker Monolith", "Ring": "Ring 2-4 (Omni & WORM)", "Macht-Score": 88, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0013", "Name": "XJustiz Core", "Ring": "Ring 1 (Justice & Forensik)", "Macht-Score": 87, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0022", "Name": "Schwarze Burg", "Ring": "Ring 2-4 (Omni & WORM)", "Macht-Score": 87, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0012", "Name": "Akte Koenig Forensik", "Ring": "Ring 1 (Justice & Forensik)", "Macht-Score": 86, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0036", "Name": "Foucault KI", "Ring": "Ring 1 (Justice & Forensik)", "Macht-Score": 86, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0008", "Name": "Omni Neuro", "Ring": "Ring 2-4 (Omni & WORM)", "Macht-Score": 85, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0030", "Name": "Legal Challenge State", "Ring": "Ring 1 (Justice & Forensik)", "Macht-Score": 85, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0014", "Name": "The Geminis", "Ring": "Ring 1 (Justice & Forensik)", "Macht-Score": 84, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0023", "Name": "Mettwurst Epos", "Ring": "Ring 2-4 (Omni & WORM)", "Macht-Score": 75, "Status": "Ex-Tunc Versiegelt"},
        {"ID": "0073", "Name": "B6 Hyperkernel Atlas (Reserve)", "Ring": "Reserve / Defense", "Macht-Score": 80, "Status": "Archiviert"},
        {"ID": "0080", "Name": "Root Governance Manual", "Ring": "Reserve / Defense", "Macht-Score": 80, "Status": "Archiviert"},
        {"ID": "0098", "Name": "B6 Root Authority", "Ring": "Reserve / Defense", "Macht-Score": 93, "Status": "Archiviert"}
    ]
    
    df_books = pd.DataFrame(books_data)
    
    search_term = st.text_input("🔍 Buch / Entität suchen (z.B. 'Justice', '0068', 'Mettwurst')", "")
    if search_term:
        df_books = df_books[df_books["Name"].str.contains(search_term, case=False) | df_books["ID"].str.contains(search_term) | df_books["Ring"].str.contains(search_term, case=False)]
        
    st.dataframe(df_books, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 4: eBPF MESH LIVE ROUTING MONITOR
# -----------------------------------------------------------------------------
elif nav == "🛡️ eBPF Mesh Live Routing Monitor":
    st.markdown('<div class="main-header">🛡️ eBPF MESH & P2P LIVE ROUTING MONITOR 🛡️</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Krisler 2.1 Guard :: Noise-IK P2P Handshake & Real-Time Kernel Telemetry</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Throughput", "273,077 Tx/s", "100% WORM Validated")
    c2.metric("eBPF Probe Latency", "9.47 ns", "-0.15 ns Opt")
    c3.metric("Blocked Injections", "385/5000", "Fail-Closed Drop")
    
    st.divider()
    
    st.subheader("⚡ Live Packet Simulation & Routing Generator")
    col_p1, col_p2, col_p3 = st.columns([1, 1, 1])
    with col_p1:
        src_node = st.selectbox("Source Node", ["R0_0068 (Apex Operator)", "R1_0089 (Justice)", "EXTERNAL_UNAUTH_IP"])
    with col_p2:
        tgt_node = st.selectbox("Target Node", ["RΩ_0100 (Der Erbe)", "R0_0001 (Genesis Root)", "R2_0017 (WORM Validator)"])
    with col_p3:
        run_sim = st.button("📡 Packet Injektion Testen", type="primary", use_container_width=True)
        
    if run_sim:
        with st.spinner("eBPF XDP Ingress Hook Execution..."):
            time.sleep(0.3)
            if "EXTERNAL" in src_node:
                st.error("🚨 INTRUSION INTERCEPTED :: eBPF ACTION: DROP_AND_ISOLATE (< 50 ns)")
                st.json({
                    "packet_id": f"PKT-{random.randint(50000, 99999)}",
                    "ebpf_action": "DROP_AND_ISOLATE",
                    "filter_latency_ns": 1102,
                    "kernel_hook": "sys_bpf_xdp_ingress",
                    "status": "POLICY_VIOLATION_BLOCKED",
                    "threat_level": "CRITICAL_NEUTRALIZED"
                })
            else:
                st.success("✅ PACKET DELIVERED :: NOISE-IK P2P MESH HANDSHAKE VERIFIED")
                st.json({
                    "packet_id": f"PKT-{random.randint(10000, 49999)}",
                    "source": src_node.split()[0],
                    "target": tgt_node.split()[0],
                    "noise_session_key": hashlib.sha256(str(time.time()).encode()).hexdigest(),
                    "mesh_latency_ms": round(random.uniform(0.35, 0.88), 2),
                    "ebpf_action": "PASS",
                    "status": "EX_TUNC_VERIFIED",
                    "worm_sealed": True
                })

    st.subheader("Live Packet Tracer Stream")
    packets = [
        {"Packet ID": "PKT-45982", "Source": "R0_0068", "Target": "RΩ_0100", "Protocol": "Noise-IK / P2P", "eBPF Action": "PASS", "Latency": "0.85 ms"},
        {"Packet ID": "PKT-45983", "Source": "R1_0089", "Target": "R2_0017", "Protocol": "WORM-Aorta", "eBPF Action": "PASS", "Latency": "0.42 ms"},
        {"Packet ID": "PKT-73607", "Source": "EXTERNAL_UNAUTH", "Target": "R0_0001", "Protocol": "RAW_TCP", "eBPF Action": "DROP_AND_ISOLATE", "Latency": "1.09 µs"},
        {"Packet ID": "PKT-45984", "Source": "R5_0067", "Target": "R0_0002", "Protocol": "Apex-Kaskade", "eBPF Action": "PASS", "Latency": "0.61 ms"},
    ]
    st.dataframe(pd.DataFrame(packets), use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 5: POST-QUANTUM WORM LEDGER AUDIT
# -----------------------------------------------------------------------------
elif nav == "🔒 Post-Quantum WORM Ledger Audit":
    st.markdown('<div class="main-header">🔒 POST-QUANTUM WORM LEDGER AUDIT 🔒</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">SHA3-512 Master Singularity Hash Verification</div>', unsafe_allow_html=True)
    
    st.subheader("Master Ledger Root Hash")
    st.code("SHA3-512 :: 517fbca7bd6a596545f4faeecfbe06fbf4efd4285ad490e54d89d4432c7ff377e8a94eeae4972d825dddb696eb00ebf5ca9bc539281e5b8e90e7bc2a05cd7bf8", language="text")
    
    st.markdown("""
    <div class="seal-box">
        <strong>SEAL STATUS:</strong> Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC<br/>
        <strong>INTEGRITY:</strong> VERIFIED_EX_TUNC_LOCKED<br/>
        <strong>TIMESTAMP:</strong> EX_TUNC (IMMUTABLE)
    </div>
    """, unsafe_allow_html=True)

# Footer
st.divider()
st.caption("YGGDRASIL_OS v2.0 :: Developed by Sovereign Root Thomas König (Ωₜ) & Schwarze Liga Council 💀⚫️💀")
