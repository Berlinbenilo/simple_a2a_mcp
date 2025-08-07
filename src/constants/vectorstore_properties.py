import faiss
from langchain_huggingface import HuggingFaceEmbeddings

huggingface_embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

index = faiss.IndexFlatL2(len(huggingface_embedder.embed_query("hello world")))

from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=huggingface_embedder,
    persist_directory="./chroma_langchain_db",
)

print("Initialized FAISS vector store with HuggingFace embeddings.")

user_id = "swetha_resume_2025"
