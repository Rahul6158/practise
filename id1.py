import streamlit as st
import docx

def count_words_in_docx(docx_file):
    try:
        doc = docx.Document(docx_file)

        total_words = 0  # Initialize the word count

        for paragraph in doc.paragraphs:
            # Count words in the current paragraph and add to the total
            words_in_paragraph = len(paragraph.text.split())
            total_words += words_in_paragraph

        return total_words

    except Exception as e:
        return str(e), 0  # Return 0 words in case of an error

def main():
    st.title("Word Counter for DOCX")

    uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])

    if uploaded_file is not None:
        st.markdown("### Uploaded DOCX File:")
        st.write(uploaded_file.name)

        total_words = count_words_in_docx(uploaded_file)

        if total_words:
            st.markdown(f"### Word Count: {total_words} words")  # Display the word count
        else:
            st.warning("No words found in the DOCX file.")

if __name__ == "__main__":
    main()
