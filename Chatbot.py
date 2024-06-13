import sqlite3
import streamlit as st
import google.generativeai as genai

# Set up SQLite database and table
def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY,
        role TEXT,
        message TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Function to add a message to the database
def add_message(role, message):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('INSERT INTO chat_history (role, message) VALUES (?, ?)', (role, message))
    conn.commit()
    conn.close()

# Function to get chat history from the database
def get_chat_history():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('SELECT role, message FROM chat_history')
    chat_history = c.fetchall()
    conn.close()
    return chat_history

# Initialize the database
init_db()

def expander_content():
    "Please Update the API Key to use the app"
    google_api_key = st.text_input("Generative API Key", key="google_api_key", type="password")
    "[Get an Generative AI API key](https://makersuite.google.com/app/apikey)"
    "[View the source code]()"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    st.info("Please add your Generative AI API key to continue.")
    if not google_api_key:
        st.stop()
    
    if google_api_key:
        genai.configure(api_key=google_api_key)
        try:
            model = genai.GenerativeModel('gemini-pro')
            chat = model.start_chat(history=[])
            response = get_gemini_response(chat, "Greetings with current time in single sentence.")
            st.session_state['connection'] = True
        except Exception as e:
            st.error("Invalid API Key")
            del google_api_key
            st.stop()

def get_gemini_response(chat, question):
    response = chat.send_message(question, stream=True)
    return response

def main():
    st.set_page_config(page_title="Chatbot")
    google_api_key = None
    expand_flag = True
    
    if 'google_api_key' in st.session_state:
        google_api_key = st.session_state['google_api_key']

    if 'connection' in st.session_state:
        if st.session_state['connection'] == True:
            expand_flag = False
    else:
        st.session_state['connection'] = False

    if expand_flag:
        with st.expander("Settings", expanded=expand_flag):
            expander_content()
    else:
        with st.expander("Settings", expanded=expand_flag):
            expander_content()
    
    if google_api_key:
        st.title("💬Gemini LLM")
        st.caption("🚀 A streamlit chatbot powered by Google Generative LLM")

        if prompt := st.chat_input():
            if 'chat_model' not in st.session_state:
                model = genai.GenerativeModel('gemini-pro')
                chat_model = model.start_chat(history=[])
                st.session_state['chat_model'] = chat_model           

            chat_model = st.session_state['chat_model']
            response = get_gemini_response(chat_model, prompt)
            add_message("You", prompt)
            
            st.subheader("Gemini:")
            res = []
            for chunk in response:
                st.write(chunk.text)
                res.append(chunk.text)
            
            add_message("Bot", "".join(res))
        
        with st.sidebar:
            with st.expander("history", expanded=False):
                chat_history = get_chat_history()
                if chat_history:
                    for role, text in reversed(chat_history):
                        st.write(f"{role}: {text}")

if __name__ == "__main__":
    main()
