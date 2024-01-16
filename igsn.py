# app.py
import streamlit as st
import requests

def register():
    st.title("User Registration")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        response = requests.post("http://localhost:5000/register", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Registration successful. Please log in.")
        else:
            st.error("Registration failed. User may already exist or an error occurred.")

def login():
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post("http://localhost:5000/login", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Login successful. Welcome, " + username + "!")
        else:
            st.error("Login failed. Please check your credentials.")

def create_post():
    st.title("Create a Post")
    username = st.text_input("Username")
    content = st.text_area("Post Content", height=200)

    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "mp4"])

    if st.button("Create Post"):
        if uploaded_file is not None:
            with open(f"{username}_post_{len(username)}.jpg", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success("File uploaded successfully.")
        else:
            st.warning("No file selected. You can upload an image or video.")

        # Wrap the requests.post in a try-except block to catch ConnectionError
        try:
            response = requests.post("http://localhost:5000/create_post", json={"username": username, "content": content})
            if response.status_code == 200:
                st.success("Post created successfully.")
            else:
                st.error(f"Failed to create post. Server returned status code {response.status_code}.")
        except requests.exceptions.ConnectionError as e:
            st.error(f"ConnectionError: {e}. Check server availability and URL.")


def main():
    st.sidebar.header("User Authentication")
    menu = ["Register", "Login", "Create Post"]
    choice = st.sidebar.radio("Select Action", menu)

    if choice == "Register":
        register()
    elif choice == "Login":
        login()
    elif choice == "Create Post":
        create_post()

if __name__ == "__main__":
    main()
