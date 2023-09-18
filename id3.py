import streamlit as st
import docx
from docx.shared import Length

# Function to remove non-string objects from a DOCX file
def remove_non_string_objects(docx_file):
    try:
        doc = docx.Document(docx_file)
        new_doc = docx.Document()

        for element in doc.element.body:
            if isinstance(element, docx.oxml.text.paragraph.CT_P):
                # Process paragraphs and their runs
                for run in element.runs:
                    if run.text.strip():  # Check if the text content is non-empty
                        new_paragraph = new_doc.add_paragraph()
                        new_run = new_paragraph.add_run(run.text)
                        new_run.bold = run.bold
                        new_run.italic = run.italic
                        new_run.underline = run.underline
                        new_run.font.size = run.font.size
                        new_run.font.color.rgb = run.font.color.rgb
                        # You can copy other run properties as needed

        # Save the modified document to a new file
        output_file_path = "document_without_non_string.docx"
        new_doc.save(output_file_path)
        
        return output_file_path

    except Exception as e:
        return str(e)

# Function to generate a download link for a file
def get_binary_file_downloader_html(link_text, file_path, mime_type='application/docx'):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    b64_file = base64.b64encode(file_data).decode()
    download_link = f'<a href="data:{mime_type};base64,{b64_file}" download="{os.path.basename(file_path)}">{link_text}</a>'
    return download_link

# Main Streamlit app
def main():
    st.title("Non-String Object Remover in DOCX")

    uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])

    if uploaded_file is not None:
        st.markdown("### Uploaded DOCX File:")
        st.write(uploaded_file.name)

        result = remove_non_string_objects(uploaded_file)

        if isinstance(result, str):
            st.success("Non-string objects removed successfully.")
            st.markdown(get_binary_file_downloader_html("Download Modified DOCX", result), unsafe_allow_html=True)
        else:
            st.error("Failed to process the DOCX file. Error: " + result)

if __name__ == "__main__":
    main()
