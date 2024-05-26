"""
This script will test the ZipExtractor class
"""

import os
import unittest

from plagiarism.adapters.zip_extractor import ZipExtractor


class TestZipExtractor(unittest.TestCase):
    def setUp(self):
        self.zip_path = "tests/unit/adapters/zip_extraction/dataset_test/dataset_test.zip"
        self.extract_path = "tests/unit/adapters/zip_extraction/raw_documents_extracted/"
        self.zip_extractor = ZipExtractor(self.zip_path, self.extract_path)

    def test_extract(self):
        self.zip_extractor.extract()
        self.assertTrue(os.path.exists(self.extract_path))

    def test_get_files(self):
        files = self.zip_extractor.get_files()
        self.assertTrue(len(files) > 0)
        self.assertTrue(all([os.path.exists(file) for file in files]))

    # def tearDown(self):
    #     if os.path.exists(self.extract_path):
    #         os.rmdir(self.extract_path)
