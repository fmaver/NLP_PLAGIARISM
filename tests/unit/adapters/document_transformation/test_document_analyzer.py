"""
This script will test the functionality of the DocumentAnalyzer class.
"""

import glob
import os

import pytest

from plagiarism.adapters.document_converter import DocumentAnalyzer


def test_convert_files_to_txt():
    doc_analyzer = DocumentAnalyzer()
    doc_files = glob.glob("tests/unit/adapters/document_transformation/raw_documents_test/*")
    output_folder = "tests/unit/adapters/document_transformation/txt_files/"

    doc_analyzer.convert_files_to_txt(doc_files, output_folder)

    txt_files = glob.glob(output_folder + "*.txt")

    assert len(txt_files) == len(doc_files) - 1
    for txt_file in txt_files:
        assert os.path.exists(txt_file)
        # os.remove(txt_file)
