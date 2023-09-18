import streamlit as st
import docx
from io import BytesIO

def find_non_string_objects(docx_file):
    non_string_objects = []

    try:
        doc = docx.Document(docx_file)
        cleaned_doc = docx.Document()  # Create a new DOCX document to store the cleaned content

        for element in doc.element.body:
            if isinstance(element, docx.oxml.text.paragraph.CT_P):
                # Check if the element is a paragraph
                new_paragraph = cleaned_doc.add_paragraph()  # Create a new paragraph in the cleaned document
                for run in element.runs:
                    if run.text.strip():  # Check if the text content is non-empty
                        # Add runs with non-empty text to the cleaned paragraph
                        new_run = new_paragraph.add_run(run.text)
                        # Copy formatting (e.g., bold, italic) from the original run to the new run
                        new_run.bold = run.bold
                        new_run.italic = run.italic
                        # You can copy other formatting attributes as needed
                    else:
                        # If the text content is empty, check for non-string objects (e.g., tables, images)
                        for child in run._r:
                            if not isinstance(child, docx.oxml.text.Run):
                                non_string_objects.append(child)

            elif not isinstance(element, docx.oxml.text.Run):
                # If the element is not a paragraph, check for non-string objects
                non_string_objects.append(element)

        cleaned_buffer = BytesIO()  # Create a buffer to store the cleaned document
        cleaned_doc.save(cleaned_buffer)
        cleaned_buffer.seek(0)

        return non_string_objects, cleaned_buffer

    except Exception as e:
        return str(e), None

def main():
    st.title("Remove Non-String Objects from DOCX and Download")

    uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])

    if uploaded_file is not None:
        st.markdown("### Uploaded DOCX File:")
        st.write(uploaded_file.name)

        non_string_objects, cleaned_buffer = find_non_string_objects(uploaded_file)

        if cleaned_buffer:
            st.info("Non-string objects removed. You can download the cleaned DOCX file below.")
            st.markdown(get_binary_file_downloader_html("Download Cleaned DOCX", cleaned_buffer, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'), unsafe_allow_html=True)
        else:
            st.warning(f"Failed to process the DOCX file. Error: {non_string_objects}")

if __name__ == "__main__":
    main()
