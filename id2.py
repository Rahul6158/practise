import streamlit as st
import io
from PIL import Image
import pytesseract
import PyPDF2
import docx2txt

# Create a Streamlit app
st.title("File Uploader with OCR")

# Create an uploader widget
uploaded_file = st.file_uploader("Upload a file", type=["docx", "pdf", "jpg", "jpeg", "png", "txt"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == "docx":
        # Display DOCX content
        docx_text = docx2txt.process(uploaded_file)
        st.write(docx_text)
    elif file_extension == "pdf":
        # Display PDF content
        pdf_text = ""
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
        st.write(pdf_text)
    elif file_extension in ["jpg", "jpeg", "png"]:
        # Display image
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        
        # Extract text from the image using pytesseract's built-in OCR
        text = pytesseract.image_to_string(img)
        st.write("Text extracted from the image:")
        st.write(text)
    elif file_extension == "txt":
        # Display TXT content
        txt_text = uploaded_file.read()
        st.write(txt_text)

# Add some instructions for the user
st.write("Supported file types: DOCX, PDF, JPG/JPEG, PNG, TXT")
