from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec
from langchain.docstore.document import Document
from typing import (
    List,
)

def text_splitter(splitter_choice:str, chunk_size:int, chunk_overlap:int, length_function:int, documents:List[Document]):
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
    return splitter.split_documents(documents)


def document_loading(temp_file, loader_choice:str, embed_keys: List[str] = None, metadata_keys: List[str] = None) -> List[Document]:
    from langchain.document_loaders import PyPDFLoader, UnstructuredFileLoader
    from JSONLoader import JSONLoader
    from CSVLoader import CSVLoader
    
    if loader_choice == "JSONLoader":
        loader = JSONLoader(file_path=temp_file, embed_keys=embed_keys, metadata_keys=metadata_keys)
    elif loader_choice == "CSVLoader":
        loader = CSVLoader(file_path=temp_file, embed_keys=embed_keys, metadata_keys=metadata_keys)
    elif loader_choice == "PDF":
        loader = PyPDFLoader(file_path=temp_file)
    elif loader_choice == "UnstructuredIO":
        loader = UnstructuredFileLoader(file_path=temp_file)
    return loader.load()