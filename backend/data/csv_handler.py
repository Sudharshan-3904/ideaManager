import pandas as pd
import os

class CSVHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.columns = ['title', 'description', 'target_customers', 'minimal_deliverables', 'future_extensions', 'hurdles', 'notes', 'architecture']
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.file_path, index=False)
            print(f"Created new data store at {self.file_path}")

    def read_all(self):
        """Reads all rows from the CSV and returns a list of dictionaries."""
        try:
            df = pd.read_csv(self.file_path)
            # Fill NaN values with empty strings to avoid issues in the UI/Logic
            df = df.fillna("")
            return df.to_dict('records')
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return []

    def write_all(self, data_list):
        """Writes a list of dictionaries to the CSV, overwriting existing content."""
        try:
            df = pd.DataFrame(data_list, columns=self.columns)
            df.to_csv(self.file_path, index=False)
        except Exception as e:
            print(f"Error writing to CSV: {e}")

    def append_row(self, row_dict):
        """Appends a single row (dict) to the CSV."""
        try:
            df = pd.read_csv(self.file_path)
            new_row = pd.DataFrame([row_dict], columns=self.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.file_path, index=False)
        except Exception as e:
            print(f"Error appending to CSV: {e}")
