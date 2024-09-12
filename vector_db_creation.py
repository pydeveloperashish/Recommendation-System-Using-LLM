from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Vector Database Setup
def setup_vector_db(df):
    documents = [Document(page_content=row['combined_text'], 
                          metadata={'id': row['ID'], 'name': row['Product Name'], 'platform': row['Platform']}) 
                 for _, row in df.iterrows()]
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local('faiss-index')
    return vectorstore

df = pd.read_csv('processed_final_data.csv')


# Set up the vector database
vectorstore = setup_vector_db(df)

