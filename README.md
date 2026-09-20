# 📊 AI-Powered Tabular Data Analyst Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Experimental-000000?logo=langchain)](https://www.langchain.com/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?logo=google)](https://ai.google.dev/)

An autonomous AI Data Analyst agent that enables non-technical business stakeholders to interact with raw tabular datasets (CSV) using natural language. Powered by **Google Gemini 2.5 Flash** and **LangChain's Tool-Calling Agent**, this application dynamically interprets analytical queries, writes and executes Python/Pandas logic in a secure sandbox, and returns structured data insights via a conversational chat interface.

---

## 🚀 Key Features

- **Natural Language Data Querying:** Ask complex, multi-part analytical questions without writing SQL or Pandas syntax.
- **Tool-Calling Architecture:** Utilizes function calling rather than fragile regex parsers, ensuring zero-hallucination code execution.
- **Conversational Memory:** Preserves multi-turn conversation context using Streamlit's `session_state`.
- **Zero-Setup User Experience:** Pre-configured secure backend secrets so recruiters and end-users do not need to provide their own API keys.
- **Dynamic Aggregations & Metrics:** Computes distributions, averages, top performers, and groupings on-the-fly.

---

## 🛠️ Architecture & Workflow

```
┌─────────────────┐       ┌────────────────────────┐       ┌───────────────────────────┐
│   User Upload   │ ----> │    Streamlit Frontend  │ ----> │    LangChain Agent        │
│    (CSV File)   │       │   (Chat Session State) │       │ (Gemini 2.5 Flash Engine) │
└─────────────────┘       └────────────────────────┘       └─────────────┬─────────────┘
                                                                         │
                                                                         ▼
┌─────────────────┐       ┌────────────────────────┐       ┌───────────────────────────┐
│ Final Insights  │ <---- │ Streamlit Output Card  │ <---- │  Python REPL Execution    │
│  & Explanations │       │   (Formatted Results)  │       │ (In-memory Pandas logic)  │
└─────────────────┘       └────────────────────────┘       └───────────────────────────┘
```

1. **Ingestion:** Raw CSV file is loaded into an in-memory Pandas DataFrame.
2. **Intent Parsing:** Gemini reads the column schema and translates the user's plain-English question into executable Pandas queries.
3. **Sandbox Execution:** The LangChain agent toolkit executes the Python code in a sandboxed REPL environment.
4. **Context Synthesis:** Quantitative results are interpreted and presented back to the user in a clean, human-readable format.

---

## 💻 Tech Stack

- **Language:** Python 3.10+
- **Frontend / Framework:** Streamlit
- **LLM Reasoning Engine:** Google Gemini (`gemini-2.5-flash`) via `langchain-google-genai`
- **Agent Framework:** `langchain-experimental` (Tool-Calling DataFrame Agent)
- **Data Manipulation:** Pandas, Tabulate

---

## 📦 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-data-analyst-agent.git
cd ai-data-analyst-agent
```

### 2. Create and Activate a Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Local Secrets
Create a `.streamlit/secrets.toml` file in the root directory:
```toml
GEMINI_API_KEY = "your-google-gemini-api-key-here"
```

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser to start analyzing data.

---

## 📄 Requirements (`requirements.txt`)

```text
streamlit
pandas
langchain-google-genai
langchain-experimental
tabulate
```

---

## ☁️ Deployment (Streamlit Community Cloud)

1. Push your repository to **GitHub** (ensure `.streamlit/secrets.toml` is included in your `.gitignore`).
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/) with your GitHub account.
3. Click **"New App"** and select your repository, branch, and `app.py`.
4. Open **Advanced Settings** -> **Secrets**, and add:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   ```
5. Click **Deploy**!

---

## 🗺️ Roadmap & Scaling Strategy

- [ ] **Multilingual & Hinglish Semantic Layer:** Implement metadata prompt injection to map non-English business terms (e.g., *"sabse zyada bikri"*, *"sasta"*, *"faayda"*) directly to numerical columns without hallucinations.
- [ ] **Interactive Visualizations:** Integrate automated Plotly charts (`st.plotly_chart`) based on agent-selected chart types (bar charts, time-series lines, heatmaps).
- [ ] **High-Scale Analytical Engines:** Transition the execution backend from single-threaded Pandas to **DuckDB** or **Polars** to query multi-gigabyte datasets without memory constraints.
- [ ] **Direct SQL Database Connectors:** Support live connections to PostgreSQL, Snowflake, and BigQuery.

---

## 👤 Author

- **GitHub:** [@your-username](https://github.com/your-username)
- **LinkedIn:** [Your Name](https://linkedin.com/in/your-profile)