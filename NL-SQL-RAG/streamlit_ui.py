import streamlit as st
from chain_config import setup_llm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_session_state():
    if 'query_engine' not in st.session_state:
        st.session_state.query_engine = setup_llm()
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm here to help you query your SQL database. How can I assist you today?"}]

def generate_response(prompt: str):
    try:
        response = st.session_state.query_engine.query(prompt)
        if 'sql_query' in response.metadata:
            logger.info(f"Generated SQL Query: {response.metadata['sql_query']}")
        return response
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return None

def create_ui():
    st.title("💬 SQL Chatbot")
    st.caption("🚀 A streamlit chatbot powered by Ollama & Open Source LLM for SQL queries")

    initialize_session_state()

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Enter your SQL query or question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.spinner("Generating response..."):
            response = generate_response(prompt)
        
        if response:
            with st.chat_message("assistant"):
                st.subheader("Response")
                st.write(response.response)
                
                st.subheader("SQL Query")
                if 'sql_query' in response.metadata:
                    st.code(response.metadata['sql_query'], language="sql")
                else:
                    st.write("No SQL query available")
                
                st.subheader("Result")
                if 'result' in response.metadata:
                    st.write(response.metadata['result'])
                else:
                    st.error("There was an error while trying to execute the query. Please try again.")
            
            content = f"Response: {response.response}\n\nSQL Query: {response.metadata.get('sql_query', 'No SQL query available')}\n\n"
            if 'result' in response.metadata:
                content += f"Result: {response.metadata['result']}"
            else:
                content += "Result: There was an error while trying to execute the query. Please try again."
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": content
            })
        else:
            st.error("An error occurred while generating the response. Please try again.")