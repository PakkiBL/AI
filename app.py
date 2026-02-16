import streamlit as st
import openai
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="AI Legal Advocate Pro",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .legal-tip {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #1E3A8A;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "case_history" not in st.session_state:
    st.session_state.case_history = []
    
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1E3A8A/FFFFFF?text=AI+Legal+Advocate", use_column_width=True)
    
    st.header("⚙️ Configuration")
    
    # API Configuration
    with st.expander("API Settings", expanded=True):
        api_key = st.text_input("OpenAI API Key", type="password")
        if api_key:
            openai.api_key = api_key
            
        model = st.selectbox(
            "Model",
            ["gpt-4", "gpt-3.5-turbo-16k", "gpt-3.5-turbo"],
            index=0
        )
    
    # Legal Practice Areas
    st.header("📚 Practice Areas")
    practice_area = st.selectbox(
        "Select Area",
        ["General Legal Advice", "Contract Law", "Family Law", 
         "Criminal Law", "Business Law", "Intellectual Property",
         "Employment Law", "Real Estate Law"]
    )
    
    # Document Upload
    st.header("📎 Document Upload")
    uploaded_file = st.file_uploader(
        "Upload legal document for review",
        type=['pdf', 'txt', 'docx']
    )
    
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    
    st.divider()
    
    # Saved Conversations
    st.header("💾 Saved Conversations")
    if st.button("Save Current Conversation"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state.case_history.append({
            "timestamp": timestamp,
            "messages": st.session_state.messages.copy()
        })
        st.success("Conversation saved!")
    
    if st.session_state.case_history:
        for i, chat in enumerate(st.session_state.case_history[-3:]):
            if st.button(f"Load: {chat['timestamp']}", key=f"load_{i}"):
                st.session_state.messages = chat["messages"]
                st.rerun()
    
    st.divider()
    
    # Legal Resources
    st.header("📖 Legal Resources")
    with st.expander("Common Legal Terms"):
        st.markdown("""
        - **Plaintiff**: Person bringing the case
        - **Defendant**: Person being sued
        - **Lawsuit**: Legal case
        - **Settlement**: Agreement outside court
        - **Appeal**: Request to review decision
        """)
    
    # Disclaimer
    st.warning(
        "⚠️ **IMPORTANT DISCLAIMER**\n\n"
        "This AI assistant provides general information only. "
        "Always consult with a licensed attorney for legal advice."
    )

# Main content area
st.markdown('<h1 class="main-header">⚖️ AI Legal Advocate Pro</h1>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Case Analysis", "⚡ Quick Tools"])

with tab1:
    # Chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Describe your legal situation..."):
            if not api_key:
                st.error("Please enter your OpenAI API key in the sidebar.")
                st.stop()
            
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                try:
                    # Create context-aware system message
                    system_message = f"""You are an AI legal advocate specializing in {practice_area}. 
                    Provide accurate, helpful information while emphasizing that you're not a substitute 
                    for professional legal advice. Include relevant legal principles but avoid giving 
                    specific legal opinions."""
                    
                    if uploaded_file:
                        system_message += "\n\nNote: A document has been uploaded for review. Consider document contents in your response if relevant."
                    
                    messages_for_api = [{"role": "system", "content": system_message}]
                    
                    # Add recent conversation history
                    for msg in st.session_state.messages[-10:]:
                        messages_for_api.append({"role": msg["role"], "content": msg["content"]})
                    
                    # Stream response
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=messages_for_api,
                        temperature=0.7,
                        stream=True
                    )
                    
                    for chunk in response:
                        if chunk.choices[0].delta.get("content"):
                            full_response += chunk.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    
                    # Add to favorites button
                    col1, col2, col3 = st.columns([1, 1, 4])
                    with col1:
                        if st.button("⭐ Save", key=f"save_{len(st.session_state.messages)}"):
                            st.session_state.favorites.append({
                                "question": prompt,
                                "answer": full_response,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            st.success("Saved to favorites!")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    full_response = "I apologize, but I encountered an error. Please try again."
                    message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    with col2:
        st.markdown("### 📋 Quick Actions")
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("Export Chat", use_container_width=True):
            chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
            st.download_button(
                label="Download Chat",
                data=chat_text,
                file_name=f"legal_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        st.markdown("### ⭐ Favorites")
        if st.session_state.favorites:
            for fav in st.session_state.favorites[-3:]:
                with st.expander(fav['question'][:50] + "..."):
                    st.write(fav['answer'])
                    st.caption(f"Saved: {fav['timestamp']}")

with tab2:
    st.header("📊 Case Analysis Dashboard")
    
    if st.session_state.messages:
        # Analyze conversation
        total_messages = len(st.session_state.messages)
        user_messages = sum(1 for m in st.session_state.messages if m["role"] == "user")
        assistant_messages = total_messages - user_messages
        
        # Create metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Messages", total_messages)
        with col2:
            st.metric("Your Questions", user_messages)
        with col3:
            st.metric("AI Responses", assistant_messages)
        
        # Sentiment analysis placeholder
        st.subheader("Conversation Flow")
        data = pd.DataFrame({
            "Message Number": range(1, total_messages + 1),
            "Type": ["User" if m["role"] == "user" else "AI" for m in st.session_state.messages]
        })
        
        fig = px.bar(data, x="Message Number", color="Type", 
                     title="Conversation Breakdown",
                     color_discrete_map={"User": "#1E3A8A", "AI": "#6B7280"})
        st.plotly_chart(fig, use_container_width=True)
        
        # Key topics extracted
        st.subheader("Key Topics Discussed")
        topics = ["Legal Rights", "Contracts", "Liabilities", "Damages", "Procedures"]
        topic_data = pd.DataFrame({
            "Topic": topics,
            "Mentions": [3, 5, 2, 4, 3]  # Placeholder data
        })
        st.dataframe(topic_data, use_container_width=True)
    
    else:
        st.info("Start a conversation to see analysis here.")

with tab3:
    st.header("⚡ Quick Legal Tools")
    
    tool_col1, tool_col2 = st.columns(2)
    
    with tool_col1:
        st.subheader("📝 Document Checklist")
        doc_type = st.selectbox(
            "Document Type",
            ["Contract", "Will", "Lease", "NDA", "Employment Agreement"]
        )
        
        if doc_type == "Contract":
            st.markdown("""
            - [ ] Parties identified correctly
            - [ ] Consideration/Price stated
            - [ ] Terms and conditions clear
            - [ ] Signatures and dates
            - [ ] Notarization if required
            """)
        elif doc_type == "Will":
            st.markdown("""
            - [ ] Testator identification
            - [ ] Beneficiaries named
            - [ ] Executor appointed
            - [ ] Witnesses signatures
            - [ ] Asset distribution clear
            """)
    
    with tool_col2:
        st.subheader("📅 Statute of Limitations Calculator")
        case_type = st.selectbox(
            "Case Type",
            ["Personal Injury", "Contract Dispute", "Property Damage", "Professional Malpractice"]
        )
        incident_date = st.date_input("Incident Date")
        
        if st.button("Calculate Deadline"):
            st.info(f"For {case_type}, typical statute of limitations is 2-3 years. Consult an attorney for exact dates.")
    
    st.subheader("🔍 Legal Research Assistant")
    research_query = st.text_input("Enter legal term or concept to research")
    if st.button("Research") and research_query:
        st.info(f"Researching '{research_query}'... This would connect to legal databases in production.")
        
        # Placeholder research results
        st.markdown("**Sample Research Results:**")
        st.markdown("""
        1. **Primary Sources**: Case law, statutes, regulations
        2. **Secondary Sources**: Law reviews, treatises, restatements
        3. **Recent Developments**: Check for recent amendments
        """)

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("© 2024 AI Legal Advocate")
with col2:
    st.caption("For informational purposes only")
with col3:
    st.caption("v1.0.0")
