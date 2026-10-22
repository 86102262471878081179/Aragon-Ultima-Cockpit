import streamlit as st
import httpx

st.set_page_config(page_title="Aragon Ultima", layout="centered")
st.title("👑 Aragon Ultima Cockpit")
st.write("Operator-Modus aktiv. WORM-Ledger & 68 Bücher verbunden.")

prompt = st.text_input("Operator-Prompt:", placeholder="Frage nach Buch 0001 oder Black King...")

if st.button("Exekutieren"):
    if prompt:
        try:
            api_url = "https://aragon-backend-api.onrender.com/prompt/check"
            
            response = httpx.post(api_url, json={"prompt": prompt}, timeout=50.0)
            data = response.json()
            
            # Status dynamisch einfärben
            risk = data.get('risk_level', 'UNKNOWN').upper()
            if risk == "HIGH":
                st.error(f"Status: {risk} (BEDROHUNG ERKANNT)")
            else:
                st.success(f"Status: {risk} (SICHER)")
                
            st.write(f"Aktion: {data.get('action')}")
            st.info(f"Antwort: {data.get('normalized_prompt')}")
            
            # Buch-Ergebnis anzeigen
            book = data.get("book_search_result")
            if book:
                st.markdown("### 📚 Buch-Gefunden")
                st.write(f"**ID:** {book.get('id')}")
                st.write(f"**Titel:** {book.get('name')}")
                st.write(f"**Ring:** {book.get('ring')}")
                st.write(f"**Status:** {book.get('status')}")
            elif "buch" in prompt.lower():
                st.warning("Kein Buch in der Registry gefunden (nur Test-Bücher 0001, 0002, 0007, 0023, 0068 aktiv).")
            
            # WORM Ledger Daten ausgeben
            worm = data.get("worm_ledger", {})
            if worm:
                st.markdown("### 🔐 WORM-Ledger & Master Seal")
                st.code(f"Node: {worm.get('node_id')}\nSHA3-512: {worm.get('sha3_512')}\nMaster-Seal: {worm.get('master_seal')}", language="json")
                
        except Exception as e:
            st.error(f"Matrix-Verbindung fehlgeschlagen: {e}")
    else:
        st.warning("Bitte gib einen Prompt ein!")
