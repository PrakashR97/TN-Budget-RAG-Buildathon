# step4_rag_query.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from logger import log_interaction_json, log_interaction_csv

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

def run_rag_query(query: str, vector_store, chat_history: list = None, scheme_name: str = "General"):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Format Streamlit history for LangChain
    formatted_history = []
    if chat_history:
        # Exclude the current user query if it was already appended in app.py
        past_messages = chat_history[:-1] if chat_history[-1]["content"] == query else chat_history
        
        for msg in past_messages:
            if msg["role"] == "user":
                formatted_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                formatted_history.append(AIMessage(content=msg["content"]))

    # 1. Fetch relevant document chunks
    retrieved_docs = retriever.invoke(query)
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    context_chunks = [doc.page_content for doc in retrieved_docs]

    # 2. Simplified prompt for direct answering
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_instruction = (
        "You are an assistant for analyzing Tamil Nadu government documents.\n"
        "Answer the user's question clearly and concisely using only the provided context.\n"
        "If the answer cannot be determined from the context, state that clearly.\n\n"
        "Context:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])
    
    chain = prompt | llm | StrOutputParser()

    # 3. Generate Answer
    answer = chain.invoke({
        "context": context_text, 
        "chat_history": formatted_history,
        "question": query
    })

    # 4. Log interaction
    log_interaction_json(scheme_name, query, answer, context_chunks)
    log_interaction_csv(scheme_name, query, answer)

    return answer