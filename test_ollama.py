from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="phi4-mini:3.8b",
    temperature=0
)

response = llm.invoke("Hi! What LLM are you?")

print(response.content)