import streamlit as st
from gtts import gTTS
import tempfile
import os
import base64

# ... (Rest of the code remains the same as in your original code)

# Define the Streamlit app
def main():
    st.image("jangirii.png", width=100)
    st.subheader("Pray, Trust and Wait")
    st.title("Text to Voice Converter")

    # Get user input
    text = st.text_input("Enter text to convert:")

    # Language selection options with full names
    language_options = [f"{full_name} ({code})" for code, full_name in language_mapping.items()]
    language = st.selectbox("Select Language", language_options)

    if st.button("Convert to Voice") and text:
        # Extract language code from the selected option
        selected_language_code = language.split(" ")[-1][1:-1]

        # Create a temporary file to store the speech as an MP3 file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_file_name = temp_file.name

            # Convert text to speech and save as an MP3 file
            convert_text_to_speech(text, temp_file_name, language=selected_language_code)

        # Send the voice note
        st.audio(temp_file_name, format='audio/mp3')

        # Provide download button for the MP3 file
        st.markdown(get_binary_file_downloader_html('download audio file', temp_file_name, 'audio/mp3'), unsafe_allow_html=True)

        # Remove the temporary file
        if temp_file_name:
            os.remove(temp_file_name)

        # Count and display the number of words in the input text
        word_count = count_words_in_text(text)
        st.write(f"Number of words in the input text: {word_count}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
