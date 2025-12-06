import io
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class DocumentProcessor:
    """
    Handles processing of PDF documents: loading, splitting, embedding, and indexing.
    """
    
    def __init__(self, embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the DocumentProcessor.
        
        Args:
            embedding_model_name: Name of the HuggingFace model for embeddings.
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    
    def process_pdf(self, pdf_file) -> FAISS:
        """
        Process an uploaded PDF file and return a FAISS vector store.
        
        Args:
            pdf_file: A file-like object (uploaded via Streamlit).
            
        Returns:
            FAISS: The vector store containing the document chunks.
        """
        # 1. Load Text from PDF
        text = self._load_text_from_pdf(pdf_file)
        
        # 2. Split Text
        chunks = self._split_text(text)
        
        # 3. Create Vector Store
        vector_store = FAISS.from_texts(chunks, embedding=self.embeddings)
        return vector_store

    def _load_text_from_pdf(self, pdf_file) -> str:
        """Helper to extract text from a PDF file-like object."""
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text

    def _split_text(self, text: str) -> list[str]:
        """Helper to split text into chunks suitable for embedding."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks
