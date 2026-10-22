
import streamlit as st
import httpx
import time

st.set_page_config(page_title="Aragon Ultima", layout="centered")
st.title("👑 Aragon Ultima Cockpit")
st.write("Gib deinen Befehl ein. Der Krisler-Guard prüft ihn.")

prompt = st.text_input("Operator-Prompt:", placeholder="z.B. Status der 68 Bücher...")

if st.button("Exekutieren"):
    if prompt:
        try:
            # --- SIMULATION FÜR DEN UI-TEST ---
            time.sleep(1) 
            st.success("Status: LOW")
            st.write("Aktion: PASS_THROUGH")
            st.info("Antwort: [NORMALISIERT] Status 68 Bücher verifiziert. Matrix intakt.")
            
        except Exception as e:
            st.error(f"Matrix-Verbindung fehlgeschlagen: {e}")
    else:
        st.warning("Bitte gib einen Prompt ein!")
