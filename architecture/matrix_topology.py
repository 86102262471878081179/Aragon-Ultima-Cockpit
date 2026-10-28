# Architektur/matrix_topology.py
import streamlit as st
from typing import Dict, Any, List, Tuple
from Architektur.kernel_loader import get_neo4j_config
from Architektur.mermaid_engine import render_mermaid

# Optionaler Import für Neo4j (falls im requirements.txt)
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

# =========================================================
# MOCK-DATEN (Fail-Safe, falls Neo4j offline ist)
# =========================================================
MOCK_NODES = [
    {"id": "APEX", "label": "Sovereign Apex (0068)", "group": "Ring 0"},
    {"id": "R0", "label": "Genesis Root", "group": "Ring 0"},
    {"id": "R1", "label": "Fortress Justice", "group": "Ring 1"},
    {"id": "R2", "label": "Quantum Tresor", "group": "Ring 2"},
    {"id": "R5", "label": "Mettwurst C88 API", "group": "Ring 5"},
    {"id": "WUS", "label": "Wusulum Core", "group": "L.S.S. Neuro"},
    {"id": "GRU", "label": "Grummel Dynasty", "group": "Threat Intel"},
    {"id": "GOT", "label": "Gotham City", "group": "Threat Intel"},
    {"id": "KG", "label": "King_Ghost", "group": "Threat Intel"},
]

MOCK_EDGES = [
    {"source": "APEX", "target": "R0", "type": "GOVERNS"},
    {"source": "APEX", "target": "R1", "type": "GOVERNS"},
    {"source": "APEX", "target": "R2", "type": "GOVERNS"},
    {"source": "APEX", "target": "R5", "type": "GOVERNS"},
    {"source": "R2", "target": "WUS", "type": "FEEDS_DATA"},
    {"source": "WUS", "target": "GRU", "type": "DETECTS_THREAT"},
    {"source": "GRU", "target": "GOT", "type": "ISOLATED_IN"},
    {"source": "GRU", "target": "KG", "type": "CONSUMED_BY"},
]

# =========================================================
# CORE FUNCTIONS
# =========================================================
def check_neo4j_connection() -> Tuple[bool, str]:
    """Prüft, ob Neo4j erreichbar ist."""
    if not NEO4J_AVAILABLE:
        return False, "Neo4j Python-Treiber nicht installiert."
    
    config = get_neo4j_config()
    try:
        driver = GraphDatabase.driver(config["uri"], auth=(config["user"], config["password"]))
        with driver.session() as session:
            session.run("RETURN 1")
        driver.close()
        return True, "Neo4j ONLINE"
    except Exception as e:
        return False, f"Neo4j OFFLINE ({str(e)[:50]}...)"

def fetch_topology_from_neo4j() -> Tuple[List[Dict], List[Dict]]:
    """
    Zieht die Topologie aus Neo4j.
    Wenn die DB offline ist, wird auf die MOCK_NODES / MOCK_EDGES zurückgegriffen.
    """
    is_online, msg = check_neo4j_connection()
    
    if not is_online:
        return MOCK_NODES, MOCK_EDGES
        
    config = get_neo4j_config()
    nodes = []
    edges = []
    
    try:
        driver = GraphDatabase.driver(config["uri"], auth=(config["user"], config["password"]))
        with driver.session() as session:
            # Ein einfaches Topologie-Query
            result = session.run("""
                MATCH (n)-[r]->(m)
                RETURN elementId(n) AS n_id, labels(n)[0] AS n_label, 
                       elementId(m) AS m_id, labels(m)[0] AS m_label, 
                       type(r) AS rel_type
                LIMIT 50
            """)
            
            for record in result:
                n_id = record["n_id"]
                m_id = record["m_id"]
                
                # Duplikate vermeiden
                if not any(n["id"] == n_id for n in nodes):
                    nodes.append({"id": n_id, "label": record["n_label"], "group": "Neo4j"})
                if not any(n["id"] == m_id for n in nodes):
                    nodes.append({"id": m_id, "label": record["m_label"], "group": "Neo4j"})
                    
                edges.append({
                    "source": n_id, 
                    "target": m_id, 
                    "type": record["rel_type"]
                })
        driver.close()
        return nodes, edges
    except Exception as e:
        st.error(f"Fehler beim Abruf aus Neo4j: {e}")
        return MOCK_NODES, MOCK_EDGES

def generate_mermaid_from_topology(nodes: List[Dict], edges: List[Dict]) -> str:
    """Konvertiert Knoten und Kanten in einen Mermaid-Flowchart-String."""
    mermaid = "flowchart LR\n"
    
    # Nodes rendern
    for n in nodes:
        # Bereinige den Label-Text für Mermaid
        safe_label = n['label'].replace('"', "'")
        mermaid += f'    {n["id"]}["{safe_label}"]\n'
        
    # Edges rendern
    for e in edges:
        mermaid += f'    {e["source"]} -->|{e["type"]}| {e["target"]}\n'
        
    return mermaid

# =========================================================
# STREAMLIT UI RENDER
# =========================================================
def render_matrix_topology():
    """Rendert die Topologie-Ansicht im Streamlit Cockpit."""
    st.markdown('<div class="main-header">🕸️ MATRIX TOPOLOGY</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Graph-Verbindungen der 201 Entitäten</div>', unsafe_allow_html=True)

    # Status-Check
    is_online, msg = check_neo4j_connection()
    if is_online:
        st.success(f"🟢 Datenbank verbunden: {msg}")
    else:
        st.warning(f"🟡 {msg} — Verwende Sovereign Fallback-Matrix (Mock Data).")

    # Daten laden
    nodes, edges = fetch_topology_from_neo4j()

    # Statistiken
    c1, c2, c3 = st.columns(3)
    c1.metric("Knoten (Entitäten)", len(nodes))
    c2.metric("Kanten (Verbindungen)", len(edges))
    c3.metric("Datenquelle", "Neo4j" if is_online else "Mock / Kernel")

    st.divider()

    # Zwei Spalten: Graph links, Rohdaten rechts
    col_graph, col_data = st.columns([2, 1])

    with col_graph:
        st.subheader("Graph-Visualisierung")
        mermaid_code = generate_mermaid_from_topology(nodes, edges)
        # Nutzt deine render_mermaid Funktion aus mermaid_engine.py
        render_mermaid(mermaid_code, height=500)

    with col_data:
        st.subheader("Rohdaten")
        tab_nodes, tab_edges = st.tabs(["Knoten", "Kanten"])
        with tab_nodes:
            st.dataframe(nodes, use_container_width=True, hide_index=True)
        with tab_edges:
            st.dataframe(edges, use_container_width=True, hide_index=True)

# =========================================================
# TEST-BLOCK
# =========================================================
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    render_matrix_topology()
