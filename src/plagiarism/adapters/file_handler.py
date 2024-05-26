import hashlib
import os


class FileHandler:
    def __init__(self):
        self.file_hashes = {}

    def calculate_hash(self, file_path):
        """Calculate the hash of the file content."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def repeated_files(self, output_file, txt_path):
        """
        This function will check similarities in file in order to avoid indexing the same file twice.
        """
        # Get the list of files in the output path
        existing_files = os.listdir(txt_path)

        # Calculate hash for the new file
        new_file_hash = self.calculate_hash(output_file)
        output_file_name = output_file.split("/")[-1]

        # Check if the new file's hash matches any existing file's hash
        for existing_file in existing_files:
            existing_file_path = os.path.join(txt_path, existing_file)
            existing_file_hash = self.calculate_hash(existing_file_path)

            if (new_file_hash == existing_file_hash) & (existing_file != output_file_name):
                print(f"The file {output_file_name} is a duplicate of {existing_file}.")
                return True
        return False
