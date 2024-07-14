from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
from langchain.schema import SystemMessage
from config import settings
from langfuse import Langfuse
from llm_guard.input_scanners import Toxicity
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import bs4

from langfuse.decorators import langfuse_context, observe

import os
 
os.environ["LANGFUSE_PUBLIC_KEY"] = settings.LANGFUSE_PK_KEY
os.environ["LANGFUSE_SECRET_KEY"] = settings.LANGFUSE_SK_KEY
os.environ["LANGFUSE_HOST"] = settings.LANGFUSE_HOST

langfuse = Langfuse()
langfuse_prompt = langfuse.get_prompt(settings.PROMPT_TEMPLATE_NAME)

toxicity_scanner = Toxicity()

# Initialize the model
model = ChatOpenAI(
    model=langfuse_prompt.config["model"],
    temperature=langfuse_prompt.config["temperature"],
    api_key=settings.OPENAI_KEY
)

intent_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=f"""
                {langfuse_prompt.get_langchain_prompt()}
            """
        ),
        MessagesPlaceholder(
            variable_name="chat_history", optional=True
        ),
        HumanMessagePromptTemplate.from_template(
            "Question : {question}"
        ),
    ]
)

general_chain = (
    intent_prompt
    | model
    | StrOutputParser()
)

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
                You are a usefull assistant. Do your best to answer the question
            """
        ),
        HumanMessagePromptTemplate.from_template(
            "Question : {question}\n"
            "Context : {context}"
        ),
    ]
)

loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(
    api_key=settings.OPENAI_KEY
))

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Create the chain
llm_agent_chain = (
    {"context": retriever | format_docs, "question":  RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# Initialize chat histories dictionary
chat_histories = {}
@observe()
def conversation(user_id: str, session_id:str, question: str):
    # Ensure the user has a chat history
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    # Get the user's chat history
    user_chat_history = chat_histories[user_id]

    # Add the new question to the user's chat history
    user_chat_history.append({"role": "user", "content": question})

    _, _, risk_score = toxicity_scanner.scan(question)

    langfuse_context.score_current_observation(
        name="input-toxicity",
        value=risk_score
    )
    langfuse_handler = langfuse_context.get_current_langchain_handler()
    trace_id = langfuse_handler.get_trace_id()

    answer = general_chain.invoke(
        {
            "question": question, 
            "chat_history": user_chat_history
        },
        config={"callbacks": [langfuse_handler]}
    )

    if answer.lower() == "llm agent":
        answer = llm_agent_chain.invoke(
            question,
            config={"callbacks": [langfuse_handler]}
        )
    langfuse_context.update_current_observation(
        input=question,
        output=answer,
        session_id=session_id,
        user_id=user_id,
        tags=langfuse_prompt.config["tags"]
    )
    # Add the assistant's response to the user's chat history
    user_chat_history.append({"role": "assistant", "content": answer})
    
    langfuse_handler.flush()
    
    return answer, trace_id