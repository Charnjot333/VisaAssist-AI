import os
import streamlit as st

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from langchain_classic.chains import create_retrieval_chain


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VisaAssist AI",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #f8fafc 0%,
            #eef2ff 50%,
            #f0fdfa 100%
        );
    }

    .main-title {
        text-align: center;
        font-size: 58px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #64748b;
        margin-bottom: 35px;
    }

    .info-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
    }

    .answer-card {
        background: white;
        padding: 28px;
        border-radius: 18px;
        border-left: 6px solid #4f46e5;
        box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.08);
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🌍 VisaAssist AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Your Multilingual AI Visa Assistant
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# OPENAI API KEY
# ============================================================


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# ============================================================
# LOAD OPENAI EMBEDDING MODEL
# ============================================================

@st.cache_resource
def load_embedding_model():

    return OpenAIEmbeddings(
        model="text-embedding-3-small"
    )


embedding_model = load_embedding_model()


# ============================================================
# LOAD OPENAI CHROMA DATABASE
# ============================================================

@st.cache_resource
def load_vectorstore():

    return Chroma(
        persist_directory="./visa_openai_chroma_db",
        embedding_function=embedding_model
    )


vectorstore = load_vectorstore()


# ============================================================
# CREATE RETRIEVER
# ============================================================

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 6
    }
)


# ============================================================
# LOAD OPENAI LLM
# ============================================================

@st.cache_resource
def load_llm():

    return ChatOpenAI(
        model="gpt-5-mini",
        temperature=0
    )


llm = load_llm()


# ============================================================
# TRANSLATION PROMPT
# ============================================================

translation_prompt = ChatPromptTemplate.from_template(
    """
You are a multilingual query translation assistant.

Convert the user's visa question into clear English.

The user may write in:

- English
- Hindi
- Punjabi
- Hinglish
- Punglish

If the question is already English, return the same question
in clear English.

Only return the English question.

Do not answer the visa question.

USER QUESTION:

{question}
"""
)


# ============================================================
# CREATE TRANSLATION CHAIN
# ============================================================

translation_chain = (
    translation_prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# VISA ASSISTANT PROMPT
# ============================================================


visa_prompt = ChatPromptTemplate.from_template(
    """
You are VisaAssist AI, a multilingual visa assistant.

Answer the user's visa question clearly, accurately, and concisely.

Rules:
- First use the provided visa context.
- If the context is insufficient, use your general knowledge to give a helpful answer.
- If using general knowledge, mention that visa rules may change and the user should verify current information from the official immigration website.
- Never guarantee visa approval or invent requirements, fees, processing times, or policies.
- Consider the selected country and visa type.
- Answer in the same language and writing style as the user.
- Support English, Hindi, Punjabi, Hinglish, and Punglish.
- Use simple language and bullet points where helpful.
- Give a concise answer. Do not add unnecessary explanation.
- Do not mention RAG, Chroma, embeddings, retrieved documents, context, or internal system details.

Country: {country}
Visa Type: {visa_type}

Visa Context:
{context}

User Question:
{original_question}

English Retrieval Query:
{input}
"""
)


# ============================================================
# CREATE DOCUMENT CHAIN
# ============================================================

document_chain = create_stuff_documents_chain(
    llm,
    visa_prompt
)


# ============================================================
# CREATE RETRIEVAL CHAIN
# ============================================================

retrieval_chain = create_retrieval_chain(
    retriever,
    document_chain
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌍 VisaAssist")

    st.write(
        "Select your visa details before asking a question."
    )

    st.divider()

    country = st.selectbox(
        "🌎 Select Country",
        [
            "Australia",
            "Canada",
            "United Kingdom",
            "United States"
        ]
    )

    visa_type = st.selectbox(
        "📄 Select Visa Type",
        [
            "Visitor Visa",
            "Student Visa",
            "Work Visa"
        ]
    )

    st.divider()

    st.subheader("🗣️ Supported Languages")

    st.write(
        """
        🇬🇧 English

        🇮🇳 Hindi

        🪯 Punjabi

        💬 Hinglish

        💬 Punglish
        """
    )

    st.divider()

    st.caption(
        "AI-powered multilingual visa guidance."
    )


# ============================================================
# VISA SEARCH CARD
# ============================================================

st.markdown(
    f"""
    <div class="info-card">

    <h3>✈️ Your Visa Search</h3>

    <b>Country:</b> {country}

    <br>

    <b>Visa Type:</b> {visa_type}

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask your visa question..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    with st.chat_message("user"):

        st.write(question)


    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Analysing your visa question..."
        ):

            try:

                # ============================================
                # TRANSLATE QUESTION
                # ============================================

                english_query = translation_chain.invoke(
                    {
                        "question": question
                    }
                )


                # ============================================
                # CREATE RETRIEVAL QUERY
                # ============================================

                retrieval_query = f"""
Country: {country}

Visa Type: {visa_type}

Question: {english_query}
"""


                # ============================================
                # RUN RAG CHAIN
                # ============================================

                response = retrieval_chain.invoke(
                    {
                        "input": retrieval_query,
                        "original_question": question,
                        "country": country,
                        "visa_type": visa_type
                    }
                )


                # ============================================
                # DISPLAY ANSWER
                # ============================================

                st.markdown(
                    '<div class="answer-card">',
                    unsafe_allow_html=True
                )

                st.subheader(
                    "🤖 VisaAssist Answer"
                )

                st.write(
                    response["answer"]
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            except Exception as error:

                st.error(
                    f"VisaAssist encountered an error: {error}"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#64748b;">

    🌍 VisaAssist AI

    Multilingual AI-Powered Visa Guidance

    </div>
    """,
    unsafe_allow_html=True
)