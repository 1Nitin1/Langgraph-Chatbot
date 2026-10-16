# LangGraph Chatbot

A Streamlit chat app built step by step with LangGraph, Groq, and SQLite. The completed version is in [`Final Chatbot/`](Final%20Chatbot/).

## How it was built

1. **Basic chatbot:** I defined a LangGraph state containing a `messages` list, using `add_messages` to append conversation messages. A single `get_chat` node calls the Groq chat model, and edges connect `START` → `get_chat` → `END`. The first version invoked the model normally, so the answer appeared only after generation finished.
2. **Streaming answers:** I changed the Streamlit response flow to use LangGraph's `stream(..., stream_mode="messages")`. `st.write_stream` displays each generated content chunk as it arrives.
3. **Threads and chat history:** I added a `thread_id` to the graph's configurable settings so each conversation has its own state. Streamlit session state tracks thread IDs and the selected thread; the UI lists conversations, starts new ones, and reloads messages with `chatbot.get_state(config)`.
4. **Persistent history with SQLite:** I replaced the in-memory checkpointer with LangGraph's `SqliteSaver`, backed by `chatbot.db`. Checkpoints now survive app restarts. The sidebar loads saved thread IDs from the SQLite `checkpoints` table.

## Run the completed app

From the project directory, install the dependencies and configure your Groq API key:

```powershell
python -m pip install streamlit langgraph langchain-core langchain-groq langgraph-checkpoint-sqlite python-dotenv
```

Create `Final Chatbot/.env` with:

```text
GROQ_API_KEY=your_groq_api_key
```

Then launch the app:

```powershell
cd "Final Chatbot"
streamlit run gpt_like_interface.py
```

The app creates/updates `chatbot.db` in `Final Chatbot` as conversations are saved. Keep `.env` private.
