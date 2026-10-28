# Architektur/apex_graph_engine.py
import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Tuple

from Architektur.kernel_loader import get_neo4j_config
from Architektur.mermaid_engine import render_mermaid

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

# =========================================================
# FALLBACK-DATEN (Wenn Neo4j offline ist)
# =========================================================
APEX_FALLBACK_QUERY = """
MATCH (a)-[r]->(b)
RETURN elementId(a) AS a_id, labels(a)[0] AS a_label, 
       elementId(b) AS b_id, labels(b)[0] AS b_label, 
       type(r) AS rel_type
LIMIT 50
"""

# =========================================================
# CORE ENGINE
# =========================================================
class ApexGraphEngine:
    def __init__(self):
        self.config = get_neo4j_config()
        self.driver = None
        self.is_connected = False
        self._connect()

    def _connect(self):
        if not NEO4J_AVAILABLE:
            return
        try:
            self.driver = GraphDatabase.driver(
                self.config.get("uri", "bolt://localhost:7687"),
                auth=(self.config.get("user", "neo4j"), self.config.get("password", "password"))
            )
            self.driver.verify_connectivity()
            self.is_connected = True
        except Exception:
            self.is_connected = False

    def execute_query(self, query: str) -> Tuple[List[Dict], List[Dict]]:
        """Führt eine Cypher-Query aus und extrahiert Nodes/Edges."""
        nodes = []
        edges = []

        if not self.is_connected:
            # Fallback: Simuliere das Ergebnis
            st.warning("⚠️ Neo4j offline. Nutze simuliertes Apex-Ergebnis.")
            return self._mock_apex_graph()

        try:
            with self.driver.session() as session:
                result = session.run(query)
                for record in result:
                    # Dynamische Extraktion: Sucht nach typischen Node/Edge-Feldern
                    a_id = record.get("a_id") or record.get("source") or record.get("n_id")
                    b_id = record.get("b_id") or record.get("target") or record.get("m_id")
                    
                    if a_id and not any(n["id"] == str(a_id) for n in nodes):
                        nodes.append({"id": str(a_id), "label": str(record.get("a_label", a_id))})
                    if b_id and not any(n["id"] == str(b_id) for n in nodes):
                        nodes.append({"id": str(b_id), "label": str(record.get("b_label", b_id))})
                        
                    if a_id and b_id:
                        edges.append({
                            "source": str(a_id), 
                            "target": str(b_id), 
                            "type": str(record.get("rel_type", "LINK"))
                        })
            return nodes, edges
        except Exception as e:
            st.error(f"🚨 Cypher-Fehler: {e}")
            return self._mock_apex_graph()

    def _mock_apex_graph(self) -> Tuple[List[Dict], List[Dict]]:
        """Ein kleiner, souveräner Fallback-Graph für die UI."""
        nodes = [
            {"id": "APEX", "label": "Sovereign Apex (Φ∅)"},
            {"id": "R0", "label": "Ring 0 (Genesis)"},
            {"id": "WUS", "label": "Wusulum Core"},
            {"id": "GRU", "label": "Grummel Threat"},
            {"id": "GOT", "label": "Gotham City"}
        ]
        edges = [
            {"source": "APEX", "target": "R0", "type": "COMMANDS"},
            {"source": "R0", "target": "WUS", "type": "GENERATES"},
            {"source": "WUS", "target": "GRU", "type": "DETECTS"},
            {"source": "GRU", "target": "GOT", "type": "ISOLATED_TO"}
        ]
        return nodes, edges

    def build_sovereign_mermaid(self, nodes: List[Dict], edges: List[Dict], direction: str = "LR") -> str:
        """Baut ein Mermaid-Script mit Sovereign-Styling."""
        mermaid = f"flowchart {direction}\n"
        
        # Node-Klassen für spezielles Styling
        mermaid += "    classDef apexNode fill:#00e5ff,color:#000,stroke:#fff,stroke-width:2px;\n"
        mermaid += "    classDef threatNode fill:#ff0000,color:#fff,stroke:#ff0000;\n"
        mermaid += "    classDef defaultNode fill:#141424,color:#fff,stroke:#333;\n"

        # Nodes rendern
        for n in nodes:
            safe_label = str(n["label"]).replace('"', "'")
            mermaid += f'    {n["id"]}["{safe_label}"]\n'
            
            # Styling-Zuweisung basierend auf Label
            if "Apex" in safe_label or "Φ∅" in safe_label:
                mermaid += f'    class {n["id"]} apexNode;\n'
            elif "Grummel" in safe_label or "Gotham" in safe_label:
                mermaid += f'    class {n["id"]} threatNode;\n'
            else:
                mermaid += f'    class {n["id"]} defaultNode;\n'

        # Edges rendern
        for e in edges:
            mermaid += f'    {e["source"]} -->|{e["type"]}| {e["target"]}\n'
            
        return mermaid

# =========================================================
# STREAMLIT UI
# =========================================================
def render_apex_graph_engine():
    st.markdown('<div class="main-header">🕸️ APEX GRAPH ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interaktive Neo4j Topologie & Sovereign Exploration</div>', unsafe_allow_html=True)

    engine = ApexGraphEngine()

    # Status-Anzeige
    if engine.is_connected:
        st.success(f"🟢 Verbunden mit Neo4j: `{engine.config.get('uri')}`")
    else:
        st.warning("🟡 Neo4j nicht erreichbar. Der Fallback-Graph wird genutzt.")

    # Steuerungs-Panel
    with st.expander("⚙️ Cypher-Query & Graph-Steuerung", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            query = st.text_area(
                "Cypher Query", 
                value=APEX_FALLBACK_QUERY,
                height=100,
                help="Standard: MATCH (a)-[r]->(b) RETURN elementId(a) AS a_id..."
            )
        with col2:
            direction = st.selectbox("Layout", ["LR", "TB", "RL", "BT"])
            st.write("")
            st.write("")
            run_btn = st.button("🚀 Graph ausführen", type="primary", use_container_width=True)

    # Ausführung und Rendering
    if run_btn:
        with st.spinner("Führe Apex-Query aus..."):
            nodes, edges = engine.execute_query(query)
            
            if not nodes:
                st.info("Keine Knoten für diese Query gefunden.")
                return

            # Statistiken
            c1, c2 = st.columns(2)
            c1.metric("Extrahierte Knoten", len(nodes))
            c2.metric("Extrahierte Kanten", len(edges))
            
            st.divider()

            # Graph rendern
            mermaid_code = engine.build_sovereign_mermaid(nodes, edges, direction)
            render_mermaid(mermaid_code, height=500)

            # Rohdaten-Ansicht
            with st.expander("📊 Rohdaten anzeigen"):
                tab1, tab2 = st.tabs(["Nodes", "Edges"])
                with tab1:
                    st.dataframe(pd.DataFrame(nodes), use_container_width=True, hide_index=True)
                with tab2:
                    st.dataframe(pd.DataFrame(edges), use_container_width=True, hide_index=True)

# =========================================================
# TEST-BLOCK
# =========================================================
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    render_apex_graph_engine()
