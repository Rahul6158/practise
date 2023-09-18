import streamlit as st
from gtts import gTTS
import tempfile
import os
import base64
import fitz  # PyMuPDF for PDF extraction
import pytesseract  # For OCR text extraction from images
from googletrans import Translator  # For translation
from docx import Document  # For DOCX processing
from PIL import Image
import io

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
def convert_text_to_speech(text, output_file, language='en'):
    if text:
        tts = gTTS(text=text, lang=language)
        tts.save(output_file)

# Function to count words in input text
def count_words_in_text(text):
    words = text.split()
    return len(words)

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

# Function to extract text from an image using OCR
def extract_text_from_image(uploaded_image):
    image_data = uploaded_image.read()
    img = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(img)
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Function to translate text
def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

# Function to generate a download link for a file
def get_binary_file_downloader_html(link_text, file_content, file_format, language_code):
    translated_filename = f"translated.{file_format}"
    
    if file_format == "pdf":
        # Create a temporary PDF file for download
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf_file:
            temp_pdf_file.write(file_content.encode())
            translated_filename = temp_pdf_file.name
    elif file_format == "docx":
        # Create a temporary DOCX file for download
        doc = Document()
        doc.add_paragraph(file_content)
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_docx_file:
            doc.save(temp_docx_file)
            translated_filename = temp_docx_file.name
    elif file_format in ["jpg", "jpeg", "png"]:
        # For images, create a text file with the translated text
        translated_filename = f"translated.{file_format}.txt"
        with open(translated_filename, "w", encoding="utf-8") as txt_file:
            txt_file.write(file_content)
    
    with open(translated_filename, 'rb') as f:
        file_data = f.read()
    b64_file = base64.b64encode(file_data).decode()
    download_link = f'<a href="data:{file_format};base64,{b64_file}" download="{translated_filename}">{link_text}</a>'
    return download_link

# Function to convert translated text to speech and save as an MP3 file
def convert_translated_text_to_speech(text, output_file, language='en'):
    if text:
        tts = gTTS(text=text, lang=language)
        tts.save(output_file)

# Define the Streamlit app
def main():
    st.image("jangirii.png", width=100)
    st.subheader("Pray, Trust and Wait")
    st.title("Text to Voice Converter")

    # Step 0: Input Text and Language Selection
    input_text = st.text_input("Enter text to convert:")
    input_language = st.selectbox("Select Language for Input Text", list(language_mapping.values()))

    uploaded_file = st.file_uploader("Step 1: Upload File (PDF, DOCX, or Image)", type=["pdf", "docx", "jpg", "jpeg", "png"])

        if uploaded_file:
            st.subheader("Extracted Text and Language Selection")
            
            # Determine the file format
            if uploaded_file.type == "application/pdf":
                file_format = "pdf"
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                file_format = "docx"
            elif uploaded_file.type in ["image/jpeg", "image/jpg", "image/png"]:
                file_format = uploaded_file.type.split("/")[-1]
            else:
                st.write("Unsupported file type. Please upload a PDF, DOCX, or image file.")
                return

            # Extract text from the uploaded file
            if file_format == "pdf":
                file_text = extract_text_from_pdf(uploaded_file)
            elif file_format == "docx":
                file_text = extract_text_from_docx(uploaded_file)
            elif file_format in ["jpg", "jpeg", "png"]:
                file_text = extract_text_from_image(uploaded_file)
            
            st.write("Extracted File Content:")
            st.write(file_text)

            # Step 3: Translation and Text-to-Speech Conversion
            selected_language = st.selectbox("Select Language for Translation and Text-to-Speech", list(language_mapping.values()))
            
            if st.button("Step 4: Get Translated Audio and Document"):
                st.subheader("Step 4: Translated Text and Audio")
                st.write("Translating...")
                
                # Translate the input text and the extracted file content
                input_text_translated = translate_text(input_text, target_language=input_language)
                file_text_translated = translate_text(file_text, target_language=selected_language)
                
                st.write(f"Translated Input Text ({input_language} to {selected_language}):")
                st.write(input_text_translated)
                
                st.write(f"Translated File Content ({input_language} to {selected_language}):")
                st.write(file_text_translated)
                
                # Step 5: Play and Download Translated Audio
                st.subheader("Step 5: Translated Audio and Document Download")
                
                # Convert translated text to speech
                input_text_audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                file_text_audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                
                convert_translated_text_to_speech(input_text_translated, input_text_audio_file.name, language=selected_language)
                convert_translated_text_to_speech(file_text_translated, file_text_audio_file.name, language=selected_language)
                
                # Play the translated audio
                st.audio(input_text_audio_file.name, format='audio/mp3', label=f"Translated Input Text ({input_language} to {selected_language})")
                st.audio(file_text_audio_file.name, format='audio/mp3', label=f"Translated File Content ({input_language} to {selected_language})")
                
                # Provide download buttons for the translated content in the uploaded source file format
                st.markdown(get_binary_file_downloader_html(f'Download Translated Text ({selected_language})', file_text_translated, file_format, selected_language), unsafe_allow_html=True)
                st.markdown(get_binary_file_downloader_html(f'Download Translated Audio ({selected_language})', file_text_audio_file.read(), "mp3", selected_language), unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()
