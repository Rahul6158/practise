# app.py
import streamlit as st
import requests

def fetch_anime_quote():
    api_url = "https://animechan.vercel.app/api/random"
    response = requests.get(api_url)

    if response.status_code == 200:
        quote_data = response.json()
        return quote_data["anime"], quote_data["character"], quote_data["quote"]
    else:
        return None

def main():
    st.title("Anime Quote Generator")
    st.subheader("Get random anime quotes!")

    if st.button("Generate Quote"):
        anime, character, quote = fetch_anime_quote()

        if quote:
            st.success(f"Anime: {anime}")
            st.success(f"Character: {character}")
            st.info(f"Quote: {quote}")
        else:
            st.error("Failed to fetch quote. Please try again.")

if __name__ == "__main__":
    main()
