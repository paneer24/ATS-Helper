import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai

def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if input_text != "":
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(image)
    return response.text

def main():
    st.set_page_config(page_title="Gemini Image Demo")

    google_api_key = None
    if 'google_api_key' in st.session_state:
        google_api_key = st.session_state['google_api_key']

    with st.expander("Settings", expanded=True):
        if not google_api_key:
            google_api_key = st.text_input("Generative API Key", key="google_api_key", type="password")
            st.markdown("[Get a Generative AI API key](https://makersuite.google.com/app/apikey)")
            st.markdown("[View the source code]()")

        if not google_api_key:
            st.info("Please add your Generative AI API key to continue.")
            st.stop()
        else:
            genai.configure(api_key=google_api_key)
            st.session_state['google_api_key'] = google_api_key

    if google_api_key:
        st.title("💬 Chatbot with image input")
        st.caption("🚀 A Streamlit chatbot powered by Google Generative LLM")

        st.header("Chat with Image input and optional prompt")

        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        uploaded_files = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        
        images = []
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image.", use_column_width=True)
                images.append(image)  # Save each image in the list

        submit = st.button("Tell me about the image")

        if submit:
            if not uploaded_files:
                st.info("Please upload an image to continue.")
                st.stop()

            genai.configure(api_key=google_api_key)
            response = get_gemini_response("", images[0])  # Process only the first image for now
            st.subheader("The Response is")
            st.write(response)
            st.session_state['chat_history'].append(("Bot", response))

        if prompt := st.chat_input():
            if not uploaded_files:
                st.info("Please upload an image to continue.")
                st.stop()

            response = get_gemini_response(prompt, images[0])
            st.session_state['chat_history'].append(("You", prompt))
            st.subheader("The Response is")
            st.write(response)
            st.session_state['chat_history'].append(("Bot", response))

        with st.sidebar:
            with st.expander("History", expanded=False):
                if st.session_state['chat_history']:
                    "The Chat History is:"
                    for role, text in st.session_state['chat_history']:
                        st.write(f"{role}: {text}")

if __name__ == "__main__":
    main()
