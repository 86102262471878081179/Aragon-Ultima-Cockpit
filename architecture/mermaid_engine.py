# Architektur/mermaid_engine.py
import streamlit as st
import streamlit.components.v1 as components
import os

def render_mermaid(code: str, height: int = 600, theme: str = "dark"):
    """
    Rendert einen Mermaid-Graphen in Streamlit.
    
    Args:
        code (str): Der Mermaid-Code (z.B. "flowchart TB...")
        height (int): Höhe des gerenderten Iframes in Pixeln.
        theme (str): Das Mermaid-Theme ("dark", "default", "forest", "neutral").
    """
    
    # Das HTML-Template mit Mermaid.js CDN und Blue-Core-Styling
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{
                startOnLoad: true,
                theme: '{theme}',
                securityLevel: 'loose',
                fontFamily: 'monospace',
                flowchart: {{
                    curve: 'basis',
                    htmlLabels: true
                }}
            }});
        </script>
        <style>
            body {{
                background-color: #0a122a; /* Blue Core Dark */
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                overflow: hidden;
            }}
            .mermaid {{
                width: 100%;
                text-align: center;
            }}
            /* SVG Text-Farbe anpassen für Dark Mode */
            .mermaid svg {{
                max-width: 100%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <div class="mermaid">
            {code}
        </div>
    </body>
    </html>
    """
    
    # Rendert das HTML im Streamlit-Frontend
    components.html(html_code, height=height, scrolling=True)

def render_mermaid_page():
    """
    Eine vollständige Streamlit-Seite für die Architektur-Ansicht.
    Wird aufgerufen, wenn der Nutzer auf 'Architektur-Matrix' klickt.
    """
    st.markdown('<div class="main-header">🧬 SOVEREIGN SYSTEM ARCHITEKTUR 🧬</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ring-Topologie & Agenten-Verknüpfung</div>', unsafe_allow_html=True)

    # Beispiel: Der 4x4 Council & Ring Ω Graph
    with st.expander("🏛️ 4x4 Council & Ring Ω", expanded=True):
        council_graph = """
        flowchart TB
            APEX((Sovereign Apex)) <==> BOOK100["BUCH 100 (Φ∅)"]
            APEX --> UI["Streamlit Cockpit"]
            UI --> API["FastAPI Backend (Python)"]
            UI --> GO["Go Core (WORM & Metriken)"]
            
            API --> GUARD{"Krisler Guard"}
            GUARD -->|ALLOW| REG["Registry Engine"]
            GUARD -.->|BLOCK| FAIL["FAIL-CLOSED"]
            
            REG --> WORM[(WORM Ledger)]
            GO --> WORM
            
            style APEX fill:#00e5ff,color:#000
            style WORM fill:#00ff00,color:#000
            style FAIL fill:#ff0000,color:#fff
            style GO fill:#00add8,color:#fff
        """
        render_mermaid(council_graph, height=450)

    # Beispiel: Feindregister & Isolation Flow
    with st.expander("🛡️ Feindregister & Isolation Flow", expanded=False):
        isolation_graph = """
        flowchart LR
            PKT["Ingress Packet"] --> GUARD{"Krisler Guard"}
            GUARD -->|matched Grummel-ID| ISOLATE["DROP_AND_ISOLATE"]
            GUARD -->|clean| WORM[(WORM Ledger)]
            
            ISOLATE --> GOTHAM["Gotham City Sandbox"]
            ISOLATE --> KINGGHOST["King_Ghost Shadow Pool"]
            
            GOTHAM --> REGISTRY["Feindregister Update"]
            REGISTRY --> KILL{"Kill-Switch Trigger?"}
            
            KILL -->|yes| TOTAL["TOTAL ISOLATION"]
            KILL -->|no| ALERT["ALERT Log"]
            
            style ISOLATE fill:#ff0000,color:#fff
            style TOTAL fill:#ff00ff,color:#000
            style GOTHAM fill:#1a001a,color:#ff88ff
            style KINGGHOST fill:#330000,color:#ff4444
        """
        render_mermaid(isolation_graph, height=350)

    # Beispiel: L.S.S. Neuro-Core Pipeline
    with st.expander("🌀 L.S.S. Neuro-Core Pipeline", expanded=False):
        neuro_graph = """
        flowchart LR
            IN["User Input"] --> SENSOR["10 Ohren (TenEars)"]
            SENSOR --> PERSP["44 Perspektiven (Attention)"]
            PERSP --> BIO["Polyvagal-Regler"]
            
            BIO -->|Stress < 0.4| VENTRAL["Ventral-Vagal (Kreativ)"]
            BIO -->|Stress < 0.8| SYMP["Sympathikus (Kampf)"]
            BIO -->|Stress >= 0.8| DORSAL["Dorsal-Vagal (Shutdown)"]
            
            VENTRAL --> WUS["Wusulum Core (Generation)"]
            SYMP --> FOUC["Foucault Inversion"]
            
            WUS --> ADV["Advocatus Diaboli (Logic Check)"]
            FOUC --> ADV
            
            ADV -->|Pass| XJ["XJustiz XML Gate"]
            ADV -->|Fail| CONTAIN["CONTAINED (Gotham)"]
            
            XJ --> WORM2[(WORM Seal)]
            
            style WORM2 fill:#00ff00,color:#000
            style ADV fill:#ff00ff,color:#fff
            style DORSAL fill:#ff0000,color:#fff
            style CONTAIN fill:#660000,color:#fff
        """
        render_mermaid(neuro_graph, height=400)

if __name__ == "__main__":
    # Wenn die Datei direkt ausgeführt wird, startet ein Test-Render
    st.set_page_config(layout="wide")
    render_mermaid_page()
