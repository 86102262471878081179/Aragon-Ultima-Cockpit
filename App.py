import streamlit as st
import httpx

st.set_page_config(page_title="Aragon Ultima", layout="centered")
st.title("👑 Aragon Ultima Cockpit")
st.write("Gib deinen Befehl ein. Der Krisler-Guard prüft ihn.")

prompt = st.text_input("Operator-Prompt:", placeholder="z.B. Status der 68 Bücher...")

if st.button("Exekutieren"):
    if prompt:
        try:
            # Platzhalter für deine echte FastAPI/K8s URL
            response = httpx.post("http://localhost:8000/prompt/check", json={"prompt": prompt}, timeout=5.0)
            data = response.json()
            
            st.success(f"Status: {data.get('risk_level', 'UNKNOWN').upper()}")
            st.write(f"Aktion: {data.get('action')}")
            st.info(f"Antwort: {data.get('normalized_prompt')}")
            
        except Exception as e:
            st.error(f"Matrix-Verbindung fehlgeschlagen: {e}")
    else:
        st.warning("Bitte gib einen Prompt ein!")
