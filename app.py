import streamlit as st
import httpx

st.set_page_config(page_title="Aragon Ultima", layout="centered")
st.title("👑 Aragon Ultima Cockpit")
st.write("Operator-Modus aktiv. WORM-Ledger & 68 Bücher verbunden.")

prompt = st.text_input("Operator-Prompt:", placeholder="Frage nach Buch 0002, Mettwurst oder Hades...")

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
            
            # Buch-Ergebnisse anzeigen (Liste)
            books = data.get("books_found")
            if books:
                st.markdown("### 📚 Bücher Gefunden:")
                for book in books:
                    st.write(f"**ID:** {book.get('id')} | **Titel:** {book.get('name')} | **Ring:** {book.get('ring')} | **Status:** {book.get('status')}")
            elif "buch" in prompt.lower():
                st.warning("Kein Buch in der Registry gefunden (prüfe Schreibweise).")
            
            # WORM Ledger Daten ausgeben
            worm = data.get("worm_ledger", {})
            if worm:
                st.markdown("### 🔐 WORM-Ledger & Master Seal")
                st.code(f"Node: {worm.get('node_id')}\nSHA3-512: {worm.get('sha3_512')}\nMaster-Seal: {worm.get('master_seal')}", language="json")
                
        except Exception as e:
            st.error(f"Matrix-Verbindung fehlgeschlagen: {e}")
    else:
        st.warning("Bitte gib einen Prompt ein!")
