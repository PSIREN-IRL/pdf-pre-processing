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
processed_output_directory = "./processed_images" # Output for processed images
os.makedirs(output_directory, exist_ok=True)
os.makedirs(processed_output_directory, exist_ok=True) # Create processed output directory

# Convert PDF pages to images
def pdf_to_images(pdf_path, output_dir, dpi=400):
    try:
        pages = convert_from_path(pdf_path, dpi=dpi)
        for i, page in enumerate(pages):
            image_name = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{i+1}.png"
            image_path = os.path.join(output_dir, image_name)
            page.save(image_path, "PNG")
            print(f"Saved: {image_path}")
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        import traceback
        traceback.print_exc()

# Pre-process image for OCR
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None: # Check if image loading failed
        print(f"Error: Could not load image at {image_path}")
        return None  # Return None to indicate failure

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- Re-implement Dilation and Erosion ---
    # Define kernel size for dilation and erosion.
    # Experiment with (2, 2), (3, 3), or even try (1, 1) to disable (almost no effect)
    kernel_size = (3, 3)
    kernel = np.ones(kernel_size, np.uint8)

    # --- Option 1: Dilation followed by Erosion (Opening operation for noise removal and smoothing) ---
    # iterations_dilate = 1  # Start with 1 iteration for dilation, experiment with 0, 2, etc.
    # iterations_erode = 1   # Start with 1 iteration for erosion, experiment with 0, 2, etc.

    # dilated_img = cv2.dilate(gray_img, kernel, iterations=iterations_dilate)
    # eroded_img = cv2.erode(dilated_img, kernel, iterations=iterations_erode)
    # img = eroded_img # Use the eroded image for further processing


    # --- Option 2: Just Dilation (for thickening faint text) ---
    iterations_dilate = 2  # Start with 1 iteration for dilation, experiment with 0, 2, etc.
    iterations_erode = 0   # No erosion in this option

    dilated_img = cv2.dilate(gray_img, kernel, iterations=iterations_dilate)
    img = dilated_img # Use the dilated image for further processing


    # --- Option 3: No Dilation/Erosion (Baseline - use if D/E is not helpful) ---
    # img = gray_img # Use grayscale image directly - comment out Dilation/Erosion sections above
    # pass # Use 'pass' to skip dilation and erosion


    # Apply Gaussian blur (after dilation and erosion, or directly on grayscale if D/E is skipped)
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
        print(f"Processing PDF: {pdf_path}")
        pdf_to_images(pdf_path, output_directory)

print("\nPDF to Image conversion complete. Starting image pre-processing...\n")

# --- Modified section: Process all images in output_directory ---
for filename in os.listdir(output_directory):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"): # Process JPG, JPEG, PNG images (adjust if needed)
        image_path = os.path.join(output_directory, filename)
        print(f"Processing image: {image_path}")
        processed_img = preprocess_image(image_path)
        if processed_img is not None: # Only save if processing was successful
            processed_image_name = f"processed_{filename}" # Create a new filename for processed image
            processed_image_path = os.path.join(processed_output_directory, processed_image_name)
            save_image(processed_img, processed_image_path)
        else:
            print(f"Skipping saving processed image for {image_path} due to processing error.")

print("\nImage pre-processing complete. Processed images saved in:", processed_output_directory)
