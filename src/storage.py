import feedparser

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
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

def parse_each_item(feed):
    global db
    print("Parsing individual feed entries...")
    for entry in feed.entries:
        document = get_html_for_url(entry.link)
        docs = get_text_chunks_langchain(document)
        db = Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")
    db.persist()
    
def parse_rss_xml():
    url = "https://arjunrao.co/feed.xml"
    feed = feedparser.parse(url)
    parse_each_item(feed)

def store():
    print("Launching Arjun RSS...")
    parse_rss_xml()
    print("Parsing of feed complete.")

store()
