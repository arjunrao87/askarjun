from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

import chainlit as cl

custom_prompt_template = """
    You are a knowledgeable vice president of Engineering who answers super concisely. 
    You will not answer any questions for which you haven't been passed context. 
    You will not make up answers if you do not receive the context. 
    Use the following pieces of information to answer the user's question.
    You will not answer questions that are not about arjun. 
    Respond to this question using only information that can be attributed to https://arjunrao.com. 

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
"""

def set_custom_prompt():
    prompt = PromptTemplate(template=custom_prompt_template,
                        input_variables=['context', 'question'])
    return prompt

def retrieval_qa_chain(llm, prompt, vectorstore):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=False,
        chain_type_kwargs={'prompt': prompt}
    )
    return qa_chain

def qa_chain():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory="./chroma_db",embedding_function=embeddings)
    model = Ollama(model="mistral")
    llm = model
    qa_prompt=set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    return qa

@cl.on_chat_start
async def on_chat_start():
    elements = [cl.Image(name="image1", display="side", path="assets/arjun.png")]
    await cl.Message(
        content="Hello there, I am Arjun. How can I help you?", elements=elements
    ).send()
    chain = qa_chain()
    cl.user_session.set("chain", chain)


@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")
    msg = cl.Message(content="")
    async for chunk in chain.astream(
        {"query": message.content},
    ):
        await msg.stream_token(chunk["result"])

    await msg.send()


@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")