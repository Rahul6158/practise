import streamlit as st
import docx
from docx.shared import Length

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

            elif isinstance(element, docx.oxml.text.Table):
                # Handle tables (you can skip or process them as needed)
                new_table = new_doc.add_table(rows=element.rows, cols=element.cols)
                for i, row in enumerate(element.rows):
                    for j, cell in enumerate(row.cells):
                        new_table.cell(i, j).text = cell.text
                        # You can copy cell properties as needed

        # Save the modified document to a new file
        new_doc.save("document_without_non_string.docx")
        
        return "document_without_non_string.docx"

    except Exception as e:
        return str(e)

def main():
    st.title("Non-String Object Remover in DOCX")

    uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])

    if uploaded_file is not None:
        st.markdown("### Uploaded DOCX File:")
        st.write(uploaded_file.name)

        result = remove_non_string_objects(uploaded_file)

        if isinstance(result, str):
            st.success("Non-string objects removed successfully.")
            st.markdown(get_binary_file_downloader_html("Download Modified DOCX", result, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'), unsafe_allow_html=True)
        else:
            st.error("Failed to process the DOCX file. Error: " + result)

if __name__ == "__main__":
    main()
