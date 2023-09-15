import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, Language
import code_snippets as code_snippets
import tiktoken
import introspector
import urllib
import urllib.parse        
oparams = st.experimental_get_query_params()
params = {
    x: oparams[x][0]  for x in oparams
}

# Streamlit UI
st.title("Text Splitter Playground")
st.info("""Split a text into chunks using a **Text Splitter**. Parameters include:

- `chunk_size`: Max size of the resulting chunks (in either characters or tokens, as selected)
- `chunk_overlap`: Overlap between the resulting chunks (in either characters or tokens, as selected)
- `length_function`: How to measure lengths of chunks, examples are included for either characters or tokens
- The type of the text splitter, this largely controls the separators used to split on
""")
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    chunk_size = st.number_input(
        min_value=1,
        label="Chunk Size",
        value=int(params.get("chunk-size",1000)),
        key="chunk-size")

with col2:
    # Setting the max value of chunk_overlap based on chunk_size
    chunk_overlap = st.number_input(
        min_value=1,
        max_value=chunk_size - 1,
        label="Chunk Overlap",
        value=int(params.get("chunk-overlap",int(chunk_size * 0.2))),
        key="chunk-overlap"
    )

    # Display a warning if chunk_overlap is not less than chunk_size
    if chunk_overlap >= chunk_size:
        st.warning("Chunk Overlap should be less than Chunk Length!")

with col3:
    opts =["Characters", "Tokens"]
    length_function = st.selectbox(
        "Length Function", opts,
        key="LengthFunction",
        index=opts.index(params.get("LengthFunction","Characters"))
    )

splitter_choices = ["RecursiveCharacter", "Character"] + [str(v) for v in Language]

with col4:
#    splitter_choices
    choice = params.get("text_splitter",splitter_choices[0])
    opt_index = 0
    if choice in splitter_choices:
        opt_index = splitter_choices.index(choice)
    
    splitter_choice = st.selectbox(
        "Select a Text Splitter", splitter_choices,
        key="text_splitter",
        index=opt_index,
    )

if length_function == "Characters":
    length_function = len
    length_function_str = code_snippets.CHARACTER_LENGTH
elif length_function == "Tokens":
    enc = tiktoken.get_encoding("cl100k_base")


    def length_function(text: str) -> int:
        return len(enc.encode(text))


    length_function_str = code_snippets.TOKEN_LENGTH
else:
    raise ValueError

if splitter_choice == "Character":
    import_text = code_snippets.CHARACTER.format(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function_str
    )

elif splitter_choice == "RecursiveCharacter":
    import_text = code_snippets.RECURSIVE_CHARACTER.format(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function_str
    )

elif "Language." in splitter_choice:
    import_text = code_snippets.LANGUAGE.format(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        language=splitter_choice,
        length_function=length_function_str
    )
else:
    raise ValueError

st.info(import_text)

#for x in oparams:
#    if x in st.session_state:
        # fixme validate thise
        #if x in ("mode","input_id","workflow"):
        #st.write("DEBUG",x,st.session_state[x],oparams[x][0])
        #st.session_state[x] = oparams[x][0]

# Box for pasting text
default_text = introspector.get_input()
#st.code(default_text)
base_url = st.text_input("base_url", key="base-url", value=params.get("base-url",""), help="for the target")

doc = st.text_area("Paste your text here:", key="text-input", value=default_text, height=400)

## create self  link
q= st.experimental_get_query_params()
for x in st.session_state:
    v = st.session_state[x]
    q[x]= v
q["text-input"]=q["text-input"][0:256] #truncate
encoded_query = urllib.parse.urlencode(q, doseq=True)
st.markdown(f"* share [input_link full]({base_url}/?{encoded_query})")

# Split text button
#if (len(default_text ) >10) or
if st.button("Split Text"):
    # Choose splitter
    if splitter_choice == "Character":
        splitter = CharacterTextSplitter(separator = "\n\n",
                                         chunk_size=chunk_size, 
                                         chunk_overlap=chunk_overlap,
                                         length_function=length_function)
    elif splitter_choice == "RecursiveCharacter":
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                  chunk_overlap=chunk_overlap,
                                         length_function=length_function)
    elif "Language." in splitter_choice:
        language = splitter_choice.split(".")[1].lower()
        splitter = RecursiveCharacterTextSplitter.from_language(language,
                                                                chunk_size=chunk_size,
                                                                chunk_overlap=chunk_overlap,
                                         length_function=length_function)
    else:
        raise ValueError
    # Split the text
    splits = splitter.split_text(doc)

    # Display the splits
    for idx, split in enumerate(splits, start=1):
        st.text_area(
            
            f"Split {idx}", split, height=200,
            #key=
        )
        q["text-input"] = split
        q["idx"] = split
        encoded_query = urllib.parse.urlencode(q, doseq=True)
        st.markdown(f"* share [input_link {split[0:50]}]({base_url}/?{encoded_query})")



