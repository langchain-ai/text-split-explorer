import streamlit as st
from langchain.text_splitter import Language
import tiktoken
import tempfile
import os
from pathlib import Path
from utils import text_splitter, document_loading


# Streamlit UI
st.title("Pre-processing playground")
st.info("""Pre-process your document into chunks and metadata using Langchain. Transformations included:

- `Document Loader`: Load a document using built-in document loaders.
- `Text Selectors`: Select fields from text to be: 1) embedded and 2) added as metadata. (Only supported for CSV and JSON document types.)
- `Text Splitter` : Split the text to be embedded into chunks using different chunking techniques.
        
""")

# Loaders
st.header("Document Loading")
st.info("""Load a document from a URL or a file. Pick the type of loader you want to use.""")
doc = None
# url = st.text_input(label="File URL", placeholder="URL for the file")
# st.text("or")
uploaded_file = st.file_uploader("Choose a file")
loader_choices = ["JSONLoader", "CSVLoader", "PDF", "UnstructuredIO"]
loader_choice = st.selectbox(
    "Select a document loader", loader_choices
)

# Selectors
st.header("Metadata Selectors")
st.info("""Only supported for JSON or CSV. \n
Select what fields from the object you want to use for embeddings vs just as metadata""")
selectors = False
if st.toggle(label="Enable selectors"):
    selectors = True
    string_to_embed = st.text_input(label="Fields to Embed", placeholder="Comma separated list of fields")
    string_to_metadata = st.text_input(label="Fields for Metadata", placeholder="Comma separated list of fields")

#Splitters
st.header("Text Splitter")
st.info("""Split a text into chunks using a **Text Splitter**. Parameters include:

- `chunk_size`: Max size of the resulting chunks (in either characters or tokens, as selected)
- `chunk_overlap`: Overlap between the resulting chunks (in either characters or tokens, as selected)
- `length_function`: How to measure lengths of chunks, examples are included for either characters or tokens
- The type of the text splitter, this largely controls the separators used to split on
""")
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    chunk_size = st.number_input(min_value=1, label="Chunk Size", value=1000)

with col2:
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

with col3:
    length_function = st.selectbox(
        "Length Function", ["Characters", "Tokens"]
    )

if length_function == "Characters":
    length_function = len
elif length_function == "Tokens":
    enc = tiktoken.get_encoding("cl100k_base")
    def length_function(text: str) -> int:
        return len(enc.encode(text))
else:
    raise ValueError

splitter_choices = ["RecursiveCharacter", "Character"] + [str(v) for v in Language]

with col4:
    splitter_choice = st.selectbox(
        "Select a Text Splitter", splitter_choices
    )

chunks = []
# Split text button
if st.button("Process Text", use_container_width=True):
    # Load
    if(uploaded_file):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # Write the data from the BytesIO object to the temporary file
            temp_file.write(uploaded_file.read())
                # Explicitly close the file
            temp_file.close()
            # Create a Path object using the temporary file's name attribute
        file_path = Path(temp_file.name).resolve()
        if(selectors):
            fields_to_embed = string_to_embed.split(",")
            fields_to_metadata = string_to_metadata.split(",")
            documents = document_loading(temp_file=file_path, loader_choice=loader_choice, embed_keys=fields_to_embed, metadata_keys=fields_to_metadata)
        else: 
            documents = document_loading(temp_file=file_path, loader_choice=loader_choice)
        # Split
        print(documents)
        chunks = text_splitter(splitter_choice=splitter_choice, chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=length_function, documents=documents)
        os.remove(temp_file.name)

if(len(chunks) > 0 ):
    tabs = []
    for i in range(len(chunks)):
        tabs.append("Chunk " + str(i+1))
    allTabs = st.tabs(tabs)

    for i in range(len(allTabs)):
        with allTabs[i]:
            st.subheader("Page Content")
            st.text(chunks[i].page_content)
            if(selectors):
                st.subheader("Metadata")
                st.text(chunks[i].metadata)
