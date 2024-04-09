from PIL import Image
import pytesseract

def process_image(filename):
    try:
        with Image.open(filename) as img:
            width, height = img.size
            # text = pytesseract.image_to_string(img)
            return f"The image width is {width} pixels, height is {height} pixels, and the extracted text is:\n"
    except Exception as e:
        return f"Error processing image: {e}"
