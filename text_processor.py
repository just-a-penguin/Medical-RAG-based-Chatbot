# text_processor.py

# def generate_response(user_input):
#     # Your logic for generating responses based on user input goes here
#     if user_input.lower() == "hello":
#         return "Hi there!"
#     elif user_input.lower() == "how are you?":
#         return "I'm doing well, thank you for asking!"
#     else:
#         return "Sorry, I didn't understand that. Can you please rephrase?"



import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
import pandas as pd
import numpy as np
import googletrans
from googletrans import Translator

def translate_to_hindi(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='hi')
    return translated_text.text



def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True)) 

GOOGLE_API_KEY="AIzaSyAvmQS5uovgaT_UZy2ZfdmyL7zlLuW2oG4"

genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

model = genai.GenerativeModel('gemini-pro')
generation_config = genai.GenerationConfig(temperature=0.5) 


#  load dataset.csv
dataset = pd.read_csv('dataset.csv')

# make a list of all the medicines by usiong the "Medicine Name" column of the dataset and splitting the values by space  and addding them into a set
medicines = set()
for medicine in dataset['Medicine Name']:
    for word in medicine.split():
        medicines.add(word)

def generate_response(user_input):
    inputTokens = user_input.split()
    # check if the user input is a medicine and find its index
    medicine_index = -1
    for i, token in enumerate(inputTokens):
        if token in medicines:
            medicine_index = i
            break
    if medicine_index == -1:
      response = model.generate_content(f"Can you give me a chatbot response for the following patient query: {user_input}?")
      return response.text
    else:
      #  rettrieve the medicine name from the user input
      medicine = inputTokens[medicine_index]
      #  get the medicine details from the dataset
      medicine_details = dataset[dataset['Medicine Name'].str.contains(medicine, case=False)]
      #  if the medicine details are not found, return a response
      if medicine_details.empty:
          return f"Sorry, I don't have information about {medicine}."
      #  get the first row of the medicine details
      medicine_info = medicine_details.iloc[0]
      #  return the medicine details using  Medicine Name	Composition	Uses	Side_effects	Image URL	Manufacturer	Excellent Review %	Average Review %	Poor Review % imformation
      st= f"Here is the information about {medicine}:\n\n" + \
             f"• Composition: {medicine_info['Composition']}\n" + \
             f"• Uses: {medicine_info['Uses']}\n" + \
             f"• Side Effects: {medicine_info['Side_effects']}\n" + \
             f"• Manufacturer: {medicine_info['Manufacturer']}\n" + \
             f"• Excellent Review %: {medicine_info['Excellent Review %']}\n" + \
             f"• Average Review %: {medicine_info['Average Review %']}\n" + \
             f"• Poor Review %: {medicine_info['Poor Review %']}\n" + \
             f"• Image URL: {medicine_info['Image URL']}"
      response= model.generate_content(f"Can you give a short description of {medicine} using {st} informationm")
      return response.text
        

  
# def generate_response(user_input):
#     inputTokens = user_input.split()
#     # check if the user input is a medicine and find its index
#     medicine_index = -1
#     for i, token in enumerate(inputTokens):
#         if token in medicines:
#             medicine_index = i
#             break
#     if medicine_index == -1:
#         response = model.generate_content(f"Can you give me a chatbot response for the following patient query: {user_input}?")
#         return translate_to_hindi(response.text)
#     else:
#         #  rettrieve the medicine name from the user input
#         medicine = inputTokens[medicine_index]
#         #  get the medicine details from the dataset
#         medicine_details = dataset[dataset['Medicine Name'].str.contains(medicine, case=False)]
#         #  if the medicine details are not found, return a response
#         if medicine_details.empty:
#             return translate_to_hindi(f"Sorry, I don't have information about {medicine}.")
#         #  get the first row of the medicine details
#         medicine_info = medicine_details.iloc[0]
#         #  return the medicine details using  Medicine Name	Composition	Uses	Side_effects	Image URL	Manufacturer	Excellent Review %	Average Review %	Poor Review % imformation
#         st= f"Here is the information about {medicine}:\n\n" + \
#                 f"• Composition: {medicine_info['Composition']}\n" + \
#                 f"• Uses: {medicine_info['Uses']}\n" + \
#                 f"• Side Effects: {medicine_info['Side_effects']}\n" + \
#                 f"• Manufacturer: {medicine_info['Manufacturer']}\n" + \
#                 f"• Excellent Review %: {medicine_info['Excellent Review %']}\n" + \
#                 f"• Average Review %: {medicine_info['Average Review %']}\n" + \
#                 f"• Poor Review %: {medicine_info['Poor Review %']}\n" + \
#                 f"• Image URL: {medicine_info['Image URL']}"
#         response = model.generate_content(f"Can you give a short description of {medicine} using {st} informationm")
#         return translate_to_hindi(response.text)