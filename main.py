import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

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
    llm = ChatOpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain.run(user_input)

def get_recommendations(vectorstore, processed_input, top_k=3):
    results = vectorstore.similarity_search(processed_input, k=top_k)
    return results

def display_recommendations(recommendations, title):
    st.subheader(title)
    for i, doc in enumerate(recommendations, 1):
        with st.expander(f"Recommendation {i}: {doc.metadata['name']}"):
            st.write(f"**Platform:** {doc.metadata['platform']}")
            st.write(f"**Description:** {doc.page_content[:200]}...")

def main():
    st.title("Product Recommendation System")

    # Load the vector database
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.load_local('faiss-index', embeddings, allow_dangerous_deserialization=True)

    # Initialize session state
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'processed_input' not in st.session_state:
        st.session_state.processed_input = None

    # User input
    user_input = st.text_area("Enter your requirements:", height=100)

    if st.button("Get Recommendations") or st.session_state.recommendations is not None:
        if user_input or st.session_state.processed_input is not None:
            if user_input:
                st.session_state.processed_input = process_user_input(user_input)
            
            # st.subheader("Processed Input:")
            # st.write(st.session_state.processed_input)

            st.session_state.recommendations = get_recommendations(vector_db, st.session_state.processed_input)
            display_recommendations(st.session_state.recommendations, "Top Recommendations")

            # Check satisfaction
            satisfaction = st.radio("Are you satisfied with these recommendations?", ('Yes', 'No'))
            if st.button("Submit"):
                if satisfaction == 'Yes':
                    st.success("Thank you for using the Product Recommendation System!")
                    st.session_state.recommendations = None  # Reset for next use
                else:
                    # Get new recommendations without new input
                    st.session_state.recommendations = get_recommendations(vector_db, st.session_state.processed_input, top_k=6)
                    st.experimental_rerun()
        else:
            st.warning("Please enter your requirements.")

if __name__ == "__main__":
    main()