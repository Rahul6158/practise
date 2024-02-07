import requests
import streamlit as st

# Function to transcribe audio using AssemblyAI API
def transcribe_audio(audio_file):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    headers = {
        "authorization": "d325d0881c4049839b0da5cb5905e6fe",
        "content-type": "application/json"
    }
    
    # Read audio file content as binary
    audio_content = audio_file.read()

    response = requests.post(endpoint, data=audio_content, headers=headers)
    if response.status_code == 201:
        transcript_id = response.json()['id']
        return get_transcription(transcript_id)
    else:
        st.error(f"Error: {response.text}")
        return None

# Function to get transcription using AssemblyAI API
def get_transcription(transcript_id):
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": "YOUR_API_KEY"
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()['text']
    else:
        st.error(f"Error: {response.text}")
        return None

# Streamlit App
def main():
    st.title("Audio Transcription App")
    
    # Upload an audio file
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    if audio_file is not None:
        st.audio(audio_file, format='audio/mp3', start_time=0)
        st.write("Transcription:")

        # Start transcription
        with st.spinner("Transcribing..."):
            transcript = transcribe_audio(audio_file)

        if transcript is not None:
            st.write(transcript)

if __name__ == "__main__":
    main()
