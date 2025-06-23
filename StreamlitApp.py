import streamlit as st
import os

from QAWithPDF.data_ingestion import load_data
from QAWithPDF.embedding import download_gemini_embedding
from QAWithPDF.model_api import load_model

def main():
    st.set_page_config(page_title="📄✨ QA with Documents", page_icon="📚", layout="centered")

    # Custom CSS for prettiness 💅
    st.markdown("""
    <style>
        .main {
            background-color: #0d1117; /* dark base */
            font-family: 'Segoe UI', sans-serif;
            color: #c9d1d9;
        }

        /* File uploader */
        .stFileUploader {
            background-color: #161b22 !important;
            border: 1px solid #30363d;
            padding: 1em;
            border-radius: 12px;
            color: #c9d1d9;
        }

        /* Text input */
        .stTextInput>div>div>input {
            background-color: #161b22;
            color: #c9d1d9;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 0.6em;
        }

        /* Button */
        .stButton > button {
            background: linear-gradient(to right, #6f42c1, #d63384);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.5em 1.5em;
            font-size: 1em;
            transition: background 0.3s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(to right, #5a32a3, #ad296a);
        }

        /* Response box */
        .response-box {
            background-color: #161b22;
            border-left: 4px solid #6f42c1;
            padding: 1em;
            border-radius: 12px;
            margin-top: 20px;
            font-size: 1.1em;
            color: #f0f6fc;
        }

        /* File name text color fix */
        .uploadedFileName {
            color: #c9d1d9 !important;
        }
    </style>
""", unsafe_allow_html=True)



    st.title("📚💬 QA with Documents")
    st.caption("Ask intelligent questions. Get instant answers from your PDFs.")

    st.markdown("---")

    # Upload document
    uploaded_file = st.file_uploader("📎 Upload your **PDF** document here:", type=["pdf"])
    user_question = st.text_input("🤔 Ask your question:")

    if st.button("🚀 Submit & Process"):
        if uploaded_file is not None:
            with st.spinner("🔍 Analyzing your document..."):
                
                # Save uploaded file to 'Data/' directory
                if not os.path.exists("Data"):
                    os.makedirs("Data")
                
                # Clear old files
                for file in os.listdir("Data"):
                    os.remove(os.path.join("Data", file))
                
                # Save new file
                with open(os.path.join("Data", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load and process
                document = load_data("Data")
                model = load_model()
                query_engine = download_gemini_embedding(model, document)
                response = query_engine.query(user_question)

                st.markdown(f"<div class='response-box'>{response.response}</div>", unsafe_allow_html=True)

        else:
            st.warning("⚠️ Please upload a PDF before submitting.")

if __name__ == "__main__":
    main()
