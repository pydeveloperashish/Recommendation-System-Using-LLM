import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os 

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# User Input Processing
def process_user_input(user_input):
    template = """
    Extract key information from the following user request:
    {user_input}
    
    Provide the output in the following format:
    Product Type:
    Platform:
    Key Features:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["user_input"])
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(user_input)

# Recommendation System
def get_recommendations(vectorstore, processed_input, top_k=3):
    results = vectorstore.similarity_search(processed_input, k=top_k)
    return results

# Streamlit UI
st.title("Product Recommendation System")

# Load embeddings and vector database
@st.cache_resource
def load_vectorstore():
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    return FAISS.load_local('faiss-index', embeddings, allow_dangerous_deserialization=True)

vector_db = load_vectorstore()

# User input
user_input = st.text_area("Enter your requirements:", height=100)

if st.button("Get Recommendations"):
    if user_input:
        processed_input = process_user_input(user_input)
        
        st.subheader("Processed Input:")
        st.text(processed_input)
        
        st.subheader("Top Recommendations:")
        
        recommendations = get_recommendations(vector_db, processed_input)
        
        for i, doc in enumerate(recommendations, 1):
            st.markdown(f"**Recommendation {i}:**")
            st.write(f"**Product:** {doc.metadata['name']}")
            st.write(f"**Platform:** {doc.metadata['platform']}")
            st.write(f"**Description:** {doc.page_content[:200]}...")
            st.markdown("---")
        
        satisfaction = st.radio("Are you satisfied with these recommendations?", ("Yes", "No"))
        if satisfaction == "Yes":
            st.success("Great! Thank you for using the Product Recommendation System!")
        else:
            st.info("Feel free to modify your requirements and try again.")
    else:
        st.warning("Please enter your requirements.")