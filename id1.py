import streamlit as st
import docx
import re

def extract_bullets_from_docx(docx_file):
    try:
        doc = docx.Document(docx_file)

        bullet_points = []

        for paragraph in doc.paragraphs:
            if paragraph.style.name.startswith('List Bullet'):
                # Use regex to capture alphanumeric characters and spaces
                bullet_text = re.sub(r'[^a-zA-Z0-9\s]', '', paragraph.text)
                if bullet_text.strip():
                    bullet_points.append(bullet_text)

        return bullet_points

    except Exception as e:
        return str(e)

def main():
    st.title("Bullet Point Extractor from DOCX")

    uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])

    if uploaded_file is not None:
        st.markdown("### Uploaded DOCX File:")
        st.write(uploaded_file.name)

        bullet_points = extract_bullets_from_docx(uploaded_file)

        if bullet_points:
            st.markdown("### Extracted Bullet Points:")
            for i, bullet_point in enumerate(bullet_points, start=1):
                st.write(f"{i}. {bullet_point}")
        else:
            st.warning("No bullet points found in the DOCX file.")

if __name__ == "__main__":
    main()
