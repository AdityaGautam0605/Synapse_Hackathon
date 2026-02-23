from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def get_recovery_advice(query):
    embeddings = OpenAIEmbeddings()

    vector_store = Chroma(
        persist_directory="app/db/chroma_store",
        embedding_function=embeddings
    )

    docs = vector_store.similarity_search(query, k=3)

    context = " ".join([doc.page_content for doc in docs])

    response = call_gemini(context)

    return response