import streamlit as st

st.set_page_config(page_title="AI Advocate", page_icon="⚖️")

st.title("⚖️ AI Advocate - Legal Assistant")
st.write("Describe your legal issue. The AI Advocate will guide you.")

# ----------------------------
# Legal Knowledge Base
# ----------------------------

legal_database = {
    "divorce": {
        "category": "Family Law",
        "law": "Hindu Marriage Act, 1955",
        "advice": "You can file for divorce on grounds like cruelty, desertion, adultery, etc. Mutual consent divorce is also possible if both parties agree."
    },
    "domestic violence": {
        "category": "Family Law",
        "law": "Protection of Women from Domestic Violence Act, 2005",
        "advice": "You can file a complaint at the nearest police station or approach a protection officer. You may also request protection, residence, or maintenance orders."
    },
    "cyber": {
        "category": "Cyber Crime",
        "law": "Information Technology Act, 2000 (Section 66)",
        "advice": "Cyber crimes like hacking, fraud, and identity theft can be reported at cybercrime.gov.in or your local police station."
    },
    "property": {
        "category": "Property Law",
        "law": "Transfer of Property Act, 1882",
        "advice": "Property disputes can be resolved through civil court. Ensure proper documentation and ownership proof."
    },
    "salary": {
        "category": "Labour Law",
        "law": "Payment of Wages Act, 1936",
        "advice": "If your employer is not paying salary, you can file a complaint with the labour commissioner."
    },
    "cheque": {
        "category": "Financial Law",
        "law": "Negotiable Instruments Act, 1881 (Section 138)",
        "advice": "Cheque bounce cases can be filed in court within 30 days after receiving bank memo."
    },
    "arrest": {
        "category": "Criminal Law",
        "law": "Criminal Procedure Code (CrPC)",
        "advice": "You have the right to know the reason for arrest and the right to a lawyer."
    }
}

# ----------------------------
# User Input
# ----------------------------

user_input = st.text_area("Enter your legal issue:")

if st.button("Analyze Case"):
    if user_input:
        user_input_lower = user_input.lower()

        found = False

        for keyword in legal_database:
            if keyword in user_input_lower:
                data = legal_database[keyword]

                st.success(f"📌 Case Type: {data['category']}")
                st.info(f"📖 Relevant Law: {data['law']}")
                st.write(f"💡 Guidance: {data['advice']}")

                found = True
                break

        if not found:
            st.warning("⚠️ Sorry, this issue is not in the current legal database.")
            st.write("Please consult a certified advocate for professional advice.")

        st.warning("⚖️ Disclaimer: This is AI-generated preliminary legal guidance. For official advice, consult a qualified advocate.")

    else:
        st.error("Please describe your issue.")
