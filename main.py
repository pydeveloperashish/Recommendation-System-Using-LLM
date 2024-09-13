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

def process_user_input(user_input, history):
    template = """
    Previous interactions:
    {history}

    New user request:
    {user_input}
    
    Based on the previous interactions and the new user request, extract key information.
    If this is a refinement of previous requests, focus on what's new or different.
    
    Provide the output in the following format:
    Product Type:
    Platform:
    Key Features:
    
    Also, briefly explain how this differs from or builds upon previous requests, if applicable.
    """
    
    prompt = PromptTemplate(template=template, input_variables=["history", "user_input"])
    llm = ChatOpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain.run(history=history, user_input=user_input)

def get_recommendations(vectorstore, processed_input, top_k=3):
    results = vectorstore.similarity_search(processed_input, k=top_k)
    return results

def display_recommendations(recommendations, title):
    st.subheader(title)
    for i, doc in enumerate(recommendations, 1):
        with st.expander(f"Recommendation {i}: {doc.metadata['name']}"):
            st.write(f"**Platform:** {doc.metadata['platform']}")
            st.write(f"**Description:** {doc.page_content[:200]}...")

def format_history(history):
    formatted = ""
    for i, (input, processed) in enumerate(history, 1):
        formatted += f"Query {i}:\nUser Input: {input}\nProcessed Output: {processed}\n\n"
    return formatted

def main():
    st.title("Product Recommendation System")

    # Load the vector database
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.load_local('faiss-index', embeddings, allow_dangerous_deserialization=True)

    # Initialize session state
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None

    # User input
    user_input = st.text_area("Enter your requirements:", height=100)

    if st.button("Get Recommendations") or st.session_state.recommendations is not None:
        if user_input or st.session_state.history:
            if user_input:
                history_context = format_history(st.session_state.history)
                processed_input = process_user_input(user_input, history_context)
                st.session_state.history.append((user_input, processed_input))
            else:
                processed_input = st.session_state.history[-1][1]  # Use the last processed input

            st.session_state.recommendations = get_recommendations(vector_db, processed_input)
            display_recommendations(st.session_state.recommendations, "Top Recommendations")

            # Check satisfaction
            satisfaction = st.radio("Are you satisfied with these recommendations?", ('Yes', 'No'))
            if st.button("Submit"):
                if satisfaction == 'Yes':
                    st.success("Thank you for using the Product Recommendation System!")
                else:
                    # Get new recommendations without new input, but considering history
                    history_context = format_history(st.session_state.history)
                    refined_input = process_user_input(f"{processed_input} Please provide more diverse recommendations", history_context)
                    st.session_state.recommendations = get_recommendations(vector_db, refined_input, top_k=6)
                st.rerun()
        else:
            st.warning("Please enter your requirements.")

    # Display history
    # if st.session_state.history:
    #     st.subheader("Output history History:")
    #     for i, (input, processed) in enumerate(st.session_state.history, 1):
    #         with st.sidebar(f"Query {i}"):
    #             st.write(f"**User Input:** {input}")
    #             st.write(f"**Processed:** {processed}")

if __name__ == "__main__":
    main()