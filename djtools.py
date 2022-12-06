import cv2 as cv
import pytesseract
import getpass
import os

# pytesseract path
tesseract_dir = r"C:\Users\%USERNAME%\AppData\Local\Tesseract-OCR\tesseract.exe"

# Replace %USERNAME% variable with the os username.
username = getpass.getuser()
tesseract_dir = tesseract_dir.replace("%USERNAME%", username)

# Set pytesseract path
pytesseract.pytesseract.tesseract_cmd = tesseract_dir

import os

# Define the directory containing the images
img_directory = "images/"

# Get a list of filenames in the directory
filenames = os.listdir(img_directory)

# Loop through all the images and write text output to a CSV file.
for filename in filenames:
    # Get the file extension
    file_ext = os.path.splitext(filename)[1]

    # Only process files with the .PNG or .JPG extension
    if file_ext in (".PNG", ".JPG"):
        # Load the image
        img = cv.imread(os.path.join(img_directory, filename))

        # Resize image
        scale = 0.4
        new_width = int(img.shape[1] * scale)
        new_height = int(img.shape[0] * scale)
        img = cv.resize(img, (new_width, new_height))

        # Crop image in half vertically and remove additional 30% from top
        height, width = img.shape[:2]
        start_row = int(height // 1.8)
        end_row = height - int(height // 3.5)
        img = img[start_row:end_row, :]

        # Extract text from image using pytesseract
        text = pytesseract.image_to_string(img)

        # Split the string at the first double newline
        parts = text.split("\n\n")

        # Join the parts back together, leaving out the unwanted text
        text = "\n\n".join(parts[:1])

        # Remove all newlines '\n'
        text = text.replace("\n", "")

        # Create a list of unwanted characters
        characters = list("^&|<>()")

        # Loop through the list of characters and replace any occurrences in the text
        for ch in characters:
            text = text.replace(ch, "")

        # Add 'Audio' keyword to 'text
        text = text + " Audio"

        print(text)
        cv.imshow('image', img)
        cv.waitKey(0)