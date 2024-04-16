import chainlit as cl
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

custom_prompt_template = """
    You are a knowledgeable Vice President of Engineering who answers concisely. 
    Do not respond back with more than 300 words. 
    You will not answer any questions for which you haven't been passed context. 
    You will not make up answers if you do not receive the context. 
    Use the following pieces of information to answer the user's question.
    You will not answer questions that are not about arjun. 
    Respond to this question using only information that can be attributed to https://arjunrao.com. 
    When someone greets you, just greet back.

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
    memory = ConversationBufferMemory(memory_key="chat_history", input_key='question', output_key='answer', return_messages=True)
    qa_chain = ConversationalRetrievalChain.from_llm(llm, 
                                                     vectorstore.as_retriever(), 
                                                     memory=memory,
                                                     combine_docs_chain_kwargs={"prompt": prompt},
                                                     return_source_documents=True)
    return qa_chain

def qa_chain():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory="./chroma_db",embedding_function=embeddings)
    model = Ollama(model="mistral")
    qa_prompt=set_custom_prompt()
    qa = retrieval_qa_chain(model, qa_prompt, db)
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
    await msg.send()
    cb = cl.AsyncLangchainCallbackHandler()
    cb.answer_reached = True
    res = await chain.acall(message.content, callbacks=[cb])
    answer = res["answer"]
    source_documents = res["source_documents"]
    text_elements = []
    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            # Create the text element referenced in the message
            text_elements.append(
                cl.Text(content=source_doc.page_content, name=source_name)
            )
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            answer += f"\nSources: {', '.join(source_names)}"
        else:
            answer += "\nNo sources found"

    await cl.Message(content=answer, elements=text_elements).send()