import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import os

# Streamlit secrets se key direct environment me set karein
os.environ["GOOGLE_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# Page config
st.set_page_config(page_title="AI Data Analyst", page_icon="📊", layout="wide")
st.title("📊 AI Data Analyst Agent")
st.markdown("Upload your CSV file and chat with your data!")

# Chat history ko memory me save karne ka logic
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# File Uploader
uploaded_file = st.file_uploader("Upload your CSV data file", type=["csv"])

if uploaded_file:
    # Data load karein
    df = pd.read_csv(uploaded_file)
    
    # Agent Initialize karein
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    agent = create_pandas_dataframe_agent(
        llm, 
        df, 
        verbose=True, 
        allow_dangerous_code=True,
        agent_type="tool-calling"
    )

    # Purani chat history screen par dikhayein
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # Naya chat input box (niche dikhega)
    user_question = st.chat_input("Ask a question about your data... (e.g., Total sales and top product?)")

    if user_question:
        # User ka question history me save aur display karein
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        # Agent se answer generate karwayein
        with st.chat_message("assistant"):
            with st.spinner("Analyzing data..."):
                try:
                    response = agent.invoke(user_question)
                    output = response["output"]
                    
                    # JSON/List list output theek karne ka logic
                    if isinstance(output, list) and len(output) > 0 and isinstance(output[0], dict) and "text" in output[0]:
                        final_answer = output[0]["text"]
                    else:
                        final_answer = output
                        
                    # Answer screen par print karein aur history me save karein
                    st.markdown(final_answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": final_answer})
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")