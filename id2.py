import streamlit as st
import io
from PIL import Image
import pytesseract
import PyPDF2
import docx2txt

# Language mapping dictionary
language_mapping = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    # Add more languages as needed
}

# Function to display language options and translate text
def translate_text(text, target_language):
    if target_language not in language_mapping:
        st.warning("Invalid target language selected.")
        return

    st.write(f"Original Text ({language_mapping['en']}):")
    st.write(text)

    st.write(f"Translated Text ({language_mapping[target_language]}):")
    st.write("Translation not supported in this demo.")  # You can add your translation logic here

# Create a Streamlit app
st.title("File Uploader with OCR and Translation")

# Create an uploader widget
uploaded_file = st.file_uploader("Upload a file", type=["docx", "pdf", "jpg", "jpeg", "png", "txt"])

# Language selection widget
target_language = st.selectbox("Select Target Language", list(language_mapping.values()))

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == "docx":
        # Display DOCX content
        docx_text = docx2txt.process(uploaded_file)
        translate_text(docx_text, target_language)
    elif file_extension == "pdf":
        # Display PDF content
        pdf_text = ""
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
        translate_text(pdf_text, target_language)
    elif file_extension in ["jpg", "jpeg", "png"]:
        # Display image
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Extract text from the image using pytesseract's built-in OCR
        text = pytesseract.image_to_string(img)
        translate_text(text, target_language)
    elif file_extension == "txt":
        # Display TXT content
        txt_text = uploaded_file.read()
        translate_text(txt_text, target_language)

# Add some instructions for the user
st.write("Supported file types: DOCX, PDF, JPG/JPEG, PNG, TXT")
