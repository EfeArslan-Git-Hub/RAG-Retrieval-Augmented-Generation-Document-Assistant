import streamlit as st
import os
from src.document_processor import DocumentProcessor
from src.chatbot import GeminiRAGChatbot

# Page Config
st.set_page_config(page_title="Free-Tier RAG Assistant", layout="wide")

def main():
    st.title("🤖 Free-Tier RAG Document Assistant by Efe Arslan")
    st.markdown("Chat with your documents using **Gemini Pro** and **Local Embeddings**.")

    # --- Sidebar: Configuration ---
    st.sidebar.header("Configuration")
    
    # 1. API Key Input
    api_key = st.sidebar.text_input(
        "Enter Google API Key", 
        type="password", 
        help="Get your key from https://aistudio.google.com/"
    )

    if not api_key:
        st.warning("Please enter your Google API Key in the sidebar to proceed.")
        return

    # 2. File Upload
    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

    # --- Session State Initialization ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None

    if "vector_store_ready" not in st.session_state:
        st.session_state.vector_store_ready = False

    if "current_file_name" not in st.session_state:
        st.session_state.current_file_name = None

    # --- Processing Logic ---
    # Check if a new file is uploaded
    if uploaded_file and uploaded_file.name != st.session_state.current_file_name:
        st.session_state.messages = []
        st.session_state.vector_store_ready = False
        st.session_state.chatbot = None
        st.session_state.current_file_name = uploaded_file.name

    if uploaded_file and not st.session_state.vector_store_ready:
        with st.spinner("Processing PDF... This may take a moment (creating embeddings locally)"):
            try:
                # Initialize Processor
                processor = DocumentProcessor()
                vector_store = processor.process_pdf(uploaded_file)
                
                # Initialize Chatbot
                chatbot = GeminiRAGChatbot(api_key)
                chatbot.setup_chain(vector_store)
                
                # Store in Session
                st.session_state.chatbot = chatbot
                st.session_state.vector_store_ready = True
                st.success("PDF processed successfully! You can now ask questions.")
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")

    # --- Chat Interface ---
    if st.session_state.vector_store_ready:
        # Display Chat History
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User Input
        if prompt := st.chat_input("Ask a question about your document..."):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.chatbot.ask_question(prompt)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
    
    # Reset Button (Optional)
    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
