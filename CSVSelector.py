import csv
from typing import Dict, List, Optional

class CSVSelector:
    def __init__(
        self,
        file_path: str,
        csv_args: Optional[Dict] = None,
        encoding: Optional[str] = None,
        filter_keys: Optional[List[str]] = None  # Parameter for filtering columns
    ):
        self.file_path = file_path
        self.encoding = encoding
        self.csv_args = csv_args or {}
        self.filter_keys = filter_keys  # Store the filter_keys

    def select(self) -> List[Dict]:
        """Load data into a list of dictionary objects."""

        dicts = []  # This will hold the filtered rows as dictionaries
        with open(self.file_path, newline="", encoding=self.encoding) as csvfile:
            csv_reader = csv.DictReader(csvfile, **self.csv_args)  # type: ignore
            for row in csv_reader:
                # Only include the columns that are in filter_keys if filter_keys is not None
                if self.filter_keys is not None:
                    row = {k: row[k] for k in self.filter_keys if k in row}
                dicts.append(row)  # Append the filtered row dictionary to the list

        return dicts
