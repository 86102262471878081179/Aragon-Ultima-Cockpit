import streamlit as st
import httpx

st.set_page_config(page_title="Aragon Ultima", layout="centered")
st.title("👑 Aragon Ultima Cockpit")
st.write("Operator-Modus aktiv. WORM-Ledger & 68 Bücher verbunden.")

prompt = st.text_input("Operator-Prompt:", placeholder="Frage nach Buch 0001, Mettwurst oder Hades...")

if st.button("Exekutieren"):
    if prompt:
        try:
            api_url = "https://aragon-backend-api.onrender.com/prompt/check"
            
            response = httpx.post(api_url, json={"prompt": prompt}, timeout=50.0)
            data = response.json()
            
            # Werte aus dem JSON holen
            risk = str(data.get("risk_level", "UNKNOWN")).upper()
            action = str(data.get("action", ""))
            antwort_text = str(data.get("normalized_prompt", ""))
            
            # Status anzeigen (ohne verschachtelte Anführungszeichen)
            if risk == "HIGH":
                st.error("Status: " + risk + " (BEDROHUNG ERKANNT)")
            else:
                st.success("Status: " + risk + " (SICHER)")
                
            st.write("Aktion: " + action)
            st.info("Antwort: " + antwort_text)
            
            # ==========================================
            # HIER IST DER NEUE KI-BLOCK (RAG)
            # ==========================================
            if data.get("ai_answer"):
                st.markdown("### 🧠 KI-Antwort:")
                st.success(data.get("ai_answer"))
            # ==========================================
            
            # Buch-Ergebnisse anzeigen
            books = data.get("books_found")
            if books:
                st.markdown("### 📚 Bücher Gefunden:")
                for book in books:
                    b_id = str(book.get("id", ""))
                    b_name = str(book.get("name", ""))
                    b_ring = str(book.get("ring", ""))
                    b_status = str(book.get("status", ""))
                    st.write("**ID:** " + b_id + " | **Titel:** " + b_name + " | **Ring:** " + b_ring + " | **Status:** " + b_status)
            elif "buch" in prompt.lower():
                st.warning("Kein Buch in der Registry gefunden (prüfe Schreibweise oder ID).")
            
            # WORM Ledger Daten ausgeben
            worm = data.get("worm_ledger", {})
            if worm:
                st.markdown("### 🔐 WORM-Ledger & Master Seal")
                node = str(worm.get("node_id", ""))
                sha = str(worm.get("sha3_512", ""))
                seal = str(worm.get("master_seal", ""))
                status = str(worm.get("status", ""))
                
                ledger_text = "Node: " + node + "\nSHA3-512: " + sha + "\nMaster-Seal: " + seal
                st.code(ledger_text, language="json")
                st.caption("Status: " + status)
                
        except Exception as e:
            st.error("Matrix-Verbindung fehlgeschlagen: " + str(e))
    else:
        st.warning("Bitte gib einen Prompt ein!")
