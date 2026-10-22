import streamlit as st
import httpx

st.set_page_config(page_title="Aragon Ultima", layout="centered")
st.title("👑 Aragon Ultima Cockpit")
st.write("Gib deinen Befehl ein. Der Krisler-Guard prüft ihn.")

prompt = st.text_input("Operator-Prompt:", placeholder="z.B. Status der 68 Bücher...")

if st.button("Exekutieren"):
    if prompt:
        try:
            # DEINE ECHTE RENDER URL
            api_url = "https://aragon-backend-api.onrender.com/prompt/check"
            
            response = httpx.post(api_url, json={"prompt": prompt}, timeout=50.0)
            data = response.json()
            
            st.success(f"Status: {data.get('risk_level', 'UNKNOWN').upper()}")
            st.write(f"Aktion: {data.get('action')}")
            st.info(f"Antwort: {data.get('normalized_prompt')}")
            
        except Exception as e:
            st.error(f"Matrix-Verbindung fehlgeschlagen: {e}")
    else:
        st.warning("Bitte gib einen Prompt ein!")
