# imports
import streamlit as st
from backend import chatbot, retrieve_chat_history, cursor
from langchain_core.messages import HumanMessage
import uuid


#initialize if empty
if 'thread_ids' not in st.session_state:
    st.session_state['thread_ids'] = retrieve_chat_history()

# generate thread id
def generate_thread_id():
    thread_id = str(uuid.uuid4())
    st.session_state['thread_ids'].append(thread_id)
    return thread_id


# reset chat for new chat
def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()


# initialize if empty

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()


# sidebar Ui
st.sidebar.title("Langgraph Chatbot")

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('Conversation History')

# display previous threads in reverse order
for thread_id in st.session_state['thread_ids'][::-1]:
    if st.sidebar.button(f'Chat {thread_id}'):
        st.session_state['thread_id'] = thread_id

# config for current thread
CONFIG = {'configurable': {'thread_id':st.session_state['thread_id']}}

# load previous chat
for message in chatbot.get_state(CONFIG).values.get('messages', []):
    if isinstance(message, HumanMessage):
        with st.chat_message('user'):
            st.text(message.content)
    else:
        with st.chat_message('ai'):
            st.text(message.content)



user_input = st.chat_input('type here')

if user_input:
    #show input
    with st.chat_message('user'):
        st.text(user_input)
   

    # show response
    with st.chat_message('ai'):
        response=st.write_stream(
            message_chunk.content for message_chunk,_ in chatbot.stream({'messages':[HumanMessage(content=user_input)]}, 
            config=CONFIG,
            stream_mode='messages')
        )
