from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

import feedparser

def store_item_to_vectordb(title, link, published, summary):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    text_splitter = RecursiveCharacterTextSplitter()
    split_documents = text_splitter.split_documents(docs)
    vector_store = FAISS.from_documents(split_documents, embeddings)
    return 

def parse_each_item(feed):
    for entry in feed.entries:
        store_item_to_vectordb(entry.title, entry.link, entry.published, entry.summary)

def parse_rss_xml():
    url = "https://lethain.com/feeds.xml"
    feed = feedparser.parse(url)
    parse_each_item(feed)


def main():
    print("Launching lethain RSS...")
    parse_rss_xml()
    print("Storage completed.")

main()
