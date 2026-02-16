import streamlit as st
import openai
from gtts import gTTS
import os
from io import BytesIO

# ----------------------
# SET API KEY
# ----------------------
openai.api_key = st.secrets["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"]

st.set_page_config(page_title="AI Advocate Pro", page_icon="⚖️")

st.title("⚖️ AI Advocate - Voice Legal Assistant")

st.write("Speak or type your legal issue. AI will respond with guidance.")

# ----------------------
# USER INPUT
# ----------------------
user_input = st.text_area("Describe your legal issue:")

if st.button("Get Legal Advice"):
    if user_input:

        with st.spinner("Analyzing your case..."):

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an Indian legal assistant. Provide helpful preliminary legal guidance with disclaimer."},
                    {"role": "user", "content": user_input}
                ]
            )

            answer = response["choices"][0]["message"]["content"]

            st.success("AI Legal Advice:")
            st.write(answer)

            # ----------------------
            # TEXT TO SPEECH
            # ----------------------
            tts = gTTS(answer)
            audio_file = BytesIO()
            tts.write_to_fp(audio_file)
            st.audio(audio_file.getvalue())

            st.warning("⚠️ This is AI-generated guidance. Consult a certified advocate for official legal advice.")

    else:
        st.error("Please enter your legal issue.")
