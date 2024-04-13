import feedparser

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from urllib.request import urlopen
from bs4 import BeautifulSoup

embeddings = OllamaEmbeddings(model="nomic-embed-text")
db = None


def get_text_chunks_langchain(text):
   text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
   docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
   return docs

def get_html_for_url(link):
    html = urlopen(link).read()
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text()
    return text

def read_from_db():
    query = "what were some highlights from stripe's report?"
    ollama = Ollama(model="mistral")
    qachain=RetrievalQA.from_chain_type(ollama, retriever=db.as_retriever())
    print(qachain.invoke({"query": query}))

def parse_each_item(feed):
    global db
    print("Parsing individual feed entries...")
    count = 0
    for entry in feed.entries:
        if count > 3: 
            break
        count = count + 1
        document = get_html_for_url(entry.link)
        docs = get_text_chunks_langchain(document)
        db = Chroma.from_documents(docs, embeddings)

def parse_rss_xml():
    url = "https://arjunrao.co/feed.xml"
    feed = feedparser.parse(url)
    parse_each_item(feed)

def main():
    print("Launching Arjun RSS...")
    parse_rss_xml()
    print("Parsing of feed complete.")
    read_from_db()

main()
