import streamlit as st
import whisper

st.title("Audio to Text Converter")

audio_file=st.file_uploader("upload audio file")

if audio_file is not None:
    model=whisper.load_model("base")
    st.write("file uploaded")
    with open("audio_temp.wav","wb") as f:
        f.write(audio_file.getbuffer())
    st.audio(audio_file)
    with st.spinner("Converting to Text"):
        result=model.transcribe("audio_temp.wav")
    st.write(result["language"])
    st.write(result["text"])
