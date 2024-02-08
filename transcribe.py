import streamlit as st
import speech_recognition as sr

def convert_audio_to_text(audio_data):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(audio_data)

    with audio_file as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Error occurred: {0}".format(e)

def main():
    st.title("Audio to Text Converter")

    uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

    if uploaded_file is not None:
        audio_data = uploaded_file.read()
        st.audio(audio_data, format='audio/wav')

        if st.button("Convert to Text"):
            text = convert_audio_to_text(audio_data)
            st.write("Transcribed Text:")
            st.write(text)

if __name__ == "__main__":
    main()
