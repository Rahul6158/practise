import streamlit as st
import speech_recognition as sr
import io

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

    uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format='audio/wav')

        if st.button("Convert to Text"):
            audio_data = io.BytesIO(audio_bytes)
            text = convert_audio_to_text(audio_data)
            st.write("Transcribed Text:")
            st.write(text)

if __name__ == "__main__":
    main()
