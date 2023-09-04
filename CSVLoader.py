
import csv
from typing import Dict, List, Optional

from langchain.docstore.document import Document  # Assume this is part of your existing code
from langchain.document_loaders.base import BaseLoader  # Assume this is part of your existing code

class CSVLoader(BaseLoader):
    def __init__(
        self,
        file_path: str,
        source_column: Optional[str] = None,
        csv_args: Optional[Dict] = None,
        encoding: Optional[str] = None,
        filter_keys: Optional[List[str]] = None  # New parameter for filtering columns
    ):
        self.file_path = file_path
        self.source_column = source_column
        self.encoding = encoding
        self.csv_args = csv_args or {}
        self.filter_keys = filter_keys  # Store the filter_keys

    def load(self) -> List[Document]:
        """Load data into document objects."""

        docs = []
        with open(self.file_path, newline="", encoding=self.encoding) as csvfile:
            csv_reader = csv.DictReader(csvfile, **self.csv_args)  # type: ignore
            for i, row in enumerate(csv_reader):
                # Only include the columns that are in filter_keys if filter_keys is not None
                if self.filter_keys is not None:
                    row = {k: row[k] for k in self.filter_keys if k in row}
                content = "\n".join(f"{k.strip()}: {v.strip()}" for k, v in row.items())
                try:
                    source = (
                        row[self.source_column]
                        if self.source_column is not None
                        else self.file_path
                    )
                except KeyError:
                    raise ValueError(
                        f"Source column '{self.source_column}' not found in CSV file."
                    )
                metadata = {"source": source, "row": i}
                doc = Document(page_content=content, metadata=metadata)
                docs.append(doc)

        return docs