import streamlit as st
import os
import base64
import docx2txt
from translate import Translator
from gtts import gTTS
import io
from docx import Document
from bs4 import BeautifulSoup
from PIL import Image
import PyPDF2
import pytesseract
import easyocr
from PIL import Image
from langdetect import detect  # Add this import for language detection

# ... (Rest of the code remains the same)

# Function to detect the language of the input text
def detect_language(text):
    try:
        return detect(text)
    except Exception as e:
        st.warning(f"Language detection error: {str(e)}")
        return "en"  # Default to English if language detection fails

# Main Streamlit app
def main():
    st.image("jangirii.png", width=50)
    st.title("Text Translation and Conversion to Speech (Multilingual Support)")

    # Add a file uploader for DOCX, PDF, images
    uploaded_file = st.file_uploader("Upload a file", type=["docx", "pdf", "jpg", "jpeg", "png", "txt"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()

        # Initialize text as None
        text = None

        if file_extension == "docx":
            # Display DOCX content
            text = process_docx_text_without_lists(uploaded_file)
        elif file_extension == "pdf":
            # Display PDF content
            pdf_text = process_pdf_text_without_lists(uploaded_file)
            text = pdf_text
        elif file_extension in ["jpg", "jpeg", "png"]:
            # Display image
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Image", use_column_width=True)

            # Extract text from the image using custom function
            image_bytes = uploaded_file.read()  # Read the image as bytes
            extracted_text = extract_text_from_image(image_bytes)
            st.write("Text extracted from the image:")
            st.write(extracted_text)
        elif file_extension == "txt":
            # Display TXT content
            txt_text = uploaded_file.read()
            text = txt_text

        if text is not None:
            st.subheader("Text Extracted from Uploaded File:")
            st.write(text)

            # Detect the source language of the input text
            source_language = detect_language(text)

            st.subheader(f"Source Language Detected: {language_mapping.get(source_language, 'Unknown')}")

            st.subheader('Select Target Language for Translation:')
            target_language = st.selectbox("Select target language:", list(language_mapping.values()))

            # Check if text is not empty or None before attempting translation
            if text and len(text.strip()) > 0:
                # Translate the extracted text
                try:
                    translated_text = translate_text(text, source_language, target_language)
                except Exception as e:
                    st.error(f"Translation error: {str(e)}")
                    translated_text = None
            else:
                st.warning("Input text is empty. Please check your document.")
                translated_text = None

            # Display translated text
            if translated_text:
                st.subheader(f"Translated text ({target_language}):")
                st.write(translated_text)
            else:
                st.warning("Translation result is empty. Please check your input text.")

            # Convert the translated text to speech
            if st.button("Convert to Speech and Get Translated Document"):
                output_file = "translated_speech.mp3"
                convert_text_to_speech(translated_text, output_file, language=target_language)

                # Play the generated speech
                audio_file = open(output_file, 'rb')
                st.audio(audio_file.read(), format='audio/mp3')

                # Provide a download link for the MP3 file
                st.markdown(get_binary_file_downloader_html("Download Audio File", output_file, 'audio/mp3'), unsafe_allow_html=True)

                # Convert the translated text to a Word document
                word_output_file = "translated_text.docx"
                convert_text_to_word_doc(translated_text, word_output_file)
                # Provide a download link for the Word document
                st.markdown(get_binary_file_downloader_html("Download Word Document", word_output_file, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
