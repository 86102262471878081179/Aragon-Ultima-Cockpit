# Architektur/system_map.py
import streamlit as st
from Architektur.mermaid_engine import render_mermaid
from Architektur.kernel_loader import load_kernel, get_rings

def generate_dynamic_system_mermaid() -> str:
    """
    Generiert den großen System-Map-Mermaid-Graphen.
    Zieht die Ringe dynamisch aus der kernel.yaml.
    """
    kernel = load_kernel()
    rings = get_rings()
    mode = kernel.get("mode", "APEX_SINGULARITY_LOCKED")
    seal = kernel.get("governance", {}).get("seal", "UNKNOWN_SEAL")

    mermaid = f"""
    flowchart TB

    %% ROOT & CORE
    SOV((SOVEREIGN CORE))
    APEX[/"APEX OPERATOR (Φ∅)"/]
    
    %% KERNEL LAYER
    subgraph KERNEL_LAYER["Kernel Layer ({mode})"]
        KERNEL[[Kernel Core]]
        GOV{{"Governance<br/>{seal}"}}
        WORM[("WORM Ledger")]
    end

    %% RUNTIME LAYER
    subgraph RUNTIME_LAYER["Runtime & Services"]
        RUNTIME((Runtime Engine))
        EVENT_BUS[/"Event Bus"/]
        CLUSTER(("Cluster Engine"))
    end

    %% CONNECTIONS & DATA
    subgraph DATA_LAYER["Data & Connectivity"]
        BACKEND["Backend API (Python)"]
        GRAPH[("Neo4j Graph")]
        GO["Go Core (Metrics)"]
    end

    %% COCKPIT UI
    COCKPIT[/"Streamlit Cockpit"/]

    %% CONNECTIONS
    SOV ===> APEX
    APEX --> KERNEL
    KERNEL --> GOV
    KERNEL --> WORM
    KERNEL --> RUNTIME
    
    RUNTIME --> EVENT_BUS
    RUNTIME --> CLUSTER
    
    GOV --> BACKEND
    WORM --> GO
    RUNTIME --> BACKEND
    BACKEND --> GRAPH
    
    %% UI CONNECTIONS
    COCKPIT -.->|Queries| BACKEND
    COCKPIT -.->|Queries| GO
    COCKPIT -.->|Queries| GRAPH
    COCKPIT --> RUNTIME
    """

    # Dynamische Ringe hinzufügen
    mermaid += '\n    %% MATRIX RINGS\n'
    mermaid += '    subgraph RINGS["Matrix Rings (kernel.yaml)"]\n'
    mermaid += '        direction LR\n'
    for ring in rings:
        rid = ring["id"]
        rname = ring["name"]
        rrole = ring["role"]
        mermaid += f'        {rid}["{rname}<br/>({rrole})"]\n'
    
    mermaid += '    end\n'
    mermaid += '    KERNEL --> RINGS\n'

    # Styling (Blue Core Vibe)
    mermaid += """
    %% STYLING
    classDef sovereign fill:#00e5ff,color:#000,stroke:#fff,stroke-width:3px,font-weight:bold;
    classDef kernel fill:#b800ff,color:#fff,stroke:#fff,stroke-width:2px;
    classDef data fill:#0a122a,color:#00e5ff,stroke:#00e5ff,stroke-width:1px;
    classDef ring fill:#141424,color:#d0d0e0,stroke:#333,stroke-width:1px;
    
    class SOV,APEX sovereign;
    class KERNEL,GOV,WORM kernel;
    class BACKEND,GRAPH,GO data;
    class RUNTIME,EVENT_BUS,CLUSTER ring;
    """
    
    return mermaid

def render_system_map():
    """
    Rendert die Sovereign System Map im Streamlit-Cockpit.
    """
    st.markdown('<div class="main-header">🗺️ SOVEREIGN SYSTEM MAP</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Globale Architektur & Ring-Topologie</div>', unsafe_allow_html=True)

    # Info-Zeile
    kernel = load_kernel()
    c1, c2, c3 = st.columns(3)
    c1.metric("Kernel ID", kernel.get("kernel_id", "UNKNOWN"))
    c2.metric("Kernel Mode", kernel.get("mode", "UNKNOWN"))
    c3.metric("Ringe", len(kernel.get("rings", [])))

    st.divider()

    # Graph generieren und rendern
    mermaid_code = generate_dynamic_system_mermaid()
    
    with st.container():
        render_mermaid(mermaid_code, height=700)

    # Rohdaten-Ansicht (optional, für Audit)
    with st.expander("📊 Kernel Ring-Daten (Rohdaten)"):
        st.json(kernel.get("rings", []))

# =========================================================
# TEST-BLOCK
# =========================================================
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    render_system_map()
