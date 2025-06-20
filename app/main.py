import streamlit as st

st.title('My first Streamlit App')

st.text('Welcome to my Streamlit app')

user_input = st.text_input('Enter a custom messagem:', 'Hello, Streamlit')

st.write('Customized Message:', user_input)