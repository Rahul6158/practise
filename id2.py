import streamlit as st
import io
from PIL import Image
import PyPDF2
import docx2txt

# Create a Streamlit app
st.title("File Uploader")

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
        pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            pdf_text += page.extractText()
        st.write(pdf_text)
    elif file_extension in ["jpg", "jpeg", "png"]:
        # Display image
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)
    elif file_extension == "txt":
        # Display TXT content
        txt_text = uploaded_file.read()
        st.write(txt_text)

# Add some instructions for the user
st.write("Supported file types: DOCX, PDF, JPG/JPEG, PNG, TXT")
