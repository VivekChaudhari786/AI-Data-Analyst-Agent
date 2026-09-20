import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import os

# 1. Streamlit secrets se Gemini API key direct environment me set karein
os.environ["GOOGLE_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# 2. Page configuration
st.set_page_config(page_title="AI Data Analyst Agent", page_icon="📊", layout="wide")
st.title("📊 AI Data Analyst Agent")
st.markdown("Upload your CSV file and chat with your data!")

# 3. Chat history ko session state me save karne ka logic
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. File Uploader
uploaded_file = st.file_uploader("Upload your CSV data file", type=["csv"])

if uploaded_file:
    # Data load karein
    df = pd.read_csv(uploaded_file)
    
    # 5. Smart Master Prompt (To fix logic errors for Hinglish and max/min queries)
    master_prompt = """
    You are an expert Data Analyst who understands Hindi and Hinglish.
    CRITICAL PANDAS RULES:
    1. When asked for "sabse zyada" (highest/most) or "sabse kam" (lowest/least) of a product/category, YOU MUST ALWAYS use df.groupby() and .sum() to aggregate the data first. DO NOT just find the max value of a single row.
    2. For example, if asked "sabse jyada sale kis product ki hui" or "sabse zyada Total Sales", the correct logic is: df.groupby('Product Name')['Total Sales (INR)'].sum().idxmax().
    3. If asked about "Quantity Sold ke hisab se sabse zyada", the correct logic is: df.groupby('Product Name')['Quantity Sold'].sum().idxmax().
    4. Never return the result of a single transaction unless explicitly asked for a single order. Always aggregate total sales or total quantity across the entire dataset.
    """
    
    # 6. Agent Initialize karein (with prefix prompt)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    agent = create_pandas_dataframe_agent(
        llm, 
        df, 
        verbose=True, 
        allow_dangerous_code=True,
        agent_type="tool-calling",
        prefix=master_prompt
    )

    # 7. Purani chat history screen par dikhayein
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # 8. Naya chat input box (niche dikhega)
    user_question = st.chat_input("Ask a question about your data... (e.g., Sabse jyada sale kis product ki hui?)")

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
                    
                    # JSON/List output ko clean text me badalne ka logic
                    if isinstance(output, list) and len(output) > 0 and isinstance(output[0], dict) and "text" in output[0]:
                        final_answer = output[0]["text"]
                    else:
                        final_answer = output
                        
                    # Answer screen par print karein aur history me save karein
                    st.markdown(final_answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": final_answer})
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
