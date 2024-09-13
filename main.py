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
    If the new request is refining or changing previous requirements, focus on the changes or additions.
    
    Provide the output in the following format:
    Product Type:
    Platform:
    Key Features:
    
    Also, briefly explain how this differs from or builds upon previous requests.
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
    for i, (input, processed, _) in enumerate(history, 1):
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

    # Initial input
    user_input = st.text_area("Enter your requirements:", height=100, key="initial_input")

    if st.button("Get Recommendations"):
        if user_input:
            history_context = format_history(st.session_state.history)
            processed_input = process_user_input(user_input, history_context)
            st.subheader("Processed Input:")
            st.write(processed_input)

            recommendations = get_recommendations(vector_db, processed_input)
            st.session_state.history.append((user_input, processed_input, recommendations))

    # Display all recommendations
    for i, (input, processed, recs) in enumerate(st.session_state.history):
        st.markdown(f"**Query {i+1}:** {input}")
        st.markdown(f"**Processed:** {processed}")
        display_recommendations(recs, f"Recommendations for Query {i+1}")

    # Check satisfaction only if there are recommendations
    if st.session_state.history:
        satisfaction = st.radio("Are you satisfied with these recommendations?", ('Yes', 'No'))
        if st.button("Submit"):
            if satisfaction == 'Yes':
                st.success("Thank you for using the Product Recommendation System!")
            else:
                st.write("Please provide more specific or different requirements:")
                new_input = st.text_area("Enter your new requirements:", height=100, key="new_input")
                if st.button("Get New Recommendations"):
                    if new_input:
                        history_context = format_history(st.session_state.history)
                        processed_input = process_user_input(new_input, history_context)
                        st.subheader("Processed Input:")
                        st.write(processed_input)

                        new_recommendations = get_recommendations(vector_db, processed_input)
                        st.session_state.history.append((new_input, processed_input, new_recommendations))
                        st.experimental_rerun()  # Rerun to display new recommendations
                    else:
                        st.warning("Please enter your new requirements.")

if __name__ == "__main__":
    main()