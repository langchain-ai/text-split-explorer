import json
from pathlib import Path
from typing import Dict, List, Optional, Union

class JSONSelector:
    def __init__(
        self,
        file_path: Union[str, Path],
        filter_keys: Optional[List[str]] = None  # New parameter for filtering
        ):
        self.file_path = file_path
        self.filter_keys = filter_keys  # Store the filter_keys
    
    def process_item(self, item, prefix=""):
        if isinstance(item, dict):
            result = {}
            for key, value in item.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                if self.filter_keys is None or new_prefix in self.filter_keys:  # Check if this key should be processed
                    result[new_prefix] = self.process_item(value, new_prefix)
            return result
        elif isinstance(item, list):
            result = []
            for value in item:
                result.append(self.process_item(value, prefix))
            return result
        else:
            return item

    def process_json(self, data):
        if isinstance(data, list):
            processed_data = []
            for item in data:
                processed_data.append(self.process_item(item))
            return processed_data
        elif isinstance(data, dict):
            return self.process_item(data)
        else:
            return []

    def load(self) -> List[Dict]:
        """Load and return filtered data from the JSON file."""

        dicts = []
        with open(self.file_path, 'r') as json_file:
            try:
                data = json.load(json_file)
                processed_json = self.process_json(data)
                dicts.append(processed_json)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in the file.")
        return dicts