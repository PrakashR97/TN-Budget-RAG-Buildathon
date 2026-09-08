
import os
import streamlit as st

# Import functions from your pipeline modules
from step1_load import load_document
from step2_split import split_documents
from step3_embed_and_vectorstore import create_vector_store
from step4_rag_query import run_rag_query

st.set_page_config(
    page_title="Tamil Nadu Budget 2026–27 AI",
    page_icon="🏛️",
    layout="wide"
)

# Map dropdown selections to PDF files stored in data/ folder
# Double-check that these file names match your exact disk spelling
SCHEME_MAP = {
    "ArtCulture Scheme": "data/art_and_culture.pdf",
    "Tamil Development Scheme": "data/tamil_devlop.pdf",
    "Transportation Scheme": "data/transport_depart.pdf",
    "Natural Resources Scheme": "data/natural_resource.pdf",
    "Law Department": "data/law_department.pdf",
    "Industries Investment Scheme": "data/industries_investment.pdf",
    "Agriculture Scheme": "data/agriculture.pdf",
    "Diary Development Scheme": "data/diary_development.pdf",
}

# 1. Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_scheme" not in st.session_state:
    st.session_state.current_scheme = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# 2. Sidebar setup
with st.sidebar:
    st.title("🏛️ Select Department")
    
    department = st.selectbox(
        "Department:",
        [
            "Department of Artculture",
            "Department of Tamil Development",
            "Department of Transportation",
            "Department of Natural Resources",
            "Department of Law"
            "Department of Industries",
            "Department of Agriculture",
            "Department of Diary Development"
        ]
    )

    if department == "Department of Art and Culture":
        scheme_options = ["ArtCulture Scheme"]
    elif department == "Department of Transportation":
        scheme_options = ["Transportation Scheme"]
    elif department == "Department of Natural Resources":
        scheme_options = ["Natural Resources Scheme"] 
    elif department == "Department of Law":
        scheme_options = ["Law Department"]
    elif department == "Department of Industries":
        scheme_options = ["Industries Investment Scheme"]
    elif department == "Department of Agriculture":
        scheme_options = ["Agriculture Scheme"]
    elif department == "Department of Diary Development":
        scheme_options = ["Diary Development Scheme"]
    else:
        scheme_options = ["Tamil Development Scheme"]

    selected_scheme = st.selectbox("Budget Section:", scheme_options)
    
    if st.button("Load Budget", use_container_width=True):
        pdf_path = SCHEME_MAP.get(selected_scheme)

        if not pdf_path or not os.path.exists(pdf_path):
            st.error(f"File not found: '{pdf_path}'")
        else:
            with st.spinner("Processing Tamil Nadu Budget 2026–27..."):
                docs = load_document(pdf_path)
                chunks = split_documents(docs)
                vector_store, embeddings = create_vector_store(chunks)

            st.session_state.vector_store = vector_store
            st.session_state.current_scheme = selected_scheme
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": f"Hi! I'm ready to help you with the **Tamil Nadu Budget 2026–27 – {selected_scheme}**. What would you like to know?"
                }
            ]
            st.rerun()

    if st.session_state.vector_store is not None:
        st.divider()
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": f"Chat reset! Ask me anything about **Tamil Nadu Budget 2026–27 – {st.session_state.current_scheme}**."
                }
            ]
            st.rerun()

# 3. Main Chat Interface
st.title("🏛️ Tamil Nadu Budget 2026–27 Assistant")

if st.session_state.vector_store is None:
    st.info(
        "👈 Please select a department and budget section from the sidebar "
        "and click **Load Budget** to begin chatting!"
    )
else:
    st.caption(
        f"Currently discussing: **Tamil Nadu Budget 2026–27 – {st.session_state.current_scheme}**"
    )

    # Display past conversation
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if user_query := st.chat_input(
        "Ask anything about Tamil Nadu Budget 2026–27..."
    ):
        # Display user question immediately
        st.chat_message("user").markdown(user_query)
        
        # Append user query to messages BEFORE passing to RAG query
        st.session_state.messages.append(
            {"role": "user", "content": user_query}
        )

        # Generate response using RAG pipeline
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = run_rag_query(
                    query=user_query,
                    vector_store=st.session_state.vector_store,
                    chat_history=st.session_state.messages,
                    scheme_name=st.session_state.current_scheme
                )
                st.markdown(answer)

        # Append assistant response to messages
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

