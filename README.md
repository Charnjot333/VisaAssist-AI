# 🌍 VisaAssist AI

VisaAssist AI is a multilingual AI-powered visa assistance application built using Retrieval-Augmented Generation (RAG), OpenAI, LangChain, ChromaDB, and Streamlit.

The application helps users ask visa-related questions in multiple languages and receive simple, concise, and context-aware answers.

## 🚀 Live Demo

VisaAssist AI is deployed on Streamlit Community Cloud.

Live Application:

https://visaassist-ai-4eblxgnr7mvwkdzzg2gsb2.streamlit.app/

---

## 📌 Project Overview

Visa information is usually distributed across multiple PDF documents, visa checklists, FAQs, and government websites.

VisaAssist AI combines this information into a searchable AI knowledge base.

The system retrieves relevant visa information from the vector database and provides the retrieved context to a Large Language Model for generating the final answer.

The application currently supports visa information for:

- 🇦🇺 Australia
- 🇨🇦 Canada
- 🇬🇧 United Kingdom
- 🇺🇸 United States

Supported visa categories include:

- Visitor Visa
- Student Visa
- Work Visa

---

## ✨ Features

- Multilingual visa question answering
- Retrieval-Augmented Generation (RAG)
- Semantic search using vector embeddings
- PDF document processing
- Web content loading
- ChromaDB vector storage
- OpenAI-based embeddings
- LLM-based answer generation
- Country and visa type selection
- Context-aware visa responses
- General knowledge fallback when stored context is insufficient
- Streamlit-based interactive user interface
- Cloud deployment using Streamlit Community Cloud

---

## 🗣️ Multilingual Support

VisaAssist AI supports questions written in:

- English
- Hindi
- Punjabi
- Hinglish
- Punglish

The application first converts multilingual questions into a clear English retrieval query.

The translated query is used for semantic retrieval from the vector database.

The final answer is generated in the same language or writing style used by the user.

Example:

User Question:

Mainu Australia visitor visa layi kehde documents chahide ne?

Retrieval Query:

What documents are required for an Australia visitor visa?

The system retrieves the relevant Australia visa documents and generates the final response for the user.

---

## 🧠 What I Learned

While developing VisaAssist AI, I learned how Large Language Model applications are built beyond a simple chatbot.

### 1. Retrieval-Augmented Generation (RAG)

I learned how RAG combines external knowledge with a Large Language Model.

Instead of depending only on the model's internal knowledge, the system retrieves relevant information from a custom knowledge base.

RAG Flow:

User Question
        ↓
Query Processing
        ↓
Vector Database Search
        ↓
Relevant Documents Retrieved
        ↓
Context + User Question
        ↓
Large Language Model
        ↓
Final Answer

---

### 2. Document Loading

I learned how to load information from different data sources.

The project uses:

- PDF documents
- Visa checklists
- Visa FAQ documents
- Government visa web pages

PDF documents were loaded using LangChain document loaders.

Web content was collected from selected official visa and immigration web pages.

Each loaded source was converted into LangChain Document objects.

A Document contains:

- page_content
- metadata

The page_content contains the actual text.

The metadata stores information such as the document source and page details.

---

### 3. Web Content Loading

I learned how web pages can be loaded and converted into documents for an AI knowledge base.

During development, I also encountered practical web-loading problems such as:

- Request timeouts
- Remote server disconnections
- Websites blocking automated requests
- Slow government websites

This helped me understand that web document loading is not always reliable and requires error handling.

Some official web content was successfully loaded and combined with the PDF documents.

---

### 4. Text Chunking

Large documents cannot be directly passed to an LLM or efficiently searched as one large block of text.

I learned how to divide documents into smaller text chunks using RecursiveCharacterTextSplitter.

The project uses chunking to divide visa documents into smaller meaningful sections.

Example flow:

Large PDF Document
        ↓
Text Extraction
        ↓
RecursiveCharacterTextSplitter
        ↓
Small Text Chunks

The project used:

- chunk_size = 1000
- chunk_overlap = 200

Chunk overlap helps preserve context between neighbouring chunks.

After combining the PDF and web documents, the final knowledge base contained 76 text chunks.

---

### 5. Vector Embeddings

I learned that embedding models convert text into numerical vector representations.

These vectors capture the semantic meaning of text.

For example:

"What documents are required for a UK visitor visa?"

and

"Which papers do I need for a UK visit visa?"

