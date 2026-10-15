from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
import operator
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict, List

load_dotenv()

model = ChatGroq(model='openai/gpt-oss-20b')

class Messages(TypedDict):
    messages: Annotated[List[BaseMessage],add_messages]

graph = StateGraph(Messages)

def get_chat(state:Messages)->Messages:
    result = model.invoke(state['messages'])
    return {'messages':[result]}

# nodes 
graph.add_node('get_chat',get_chat)

# edges
graph.add_edge(START,'get_chat')
graph.add_edge('get_chat',END)

checkpointer = InMemorySaver()
chatbot=graph.compile(checkpointer=checkpointer)