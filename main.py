from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

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
    llm = OpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain.run(user_input)


# Recommendation System
def get_recommendations(vectorstore, processed_input, top_k=3):
    results = vectorstore.similarity_search(processed_input, k=top_k)
    return results


# Main execution
if __name__ == "__main__":
 
   
    # Preprocess the data
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.load_local('faiss-index', embeddings, allow_dangerous_deserialization=True)

    # User interaction loop
    while True:
        user_input = input("Enter your requirements (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
        
        processed_input = process_user_input(user_input)
        print("Processed Input:")
        print(processed_input)
        print("\nTop Recommendations:")
        
        recommendations = get_recommendations(vector_db, processed_input)
        
        for doc in recommendations:
            print(f"Product: {doc.metadata['name']}")
            print(f"Platform: {doc.metadata['platform']}")
            print(f"Description: {doc.page_content[:200]}...")
            print("---")
        
        satisfaction = input("Are you satisfied with these recommendations? (y/n): ")
        if satisfaction.lower() == 'y':
            break

print("Thank you for using the Product Recommendation System!")