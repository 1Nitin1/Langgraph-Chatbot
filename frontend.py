import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

# thread id
thread_id = 'chatbot_thread1'

# initialize if empty
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

# load previous chat
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])





user_input = st.chat_input('type here')

if user_input:
    #show input
    with st.chat_message('user'):
        st.text(user_input)

    # save input
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})

   

    # show response
    with st.chat_message('ai'):
        response=st.write_stream(
            message_chunk.content for message_chunk,_ in chatbot.stream({'messages':[HumanMessage(content=user_input)]}, 
            config={'configurable': {'thread_id': thread_id}},
            stream_mode='messages')
        )


    # save response
    st.session_state['message_history'].append({'role': 'ai', 'content': response})
