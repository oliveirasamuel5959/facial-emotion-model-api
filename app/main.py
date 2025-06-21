import streamlit as st
from PIL import Image

st.title('Facial Emotion Recognition')

st.text('emotion detection using deep learning')

user_input = st.text_input('Enter a custom messagem:', 'Hello, Streamlit')

st.write('Customized Message:', user_input)

uploaded_image = st.file_uploader("Choose an image file", type="jpg")

if uploaded_image:
    image = Image.open(uploaded_image)
    image.save("./images/output_image.jpg")
    st.image("./images/output_image.jpg")