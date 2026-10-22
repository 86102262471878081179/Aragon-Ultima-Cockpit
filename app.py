try:
            # DEINE LIVE RENDER URL
            api_url = "https://aragon-backend-api.onrender.com/prompt/check"
            
            response = httpx.post(api_url, json={"prompt": prompt}, timeout=50.0)
            data = response.json()
            
            st.success(f"Status: {data.get('risk_level', 'UNKNOWN').upper()}")
            st.write(f"Aktion: {data.get('action')}")
            st.info(f"Antwort: {data.get('normalized_prompt')}")
            
        except Exception as e:
            st.error(f"Matrix-Verbindung fehlgeschlagen: {e}")
