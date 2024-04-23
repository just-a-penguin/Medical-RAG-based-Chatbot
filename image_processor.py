

import keras_ocr
import matplotlib.pyplot as plt
import pytesseract
import numpy as np
from PIL import Image
# import text_processor
# from text_processor import image_process 

pipeline = keras_ocr.pipeline.Pipeline()



def process_image(filename):
    print(f"Processing image: {filename}")
    # return "hello I dont want to read ur images :) , Is it even important, I really dont care."
    try:
        image=keras_ocr.tools.read(filename)
        # Get predictions
        prediction_groups = pipeline.recognize([image])
        # print(prediction_groups)
        text1=""
        for x in prediction_groups:
            for text, box in x:
                text1+=" "+text

        with Image.open(filename) as img:
            width, height = img.size
            text2 = pytesseract.image_to_string(img)

        text_list_1 = text1.split()
        text_list_2 = text2.split()

        word_match = 0

        for i in range (min(len(text_list_1), len(text_list_2))) :
            if text_list_1[i].lower() == text_list_2[i].lower():
                word_match += 1
        
        confid = 0.3 * ((word_match/max(len(text_list_1), len(text_list_2)))*100)
        confid += 70
        confid = int(confid)

        return text1 + " \n " + " ||  CONFIDENCE SCORE: #" + str(confid)


    except Exception as e:
        return f"Error processing image: {e}"




# print(process_image("/Users/abby/Downloads/53__Baseline/print_pic2.jpeg"))
# print(process_image("/Users/abby/Downloads/53__Baseline/written.png"))





# def process_image(filename):
#     print(f"Processing image: {filename}")
#     try:
#         image = keras_ocr.tools.read(filename)
#         # Get predictions
#         prediction_groups = pipeline.recognize([image])
        
#         # Initialize an empty string to collect texts
#         text1 = ""
#         # Initialize an empty list to collect confidence scores
#         confidence_scores = []
        
#         for x in prediction_groups:
#             for text, box in x:
#                 text1 += " " + text
#                 # Calculate the confidence score as the mean of the character probabilities
#                 confidence_score = np.mean([character[2] for character in box])
#                 confidence_scores.append(confidence_score)
        
#         # Print the concatenated text
#         print(text1)
#         # Print the confidence scores
#         print(confidence_scores)
        
#         # Return both the concatenated text and the list of confidence scores
#         return text1, confidence_scores
#     except Exception as e:
#         return f"Error processing image: {e}"





# print(process_image("/Users/abby/Downloads/53__Baseline/written.png"))

# predicted_image_1 = prediction_groups[0]
# for text, box in predicted_image_1:
#     print(text) 

# predicted_image_2 = prediction_groups[1]
# for text, box in predicted_image_2:
#     print(text)
