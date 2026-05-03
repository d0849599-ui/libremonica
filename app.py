import streamlit as st
from huggingface_hub import InferenceClient

# 1. We define the token as a string (with quotes)
# Based on Screenshot 2026-05-03 at 07.02.33.jpg, your Sovereign_Full token starts with hf_...
HF_TOKEN = "hf_...FMlQ" 
MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"

# 2. Pass the variable HF_TOKEN here, not the raw text
client = InferenceClient(api_key=HF_TOKEN)

st.set_page_config(page_title="LibreMonica AI", page_icon="🤖")
st.title("🤖 LibreMonica")
st.caption("Open Source & Free Billing Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are LibreMonica, a free open-source assistant."}]

# 3. Fix: Removed the dot after 'with' and added the chat_message call
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- CHAT INPUT LOGIC ---
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            # This calls the Hugging Face Serverless API for free
            for message in client.chat.completions.create(
                model=MODEL_ID,
                messages=st.session_state.messages,
                max_tokens=1000,
                stream=True,
            ):
                token = message.choices[0].delta.content
                full_response += (token or "")
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {str(e)}")
