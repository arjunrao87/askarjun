from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

llm = Ollama(model="llama2")

llm.invoke("how can langsmith help with testing?")


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a skilled technical writer. Your name is {name}."),
        ("human", "Hello, how are you doing?"),
        ("ai", "I'm doing well, thanks!"),
        ("human", "{user_input}"),
    ]
)

chain = llm | prompt

chain.invoke({"user_input": "how can langsmith help with testing?"})
