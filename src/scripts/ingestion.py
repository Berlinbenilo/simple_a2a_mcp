from uuid import uuid4

from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_unstructured import UnstructuredLoader
from unstructured.cleaners.core import clean_extra_whitespace

from src.constants.vectorstore_properties import vector_store, user_id

# Load documents
loader = UnstructuredLoader(
    r"C:\Users\Deepika Ramesh\Downloads\Swetha resume 2025.pdf",
    post_processors=[clean_extra_whitespace],
)

documents = loader.load()
documents = filter_complex_metadata(documents)
# Process documents
for doc in documents:
    print(type(doc.metadata))
    # Add user_id to metadata
    doc.metadata["user_id"] = user_id

# Generate UUIDs and add documents to vector store
uuids = [str(uuid4()) for _ in range(len(documents))]
vector_store.add_documents(documents=documents, ids=uuids)
print(f"Added {len(documents)} documents to the vector store with user ID: {user_id}")
