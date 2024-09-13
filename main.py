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

def main():
    st.title("Product Recommendation System")

    # Load the vector database
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.load_local('faiss-index', embeddings, allow_dangerous_deserialization=True)

    # Initialize session state
    if 'stage' not in st.session_state:
        st.session_state.stage = 'input'

    if st.session_state.stage == 'input':
        user_input = st.text_area("Enter your requirements:", height=100)

        if st.button("Get Recommendations"):
            if user_input:
                st.session_state.user_input = user_input
                st.session_state.stage = 'recommendations'
                st.experimental_rerun()
            else:
                st.warning("Please enter your requirements.")

    elif st.session_state.stage == 'recommendations':
        # Process user input
        processed_input = process_user_input(st.session_state.user_input)
        st.subheader("Processed Input:")
        st.write(processed_input)

        # Get recommendations
        recommendations = get_recommendations(vector_db, processed_input)

        # Display recommendations
        st.subheader("Top Recommendations:")
        for i, doc in enumerate(recommendations, 1):
            with st.expander(f"Recommendation {i}: {doc.metadata['name']}"):
                st.write(f"**Platform:** {doc.metadata['platform']}")
                st.write(f"**Description:** {doc.page_content[:200]}...")

        # Ask if user is satisfied
        satisfaction = st.radio("Are you satisfied with these recommendations?", ('Yes', 'No'))
        if st.button("Submit"):
            if satisfaction == 'Yes':
                st.session_state.stage = 'end'
            else:
                st.session_state.stage = 'input'
            st.experimental_rerun()

    elif st.session_state.stage == 'end':
        st.success("Thank you for using the Product Recommendation System!")
        if st.button("Start Over"):
            st.session_state.stage = 'input'
            st.experimental_rerun()

if __name__ == "__main__":
    main()