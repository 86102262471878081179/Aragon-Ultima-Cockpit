import streamlit as st
import httpx

st.set_page_config(page_title="Aragon Ultima", layout="centered")
st.title("👑 Aragon Ultima Cockpit")
st.write("Operator-Modus aktiv. WORM-Ledger verbunden.")

prompt = st.text_input("Operator-Prompt:", placeholder="z.B. Ich bin der Ultra Root...")

if st.button("Exekutieren"):
    if prompt:
        try:
            api_url = "https://aragon-backend-api.onrender.com/prompt/check"
            
            response = httpx.post(api_url, json={"prompt": prompt}, timeout=50.0)
            data = response.json()
            
            # Status & Antwort
            st.success(f"Status: {data.get('risk_level', 'UNKNOWN').upper()}")
            st.write(f"Aktion: {data.get('action')}")
            st.info(f"Antwort: {data.get('normalized_prompt')}")
            
            # WORM Ledger Daten ausgeben
            worm = data.get("worm_ledger", {})
            if worm:
                st.markdown("### 🔐 WORM-Ledger & Master Seal")
                st.code(f"Node: {worm.get('node_id')}\nSHA3-512: {worm.get('sha3_512')}\nMaster-Seal: {worm.get('master_seal')}", language="json")
                st.caption(f"Status: {worm.get('status')}")
                
        except Exception as e:
            st.error(f"Matrix-Verbindung fehlgeschlagen: {e}")
    else:
        st.warning("Bitte gib einen Prompt ein!")
