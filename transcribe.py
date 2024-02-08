import streamlit as st
import speech_recognition as sr
import io
import tempfile
import os

def convert_audio_to_text(audio_data):
    recognizer = sr.Recognizer()

    with io.BytesIO(audio_data) as source:
        audio_data = recognizer.record(sr.AudioData(source.read(), sample_rate=44100, sample_width=2))

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
            text = convert_audio_to_text(audio_bytes)
            st.write("Transcribed Text:")
            st.write(text)

if __name__ == "__main__":
    main()
