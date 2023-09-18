import streamlit as st
import io
from PIL import Image
import pytesseract
import PyPDF2
import docx2txt
from translate import Translator

# Language mapping
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

# Custom function to process DOCX text without lists
def process_docx_text_without_lists(docx_file):
    text = docx2txt.process(docx_file)
    
    # Remove list items
    text = '\n'.join([line for line in text.split('\n') if not line.startswith(('- ', '• ', 'o '))])
    
    return text

# Custom function to process PDF text without lists
def process_pdf_text_without_lists(pdf_file):
    pdf_text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()
    
    # Remove list items
    pdf_text = '\n'.join([line for line in pdf_text.split('\n') if not line.startswith(('- ', '• ', 'o '))])
    
    return pdf_text

# Custom function to extract text from an image
def extract_text_from_image(img):
    text = pytesseract.image_to_string(img)
    return text

# Create a Streamlit app
st.title("File Uploader with OCR and Translation")

# Create an uploader widget
uploaded_file = st.file_uploader("Upload a file", type=["docx", "pdf", "jpg", "jpeg", "png", "txt"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == "docx":
        # Display DOCX content
        docx_text = process_docx_text_without_lists(uploaded_file)
        st.write(docx_text)
    elif file_extension == "pdf":
        # Display PDF content
        pdf_text = process_pdf_text_without_lists(uploaded_file)
        st.write(pdf_text)
    elif file_extension in ["jpg", "jpeg", "png"]:
        # Display image
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        
        # Extract text from the image using custom function
        text = extract_text_from_image(img)
        st.write("Text extracted from the image:")
        st.write(text)
    elif file_extension == "txt":
        # Display TXT content
        txt_text = uploaded_file.read()
        st.write(txt_text)

    # Language translation
    translation_language = st.selectbox("Select a language for translation:", options=list(language_mapping.values()))
    target_language = [key for key, value in language_mapping.items() if value == translation_language][0]
    
    if st.button("Translate"):
        # Split the text into sentences and translate each sentence
        sentences = text.split('.')
        translated_sentences = []

        for sentence in sentences:
            translator = Translator(to_lang=target_language)
            translated_sentence = translator.translate(sentence)
            translated_sentences.append(translated_sentence)

        translated_text = '. '.join(translated_sentences)
        st.write(f"Translated text to {translation_language}:")
        st.write(translated_text)

# Add some instructions for the user
st.write("Supported file types: DOCX, PDF, JPG/JPEG, PNG, TXT")
