import streamlit as st
import docx

def find_non_string_objects(docx_file):
    non_string_objects = []

    try:
        doc = docx.Document(docx_file)

        for element in doc.element.body:
            if isinstance(element, docx.oxml.text.paragraph.CT_P):
                # Check if the element is a paragraph
                for run in element.runs:
                    if run.text.strip():  # Check if the text content is non-empty
                        continue
                    # If the text content is empty, check for non-string objects (e.g., tables, images)
                    for child in run._r:
                        if not isinstance(child, docx.oxml.text.Run):
                            non_string_objects.append(child)

            elif not isinstance(element, docx.oxml.text.Run):
                # If the element is not a paragraph, check for non-string objects
                non_string_objects.append(element)

        return non_string_objects

    except Exception as e:
        return str(e)

def main():
    st.title("Non-String Object Finder in DOCX")

    uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])

    if uploaded_file is not None:
        st.markdown("### Uploaded DOCX File:")
        st.write(uploaded_file.name)

        non_string_objects = find_non_string_objects(uploaded_file)

        if non_string_objects:
            st.markdown("### Non-String Objects Found:")
            for i, obj in enumerate(non_string_objects, start=1):
                st.write(f"{i}. {obj}")
        else:
            st.info("No non-string objects found in the DOCX file.")

if __name__ == "__main__":
    main()
