import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import openai

# Access the API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Print a masked version of the key for debugging
st.sidebar.write(f"API Key (masked): {openai_api_key[:5]}...{openai_api_key[-5:]}")

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
    try:
        llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(user_input)
    except openai.error.AuthenticationError as e:
        st.error(f"Authentication Error: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()

# Recommendation System
def get_recommendations(vectorstore, processed_input, top_k=3):
    results = vectorstore.similarity_search(processed_input, k=top_k)
    return results

# Streamlit UI
st.title("Product Recommendation System")

# Load embeddings and vector database
@st.cache_resource
def load_vectorstore():
    try:
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        return FAISS.load_local('faiss-index', embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        st.error(f"Error loading vector store: {str(e)}")
        st.stop()

vector_db = load_vectorstore()

# User input
user_input = st.text_area("Enter your requirements:", height=100)

if st.button("Get Recommendations"):
    if user_input:
        try:
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
                if st.button("Try Again"):
                    st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter your requirements.")