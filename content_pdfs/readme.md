# VisaAssist AI Knowledge Base

This folder represents the content used to build the VisaAssist AI knowledge base.

## PDF Documents

The visa-related PDF documents used in this project contain information about:

- Australia visa requirements
- Canada visa requirements
- United Kingdom visa requirements
- United States visa requirements
- Visitor visa documents and checklists
- Student visa documents and checklists
- Work visa documents and checklists
- Financial requirements
- Visa FAQs and supporting documents

These PDF documents were loaded, processed, and split into smaller text chunks.

## Web Content

Visa-related web content was also collected from official government immigration websites.

The web sources used include:

- UK Standard Visitor Visa website
- US Tourism and Visitor Visa website
- Australia Visitor Visa website

The web content was loaded from official government visa and immigration sources.

## Vector Embeddings

The PDF documents and web content were combined and divided into text chunks.

The text chunks were converted into vector embeddings using OpenAI embeddings.

The generated vector embeddings are stored in the `visa_openai_chroma_db` folder using ChromaDB.

## Knowledge Base Flow

PDF Documents + Official Web Content  
↓  
Document Loading  
↓  
Text Chunking  
↓  
OpenAI Embeddings  
↓  
ChromaDB Vector Database  
↓  
VisaAssist AI Retrieval System

The VisaAssist AI application retrieves relevant visa information from this vector database to answer user queries.
