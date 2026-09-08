# 🏛️ Tamil Nadu Budget AI Assistant

An interactive Retrieval-Augmented Generation (RAG) web application powered by **LangChain**, **OpenAI (GPT-4o-mini)**, and **Streamlit**. This assistant enables users to query and analyze specific departmental budget documents and government schemes for the Tamil Nadu Budget with high accuracy and contextual understanding.

## 📌 Project Overview

The **Tamil Nadu Budget AI Assistant** simplifies navigating complex government budget documents. By selecting a target department, the application dynamically loads, chunks, embeds, and indexes the corresponding budget PDF. Users can then engage in a natural conversation with the AI to ask questions, extract specific figures, or clarify scheme details.

The core pipeline leverages LangChain's expression language (`LCEL`) combined with OpenAI's `gpt-4o-mini` model to ensure answers are grounded exclusively in the provided budget context while maintaining multi-turn chat history.

## ✨ Key Features

* **Department & Scheme Filtering**: Easily switch between budget sections (e.g., Agriculture, Transportation, Art & Culture, Law, Industries).

* **Dynamic PDF Processing**: Seamlessly loads and creates vector stores for selected documents on demand.

* **Context-Aware RAG Pipeline**:

  * Top-$k$ document chunk retrieval ($k=3$) using vector similarity search.

  * Context-constrained prompting to eliminate model hallucinations.

* **Multi-turn Chat Memory**: Preserves past conversation history (`HumanMessage` and `AIMessage`) for natural follow-up queries.

* **Interaction Analytics & Audit Logging**: Automatically records every user prompt, generated answer, and source document chunk into both `.json` and `.csv` files for tracking and auditability.

* **User-Friendly UI**: Built with Streamlit featuring dynamic sidebars, clear action buttons, and responsive chat interface state handling.

## 📁 Project Structure

```
├── data/                         # Folder containing departmental PDF budget documents
│   ├── agriculture.pdf
│   ├── art_and_culture.pdf
│   ├── diary_development.pdf
│   ├── industries_investment.pdf
│   ├── law_department.pdf
│   ├── natural_resource.pdf
│   ├── tamil_devlop.pdf
│   └── transport_depart.pdf
├── app.py                        # Streamlit web application interface and state management
├── step1_load.py                 # PDF document loading module
├── step2_split.py                # Document splitting and chunking logic
├── step3_embed_and_vectorstore.py # Embedding generation & vector store creation
├── step4_rag_query.py            # Core RAG chain setup and response generation execution
├── logger.py                     # Interaction logging utilities (JSON and CSV writers)
├── .env                          # Environment variables configuration (API keys)
├── requirements.txt              # Project Python dependencies
└── README.md                     # Technical documentation

```

## ⚙️ How It Works (Pipeline Architecture)

1. **Document Ingestion (`step1_load.py` & `step2_split.py`)**:
   When a user selects a department and clicks **Load Budget**, the associated PDF file is loaded into memory and split into smaller chunks suitable for embedding.

2. **Embedding & Vector Storage (`step3_embed_and_vectorstore.py`)**:
   Text chunks are converted into dense vector representations using OpenAI embeddings and stored in an in-memory vector store.

3. **Query & Context Retrieval (`step4_rag_query.py`)**:

   * The user inputs a query in the chat UI.

   * The vector store retrieves the top 3 most relevant document chunks based on semantic similarity.

   * Previous conversation history from `st.session_state` is formatted into LangChain message objects (`HumanMessage` / `AIMessage`).

4. **Response Generation**:

   * The combined prompt (System Prompt + Context + Chat History + User Question) is passed to `ChatOpenAI(model="gpt-4o-mini", temperature=0)`.

   * `StrOutputParser()` parses and streams the final answer back to the UI.

5. **Logging (`logger.py`)**:

   * The session details, scheme name, question, answer, and retrieved chunks are saved locally for analysis and auditing.

## 🚀 Getting Started

### Prerequisites

* Python 3.9 or higher

* An active **OpenAI API Key**

### 1. Clone the Repository

```
git clone https://github.com/your-username/tn-budget-ai-assistant.git
cd tn-budget-ai-assistant

```

### 2. Create and Activate a Virtual Environment

* **On macOS/Linux:**

  ```
  python3 -m venv venv
  source venv/bin/activate
  
  ```

* **On Windows:**

  ```
  python -m venv venv
  venv\Scripts\activate
  
  ```

### 3. Install Dependencies

```
pip install -r requirements.txt

```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_actual_openai_api_key_here

```

### 5. Prepare Data Directory

Ensure all required budget PDF files are placed in the `data/` folder matching the file paths configured in `app.py`:

* `data/art_and_culture.pdf`

* `data/tamil_devlop.pdf`

* `data/transport_depart.pdf`

* `data/natural_resource.pdf`

* `data/law_department.pdf`

* `data/industries_investment.pdf`

* `data/agriculture.pdf`

* `data/diary_development.pdf`

## 💻 Running the Application

Launch the Streamlit server:

```
streamlit run app.py

```

1. Open your browser and navigate to `http://localhost:8501`.

2. Select a **Department** and **Budget Section** from the left sidebar.

3. Click **Load Budget**.

4. Once processed, start asking questions regarding the budget in the chat box!

## 🛠️ Key Technologies & Frameworks

| **Component** | **Technology** | 
| **Frontend / Web UI** | [Streamlit](https://streamlit.io/) | 
| **LLM Orchestration** | [LangChain](https://www.langchain.com/) | 
| **LLM Model** | OpenAI `gpt-4o-mini` | 
| **Document Loaders** | `langchain_community` / PyPDF | 
| **Environment Config** | `python-dotenv` | 
| **Language** | Python 3.9+ | 

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