may use different words but have similar meanings.

Embedding models help the system identify this semantic similarity.

During development, I experimented with:

- sentence-transformers/all-MiniLM-L6-v2
- BAAI/bge-m3
- OpenAI Embeddings

The final application uses OpenAI embeddings.

---

### 6. GPU and CUDA

During the development of the project, I received access to an NVIDIA A100 GPU environment.

I learned how to check CUDA availability using PyTorch.

I also encountered a CUDA compatibility issue where the installed PyTorch version was compiled for a newer CUDA version than the available NVIDIA driver supported.

This helped me understand the relationship between:

- NVIDIA GPU Driver
- CUDA
- PyTorch
- GPU-enabled machine learning models

I also learned that a powerful GPU does not automatically improve every AI workflow.

API-based embedding models such as OpenAI embeddings are processed remotely and therefore do not use the local GPU.

---

### 7. Vector Database and ChromaDB

I learned how vector databases store embeddings and perform semantic similarity search.

VisaAssist AI uses ChromaDB as its vector database.

The final vector database is stored in:

visa_openai_chroma_db/

The vector database contains embeddings generated from the processed visa document chunks.

ChromaDB allows the application to compare the user's query embedding with stored document embeddings.

The most semantically relevant chunks are retrieved.

Retrieval Flow:

User Query
        ↓
Query Embedding
        ↓
ChromaDB
        ↓
Vector Similarity Search
        ↓
Top Relevant Chunks

---

### 8. Embedding Model Consistency

One important concept I learned was that the same embedding model must be used when creating and querying a vector database.

Initially, the vector database was created using a Sentence Transformer embedding model.

When changing the application to OpenAI embeddings, the vector database had to be rebuilt.

The final system uses OpenAI embeddings for both:

- Document embedding
- User query embedding

This ensures that document and query vectors belong to the same embedding space.

---

### 9. Retriever

I learned how a vector store can be converted into a retriever.

The retriever searches ChromaDB and returns the most relevant document chunks.

The project retrieves the top 6 relevant chunks.

The retriever does not generate the final answer.

Its responsibility is only to find relevant information.

Retriever
    ↓
Relevant Documents
    ↓
LLM

---

### 10. Prompt Engineering

I learned how important prompts are when building LLM applications.

The VisaAssist AI prompt defines:

- The role of the AI assistant
- How retrieved context should be used
- Language behaviour
- Answer length
- Visa safety rules
- General knowledge fallback behaviour

The prompt instructs the assistant to:

- Prioritize retrieved visa context
- Give concise answers
- Answer in the user's language style
- Avoid guaranteeing visa approval
- Avoid inventing visa policies
- Recommend official verification when visa information may change

I also learned that incorrect prompt variables can cause LangChain errors.

For example, I encountered:

KeyError: Input to ChatPromptTemplate is missing variables

This happened because a prompt expecting multiple variables was incorrectly used in the translation chain.

The issue was solved by creating two separate prompts:

- translation_prompt
- visa_prompt

---

### 11. LangChain Chains

I learned how LangChain connects different AI components.

The project uses:

- ChatPromptTemplate
- StrOutputParser
- create_stuff_documents_chain
- create_retrieval_chain

The translation chain performs:

Translation Prompt
        ↓
OpenAI LLM
        ↓
StrOutputParser
        ↓
English Retrieval Query

The retrieval chain performs:

User Query
        ↓
Retriever
        ↓
Relevant Visa Documents
        ↓
Document Chain
        ↓
LLM
        ↓
Final Answer

---

### 12. General Knowledge Fallback

The initial version of VisaAssist AI followed strict RAG.

If information was not present in the retrieved documents, the assistant returned:

"The information was not found in the provided visa documents."

This made the chatbot unable to answer some common visa questions.

The final system uses a hybrid answering approach.

Answering Logic:

Relevant Context Available
        ↓
Use Retrieved Visa Context

Context Insufficient
        ↓
Use General LLM Knowledge
        ↓
Recommend Official Verification

The assistant does not claim that general model knowledge is a live government web search.

---

### 13. Streamlit Application Development

I learned how to convert a Jupyter Notebook RAG pipeline into a complete web application using Streamlit.

The Streamlit interface includes:

- Country selection
- Visa type selection
- Chat input
- AI-generated visa answers
- Custom CSS
- Sidebar
- Loading spinner
- Error handling

I also learned how Streamlit reruns the Python application when users interact with widgets.

