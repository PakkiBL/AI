import streamlit as st
from openai import OpenAI
from gtts import gTTS
from io import BytesIO

# --------------------
# Setup
# --------------------
st.set_page_config(page_title="AI Advocate Pro", page_icon="⚖️")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("⚖️ AI Advocate - Legal Assistant")
st.write("Type your legal issue. AI will respond with guidance and voice.")

# --------------------
# Input
# --------------------
user_input = st.text_area("Describe your legal issue:")

if st.button("Get Legal Advice"):
    if user_input:

        with st.spinner("Analyzing your case..."):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an Indian legal assistant. Provide helpful preliminary legal guidance with disclaimer."},
                    {"role": "user", "content": user_input}
                ]
            )

            answer = response.choices[0].message.content

            st.success("AI Legal Advice:")
            st.write(answer)

            # Voice Output
            tts = gTTS(answer)
            audio_file = BytesIO()
            tts.write_to_fp(audio_file)
            st.audio(audio_file.getvalue())

            st.warning("⚠️ This is AI-generated guidance. Please consult a certified advocate for official legal advice.")

    else:
        st.error("Please enter your legal issue.")
