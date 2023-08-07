import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter


# Streamlit UI
st.title("Document Splitter Playground")
st.info("Split a document into chunks using a `Document Splitter` with input `chunk_size` and `chunk_overlap`")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    chunk_size = st.number_input(min_value=1, label="Chunk Size (Characters or Tokens)", value=1000)

with col2:
    # Setting the max value of chunk_overlap based on chunk_size
    chunk_overlap = st.number_input(
        min_value=1,
        max_value=chunk_size - 1,
        label="Chunk Overlap (Characters or Tokens)",
        value=int(chunk_size * 0.2),
    )

    # Display a warning if chunk_overlap is not less than chunk_size
    if chunk_overlap >= chunk_size:
        st.warning("Chunk Overlap should be less than Chunk Length!")

with col3:
    splitter_choice = st.selectbox(
        "Select a Document Splitter", ["Characters", "Recursive Characters", "Tokens"]
    )

if splitter_choice == "Characters":
    import_text = """```python
    from langchain.text_splitter import CharacterTextSplitter

    splitter = CharacterTextSplitter(
        separator = " ", # Split character (default \\n\\n)
        chunk_size={chunk_size}, # Measure chunk length by number of characters
        chunk_overlap={chunk_overlap}
    )
    text = "foo bar"
    splits = splitter.split_text(text)
    """.format(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

elif splitter_choice == "Recursive Characters":
    import_text = """```python
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    # The default list of split characters is [\\n\\n, \\n, " ", ""]
    # Tries to split on them in order until the chunks are small enough
    # Keep paragraphs, sentences, words together as long as possible
    splitter = RecursiveCharacterTextSplitter(
        chunk_size={chunk_size}, 
        chunk_overlap={chunk_overlap}
    )
    text = "foo bar"
    splits = splitter.split_text(text)
    """.format(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

else: # Tokens
    import_text = """```python
    from langchain.text_splitter import CharacterTextSplitter

    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator = " ", # Split character (default \\n\\n)
        chunk_size={chunk_size}, # Measure chunk length by number of characters
        chunk_overlap={chunk_overlap}
    )
    text = "foo bar"
    splits = splitter.split_text(text)
    """.format(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

st.info(import_text)

# Box for pasting document
doc = st.text_area("Paste your document here:")

# Split document button
if st.button("Split Document"):
    # Choose splitter
    if splitter_choice == "Characters":
        splitter = CharacterTextSplitter(separator = " ", 
                                         chunk_size=chunk_size, 
                                         chunk_overlap=chunk_overlap)
    elif splitter_choice == "Recursive Characters":
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                  chunk_overlap=chunk_overlap)
    else: # Tokens
        splitter = CharacterTextSplitter.from_tiktoken_encoder(separator = " ",
                                                               chunk_size=chunk_size,
                                                               chunk_overlap=chunk_overlap)
    # Split the document
    splits = splitter.split_text(doc)

    # Display the splits
    for idx, split in enumerate(splits, start=1):
        st.text_area(
            f"Split {idx}", split, height=200
        )
