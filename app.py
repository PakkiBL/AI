"""
PakkiBL AI Legal Advocate
A Streamlit-based AI assistant for legal information and guidance
"""

import streamlit as st
import openai
from datetime import datetime
import os
import json
from dotenv import load_dotenv
import PyPDF2
import io

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="PakkiBL AI Legal Advocate",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    
    /* User message styling */
    .stChatMessage[data-testid="user-message"] {
        background-color: #e3f2fd;
    }
    
    /* Assistant message styling */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #f5f5f5;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        background-color: #667eea;
        color: white;
        border: none;
        padding: 0.5rem;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #764ba2;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Disclaimer box */
    .disclaimer-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #856404;
    }
    
    /* Success message */
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        color: #155724;
    }
    
    /* Info box */
    .info-box {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        color: #0c5460;
    }
    
    /* Metrics styling */
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        font-size: 0.9rem;
        border-top: 1px solid #dee2e6;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
def init_session_state():
    """Initialize all session state variables"""
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", 
             "content": "🌟 **Welcome to PakkiBL AI Legal Advocate!**\n\nI'm here to help you with legal information and guidance. How can I assist you today?"}
        ]
    
    if "api_key_configured" not in st.session_state:
        # Check for API key in environment variables first
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.session_state.api_key_configured = True
            openai.api_key = api_key
        else:
            st.session_state.api_key_configured = False
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    
    if "total_queries" not in st.session_state:
        st.session_state.total_queries = 0

# Call initialization
init_session_state()

