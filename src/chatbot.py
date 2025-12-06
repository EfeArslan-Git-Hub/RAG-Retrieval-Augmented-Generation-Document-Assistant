from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

class GeminiRAGChatbot:
    """
    Manages the Gemini LLM and RAG interaction.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Chatbot with Google API Key.
        """
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3
        )
        self.chain = None

    def setup_chain(self, vector_store: FAISS):
        """
        Sets up the RetrievalQA chain with the given vector store.
        """
        retriever = vector_store.as_retriever()
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

    def ask_question(self, query: str) -> str:
        """
        Asks a question to the RAG chain.
        """
        if not self.chain:
            return "Please upload a document first to initialize the knowledge base."
        
        response = self.chain.invoke({"query": query})
        return response["result"]
