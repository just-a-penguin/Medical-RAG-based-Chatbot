import textwrap
import pandas as pd
from langchain import PromptTemplate, LLMChain
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai.llms import GoogleGenerativeAI

# Set up the Google AI LLM
GOOGLE_API_KEY = "AIzaSyAvmQS5uovgaT_UZy2ZfdmyL7zlLuW2oG4"
llm = GoogleGenerativeAI(model_name="gemini-pro", generation_config={"temperature": 0.5}, google_api_key=GOOGLE_API_KEY)

# Load the dataset
dataset = pd.read_csv('dataset.csv')

# Define the prompt template for generating responses
response_template = """Can you give me a chatbot response for the following patient query: {user_input}?

Medicine Details:
{medicine_details}"""

response_prompt = PromptTemplate(
    input_variables=["user_input", "medicine_details"],
    template=response_template,
)

# Create the LLM chain
response_chain = LLMChain(llm=llm, prompt=response_prompt)

def generate_response(user_input):
    inputTokens = user_input.split()
    medicines = set(word for medicine in dataset['Medicine Name'] for word in medicine.split())

    # Check if the user input contains a medicine
    medicine_index = -1
    for i, token in enumerate(inputTokens):
        if token in medicines:
            medicine_index = i
            break

    if medicine_index == -1:
        # No medicine found, generate a general response
        return response_chain.run(user_input=user_input, medicine_details="")
    else:
        # Get the medicine name and details from the dataset
        medicine = inputTokens[medicine_index]
        medicine_details = dataset[dataset['Medicine Name'].str.contains(medicine, case=False)]

        if medicine_details.empty:
            return f"Sorry, I don't have information about {medicine}."

        medicine_info = medicine_details.iloc[0]
        st = textwrap.dedent(f"""
            • Composition: {medicine_info['Composition']}
            • Uses: {medicine_info['Uses']}
            • Side Effects: {medicine_info['Side_effects']}
            • Manufacturer: {medicine_info['Manufacturer']}
            • Excellent Review %: {medicine_info['Excellent Review %']}
            • Average Review %: {medicine_info['Average Review %']}
            • Poor Review %: {medicine_info['Poor Review %']}
            • Image URL: {medicine_info['Image URL']}""")

        # Generate a response based on the medicine details
        return response_chain.run(user_input=user_input, medicine_details=st)
    

# Example usage
user_input = "What are the side effects of Paracetamol?"
response = generate_response(user_input)
print(response)
