## Load data into chroma 

```py
    from langchain_community.embeddings import OllamaEmbeddings
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    from langchain_community.vectorstores import Chroma

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    link = "https://arjunrao.co/posts/stripe-2023"
    html = urlopen(link).read()
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text()
    docs = get_text_chunks_langchain(text)
    db = Chroma.from_documents(docs, embeddings)
```

## Query using similarity search in Chroma 

```py
    print(">>>> Query with Chromadb")
    query = "what were some highlights from stripe's report?"
    print("\n" + query)
    docs = db.similarity_search(query)
    # print results
    print(docs[0].page_content)
```

### Response
```
Highlights from Stripe annual 2023 letter | arjunraoarjunraoNewsletterWritingsProjectsHomeNewsletterWritingsProjectsPublished onWednesday, March 20, 2024Highlights from Stripe annual 2023 letterStripe published its 2023 annual letter last week. Much like the previous edition it was filled with a lot of interesting nuggets. Stripe has a strong history of being fairly transparent with its practices. These range from engineering challenges through its blogs as well as thought leadership in the
```

## Query using Mistral + Ollama 

```py
    from langchain_community.llms import Ollama
    from langchain.chains import RetrievalQA
    
    ollama = Ollama(model="mistral")
    print(">>>> Query with Ollama")
    qachain=RetrievalQA.from_chain_type(ollama, retriever=db.as_retriever())
    print(qachain.invoke({"query": query}))
```

### Response

```
Stripe published its 2023 annual letter last week. Here are some highlights from the letter:\n\n1. Financial Performance:\n- Companies founded in 2022 were 60% more likely to start collecting revenue within their first year and 57% more likely to process $1 million within their first year, compared to those founded in 2019.\n- During Black Friday/Cyber Monday (BFCM) 2023, Stripe maintained an uptime of over 99.999% and processed more than 300 million transactions with a total volume of $18.6 billion.\n\n2. Operational Efficiency:\n- Stripe's progressive rollouts undergo rigorous monitoring, with machines running new code inspected against 55,000 different metrics. Anomalous telemetry results in the automatic withdrawal of affected machines and redirection of traffic to older, known-good versions.\n- The company aims to detect and remediate as many incidents as possible through automated monitoring, invoking redundant rails or enabling emergency systems when necessary.\n\n3. Reflections:\n- Companies founded in 2022 showed a higher likelihood of generating revenue and processing larger volumes within their first year compared to those founded in 2019.\n- During the highest-load period, BFCM 2023, Stripe achieved uptime above 99.999% while handling over 300 million transactions with a total volume of $18.6 billion.\n- One in six new companies registered in Delaware now utilize Stripe for their payment processing needs.\n\nThe letter's writing style is characterized by humorous anecdotes, quirky observations, and intelligent historical narratives, making it an engaging read.
```