import streamlit as st
import google.generativeai as genai
from tenacity import retry, wait_random_exponential, stop_after_attempt

# 1. Page Configuration (Mandatory as per your requirement)
st.set_page_config(page_title="Samrat Chatbot", page_icon="👑")
st.title("The Great Samrat Dhakal")
st.subheader("Enjoy Boys And Girls : Have Fun With AI")

# 2. Configure API Key
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Using the current stable model
    model = genai.GenerativeModel('gemini-2.5-flash') 
except Exception as e:
    st.error("Error: Could not configure Gemini API. Check your Streamlit Secrets.")
    st.stop()

# 3. Retry Logic for 429 Errors
# This automatically waits and retries if you hit rate limits
@retry(wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
def get_ai_response(chat_session, prompt):
    return chat_session.send_message(prompt)

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display History
for msg in st.session_state.messages:
    role = "assistant" if msg["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(msg["content"])

# 6. Handle Chat Input
if prompt := st.chat_input("K Sodni Ho :Yehi Lekh"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Rok Ekxin:Sochi Rachu"):
            try:
                # Prepare history (Gemini requires 'model' role, not 'assistant')
                history = [
                    {"role": "model" if m["role"] == "model" else "user", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ]
                chat = model.start_chat(history=history)
                
                # Use the retry-enabled function
                response = get_ai_response(chat, prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"An error occurred: {e}")