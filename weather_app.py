import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Samrat Chatbot", page_icon="👑")
st.title("\tThe Great Samrat Dhakal")
st.subheader("Enjoy Boys And Girls : Have Fun With AI")

# 2. Configure API Key
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash') 
except Exception as e:
    st.error("Error: Could not configure Gemini API. Check your Streamlit Secrets.")
    st.stop()

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle Chat Input
if prompt := st.chat_input("Ask me anything..."):
    # Display and Save User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Maintain chat history by passing existing messages
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]
                ])
                
                response = chat.send_message(prompt)
                ai_response = response.text
                
                # Display and Save Assistant Response
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
