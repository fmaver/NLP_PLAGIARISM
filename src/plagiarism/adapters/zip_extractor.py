"""
This script defines a Class that extract a zip folder and save the files in a specific folder.
"""
import os
import zipfile


class ZipExtractor:
    def __init__(self, zip_path, extract_path):
        self.zip_path = zip_path
        self.extract_path = extract_path

    def extract(self):
        """
        Extract the zip file to a specific folder
        Returns: None
        """
        with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
            zip_ref.extractall(self.extract_path)
        print("Zip file extracted successfully")

    def get_files(self):
        """
        Get the files extracted from the zip folder
        Returns: list of files
        """
        files = []

        for r, _, f in os.walk(self.extract_path):
            for file in f:
                files.append(os.path.join(r, file))
        print("Files extracted successfully")
        return files
