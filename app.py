import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ----------------------------
# Sample Legal Dataset
# ----------------------------
data = {
    "text": [
        "My husband is asking for divorce",
        "Someone hacked my Instagram account",
        "My landlord is not returning deposit",
        "Police arrested me without reason",
        "Property dispute between brothers",
        "Online fraud transaction happened",
        "Domestic violence issue",
        "Cyber bullying case",
        "Cheque bounce problem",
        "Company not paying salary"
    ],
    "label": [
        "Family Law",
        "Cyber Crime",
        "Property Law",
        "Criminal Law",
        "Property Law",
        "Cyber Crime",
        "Family Law",
        "Cyber Crime",
        "Financial Law",
        "Labour Law"
    ]
}

df = pd.DataFrame(data)

# ----------------------------
# ML Model Training
# ----------------------------
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["text"])
model = MultinomialNB()
model.fit(X, df["label"])

# ----------------------------
# IPC Reference Dictionary
# ----------------------------
ipc_sections = {
    "Cyber Crime": "IT Act 2000 - Section 66",
    "Family Law": "Hindu Marriage Act 1955",
    "Property Law": "Transfer of Property Act 1882",
    "Criminal Law": "IPC Section 41",
    "Financial Law": "Negotiable Instruments Act 1881",
    "Labour Law": "Payment of Wages Act 1936"
}

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="AI Advocate", page_icon="⚖️", layout="centered")

st.title("⚖️ AI Advocate - Legal Assistant")
st.write("Get preliminary legal guidance instantly.")

user_input = st.text_area("Describe your legal issue:")

if st.button("Analyze Case"):
    if user_input:
        input_vector = vectorizer.transform([user_input])
        prediction = model.predict(input_vector)[0]

        st.success(f"📌 Case Type Identified: {prediction}")

        if prediction in ipc_sections:
            st.info(f"📖 Relevant Law: {ipc_sections[prediction]}")

        st.warning("⚠️ Disclaimer: This is AI-generated preliminary guidance. Please consult a certified advocate for official legal advice.")
    else:
        st.error("Please describe your issue.")
