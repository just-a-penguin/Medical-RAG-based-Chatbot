import os
import math
import imgaug
import numpy as np
import matplotlib.pyplot as plt
import sklearn.model_selection
import tensorflow as tf
import keras_ocr
import pytesseract
from PIL import Image

# Set up the initial settings and disable eager execution
tf.compat.v1.disable_eager_execution()
tf.compat.v1.experimental.output_all_intermediates(True)

# Get dataset
dataset = keras_ocr.datasets.get_icdar_2013_detector_dataset(
    cache_dir='.',
    skip_illegible=False
)

# Split dataset
train, validation = sklearn.model_selection.train_test_split(
    dataset, train_size=0.8, random_state=42
)

# Set up augmenter
augmenter = imgaug.augmenters.Sequential([
    imgaug.augmenters.Affine(scale=(1.0, 1.2), rotate=(-5, 5)),
    imgaug.augmenters.GaussianBlur(sigma=(0, 0.5)),
    imgaug.augmenters.Multiply((0.8, 1.2), per_channel=0.2)
])

# Image generator setup
generator_kwargs = {'width': 640, 'height': 640}
training_image_generator = keras_ocr.datasets.get_detector_image_generator(
    labels=train,
    augmenter=augmenter,
    **generator_kwargs
)
validation_image_generator = keras_ocr.datasets.get_detector_image_generator(
    labels=validation,
    **generator_kwargs
)

# Load model and setup training
detector = keras_ocr.detection.Detector()
batch_size = 1
training_generator, validation_generator = [
    detector.get_batch_generator(image_generator=image_generator, batch_size=batch_size)
    for image_generator in [training_image_generator, validation_image_generator]
]

detector.model.fit_generator(
    generator=training_generator,
    steps_per_epoch=math.ceil(len(train) / batch_size),
    epochs=2,
    workers=0,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(restore_best_weights=True, patience=5),
        tf.keras.callbacks.CSVLogger(os.path.join('.', 'detector_icdar2013.csv')),
        tf.keras.callbacks.ModelCheckpoint(filepath=os.path.join('.', 'detector_icdar2013.h5'))
    ],
    validation_data=validation_generator,
    validation_steps=math.ceil(len(validation) / batch_size)
)

detector.model.load_weights(os.path.join('.', 'detector_icdar2013.h5'))
detector.model.save('detector_icdar2013_trained.h5')


def process_image(filename):
    print(f"Processing image: {filename}")
    try:
        image = keras_ocr.tools.read(filename)
        # Use the trained detector to find text areas
        boxes = detector.detect(images=[image])[0]
        # Recognize text using keras-ocr
        prediction_groups = [detector.recognize(images=[image], detection_result=[boxes])]
        text1 = " ".join([text for text, box in prediction_groups[0]])

        with Image.open(filename) as img:
            width, height = img.size
            text2 = pytesseract.image_to_string(img)

        text_list_1 = text1.split()
        text_list_2 = text2.split()

        word_match = sum(1 for i in range(min(len(text_list_1), len(text_list_2)))
                         if text_list_1[i].lower() == text_list_2[i].lower())

        confid = 0.3 * ((word_match / max(len(text_list_1), len(text_list_2))) * 100)
        confid += 70
        confid = int(confid)

        return text1 + " \n " + " ||  CONFIDENCE SCORE: #" + str(confid)

    except Exception as e:
        return f"Error processing image: {e}"

# Example usage
filename = '/Users/abby/Downloads/53__Baseline/written.png'
result = process_image(filename)
print(result)
