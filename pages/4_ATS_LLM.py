import streamlit as st
import PyPDF2 as pdf
import os
import google.generativeai as genai
from langchain.prompts import PromptTemplate

# Function to get response from Gemini AI
def get_gemini_repsonse(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to extract text from a PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analysis
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and the missing keywords with high accuracy.
resumes:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

def main():
    st.set_page_config("Smart ATS")
    google_api_key = None 
    if 'google_api_key' in st.session_state:
        google_api_key = st.session_state['google_api_key']
    with st.expander("Settings", expanded=True):
        if not google_api_key:
            "Please Update the API Key to use the app"
            google_api_key = st.text_input("Generative API Key", key="google_api_key", type="password")
            "[Get a Generative AI API key](https://makersuite.google.com/app/apikey)"
            "[View the source code]()"
            "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
            
        if not google_api_key:
            st.info("Please add your Generative AI API key to continue.")
            st.stop()
        else:
            genai.configure(api_key=google_api_key)
            st.session_state['google_api_key'] = google_api_key

    if google_api_key:
        os.environ['GOOGLE_API_KEY'] = google_api_key
        genai.configure(api_key=google_api_key)
        st.text("Improve Your Resume ATS")
        jd = st.text_area("Paste the Job Description")
        uploaded_files = st.file_uploader("Upload Your Resumes", type="pdf", help="Upload one or more PDFs", accept_multiple_files=True)

        submit = st.button("Submit")

        if submit:
            if uploaded_files is not None:
                all_texts = []
                for uploaded_file in uploaded_files:
                    text = input_pdf_text(uploaded_file)
                    all_texts.append(text)
                
                combined_text = " ".join(all_texts)
                
                # Format the prompt with the combined text and job description
                prompt = input_prompt.format(text=combined_text, jd=jd)
                
                response = get_gemini_repsonse(prompt)
                st.subheader(response)

if __name__ == "__main__":
    main()
