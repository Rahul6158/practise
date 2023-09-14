import streamlit as st
import doctotxt

def extract_text_from_docx(docx_file):
    try:
        text = doctotxt.extract_text(docx_file)
        return text
    except Exception as e:
        return str(e)

def main():
    st.title("DOCX Text Extractor")

    uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])

    if uploaded_file is not None:
        st.markdown("### Uploaded DOCX File:")
        st.write(uploaded_file.name)

        if st.button("Extract Text"):
            extracted_text = extract_text_from_docx(uploaded_file)

            if extracted_text:
                st.markdown("### Extracted Text:")
                st.write(extracted_text)
            else:
                st.error("Error: Unable to extract text from the DOCX file.")

if __name__ == "__main__":
    main()
