# askarjun

## TODOs

- [x] Build a simple langchain hook to read URL link contents
- [x] Langchain crawling of arjunrao in notebook
- [x] Decide between manual vs langchain crawling
- [x] Crawl through pages 
- [x] Store contents in vectordb 
- [x] Init Ollama & LLM
- [x] Ask questions to be answered without memory using vectordb (RAG)
- [x] Simple chat interface with Chainlit 
- [x] Add short term memory
- [x] Figure out how to run ollama in a container 
- [x] Containerize chainlit
- [ ] Run ollama with chainlit
- [ ] Containerize backend 
- [ ] Deploy chatbot to "cloud"
- [ ] Deploy data ingest process
- [ ] process to store chromadb to R2
- [ ] Stream responses back instead of all together
- [ ] Add reasoning [Agent based retrieval]
- [ ] Add Streamlit Copilot at [arjunrao.co](https://docs.chainlit.io/deployment/copilot)

## Running askarjun

### 1. Running locally 

```sh
pip install -r requirements.txt
chainlit run src/chat.py
```

### 2. Container stuff

```sh
docker build -t askarjun:latest
docker-compose up
```

### 3. Pull down Ollama models 

```sh
docker exec -it askarjun-ollama-container-1  ollama pull nomic-embed-text
docker exec -it askarjun-ollama-container-1  ollama pull mistral
```

Models are stored in `./data/ollama` which are mapped into the container as a volume (see [docker-compose.yml](./docker-compose.yml))