import streamlit as st
import httpx

st.set_page_config(page_title="Aragon Ultima", layout="centered")
st.title("👑 Aragon Ultima Cockpit")
st.write("Operator-Modus aktiv. WORM-Ledger & 100 Entitäten verbunden.")

prompt = st.text_input("Operator-Prompt:", placeholder="Frage nach Buch 0001, 0068 oder 0100...")

if st.button("Exekutieren"):
    if prompt:
        try:
            api_url = "https://aragon-backend-api.onrender.com/prompt/check"
            
            # Das Auth-Seal MUSS mitgeschickt werden für den Fail-Closed Check
            payload = {
                "prompt": prompt,
                "auth_seal": "Φ_SOVEREIGN_ROOT_SEAL_EX_TUNC"
            }
            
            with st.spinner("Matrix wird abgefragt..."):
                response = httpx.post(api_url, json=payload, timeout=60.0)
            
            data = response.json()
            
            # 1. STATUS CHECK (Fail-Closed oder OK)
            status = data.get("status", "UNKNOWN")
            if status == "200_OK_ALLOW":
                st.success(f"Status: {status} (SICHER)")
                st.write(f"Guard Aktion: {data.get('krisler_guard_action')}")
                st.write(f"Routing zu Hub: `{data.get('target_hub')}`")
                st.write(f"eBPF Latenz: {data.get('ebpf_latency_ns')} ns")
            else:
                st.error(f"Status: {status} (BEDROHUNG ERKANNT)")
                st.write(f"Guard Aktion: {data.get('krisler_guard_action')}")
                st.error(f"Detail: {data.get('detail')}")
                st.stop() # Stoppt die weitere Ausführung, wenn blockiert wurde

            # 2. DATEN AUSLESEN (Verschachtelt unter "data")
            core_data = data.get("data", {})
            
            # KI-Antwort anzeigen
            if core_data.get("ai_answer"):
                st.markdown("### 🧠 KI-Antwort:")
                st.success(core_data.get("ai_answer"))
            
            # Buch-Ergebnisse anzeigen
            books = core_data.get("books_found")
            if books:
                st.markdown("### 📚 Bücher Gefunden:")
                for book in books:
                    b_id = str(book.get("id", ""))
                    b_name = str(book.get("name", ""))
                    b_ring = str(book.get("ring", ""))
                    b_score = str(book.get("score", ""))
                    st.write(f"**ID:** {b_id} | **Titel:** {b_name} | **Ring:** {b_ring} | **Score:** {b_score}")
            elif "buch" in prompt.lower():
                st.warning("Kein Buch in der Registry gefunden (prüfe Schreibweise oder ID).")
            
            # WORM Ledger Daten ausgeben
            worm = core_data.get("worm_ledger", {})
            if worm:
                st.markdown("### 🔐 WORM-Ledger & Master Seal")
                ledger_text = f"Node: NB-090_BLACK_COBRA_OMEGA\nSHA3-512: {worm.get('hash')}\nMaster-Seal: {worm.get('master_seal')}\nTimestamp: {worm.get('timestamp')}"
                st.code(ledger_text, language="json")
                
        except Exception as e:
            st.error("Matrix-Verbindung fehlgeschlagen: " + str(e))
    else:
        st.warning("Bitte gib einen Prompt ein!")
