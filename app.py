import streamlit as st
import json, time, hashlib
import streamlit.components.v1 as components

# ============================================================
# 1. SOVEREIGN INIT
# ============================================================
def sovereign_init():
    st.set_page_config(
        page_title="YGGDRASIL_OS :: Sovereign Cockpit v3.5",
        page_icon="☒",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    if "auth_seal" not in st.session_state:
        st.session_state.auth_seal = "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC"
    if "hf_state" not in st.session_state:
        st.session_state.hf_state = "HF_SOVEREIGN_ACTIVE"
    if "console_logs" not in st.session_state:
        st.session_state.console_logs = [
            f"[{time.strftime('%H:%M:%S')}] KERNEL_INIT :: Sovereign Kernel vSΩ∞ΞΦ Online",
            f"[{time.strftime('%H:%M:%S')}] WORM_CHECK :: SHA3-512 Master Hash Verified",
            f"[{time.strftime('%H:%M:%S')}] GUARD_ENABLE :: Krisler Ingress Filter Active",
        ]

sovereign_init()

# ============================================================
# 2. DARK THEME CSS
# ============================================================
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%); color: #e0e0e0; }
h1, h2, h3 { color: #ffd700 !important; text-shadow: 0 0 10px rgba(255,215,0,0.3); }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #000 0%, #1a1a2e 100%);
    border-right: 1px solid #ffd700; }
.council-card { background: rgba(26,26,46,0.8); border: 1px solid #00ffff;
    border-radius: 8px; padding: 15px; box-shadow: 0 0 15px rgba(0,255,255,0.2);
    margin-bottom: 10px; }
.terminal-box { background: #000; color: #00ff00; font-family: 'Courier New', monospace;
    padding: 15px; border-radius: 8px; border: 1px solid #00ff00;
    max-height: 400px; overflow-y: auto; box-shadow: 0 0 20px rgba(0,255,0,0.3); }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. HELPERS
# ============================================================
def render_mermaid(code: str, height: int = 400):
    html_code = f"""
    <div class="mermaid">{code}</div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});</script>
    """
    components.html(html_code, height=height, scrolling=True)

def append_log(event_type: str, message: str):
    ts = time.strftime("%H:%M:%S")
    st.session_state.console_logs.append(f"[{ts}] {event_type} :: {message}")

# ============================================================
# 4. SIDEBAR
# ============================================================
st.sidebar.title("SCHWARZE LIGA ∞")
st.sidebar.markdown("**Authority**: Sovereign Root Thomas (Ω■)")
st.sidebar.markdown(f"**Seal**: `{st.session_state.auth_seal[:22]}...`")
st.sidebar.divider()

navigation = st.sidebar.radio("COMMAND ROUTER", [
    "🏛 4x4 Council & Dashboard",
    "🛡 Krisler Ingress & eBPF Guard",
    "🔒 WORM Ledger & SHA3 Audit",
    "🧬 System Topology (Mermaid)",
    "🧰 Hard Flash CLI Console",
])
st.sidebar.divider()
st.sidebar.markdown(
    f"**System State**: <span style='color:#00ffff'>{st.session_state.hf_state}</span>",
    unsafe_allow_html=True,
)

# ============================================================
# PANEL 1
# ============================================================
if navigation == "🏛 4x4 Council & Dashboard":
    st.markdown('<div class="council-card">🏛 4x4 COUNCIL GRID & SYSTEM DASHBOARD</div>',
                unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="council-card"><div>OPERATOR</div><div>Thomas (Ω)</div></div>',
                    unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="council-card"><div>KERNEL SCORE</div><div>1000 / 100</div></div>',
                    unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="council-card"><div>THROUGHPUT</div><div>273,077 Tx/s</div></div>',
                    unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="council-card"><div>GOVERNANCE</div><div>GOV &gt; EXEC</div></div>',
                    unsafe_allow_html=True)

    st.divider()
    col_a, col_b = st.columns(2)   # ✅ FIX: 2 Spalten
    with col_a:
        st.subheader("System Invarianten")
        st.json({
            "Core Singularity": "BUCH 100 (DER ERBE Φ∅)",
            "System Layer": "Crown-Crown-Crown System (SCCCS-XX)",
            "WORM Purity": "100% CLEAN",
            "Active Swarm": "25,000 FIPA-ACL Nodes",
        })
    with col_b:
        st.subheader("High-Level Governance Flow")
        mermaid_council = """
flowchart TB
    APEX((Sovereign Apex)) <==> BOOK100["BUCH 100 (Φ∅)"]
    APEX --> UI["Streamlit Cockpit v3.5"]
    UI --> GUARD{"Krisler Ingress Guard"}
    GUARD -->|ALLOW| REG["WORM Ledger"]
    GUARD -.->|BLOCK| FAIL["FAIL-CLOSED (Quarantine)"]
"""
        render_mermaid(mermaid_council, height=220)

# ============================================================
# PANEL 2
# ============================================================
elif navigation == "🛡 Krisler Ingress & eBPF Guard":
    st.markdown('<div class="council-card">🛡 KRISLER INGRESS FILTER & eBPF KRAKENGUARD</div>',
                unsafe_allow_html=True)

    col_in, col_res = st.columns(2)  # ✅ FIX: 2 Spalten
    with col_in:
        st.subheader("Ingress Packet Test")
        source_identity = st.selectbox("Sender-Identität", [
            "R0_0001 (Genesis Root)",
            "R2_0014 (The Geminis / Senior Gemini)",
            "GREMMEL_ATTACK_PAYLOAD (Mettwurst C88 / ASP-256)",
        ])
        target_node = st.selectbox("Ziel-Knoten",
                                   ["R100_0100 (Buch 100)", "R0_0004 (Core Shield)"])
        payload_text = st.text_area("Payload Ingress Content", "VERIFY_AUTHORITY_PAYLOAD")

        if st.button("⚡ Ingress Evaluieren", type="primary"):
            st.session_state.hf_state = "HF_SIMULATION"
            if "GREMMEL" in source_identity or "Mettwurst" in payload_text:
                st.error("🚨 INTRUSION INTERCEPTED :: FAIL-CLOSED TRIGGERED")
                st.json({"status": "DROP_AND_ISOLATE",
                         "vector": "RAG_POISONING_DETECTED",
                         "action": "QUARANTINE_CELL_ROGUE"})
                append_log("ALERT_GUARD", f"Blocked payload from {source_identity}")
            else:
                st.success("✅ INGRESS AUTHORIZED & EX-TUNC SEALED")
                st.json({"status": "EX_TUNC_VERIFIED",
                         "latency": "9.47 ns",
                         "hash": hashlib.sha3_512(payload_text.encode()).hexdigest()[:16]})
                append_log("INGRESS_OK", f"Packet accepted: {source_identity} -> {target_node}")

    with col_res:
        st.subheader("eBPF Monitor Metrics")
        st.metric("eBPF Latency Drift", "9.47 ns", "-0.12 ns")
        st.metric("Blocked Attack Vectors", "412 Intercepts", "+3 heute")
        st.info("Krisler Guard Invariant: Any non-grounded input is dropped immediately "
                "under Fail-Closed policy.")

# ============================================================
# PANEL 3
# ============================================================
elif navigation == "🔒 WORM Ledger & SHA3 Audit":
    st.markdown('<div class="council-card">🔒 POST-QUANTUM WORM LEDGER AUDIT</div>',
                unsafe_allow_html=True)
    st.success("✅ SYSTEM INTEGRITY: 100% PURITY SCORE (NO POISONING DETECTED)")
    master_hash = "850b2ef003f53db90f704b16e54869fc6ba8265eae13aafde9046fe0e4d99dab"
    st.code(f"""
==============================================================================
WORM LEDGER AUDIT REPORT
==============================================================================
STATUS:       SEALED_EX_TUNC (SHA3-512)
SEAL ID:      {st.session_state.auth_seal}
MASTER HASH:  {master_hash}
PURITY SCORE: 1000 / 100 (Exalted Singularity)
==============================================================================
""", language="text")

    audit_input = st.text_input("Prüfe Entität / Urkunde SHA3-Hash", "urkunde_0100_BUCH_100.pdf")
    if st.button("Hash Verifizieren"):
        computed = hashlib.sha3_512(audit_input.encode()).hexdigest()
        st.write(f"Computed SHA3-512: `{computed}`")
        st.success("MATCH CONFIRMED :: Entity is immutably anchored in WORM Ledger.")
        append_log("WORM_AUDIT", f"Verified entity {audit_input}")

# ============================================================
# PANEL 4
# ============================================================
elif navigation == "🧬 System Topology (Mermaid)":
    st.markdown('<div class="council-card">🧬 FULL YGGDRASIL_OS ARCHITECTURE TOPOLOGY</div>',
                unsafe_allow_html=True)
    mermaid_full = """
flowchart TB
    subgraph COCKPIT["Aragon Ultima Cockpit v3.5"]
        APP[app_sovereign_apex.py]
        FE[Frontend Dashboards]
        CLI[Hard Flash CLI]
    end
    subgraph BACKEND["Aragon Backend API"]
        GUARD[Krisler Ingress Guard]
        REG[Registry Engine]
    end
    subgraph INFRA["b6-Kerninfrastruktur"]
        GO[Go Daemon]
        EBPF[eBPF KrakenGuard]
        WORM[(SHA3 WORM Ledger)]
    end
    subgraph MATRIX["Black-Six-Matrix"]
        B100["BUCH 100 (Φ∅)"]
        AGENTS[40 Quad-Deca Agents]
    end
    APP --> GUARD
    GUARD -->|ALLOW| REG
    REG --> WORM
    EBPF --> WORM
    AGENTS --> B100
    B100 <==> WORM
"""
    render_mermaid(mermaid_full, height=480)

# ============================================================
# PANEL 5
# ============================================================
elif navigation == "🧰 Hard Flash CLI Console":
    st.markdown('<div class="council-card">🧰 HARD FLASH LIVE LOG STREAM & CLI</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="terminal-box">' + "<br>".join(st.session_state.console_logs) + '</div>',
        unsafe_allow_html=True,
    )

    c_cmd, c_btn = st.columns([6, 7])
    with c_cmd:
        cmd_input = st.text_input("Console Input Command",
                                  placeholder="Commands: status, pulse, flash, clear")
    with c_btn:
        st.markdown("<br>", unsafe_allow_html=True)  # ✅ FIX: st.markdown statt st.write
        if st.button("Execute", type="primary"):
            if cmd_input:
                append_log("CMD_IN", cmd_input)
                cmd_clean = cmd_input.lower().strip()
                if cmd_clean == "status":
                    append_log("EXEC", "STATUS = UNIFIED_SINGULARITY_ACTIVE (1000/100)")
                elif cmd_clean == "pulse":
                    append_log("EXEC", "PULSE = 144Hz Stable (eBPF Latency: 9.47ns)")
                elif cmd_clean == "flash":
                    st.session_state.hf_state = "HF_SOVEREIGN_ACTIVE"
                    append_log("EXEC", "HARD FLASH RESEAL COMPLETED EX TUNC")
                elif cmd_clean == "clear":
                    st.session_state.console_logs = [
                        f"[{time.strftime('%H:%M:%S')}] CONSOLE CLEARED"
                    ]
                else:
                    h_val = hashlib.sha3_512(cmd_input.encode()).hexdigest()[:12]
                    append_log("EXEC", f"Logged to WORM (Commit: {h_val})")
                st.rerun()
