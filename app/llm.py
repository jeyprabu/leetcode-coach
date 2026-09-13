from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="phi4-mini:3.8b",
    temperature=0
)