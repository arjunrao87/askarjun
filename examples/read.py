from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

def read_from_db(db):
    query = "what were some highlights from stripe's report?"
    query1 = "what is the netflix team ethos?"
    ollama = Ollama(model="mistral")
    qachain=RetrievalQA.from_chain_type(ollama, retriever=db.as_retriever())
    print(qachain.invoke({"query": query}))
    print(qachain.invoke({"query": query1}))

def main():
    db = Chroma(persist_directory="./chroma_db",embedding_function=embeddings)
    read_from_db(db)

main()
