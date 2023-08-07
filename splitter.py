import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Streamlit UI
st.title("Document Splitter")

col1, col2 = st.columns([5, 5])

with col1:
    chunk_size = st.number_input(min_value=1, label="Chunk Size", value=1000)

    # Setting the max value of chunk_overlap based on chunk_size
    chunk_overlap = st.number_input(
        min_value=1,
        max_value=chunk_size - 1,
        label="Chunk Overlap",
        value=int(chunk_size * 0.2),
    )

    # Display a warning if chunk_overlap is not less than chunk_size
    if chunk_overlap >= chunk_size:
        st.warning("Chunk Overlap should be less than Chunk Length!")

with col2:
    splitter = st.selectbox(
        "Select a Document Splitter", ["RecursiveCharacterTextSplitter"]
    )

import_text = """```python
from langchain.text_splitter import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size={chunk_size}, chunk_overlap={chunk_overlap}
)
text = "foo bar"
splits = splitter.split_text(text)
""".format(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

st.info(import_text)


# Box for pasting document
doc = st.text_area("Paste your document here:")

# Split document button
if st.button("Split Document"):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    splits = splitter.split_text(doc)

    # Display the splits
    st.subheader("Document Splits:")
    for idx, split in enumerate(splits, start=1):
        st.text_area(
            f"Split {idx}", split, height=200
        )