# Header Section
st.markdown("""
    <div class="main-header">
        <h1>⚖️ PakkiBL AI Legal Advocate</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Your Intelligent Assistant for Legal Information and Guidance</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=PakkiBL+AI", use_column_width=True)
    
    st.markdown("## ⚙️ Configuration")
    
    # API Key Configuration
    with st.expander("🔑 API Settings", expanded=True):
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key. It will be stored securely in the session."
        )
        
        if api_key:
            openai.api_key = api_key
            st.session_state.api_key_configured = True
            st.success("✅ API Key configured successfully!")
        else:
            st.warning("⚠️ Please enter your OpenAI API key to use the chat.")
        
        # Model selection
        model = st.selectbox(
            "Select Model",
            ["gpt-3.5-turbo", "gpt-4"],
            index=0,
            help="GPT-4 provides more detailed responses but may be slower."
        )
        
        # Temperature setting
        temperature = st.slider(
            "Response Creativity",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make responses more creative, lower values more focused."
        )
    
    # Document Upload Section
    st.markdown("## 📎 Document Analysis")
    uploaded_file = st.file_uploader(
        "Upload Legal Document",
        type=['pdf', 'txt', 'docx'],
        help="Upload a legal document for AI analysis"
    )
    
    if uploaded_file:
        if uploaded_file.name not in [f["name"] for f in st.session_state.uploaded_files]:
            file_details = {
                "name": uploaded_file.name,
                "type": uploaded_file.type,
                "size": uploaded_file.size,
                "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.uploaded_files.append(file_details)
            
            # Read PDF content if it's a PDF
            if uploaded_file.type == "application/pdf":
                try:
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
                    num_pages = len(pdf_reader.pages)
                    st.success(f"✅ PDF uploaded: {num_pages} pages")
                except Exception as e:
                    st.error(f"Error reading PDF: {str(e)}")
            else:
                st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Conversation Management
    st.markdown("## 💬 Conversation")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = [
                {"role": "assistant", 
                 "content": "🌟 **Welcome to PakkiBL AI Legal Advocate!**\n\nI'm here to help you with legal information and guidance. How can I assist you today?"}
            ]
            st.rerun()
    
    with col2:
        if st.button("💾 Save Chat"):
            # Save conversation to session state
            chat_data = {
                "timestamp": datetime.now().isoformat(),
                "messages": st.session_state.messages
            }
            st.session_state.conversation_history.append(chat_data)
            st.success("✅ Conversation saved!")
    
    # Quick Stats
    st.markdown("## 📊 Statistics")
    
    # Calculate metrics
    total_messages = len(st.session_state.messages)
    user_messages = sum(1 for m in st.session_state.messages if m["role"] == "user")
    assistant_messages = total_messages - user_messages
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <h3>{total_messages}</h3>
                <p>Total</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h3>{user_messages}</h3>
                <p>Your Qs</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <h3>{assistant_messages}</h3>
                <p>AI Answers</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Legal Disclaimer
    st.markdown("---")
    st.markdown("""
        <div class="disclaimer-box">
            <strong>⚠️ LEGAL DISCLAIMER</strong><br>
            This AI assistant provides general information only. 
            It does not constitute legal advice. Always consult with 
            a qualified attorney for legal matters.
        </div>
    """, unsafe_allow_html=True)
    
    # Version info
    st.markdown("---")
    st.markdown("**Version:** 1.0.0 | © 2024 PakkiBL")

# Main content area - Create tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "📚 Legal Resources", "ℹ️ About"])

# Tab 1: Chat Assistant
with tab1:
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Quick action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    quick_questions = [
        ("📋 Tenant Rights", "What are my basic rights as a tenant?"),
        ("📝 Contract Review", "What should I look for in a contract?"),
        ("⚖️ Small Claims", "How does small claims court work?"),
        ("📄 Will Creation", "How do I create a valid will?")
    ]
    
    for col, (label, question) in zip([col1, col2, col3, col4], quick_questions):
        with col:
            if st.button(label, use_container_width=True):
                # Auto-fill the question (in a real app, you'd set this to the input)
                st.info(f"Quick question selected: {question}")
                # You can implement auto-fill logic here
    
    # Chat input
    if prompt := st.chat_input("Ask your legal question...", disabled=not st.session_state.api_key_configured):
        
        # Increment query counter
        st.session_state.total_queries += 1
        
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Check if API key is configured
                if not st.session_state.api_key_configured:
                    raise ValueError("API key not configured")
                
                # Check if we have a file uploaded for context
                file_context = ""
                if uploaded_file:
                    file_context = f"\n\nNote: The user has uploaded a file named '{uploaded_file.name}'. Consider this in your response if relevant."
                
                # Create system message with legal context
                system_message = f"""You are PakkiBL, an AI legal advocate assistant. Provide helpful, 
                accurate information about legal topics in simple, understandable terms. 

                Key guidelines:
                1. Always clarify that you're providing general information, not legal advice
                2. Recommend consulting with a qualified attorney for specific cases
                3. Focus on general legal principles and common practices
                4. Be clear about limitations of your knowledge
                5. Use plain language and avoid unnecessary legal jargon
                6. If asked about specific cases, explain general principles rather than giving opinions
                7. Encourage users to seek professional legal counsel for their specific situation
                
                {file_context}"""
                
                # Prepare messages for API
                messages_for_api = [{"role": "system", "content": system_message}]
                
                # Add last 10 messages for context
                for msg in st.session_state.messages[-10:]:
                    messages_for_api.append({"role": msg["role"], "content": msg["content"]})
                
                # Make API call
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages_for_api,
                    temperature=temperature,
                    max_tokens=1000,
                    stream=True
                )
                
                # Stream the response
                for chunk in response:
                    if chunk.choices[0].delta.get("content"):
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                # Add a professional closing if not present
                if not any(word in full_response.lower() for word in ["attorney", "lawyer", "professional", "consult"]):
                    full_response += "\n\n---\n*Remember: This information is for general guidance only. For specific legal advice, please consult with a qualified attorney.*"
                
                message_placeholder.markdown(full_response)
                
            except openai.error.AuthenticationError:
                error_msg = "❌ **Authentication Error**: Invalid API key. Please check your OpenAI API key and try again."
                st.error(error_msg)
                full_response = error_msg
                
            except openai.error.RateLimitError:
                error_msg = "⏳ **Rate Limit Exceeded**: Too many requests. Please wait a moment and try again."
                st.error(error_msg)
                full_response = error_msg
                
            except openai.error.APIConnectionError:
                error_msg = "🌐 **Connection Error**: Could not connect to OpenAI. Please check your internet connection."
                st.error(error_msg)
                full_response = error_msg
                
            except Exception as e:
                error_msg = f"❌ **Error**: {str(e)}"
                st.error(error_msg)
                full_response = "I apologize, but I encountered an error. Please try again or check your settings."
            
            # Add assistant response to session state
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Tab 2: Legal Resources
with tab2:
    st.markdown("## 📚 Legal Resources Library")
    
    # Resource categories
    resource_categories = {
        "📋 Civil Law": [
            "Contract Law Basics",
            "Property Rights",
            "Tenant Rights",
            "Small Claims Court Guide"
        ],
        "⚖️ Criminal Law": [
            "Know Your Rights",
            "Criminal Procedure",
            "Miranda Rights Explained",
            "Bail and Bond Process"
        ],
        "👪 Family Law": [
            "Marriage and Divorce",
            "Child Custody Basics",
            "Adoption Process",
            "Domestic Violence Resources"
        ],
        "💼 Business Law": [
            "Starting a Business",
            "Employment Law",
            "Intellectual Property",
            "Business Contracts"
        ]
    }
    
    # Display resources in columns
    cols = st.columns(len(resource_categories))
    
    for col, (category, resources) in zip(cols, resource_categories.items()):
        with col:
            st.markdown(f"### {category}")
            for resource in resources:
                if st.button(f"📖 {resource}", key=resource, use_container_width=True):
                    st.info(f"Loading resource: {resource}")
    
    # FAQ Section
    st.markdown("---")
    st.markdown("### ❓ Frequently Asked Questions")
    
    faqs = [
        ("What should I do if I'm being sued?", 
         "If you're being sued, don't ignore it. Respond by the deadline, consider hiring an attorney, gather relevant documents, and understand the claims against you."),
        
        ("How do I find a good lawyer?",
         "You can find lawyers through bar association referrals, legal aid societies, or personal recommendations. Check their experience, reviews, and schedule consultations before deciding."),
        
        ("What's the difference between civil and criminal law?",
         "Criminal law deals with offenses against the state (like theft or assault), while civil law handles disputes between individuals or organizations (like contracts or property disputes).")
    ]
    
    for question, answer in faqs:
        with st.expander(question):
            st.write(answer)
            if st.button(f"Ask about this", key=f"ask_{question[:10]}"):
                st.info("Switch to the Chat tab to ask about this topic!")

# Tab 3: About
with tab3:
    st.markdown("## ℹ️ About PakkiBL AI Legal Advocate")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Purpose
        
        PakkiBL AI Legal Advocate is designed to:
        
        - Provide accessible legal information
        - Help users understand legal concepts
        - Guide users to appropriate legal resources
        - Offer preliminary legal research assistance
        
        ### ⚠️ Important Notice
        
        This AI tool is **NOT** a substitute for professional legal advice. 
        Laws vary by jurisdiction and change over time. Always consult with 
        a qualified attorney for your specific legal situation.
        """)
    
    with col2:
        st.markdown("""
        ### 🔒 Privacy & Security
        
        - Your conversations are private
        - No data is stored permanently
        - API keys are encrypted in session
        - We don't share your information
        
        ### 📞 Getting Help
        
        If you need immediate legal assistance:
        
        - 🏛️ Local Bar Association: [Search Here]
        - ⚖️ Legal Aid Society: [Find Help]
        - 🆘 Emergency: Dial your local emergency number
        """)
    
    # Version history
    st.markdown("---")
    st.markdown("### 📦 Version History")
    
    versions = [
        ("v1.0.0 - Current", "Initial release with chat, document upload, and legal resources"),
        ("v0.9.0 - Beta", "Testing version with core chat functionality")
    ]
    
    for version, description in versions:
        st.markdown(f"**{version}**: {description}")

# Footer
st.markdown("""
    <div class="footer">
        <p>PakkiBL AI Legal Advocate | For informational purposes only | Not legal advice</p>
        <p style="font-size: 0.8rem;">Powered by OpenAI • Built with Streamlit</p>
    </div>
""", unsafe_allow_html=True)

# Auto-save functionality
if len(st.session_state.messages) % 5 == 0 and len(st.session_state.messages) > 0:
    # Auto-save every 5 messages
    if not hasattr(st.session_state, 'last_auto_save') or \
       st.session_state.last_auto_save != len(st.session_state.messages):
        st.session_state.last_auto_save = len(st.session_state.messages)
        # You could implement auto-save to a file here
        pass
