# PDF Pre-Processing before OCR with OpenCV

# Install required libraries
#!apt-get update && apt-get install -y poppler-utils tesseract-ocr
#!pip install opencv-python pdf2image pillow pytesseract

# Import necessary modules
import os
import cv2
import numpy as np
from pdf2image import convert_from_path

# Setup input/output directories (adjust these paths as needed)
pdf_directory = "./pdfs"  # Local directory with PDFs
output_directory = "./images"  # Output directory for images
os.makedirs(output_directory, exist_ok=True)

# Convert PDF pages to images
def pdf_to_images(pdf_path, output_dir, dpi=300):
    try:
        pages = convert_from_path(pdf_path, dpi=dpi)
        for i, page in enumerate(pages):
            image_name = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{i+1}.jpg"
            image_path = os.path.join(output_dir, image_name)
            page.save(image_path, "JPEG")
            print(f"Saved: {image_path}")
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

# Pre-process image for OCR
def preprocess_image(image_path):
    img = cv2.imread(image_path)

    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Apply Gaussian blur
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Apply binarization (Otsu's threshold)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return img

# Save processed image
def save_image(img, output_path):
    cv2.imwrite(output_path, img)
    print(f"Image saved to: {output_path}")

# Process PDFs
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, filename)
        print(f"Processing: {pdf_path}")
        pdf_to_images(pdf_path, output_directory)

# Pre-process and save the first page image (for demonstration)
sample_image = os.path.join(output_directory, "sample_page_1.jpg")  # Adjust filename as needed
processed_img = preprocess_image(sample_image)
save_image(processed_img, "./processed_image.jpg")
