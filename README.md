# PDF Pre-Processing Before OCR with OpenCV

This project demonstrates how to convert PDF files into images and preprocess them using OpenCV to optimize for Optical Character Recognition (OCR). The preprocessing steps include grayscale conversion, noise removal, Gaussian blurring, and binarization to improve OCR accuracy.

---

## **Features**
- **Convert PDFs to Images:** Uses `pdf2image` to extract PDF pages as JPEG images.
- **Grayscale Conversion:** Simplifies the image for further processing.
- **Noise Removal:** Applies dilation and erosion to clean up the image.
- **Gaussian Blur:** Reduces noise by smoothing the edges.
- **Binarization:** Converts the image to black-and-white for OCR using Otsu's threshold.

---

## **Directory Structure**
```
project/
├── pdfs/            # Place your PDF files here
├── images/          # Extracted images will be saved here
├── pre_processing.py  # Main Python script
└── README.md        # This README file
```

---

## **Dependencies**
Make sure you have the following libraries installed:

### **OS Packages**
```bash
sudo apt-get update && sudo apt-get install -y poppler-utils tesseract-ocr
```

### **Python Packages**
```bash
pip install opencv-python pdf2image pillow pytesseract
```

---

## **How to Use**
1. **Clone this repository**:
   ```bash
   git clone <your-repo-url>
   cd project
   ```

2. **Place your PDFs** in the `pdfs/` directory.

3. **Run the script**:
   ```bash
   python pre_processing.py
   ```

4. **Check the `images/` directory** for the extracted and processed images.

---

## **Pre-Processing Techniques Used**
- **Grayscale Conversion:** Reduces the image to a single color channel for easy processing.
- **Dilation & Erosion:** Cleans up noise and connects broken parts of objects.
- **Gaussian Blur:** Smooths out small variations in the image.
- **Binarization:** Converts the image to black-and-white for better OCR performance.

---

## **Example Output**
After running the script, you should see the processed images saved in the `images/` directory.

---

## **References**
- [Getting Started with Tesseract](https://towardsdatascience.com/getting-started-with-tesseract-part-i-2a6a6b1cf75e)

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for more details.