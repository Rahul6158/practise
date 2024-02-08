import streamlit as st
import speech_recognition as sr
import io
import soundfile as sf
import tempfile
import os

def convert_audio_to_text(audio_data):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_data) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error occurred: {e}"

def main():
    st.title("Audio to Text Converter")

    uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "ogg", "flac"])

    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format='audio/wav')

        if st.button("Convert to Text"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                tmp_audio.write(audio_bytes)
                text = convert_audio_to_text(tmp_audio.name)
                st.write("Transcribed Text:")
                st.write(text)
                
            os.unlink(tmp_audio.name)

if __name__ == "__main__":
    main()
