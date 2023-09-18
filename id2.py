import streamlit as st
from gtts import gTTS
import tempfile
import os
import base64
import fitz  # PyMuPDF for PDF extraction
import pytesseract  # For OCR text extraction from images
from googletrans import Translator  # For translation
from docx import Document  # For DOCX processing

# Language code mapping with full language names
language_mapping = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "hi": "Hindi",
    "ja": "Japanese",
    "ko": "Korean",
    "zh-cn": "Simplified Chinese",
    "ru": "Russian",
    "ar": "Arabic",
    "th": "Thai",
    "tr": "Turkish",
    "pl": "Polish",
    "cs": "Czech",
    "sv": "Swedish",
    "da": "Danish",
    "fi": "Finnish",
    "el": "Greek",
    "hu": "Hungarian",
    "uk": "Ukrainian",
    "no": "Norwegian",
    "id": "Indonesian",
    "vi": "Vietnamese",
    "ro": "Romanian",
    "bn": "Bengali",
    "fa": "Persian",
    "iw": "Hebrew",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "hr": "Croatian",
    "sr": "Serbian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "et": "Estonian",
    "is": "Icelandic",
    "ga": "Irish",
    "sq": "Albanian",
    "mk": "Macedonian",
    "hy": "Armenian",
    "ka": "Georgian",
    "mt": "Maltese",
    "mr": "Marathi",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu",
    "ne": "Nepali",
    "si": "Sinhala",
    "km": "Khmer",
    "lo": "Lao",
    "my": "Burmese",
    "jw": "Javanese",
    "mn": "Mongolian",
    "zu": "Zulu",
    "xh": "Xhosa"
}

# Function to convert text to speech and save as an MP3 file
def convert_text_to_speech(text, output_file, language='en', slow=False):
    tts = gTTS(text=text, lang=language, slow=slow)
    tts.save(output_file)

# Function to count words in input text
def count_words_in_text(text):
    words = text.split()
    return len(words)

# Function to extract text from a PDF file
# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_pdf):
    pdf_data = uploaded_pdf.read()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf_file:
        temp_pdf_file.write(pdf_data)
        temp_pdf_path = temp_pdf_file.name
    
    doc = fitz.open(temp_pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    
    # Remove the temporary PDF file
    os.remove(temp_pdf_path)
    
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Function to extract text from an image using OCR
def extract_text_from_image(image_file):
    text = pytesseract.image_to_string(image_file)
    return text

# Function to translate text
def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

# Function to generate a download link for a file
def get_binary_file_downloader_html(link_text, file_path, file_format):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    b64_file = base64.b64encode(file_data).decode()
    download_link = f'<a href="data:{file_format};base64,{b64_file}" download="{os.path.basename(file_path)}">{link_text}</a>'
    return download_link

# Define the Streamlit app
def main():
    st.image("jangirii.png", width=100)
    st.subheader("Pray, Trust and Wait")
    st.title("Text to Voice Converter")

    # Get user input
    text = st.text_input("Enter text to convert:")
    word_count = count_words_in_text(text)
    st.write(f"Number of words in the input text: {word_count}")

    # Language selection options with full names
    language_options = [f"{full_name} ({code})" for code, full_name in language_mapping.items()]
    language = st.selectbox("Select Language", language_options)

    uploaded_file = st.file_uploader("Upload File (PDF, DOCX, or Image)", type=["pdf", "docx", "jpg", "jpeg", "png"])

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            # Handle PDF file
            file_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Handle DOCX file
            file_text = extract_text_from_docx(uploaded_file)
        elif uploaded_file.type in ["image/jpeg", "image/jpg", "image/png"]:
            # Handle image file
            file_text = extract_text_from_image(uploaded_file)
        else:
            st.write("Unsupported file type. Please upload a PDF, DOCX, or image file.")
            return

        st.write("File Content:")
        st.write(file_text)

        # Translate file content
        translated_file_text = translate_text(file_text)
        st.write("Translated File Content:")
        st.write(translated_file_text)

# Run the Streamlit app
if __name__ == "__main__":
    main()
