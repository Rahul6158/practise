import streamlit as st
import assemblyai as aai

# Set your AssemblyAI API key
aai.settings.api_key = "d325d0881c4049839b0da5cb5905e6fe"

# Create a transcriber object
transcriber = aai.Transcriber()

# Define a function to handle the streaming transcription
def handle_transcription(transcript_chunk):
    st.write(transcript_chunk.text)

# Streamlit App
def main():
    st.title("Audio Transcription App")
    
    # Upload an audio file
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    if audio_file is not None:
        st.audio(audio_file, format='audio/mp3', start_time=0)
        st.write("Transcription:")

        # Start transcription
        transcriber.stream(audio_file, callback=handle_transcription)

if __name__ == "__main__":
    main()
