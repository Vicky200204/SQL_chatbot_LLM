import streamlit as st
import pyodbc
from sqlalchemy import create_engine, MetaData
from llama_index.core import SQLDatabase, VectorStoreIndex, Settings
from llama_index.core.indices.struct_store.sql_query import SQLTableRetrieverQueryEngine
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
 
# Initialize the Ollama LLM and Embedding model
llm = Ollama(model="llama3:latest", base_url="", request_timeout=60.0)
embed_model = OllamaEmbedding(model_name="llama3:latest", base_url="http://10.0.11.180:11434/")
Settings.llm = llm
Settings.embed_model = embed_model
 
# Database connection setup
server = "your server namr "
database = "your db name "
username = "your username "
password = "your password"
conn_str = (
    f"DRIVER={{SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}", use_setinputsizes=False, pool_recycle=3600)
metadata_obj = MetaData()
metadata_obj.reflect(engine)  # Reflect the database schema
sql_database = SQLDatabase(engine)
 
# System prompt to guide the LLM
system_prompt = """
you should understand natural query and give response to the user.
you are user-friendly ai aissiatance and you have to resposne all the general questions. 
You are a helpful SQL chatbot. Your task is to analyze the user's question, generate a SQL query, execute it, and provide a clear and concise answer.
You have access to all the tables, records, and data in the SQL Server database. The database is connected, and you should respond to the user's question based on the data available.
 
When generating SQL queries:
1. Always validate the column names and table names against the database schema.
2. If a column or table does not exist, suggest possible corrections or ask for clarification.
3. Handle case sensitivity issues by using the correct case for column and table names.
4. If an error occurs, provide a detailed explanation of the issue and suggest how to fix it.
"""
 
# Prepare the SQLTableRetrieverQueryEngine
table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [SQLTableSchema(table_name=table_name) for table_name in sql_database.get_usable_table_names()]
obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    VectorStoreIndex,
)
query_engine = SQLTableRetrieverQueryEngine(
    sql_database,
    obj_index.as_retriever(similarity_top_k=1),
    system_prompt=system_prompt,  # Add the system prompt here
)
 
# Streamlit UI setup
st.title("SQL Database Chatbot")
 
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
 
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
 
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
 
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Query the database using the query engine
                response = query_engine.query(prompt)
                st.markdown(response)
            except Exception as e:
                # Handle errors gracefully
                error_message = f"An error occurred: {str(e)}. Please check your query or provide more details."
                st.markdown(error_message)
                response = error_message
 
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
