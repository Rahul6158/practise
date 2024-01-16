# app.py
import streamlit as st
import requests

def fetch_anime_quote():
    api_url = "https://github.com/RocktimSaikia/anime-chan"
    response = requests.get(api_url)

    if response.status_code == 200:
        try:
            quote_data = response.json()
            anime = quote_data["anime"]
            character = quote_data["character"]
            quote = quote_data["quote"]
            return anime, character, quote
        except KeyError:
            st.error("Error: Unexpected response format from AnimeChan API.")
            return None
    else:
        st.error(f"Error: Unable to fetch quote. Status code {response.status_code}")
        return None

def main():
    st.title("Anime Quote Generator")
    st.subheader("Get random anime quotes!")

    if st.button("Generate Quote"):
        quote_info = fetch_anime_quote()

        if quote_info:
            anime, character, quote = quote_info
            st.success(f"Anime: {anime}")
            st.success(f"Character: {character}")
            st.info(f"Quote: {quote}")
        else:
            st.warning("Please try again.")

if __name__ == "__main__":
    main()
