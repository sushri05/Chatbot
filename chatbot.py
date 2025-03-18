import os
import cohere
import streamlit as st
import sqlite3

COHERE_API_KEY = "ULvHjpP3lVmQrsaSTQYoiIAIx2XgW8eAJq1BEs9x" 
co = cohere.Client(COHERE_API_KEY)

# Initialize database connection
conn = sqlite3.connect("chat_history.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        bot TEXT
    )
''')
conn.commit()

# Load chatbot avatar

# Custom CSS for a cuter UI
st.markdown("""
    <style>
    body {
        background-color: #ffebf1;
    }
    .chat-bubble {
        border-radius: 20px;
        padding: 10px;
        margin: 5px;
        display: inline-block;
        max-width: 80%;
    }
    .user-bubble {
        text-align: right;
    }
    .bot-bubble {
        text-align: left;
    }
    .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI

st.title("🌸  Chatbot 🌸")

# Delete Chat History Button
if st.button("🗑️ Delete Chat History"):
    c.execute("DELETE FROM chats")  # Clear database
    conn.commit()
    st.success("Chat history deleted!")  # Show success message
    st.rerun()  # Refresh UI
 # Refresh the app UI

# Display chat history
st.subheader("Chat History")
c.execute("SELECT * FROM chats")
history = c.fetchall()

for row in history:
    st.markdown(f'<div class="chat-bubble user-bubble">You: {row[1]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-bubble bot-bubble">Bot: {row[2]}</div>', unsafe_allow_html=True)

# User Input
user_input = st.text_input("Type your message here:")

if user_input:
    # Send request to Cohere API
    response = co.generate(
        model="command-r-plus",  # You can change the model if needed
        prompt=user_input,
        max_tokens=200
    )
    bot_response = response.generations[0].text.strip()

    # Display response
    st.markdown(f'<div class="chat-bubble user-bubble">You: {user_input}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-bubble bot-bubble">Bot: {bot_response}</div>', unsafe_allow_html=True)

    # Save to database
    c.execute("INSERT INTO chats (user, bot) VALUES (?, ?)", (user_input, bot_response))
    conn.commit()
