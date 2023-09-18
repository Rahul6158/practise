import streamlit as st
import docx
from io import BytesIO

def is_non_string_element(element):
    """
    Check if an element is non-string (e.g., tables, images, shapes).
    """
    if isinstance(element, docx.oxml.text.paragraph.CT_P):
        return False
    return True

def remove_non_string_objects(docx_file):
    try:
        doc = docx.Document(docx_file)

        # Create a new DOCX document to store the cleaned content
        cleaned_doc = docx.Document()

        for element in doc.element.body:
            try:
                if not is_non_string_element(element):
                    # Process only string elements (paragraphs)
                    paragraph = element
                    new_paragraph = cleaned_doc.add_paragraph()
                    for run in paragraph.runs:
                        if run.text.strip():
                            # Add runs with non-empty text to the cleaned paragraph
                            new_run = new_paragraph.add_run(run.text)
                            # Copy formatting (e.g., bold, italic) from the original run to the new run
                            new_run.bold = run.bold
                            new_run.italic = run.italic
                            # You can copy other formatting attributes as needed

            except Exception as e:
                st.error(f"Error processing the following element: {element}")
                raise e

        # Save the cleaned document to a BytesIO buffer
        cleaned_buffer = BytesIO()
        cleaned_doc.save(cleaned_buffer)
        cleaned_buffer.seek(0)

        return cleaned_buffer

    except Exception as e:
        st.error(f"Error processing the DOCX file: {str(e)}")
        return None

def main():
    st.title("Remove Non-String Objects from DOCX and Download")

    uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])

    if uploaded_file is not None:
        st.markdown("### Uploaded DOCX File:")
        st.write(uploaded_file.name)

        cleaned_buffer = remove_non_string_objects(uploaded_file)

        if isinstance(cleaned_buffer, BytesIO):
            st.info("Non-string objects removed. You can download the cleaned DOCX file below.")
            st.markdown(get_binary_file_downloader_html("Download Cleaned DOCX", cleaned_buffer, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'), unsafe_allow_html=True)
        else:
            st.warning("Failed to process the DOCX file.")

if __name__ == "__main__":
    main()