To avoid repeatedly initializing expensive resources, I used:

@st.cache_resource

This is used to cache:

- Embedding model
- ChromaDB vector store
- LLM client

---

### 14. API Key and Secrets Management

I learned that API keys should never be directly stored in public source code.

The OpenAI API key is stored using Streamlit Secrets.

The application accesses the key using:

st.secrets["OPENAI_API_KEY"]

The API key is configured in Streamlit Community Cloud and is not stored in the public GitHub repository.

---

### 15. Deployment

I learned how to deploy an AI application using Streamlit Community Cloud.

Deployment Flow:

Local Project
        ↓
GitHub Repository
        ↓
requirements.txt
        ↓
Streamlit Community Cloud
        ↓
Secrets Configuration
        ↓
Live Web Application

The application is now publicly accessible through a Streamlit deployment URL.

---

## 🏗️ System Architecture

                    ┌──────────────────────┐
                    │       USER           │
                    │ English / Hindi /    │
                    │ Punjabi / Hinglish   │
                    │ Punglish             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Streamlit Frontend   │
                    │ Country Selection    │
                    │ Visa Type Selection  │
                    │ User Question        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Translation Chain    │
                    │ Multilingual Query   │
                    │        ↓             │
                    │ English Query        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ OpenAI Embeddings    │
                    │ Query → Vector       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      ChromaDB        │
                    │ Vector Similarity    │
                    │ Search               │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Top Relevant Visa    │
                    │ Document Chunks      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ LangChain Retrieval  │
                    │ Chain                │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ OpenAI LLM           │
                    │ Context + Question   │
                    │        ↓             │
                    │ Final Visa Answer    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Streamlit Response   │
                    │ Multilingual Answer  │
                    └──────────────────────┘

---

## 📚 Knowledge Base Architecture

PDF Visa Documents
        +
Official Visa Web Content
        ↓
Document Loaders
        ↓
LangChain Documents
        ↓
RecursiveCharacterTextSplitter
        ↓
76 Text Chunks
        ↓
OpenAI Embeddings
        ↓
ChromaDB
        ↓
visa_openai_chroma_db

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Web application frontend |
| LangChain | RAG pipeline and chain orchestration |
| OpenAI | LLM and embedding generation |
| ChromaDB | Vector database |
| PyPDF | PDF document processing |
| BeautifulSoup / WebBaseLoader | Web content extraction |
| GitHub | Source code management |
| Streamlit Community Cloud | Application deployment |

---

## 📂 Project Structure

VisaAssist-AI/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── content/
│   └── README.md
│
└── visa_openai_chroma_db/
    ├── chroma.sqlite3
    └── vector database files

---

## 🔄 Complete Application Workflow

1. The user selects a country.
2. The user selects a visa type.
3. The user enters a visa-related question.
4. The multilingual question is converted into an English retrieval query.
5. OpenAI embeddings convert the retrieval query into a vector.
6. ChromaDB performs semantic similarity search.
7. The top relevant visa document chunks are retrieved.
8. LangChain provides the retrieved context and question to the LLM.
9. The LLM generates a concise visa answer.
10. If the context is insufficient, the model may provide general visa guidance with an official verification warning.
11. The answer is displayed through the Streamlit interface.

---

## ⚠️ Disclaimer

VisaAssist AI is an educational AI project.

Visa regulations, processing times, fees, and eligibility requirements may change.

Users should verify important visa information from the official immigration authority of the respective country.

VisaAssist AI does not guarantee visa approval.

---

## 🔮 Future Improvements

Future versions of VisaAssist AI can include:

- Live official government website search
- Automatic visa information updates
- Source citations in generated answers
- Country-specific retrieval filtering
- Visa document upload and analysis
- User document checklist generation
- Document completeness checking
- RAG evaluation and retrieval metrics
- Re-ranking of retrieved documents
- Conversation memory
- Voice-based multilingual visa queries

---

## 👩‍💻 Author

**Charanjot Kaur**

MCA Student  
AI / Machine Learning / Generative AI Enthusiast

---

## ⭐ Project Status

VisaAssist AI is successfully developed and deployed.

The current version demonstrates practical implementation of:

- Retrieval-Augmented Generation
- Vector Embeddings
- Semantic Search
- Vector Databases
- Prompt Engineering
- Multilingual Query Processing
- LangChain
- OpenAI
- Streamlit Deployment
