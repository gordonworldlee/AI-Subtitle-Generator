import streamlit as st
import os
from app import extract_audio, format, transcribe, generate_subs, embed_subs

st.set_page_config(page_title='Video Upload')
st.title(':blue[AI] Video Subtitle Generator')
video = st.file_uploader(label = "Upload video:")

check = True

if video and check:
    st.write("Filename: ", video.name)
    with open(video.name, 'wb') as f:
        f.write(video.getbuffer())
    pre, ext = os.path.splitext(video.name)
    os.rename(video.name, pre + 'tough')
    pre = pre + 'tough'
    st.success("File Saved")
    audio = extract_audio(pre)
    language, segments = transcribe(audio, "small")
    subs_file = generate_subs(pre, language, segments)
    name = embed_subs(pre, subs_file, language)

    os.remove(pre)
    os.remove(audio)
    os.remove(subs_file)

    with open(name, 'rb') as file:
        btn = st.download_button(label='Download Video', data=file, file_name="outputvid.mp4", mime='video/mp4')
        check = False
    os.remove(name)

