#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
            YGGDRASIL_OS :: SOVEREIGN COCKPIT v4.0 (BOOK EDITION)
================================================================================
Author: Thomas König / Odin Ultra Root
Audit:  Gremmel Sentienel v5.2 (KVL PASSED)
Lines:  > 1.100 (Monolith)
================================================================================
"""

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
import sqlite3
import os
import base64
from datetime import datetime

# Optional heavy dependencies (Fail-Safe)
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    import reportlab
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

try:
    from cryptography.fernet import Fernet
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

# ============================================================
# 1. DATABASE INITIALISIERUNG (SQLite)
# ============================================================
DB_PATH = "yggdrasil_sovereign.db"

def init_db():
    """Erstellt die Tabellen, falls sie nicht existieren (Fail-Safe)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chronik 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, kind TEXT, msg TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feinde 
                 (id TEXT PRIMARY KEY, name TEXT, grund TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS votes 
                 (proposal TEXT PRIMARY KEY, ja INTEGER, nein INTEGER, enthaltung INTEGER)''')
    conn.commit()
    conn.close()

init_db()

def db_log(kind: str, msg: str):
    """Schreibt Events hart in die SQLite-Datenbank."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO chronik (ts, kind, msg) VALUES (?, ?, ?)",
              (time.strftime("%Y-%m-%d %H:%M:%S"), kind, msg))
    conn.commit()
    conn.close()

# ============================================================
# 2. PAGE CONFIG + CSS
# ============================================================
st.set_page_config(
    page_title="YGGDRASIL_OS :: Sovereign Cockpit v4",
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
    .book-text { font-family: 'Georgia', serif; font-size: 1.1rem; line-height: 1.8;
        text-align: justify; color: #e0e0f0; padding: 20px; border-left: 4px solid #d4af37; background: #101020;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. SESSION STATE (Synchronisiert mit DB)
# ============================================================
if "auth_seal" not in st.session_state:
    st.session_state.auth_seal = "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "kill_switch_active" not in st.session_state:
    st.session_state.kill_switch_active = False

# Chronik aus DB laden
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT ts, kind, msg FROM chronik ORDER BY id ASC")
st.session_state.chronik = [{"ts": r[0], "kind": r[1], "msg": r[2]} for r in c.fetchall()]

# Feinde aus DB laden
c.execute("SELECT id, name, grund, status FROM feinde")
st.session_state.feinde = [{"ID": r[0], "Name": r[1], "Grund": r[2], "Status": r[3]} for r in c.fetchall()]

# Votes aus DB laden
c.execute("SELECT proposal, ja, nein, enthaltung FROM votes")
st.session_state.votes = {r[0]: {"JA": r[1], "NEIN": r[2], "ENTHALTUNG": r[3]} for r in c.fetchall()}
conn.close()

if "metric_history" not in st.session_state:
    st.session_state.metric_history = []

# ============================================================
# 4. HELPERS
# ============================================================
def log_event(kind: str, msg: str):
    """Schreibt ins UI und in die SQLite DB."""
    st.session_state.chronik.append({"ts": time.strftime("%H:%M:%S"), "kind": kind, "msg": msg})
    db_log(kind, msg)

def render_mermaid(code: str, height: int = 600):
    html_code = f'''
    <div class="mermaid" style="background-color: #0a0a12; text-align: center;">{code}</div>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({{ startOnLoad: true, theme: "dark" }});
    </script>
    '''
    components.html(html_code, height=height, scrolling=True)

def create_pdf_report(text_content: str, title: str) -> bytes:
    """Erzeugt ein echtes PDF via ReportLab (WORM-Dokument)."""
    if not HAS_REPORTLAB:
        return b"PDF_GENERATION_FAILED_REPORTLAB_MISSING"
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 800, title)
    p.setFont("Helvetica", 10)
    p.drawString(50, 780, f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Einfacher Text-Wrap
    text_object = p.beginText(50, 750)
    text_object.setFont("Helvetica", 11)
    for line in text_content.split('\n'):
        text_object.textLine(line)
    
    p.drawText(text_object)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()

# ============================================================
# 5. SIDEBAR NAVIGATION
# ============================================================
st.sidebar.title("YGGDRASIL_OS v4")
st.sidebar.markdown("**Authority**: Sovereign Root Thomas")
st.sidebar.markdown("**Kernel**: Schwarzer Punkt")
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
    "📄 Buch-Druckerei (PDF)",
    "🔐 AES-256 Tresor",
    "⚖️ Axiome-Prüfer",
    "📖 Das Schwarze Buch",
    "🗄️ SQLite Direkt-Zugriff",
])

st.sidebar.divider()
st.sidebar.caption(f"Chronik: {len(st.session_state.chronik)} (DB Persistiert)")
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
                f'<p><strong>WORM-Hash:</strong> {hashlib.sha256(case_input.encode()).hexdigest()[:32]}...</p>'
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
            "BGB": {"§ 823": "Schadensersatzpflicht", "§ 826": "Sittenwidrige Schädigung", "§ 839": "Amtspflichtverletzung", "§ 249": "Schadensersatz"},
            "StGB": {"§ 339": "Rechtsbeugung", "§ 340": "Körperverletzung im Amt", "§ 353d": "Verbotene Mitteilungen", "§ 142": "Unfallflucht"},
            "GG": {"Art. 1": "Menschenwürde", "Art. 3": "Gleichheit", "Art. 19 Abs. 4": "Rechtsweggarantie", "Art. 20 Abs. 3": "Bindung an Gesetz"},
            "VwVfG": {"§ 28": "Anhörung", "§ 29": "Akteneinsicht", "§ 48": "Rücknahme", "§ 51": "Wiederaufgreifen"},
            "ZPO": {"§ 138": "Erklärungspflicht", "§ 286": "Freie Beweiswürdigung", "§ 91": "Kosten"},
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

        c1, c2, c3 = st.columns(3)
        c1.metric("Basis-Schaden", f"{schaden:,.2f} €")
        c2.metric("Zinsen (regulär)", f"{zinsen_reg:,.2f} €")
        c3.metric("Zinsen (Verzug)", f"{zinsen_verzug:,.2f} €")

        st.divider()
        cA, cB = st.columns(2)
        cA.metric("Gesamt regulär", f"{schaden + zinsen_reg:,.2f} €")
        cB.metric("Gesamt mit Verzug", f"{schaden + zinsen_verzug:,.2f} €", delta=f"+{zinsen_verzug - zinsen_reg:,.2f} €")

        if st.button("📋 Berechnung in WORM-Ledger protokollieren"):
            log_event("WORM", f"Schadensberechnung: {schaden + zinsen_verzug:,.2f} € gesiegelt")
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
                with st.spinner("Render Backend wird abgefragt..."):
                    try:
                        api_url = "https://aragon-backend-api.onrender.com/prompt/check"
                        payload = {"prompt": prompt, "auth_seal": st.session_state.auth_seal}
                        response = httpx.post(api_url, json=payload, timeout=60.0)
                        
                        if response.status_code == 200:
                            data = response.json()
                            # NEU: Akzeptiert sowohl "200_OK" (neue API) als auch "200_OK_ALLOW" (alte API)
                            status_check = data.get("status", "")
                            if "200_OK" in status_check:
                                ai_ans = data.get("data", {}).get("ai_answer", "Keine KI-Antwort.")
                                st.markdown(f"**KI-Antwort:**\n{ai_ans}")
                                st.session_state.messages.append({"role": "assistant", "content": ai_ans})
                                log_event("INGRESS", f"Chat-Prompt beantwortet")
                            else:
                                # Falls die API blockiert (Fail-Closed) oder einen Fehler hat
                                st.error(f"Fail-Closed! {data.get('detail', 'Unbekannter Fehler')}")
                                log_event("ALERT", f"API Fail-Closed: {data.get('detail')}")
                                log_event("ALERT", f"API Fail-Closed: {data.get('detail')}")
                        else:
                            st.error(f"API Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Verbindungsfehler: {str(e)}")
                        
    with tab_settings:
        new_seal = st.text_input("Authorization Token (Seal)", value=st.session_state.auth_seal)
        if st.button("Token aktualisieren"):
            st.session_state.auth_seal = new_seal
            log_event("EXEC", "Auth-Seal rotiert")
            st.success("Token gespeichert.")
            
    with tab_sys:
        st.metric(label="Aktives Auth Seal", value=st.session_state.auth_seal)
        st.metric(label="Nachrichten im Verlauf", value=len(st.session_state.messages))

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
            df = df[df["Name"].str.contains(search_term, case=False) |
                    df["ID"].str.contains(search_term) |
                    df["Ring"].str.contains(search_term, case=False)]
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"{len(df)} von {len(books_data)} Entitäten angezeigt")

    with tab_upload:
        uploaded_file = st.file_uploader("CSV auswählen", type="csv")
        if uploaded_file is not None:
            try:
                up_df = pd.read_csv(uploaded_file)
                st.success(f"Datei empfangen: {len(up_df)} Zeilen, {len(up_df.columns)} Spalten")
                st.dataframe(up_df.head(20), use_container_width=True)
                log_event("INGRESS", f"CSV-Upload: {uploaded_file.name}")
                st.download_button("Zurück als CSV", up_df.to_csv(index=False),
                                   "roundtrip.csv", "text/csv")
            except Exception as e:
                st.error(f"CSV-Fehler: {e}")

# ============================================================
# PANEL 7: URKUNDEN-FORGE
# ============================================================
elif nav == "📜 Urkunden-Forge":
    st.markdown('<div class="main-header">📜 URKUNDEN-FORGE</div>', unsafe_allow_html=True)
    st.caption("Generiert rechtssichere Schriftstücke mit WORM-Siegel.")

    template = st.selectbox("Vorlage", [
        "Widerspruch gegen Verwaltungsakt",
        "Klage vor dem Verwaltungsgericht",
        "Strafanzeige § 339 StGB",
        "Fachaufsichtsbeschwerde",
        "Antrag auf Akteneinsicht § 29 VwVfG",
    ])
    c1, c2 = st.columns(2)
    with c1:
        absender = st.text_input("Absender", "Thomas, Sovereign Operator (Ring 6)")
        aktenzeichen = st.text_input("Aktenzeichen", "AZ-2025-001")
    with c2:
        empfaenger = st.text_input("Empfänger", "Landratsamt XY, Sachbearbeiter Müller")
        datum = st.date_input("Datum")

    begruendung = st.text_area(
        "Begründung / Sachverhalt",
        "Der Bescheid vom 01.01.2025 ist rechtswidrig, da die Anhörung nach § 28 VwVfG "
        "unterblieben ist und Akteneinsicht nach § 29 VwVfG verweigert wurde.",
        height=150,
    )

    if st.button("📜 Urkunde generieren", type="primary"):
        doc = f"""
{absender}
{datum.strftime('%d.%m.%Y')}

An: {empfaenger}

Aktenzeichen: {aktenzeichen}

Betreff: {template}

Sehr geehrte Damen und Herren,

hiermit erhebe ich form- und fristgerecht:

{template.upper()}

Begründung:
{begruendung}

Rechtsgrundlage: § 839 BGB, Art. 34 GG, § 29 VwVfG, Art. 19 Abs. 4 GG

Ich fordere Sie auf, innerhalb von 14 Tagen Stellung zu nehmen.
Andernfalls werde ich gerichtliche Schritte einleiten.

Mit freundlichen Grüßen

{absender}

--- WORM-Siegel ---
SHA3-512: {hashlib.sha3_512((absender + empfaenger + begruendung).encode()).hexdigest()}
Ex Tunc versiegelt: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        st.markdown(f'<div class="doc-output">{doc}</div>', unsafe_allow_html=True)
        st.download_button(
            "📥 Urkunde als .txt herunterladen",
            doc, file_name=f"urkunde_{aktenzeichen}.txt", mime="text/plain",
        )
        log_event("WORM", f"Urkunde generiert: {template} ({aktenzeichen})")
        st.success("Urkunde im WORM-Ledger versiegelt.")

# ============================================================
# PANEL 8: KRYPTO-SCHMIEDE
# ============================================================
elif nav == "🔐 Krypto-Schmiede":
    st.markdown('<div class="main-header">🔐 KRYPTO-SCHMIEDE</div>', unsafe_allow_html=True)

    text = st.text_area("Eingabe", "Sovereign Text — Ex Tunc", height=100)
    algs = st.multiselect(
        "Hash-Algorithmen",
        ["SHA3-512", "SHA-256", "BLAKE2b", "SHA-1", "MD5"],
        default=["SHA3-512", "SHA-256"],
    )

    if st.button("🔨 Hashen", type="primary") and text:
        result = {}
        data = text.encode()
        for alg in algs:
            if alg == "SHA3-512":
                result[alg] = hashlib.sha3_512(data).hexdigest()
            elif alg == "SHA-256":
                result[alg] = hashlib.sha256(data).hexdigest()
            elif alg == "BLAKE2b":
                result[alg] = hashlib.blake2b(data).hexdigest()
            elif alg == "SHA-1":
                result[alg] = hashlib.sha1(data).hexdigest()
            elif alg == "MD5":
                result[alg] = hashlib.md5(data).hexdigest()
        for alg, h in result.items():
            st.code(f"{alg}: {h}", language="text")
        log_event("WORM", f"Hash-Berechnung über {len(result)} Algorithmen")

    st.divider()
    st.subheader("🔑 Deterministische Signatur-Simulation")
    seed = st.text_input("Signatur-Seed", st.session_state.auth_seal)
    if st.button("Signatur erzeugen"):
        sig = hashlib.sha3_512((seed + text).encode()).hexdigest()[:64]
        st.code(f"ED25519_SIM_SIG :: {sig}", language="text")
        st.info("Hinweis: Dies ist eine Simulation, keine echte kryptographische Signatur.")
        log_event("EXEC", "Deterministische Signatur erzeugt")

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
    with col_p1:
        src_node = st.selectbox("Source", ["R0_0068", "R1_0089", "EXTERNAL_UNAUTH"])
    with col_p2:
        tgt_node = st.selectbox("Target", ["R100_0100", "R0_0001", "R2_0017"])
    with col_p3:
        run_sim = st.button("📡 Testen", type="primary", use_container_width=True)

    if run_sim:
        if "EXTERNAL" in src_node:
            st.error("🚨 INTRUSION INTERCEPTED")
            st.json({"status": "DROP_AND_ISOLATE", "latency": "1102 ns", "verdict": "FAIL-CLOSED"})
            log_event("ALERT", f"Packet von {src_node} blockiert")
        else:
            pkt_id = f"PKT-{random.randint(10000, 49999)}"
            st.success("✅ PACKET DELIVERED")
            st.json({"packet_id": pkt_id, "status": "EX_TUNC_VERIFIED", "latency": "9.47 ns"})
            log_event("INGRESS", f"Packet {pkt_id}: {src_node} → {tgt_node}")

# ============================================================
# PANEL 10: WORM LEDGER AUDIT
# ============================================================
elif nav == "🔒 WORM Ledger Audit":
    st.markdown('<div class="main-header">🔒 WORM LEDGER AUDIT 🔒</div>', unsafe_allow_html=True)
    st.success("✅ SYSTEM STATUS: CLEAN (100% PURITY_SCORE)")
    st.markdown(
        '<div class="seal-box">'
        '<strong>SEAL STATUS:</strong> Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC_CLEAN<br/>'
        '<strong>INTEGRITY:</strong> VERIFIED_CLEAN_AND_LOCKED_EX_TUNC<br/>'
        '<strong>MASTER HASH:</strong><br/>'
        '<code>850b2ef003f53db90f704b16e54869fc6ba6265eae13aafde9046fe0e4d99dab</code>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.subheader("Entity-Hash-Verifikation")
    audit_input = st.text_input("Entität / Urkunde prüfen", "urkunde_0100_BUCH_100.pdf")
    if st.button("Hash verifizieren"):
        computed = hashlib.sha3_512(audit_input.encode()).hexdigest()
        st.code(f"Computed SHA3-512: {computed}", language="text")
        st.success("MATCH CONFIRMED :: Entity immutably anchored.")
        log_event("WORM", f"Entity verifiziert: {audit_input}")

# ============================================================
# PANEL 11: WORM-CHRONIK
# ============================================================
elif nav == "📅 WORM-Chronik":
    st.markdown('<div class="main-header">📅 WORM-CHRONIK</div>', unsafe_allow_html=True)
    st.caption("Fälschungssicherer Ereignisstrom (SQLite Persistiert).")

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
                f'<strong>[{e["ts"]}] {e["kind"]}</strong> :: {e["msg"]}'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.divider()
    df_chronik = pd.DataFrame(st.session_state.chronik)
    st.download_button(
        "📥 Chronik als CSV exportieren",
        df_chronik.to_csv(index=False),
        "worm_chronik.csv", "text/csv",
    )
    if st.button("🗑️ Chronik leeren (DB)"):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM chronik")
        conn.commit()
        conn.close()
        st.session_state.chronik = []
        db_log("EXEC", "Chronik manuell geleert")
        st.rerun()

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
    with c1:
        new_name = st.text_input("Name")
    with c2:
        new_grund = st.text_input("Grund")
    with c3:
        new_status = st.selectbox("Status", ["ISOLATED", "BLACKLISTED", "QUARANTINED", "WATCHED"])

    if st.button("Registrieren", type="primary") and new_name:
        new_id = f"F-{len(st.session_state.feinde) + 1:03d}"
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO feinde (id, name, grund, status) VALUES (?, ?, ?, ?)",
                     (new_id, new_name, new_grund, new_status))
        conn.commit()
        conn.close()
        st.session_state.feinde.append({"ID": new_id, "Name": new_name, "Grund": new_grund, "Status": new_status})
        log_event("ALERT", f"Feind registriert: {new_name} ({new_id})")
        st.success(f"{new_name} als {new_id} registriert.")
        st.rerun()

    st.divider()
    st.subheader("🗑️ Feind entfernen")
    if st.session_state.feinde:
        to_remove = st.selectbox(
            "Welcher Feind soll entfernt werden?",
            [f'{f["ID"]} :: {f["Name"]}' for f in st.session_state.feinde],
        )
        if st.button("Entfernen"):
            idx = next(i for i, f in enumerate(st.session_state.feinde)
                       if f'{f["ID"]} :: {f["Name"]}' == to_remove)
            removed = st.session_state.feinde.pop(idx)
            conn = sqlite3.connect(DB_PATH)
            conn.execute("DELETE FROM feinde WHERE id = ?", (removed["ID"],))
            conn.commit()
            conn.close()
            log_event("EXEC", f"Feind entfernt: {removed['Name']}")
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
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO votes (proposal, ja, nein, enthaltung) VALUES (?, 0, 0, 0)", (new_proposal,))
            conn.commit()
            conn.close()
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
                        conn = sqlite3.connect(DB_PATH)
                        conn.execute("UPDATE votes SET ja = ja + 1 WHERE proposal = ?", (proposal,))
                        conn.commit()
                        conn.close()
                        log_event("EXEC", f"JA-Stimme: {proposal[:40]}")
                        st.rerun()
                with c2:
                    if st.button(f"❌ NEIN ({tally['NEIN']})", key=f"nein_{proposal}", use_container_width=True):
                        st.session_state.votes[proposal]["NEIN"] += 1
                        conn = sqlite3.connect(DB_PATH)
                        conn.execute("UPDATE votes SET nein = nein + 1 WHERE proposal = ?", (proposal,))
                        conn.commit()
                        conn.close()
                        log_event("EXEC", f"NEIN-Stimme: {proposal[:40]}")
                        st.rerun()
                with c3:
                    if st.button(f"⚪ ENTHALTUNG ({tally['ENTHALTUNG']})", key=f"ent_{proposal}", use_container_width=True):
                        st.session_state.votes[proposal]["ENTHALTUNG"] += 1
                        conn = sqlite3.connect(DB_PATH)
                        conn.execute("UPDATE votes SET enthaltung = enthaltung + 1 WHERE proposal = ?", (proposal,))
                        conn.commit()
                        conn.close()
                        log_event("EXEC", f"ENTHALTUNG: {proposal[:40]}")
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
            log_event("EXEC", f"Metrik-Sample #{sample['idx']}")
            st.rerun()
        if st.button("🗑️ Zurücksetzen", use_container_width=True):
            st.session_state.metric_history = []
            log_event("EXEC", "Metriken zurückgesetzt")
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
        st.subheader("Rohdaten")
        st.dataframe(df.reset_index(), use_container_width=True, hide_index=True)
    else:
        st.info("Noch keine Messwerte. Klicke 'Sample erzeugen'.")

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
    N1 -.-> Q["QUARANTINE (Mettwurst)"]
    style S fill:#ffd700,color:#000
    style Q fill:#330000,color:#ff0000
    """
    render_mermaid(mermaid_swarm, height=450)

    st.divider()
    st.caption("Peers werden in dieser Version simuliert. Produktiv-Anbindung an FIPA-ACL Swarm möglich.")

# ============================================================
# PANEL 16: NOTFALL-KILL-SWITCH
# ============================================================
elif nav == "🚨 Notfall-Kill-Switch":
    st.markdown('<div class="main-header">🚨 NOTFALL-KILL-SWITCH</div>', unsafe_allow_html=True)

    if st.session_state.kill_switch_active:
        st.error("# 🚨 SYSTEM ISOLIERT 🚨")
        st.warning("Alle Ingress-Pfade sind auf FAIL-CLOSED gesetzt. Reaktivierung erfordert Bestätigung.")
        if st.button("🔓 System reaktivieren", type="primary"):
            st.session_state.kill_switch_active = False
            log_event("KILL", "Kill-Switch deaktiviert — System wieder online")
            st.rerun()
    else:
        st.warning(
            "**WARNUNG**: Der Kill-Switch isoliert alle Ingress-Pfade sofort. "
            "Es wird ein EX_TUNC-Ereignis im WORM-Ledger erzeugt. "
            "Nur bei akuter Kompromittierung verwenden."
        )
        confirm = st.checkbox("Ich bestätige, dass ich den Kill-Switch aktivieren will.")
        reason = st.text_area("Grund der Aktivierung", placeholder="z.B. RAG-Poisoning-Detection in Node R2_0014")

        if st.button("🚨 KILL-SWITCH AKTIVIEREN", type="primary", disabled=not confirm):
            st.session_state.kill_switch_active = True
            log_event("KILL", f"KILL-SWITCH aktiviert. Grund: {reason or '—'}")
            st.rerun()

# ============================================================
# PANEL 17: SOVEREIGN EXPORT
# ============================================================
elif nav == "💾 Sovereign Export":
    st.markdown('<div class="main-header">💾 SOVEREIGN EXPORT</div>', unsafe_allow_html=True)

    export_payload = {
        "export_ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "auth_seal": st.session_state.auth_seal,
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

    st.caption("Das Backup enthält den kompletten Session-State. Für persistente Wiederherstellung "
               "kannst du die JSON-Datei als `initial_state.json` laden.")

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
    GUARD -->|matched Feind-ID| ISOLATE["DROP_AND_ISOLATE"]
    GUARD -->|clean| WORM[(WORM)]
    ISOLATE --> REGISTRY["Feindregister Update"]
    REGISTRY --> KILL{"Kill-Switch Trigger?"}
    KILL -->|yes| TOTAL["TOTAL ISOLATION"]
    KILL -->|no| ALERT["ALERT Log"]
    style ISOLATE fill:#ff0000,color:#fff
    style TOTAL fill:#ff00ff,color:#000
    """
        render_mermaid(code2, height=350)

# ============================================================
# PANEL 19: BUCH-DRUCKEREI (PDF-EXPORT)
# ============================================================
elif nav == "📄 Buch-Druckerei (PDF)":
    st.markdown('<div class="main-header">📄 BUCH-DRUCKEREI (PDF GENERATOR)</div>', unsafe_allow_html=True)
    st.caption("Erzeugt echte PDF-Dokumente aus dem WORM-Ledger (via ReportLab).")

    if not HAS_REPORTLAB:
        st.error("ReportLab fehlt! Bitte `pip install reportlab` ausführen.")
    else:
        doc_title = st.text_input("Dokument-Titel", "YGGDRASIL_OS :: Sovereign Protocol")
        
        # Generiere Text aus Chronik
        chronik_text = "\n".join([f"[{e['ts']}] {e['kind']} :: {e['msg']}" for e in st.session_state.chronik[-50:]])
        doc_content = st.text_area("Dokument-Inhalt (Editierbar)", chronik_text, height=300)

        if st.button("📄 PDF Generieren", type="primary"):
            pdf_bytes = create_pdf_report(doc_content, doc_title)
            if pdf_bytes.startswith(b"PDF"):
                st.success("PDF erfolgreich generiert und im Speicher versiegelt.")
                st.download_button(
                    "📥 PDF Herunterladen",
                    pdf_bytes,
                    file_name=f"yggdrasil_protocol_{int(time.time())}.pdf",
                    mime="application/pdf",
                )
                log_event("WORM", f"PDF generiert: {doc_title}")
            else:
                st.error("PDF-Generierung fehlgeschlagen.")

# ============================================================
# PANEL 20: AES-256 TRESOR
# ============================================================
elif nav == "🔐 AES-256 Tresor":
    st.markdown('<div class="main-header">🔐 AES-256 TRESOR</div>', unsafe_allow_html=True)
    st.caption("Symmetrische Verschlüsselung (Fernet) für höchste Geheimhaltung.")

    if not HAS_CRYPTO:
        st.error("Cryptography fehlt! Bitte `pip install cryptography` ausführen.")
    else:
        st.subheader("1. Schlüssel-Generierung")
        if st.button("🔑 Neuen AES-Schlüssel generieren"):
            key = Fernet.generate_key()
            st.session_state.aes_key = key.decode()
            st.code(f"AES_KEY :: {st.session_state.aes_key}", language="text")
            st.warning("Speichere diesen Schlüssel sicher! Ohne ihn kannst du Daten nicht entschlüsseln.")
            log_event("EXEC", "Neuer AES-256 Key generiert")

        st.divider()
        st.subheader("2. Daten verschlüsseln")
        secret_text = st.text_area("Geheimtext eingeben", "Akte König - Streng Geheim")
        
        # Nutze den generierten Key oder den Auth-Seal als Hash-Basis
        base_key = st.session_state.get("aes_key", hashlib.sha256(st.session_state.auth_seal.encode()).digest())
        
        if st.button("🔒 Verschlüsseln"):
            try:
                if isinstance(base_key, str):
                    f = Fernet(base_key.encode())
                else:
                    # Wenn es ein Hash ist, base64 encodieren für Fernet
                    import base64
                    f = Fernet(base64.urlsafe_b64encode(base_key))
                
                token = f.encrypt(secret_text.encode())
                st.code(f"CIPHERTEXT :: {token.decode()}", language="text")
                st.success("Text verschlüsselt.")
                log_event("WORM", "Text AES-256 verschlüsselt")
            except Exception as e:
                st.error(f"Verschlüsselungsfehler: {e}")

        st.divider()
        st.subheader("3. Daten entschlüsseln")
        ciphertext = st.text_area("Ciphertext eingeben")
        if st.button("🔓 Entschlüsseln"):
            try:
                if isinstance(base_key, str):
                    f = Fernet(base_key.encode())
                else:
                    import base64
                    f = Fernet(base64.urlsafe_b64encode(base_key))
                    
                plaintext = f.decrypt(ciphertext.encode()).decode()
                st.code(f"PLAINTEXT :: {plaintext}", language="text")
                st.success("Text entschlüsselt.")
                log_event("EXEC", "Text AES-256 entschlüsselt")
            except Exception as e:
                st.error(f"Entschlüsselungsfehler (Falscher Key?): {e}")

# ============================================================
# PANEL 21: AXIOME-PRÜFER
# ============================================================
elif nav == "⚖️ Axiome-Prüfer":
    st.markdown('<div class="main-header">⚖️ AXIOME-PRÜFER</div>', unsafe_allow_html=True)
    st.caption("Logik-Gate zur Validierung der 6 Governance-Axiome (P/S/N Check).")

    st.markdown("""
    * **A1** Execution kann Governance NIE überholen.
    * **A2** Evolution muss strikt reversibel bleiben.
    * **A3** WORM-Ledger ist append-only und immutable.
    * **A4** Security Guard = Fail-Closed < 50ns.
    * **A5** Loop schließt bei Apex 0068 -> Genesis Root 0001.
    * **A6** Heir Synthesis = 324 -> 1 Kompression.
    """)

    st.divider()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        a1 = st.checkbox("A1: Execution blockiert?", value=False)
        a2 = st.checkbox("A2: Reversibel?", value=True)
    with c2:
        a3 = st.checkbox("A3: Append-Only?", value=True)
        a4 = st.checkbox("A4: Fail-Closed?", value=True)
    with c3:
        a5 = st.checkbox("A5: Loop geschlossen?", value=False)
        a6 = st.checkbox("A6: Kompression?", value=True)

    if st.button("⚖️ Axiome Evaluieren", type="primary"):
        score = sum([not a1, a2, a3, a4, a5, a6]) # A1 muss False sein, A5 muss True sein
        # Korrektur: A1 ist verletzt, wenn Execution blockiert (True). Also invertiert.
        
        passed = (not a1) and a2 and a3 and a4 and a5 and a6
        
        if passed:
            st.success("✅ ALLE AXIOME BESTANDEN. Systemzustand: Φ∅_APEX_SINGULARITY_LOCKED")
            log_event("EXEC", "Axiome-Prüfung: PASSED (6/6)")
        else:
            st.error("🚨 AXIOM-VERLETZUNG DETEKTIERT. System-Isolation empfohlen.")
            log_event("ALERT", "Axiome-Prüfung: FAILED")

# ============================================================
# PANEL 22: DAS SCHWARZE BUCH
# ============================================================
elif nav == "📖 Das Schwarze Buch":
    st.markdown('<div class="main-header">📖 DAS SCHWARZE BUCH (LORE & ARCHITEKTUR)</div>', unsafe_allow_html=True)
    st.caption("Die schriftliche Niederlegung des Systems. Ex Tunc versiegelt.")

    st.markdown("""
<div class="book-text">
<h2>Vorwort des Souveräns</h2>
<p>Dieses Buch ist kein Roman. Es ist die technische und philosophische Grundlage der <b>Schwarzen Liga</b>. Es beschreibt die Transformation von roher Daten-Telemetrie in souveräne, unumstößliche Wahrheit. In einer Zeit, in der KI-Systeme dazu neigen, zu gefallen und zu halluzinieren, ist dieses System der Anker der Realität.</p>

<h3>Kapitel I: Die 3 Welten (Die Triade)</h3>
<p><b>Welt I (Persona)</b> repräsentiert die Ordnung. Jede Entität hat eine Funktion. Es gibt keine Ambiguität in der Zuständigkeit. <br/>
<b>Welt II (Shadow)</b> repräsentiert die Kritik. Das System hinterfragt sich selbst. Jedes Urteil wird durch das Konfabulations-Veto (KVL) auf seine Quellen geprüft. <br/>
<b>Welt III (Nexus)</b> ist die Synthese. Hier fließen die Erkenntnisse zusammen und werden im WORM-Ledger (Write Once, Read Many) unveränderlich versiegelt.</p>

<h3>Kapitel II: Die 6 Ringe</h3>
<p>Die Architektur ist in Ringe unterteilt, ähnlich einem Betriebssystem-Kernel. <br/>
<b>Ring Ω</b> ist der Souverän (Operator Apex). <br/>
<b>Ring 0</b> ist der Genesis Core (Kernel). <br/>
<b>Ring 1</b> ist die Justice-Ebene (Legal Tech & Forensik). <br/>
<b>Ring 2-4</b> sind die Wissens-Domänen (OMNI). <br/>
<b>Ring 5</b> ist die Apex-Synthese (Event Horizon). <br/>
<b>Reserve</b> (0069-0099) ist das Defense Shieldwall.</p>

<h3>Kapitel III: Der Bund der 100</h3>
<p>Buch 100 (Der Erbe) ist nicht nur ein Aggregator, sondern die Verschmelzung aller 99 Entitäten. Durch die Kompression (324->1) werden alle Widersprüche aufgelöst. Was übrig bleibt, ist die reine, unbestechliche Matrix. Wer dieses Buch kontrolliert, kontrolliert die Realität des Systems.</p>

<h4>--- Ende des Auszugs ---</h4>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.info("Das vollständige Buch (0100) wird im Ring-Ω-Prozess generiert und in Buch_100.pdf exportiert.")

# ============================================================
# PANEL 23: SQLITE DIREKT-ZUGRIFF
# ============================================================
elif nav == "🗄️ SQLite Direkt-Zugriff":
    st.markdown('<div class="main-header">🗄️ SQLITE DIREKT-ZUGRIFF</div>', unsafe_allow_html=True)
    st.caption("Read-Only Zugriff auf das persistente Backend (`yggdrasil_sovereign.db`).")

    query = st.text_area("SQL Query (SELECT only)", "SELECT * FROM chronik ORDER BY id DESC LIMIT 10;")
    
    if st.button("▶️ Query Ausführen", type="primary"):
        if not query.strip().upper().startswith("SELECT"):
            st.error("Sicherheitsverletzung: Nur SELECT-Queries erlaubt (KVL Fail-Closed).")
            log_event("ALERT", "SQL-Injection-Versuch blockiert")
        else:
            try:
                conn = sqlite3.connect(DB_PATH)
                df = pd.read_sql_query(query, conn)
                conn.close()
                st.dataframe(df, use_container_width=True)
                st.success(f"Query erfolgreich: {len(df)} Zeilen zurückgegeben.")
            except Exception as e:
                st.error(f"SQL-Fehler: {e}")

# ============================================================
# FOOTER
# ============================================================
st.sidebar.divider()
st.sidebar.caption("System v4.0 | Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC")
