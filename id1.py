import streamlit as st
import os
import base64
from googletrans import Translator
from gtts import gTTS
import io
from docx import Document
from bs4 import BeautifulSoup

# Function to extract text from a DOCX file
def process_docx_text(docx_file, skip_lists=True):
    # Extract text from the DOCX file
    if skip_lists:
        # Use custom function to remove lists
        text = process_docx_text_without_lists(docx_file)
    else:
        text = docx2txt.process(docx_file)
    return text

# Custom function to remove lists from DOCX text
def process_docx_text_without_lists(docx_file):
    doc = Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        if not paragraph.style.name.startswith('•'):
            text += paragraph.text + '\n'
    return text

# Function to translate text without using API (local translation)
def translate_text(text, target_language):
    try:
        translator = Translator(to_lang=target_language)
        translated_text = translator.translate(text)
        return translated_text

    except Exception as e:
        # Extract unexpected keyword arguments
        unexpected_kwargs = {}
        if hasattr(e, 'args') and e.args:
            for arg in e.args:
                if isinstance(arg, dict):
                    unexpected_kwargs.update(arg)
        
        # Display the error message with unexpected keyword arguments
        error_message = str(e)
        if unexpected_kwargs:
            error_message += f"\nUnexpected keyword arguments: {unexpected_kwargs}"
        
        return error_message

# Function to convert text to speech and save as an MP3 file
def convert_text_to_speech(text, output_file, language='en'):
    if text:
        tts = gTTS(text=text, lang=language)
        tts.save(output_file)

# Function to generate a download link for a file
def get_binary_file_downloader_html(link_text, file_path, file_format):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    b64_file = base64.b64encode(file_data).decode()
    download_link = f'<a href="data:{file_format};base64,{b64_file}" download="{os.path.basename(file_path)}">{link_text}</a>'
    return download_link

# Function to convert translated text to a Word document
def convert_text_to_word_doc(text, output_file):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_file)

# Function to convert Word document to HTML
def convert_word_doc_to_html(docx_file):
    txt = docx2txt.process(docx_file)
    soup = BeautifulSoup(txt, 'html.parser')
    return soup.prettify()

language_mapping = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    # Add more language codes and names here
}

# Main Streamlit app
def main():
    st.image("jangirii.png", width=50)
    st.title("Text Translation and Conversion to Speech (English - other languages)")

    # Add a file uploader for DOCX files
    uploaded_docx = st.file_uploader("Upload a DOCX file", type=["docx"])

    if uploaded_docx is not None:
        # Read the uploaded DOCX file and process its text content
        docx_text = process_docx_text(uploaded_docx)

        # Display the extracted text
        st.subheader("Text Extracted from Uploaded DOCX:")
        st.write(docx_text)

        target_language = st.selectbox("Select target language:", list(language_mapping.values()))

        # Check if the target language is in the mapping
        target_language_code = [code for code, lang in language_mapping.items() if lang == target_language][0]

        # Translate the extracted text using the local translation function
        try:
            translated_text = translate_text(docx_text, target_language_code)
        except Exception as e:
            st.error(f"Translation error: {str(e)}")
            translated_text = None

        # Display translated text
        if translated_text:
            st.subheader(f"Translated text ({target_language}):")
            st.write(translated_text)
        else:
            st.warning("Translation result is empty. Please check your input text.")

        # Convert the translated text to speech
        if st.button("Convert to Speech"):
            output_file = "translated_speech.mp3"
            convert_text_to_speech(translated_text, output_file, language=target_language_code)

            # Play the generated speech
            audio_file = open(output_file, 'rb')
            st.audio(audio_file.read(), format='audio/mp3')

            # Play the generated speech (platform-dependent)
            if os.name == 'posix':  # For Unix/Linux
                os.system(f"xdg-open {output_file}")
            elif os.name == 'nt':  # For Windows
                os.system(f"start {output_file}")
            else:
                st.warning("Unsupported operating system")

            # Provide a download link for the MP3 file
            st.markdown(get_binary_file_downloader_html("Download Audio File", output_file, 'audio/mp3'), unsafe_allow_html=True)

            # Convert the translated text to a Word document
            word_output_file = "translated_text.docx"
            convert_text_to_word_doc(translated_text, word_output_file)
            # Provide a download link for the Word document
            st.markdown(get_binary_file_downloader_html("Download Word Document", word_output_file, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
