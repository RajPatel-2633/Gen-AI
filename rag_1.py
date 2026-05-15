from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore ,RetrievalMode


pdf_path = Path(__file__).parent / "report.pdf"

loader = PyPDFLoader(file_path=pdf_path)

docs=loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(documents=docs)

# print("DOCS",len(docs))
# print("SPLIT",len(split_docs))

embedder = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    api_key="AIzaSyA3JmFExC6FZ6SeQWW24HVLO95Se82HLo8"
)

# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="testing_langchain",
#     embedding=embedder
# )

# vector_store.add_documents(documents=split_docs)
print("Ingestion Done")

retriever = QdrantVectorStore.from_existing_collection(
     url="http://localhost:6333",
    collection_name="testing_langchain",
    embedding=embedder
)

relevant_chunks = retriever.similarity_search(
    query="Which are the technologies used?"
)

# print("Relevant chunks",relevant_chunks)

SYSTEM_PROMPT= f"""
You are a helpful AI Assistant who responds to the user based on the available context.

Context:
{relevant_chunks}
"""







 