import unittest
import os
import tempfile
from unittest.mock import patch, mock_open
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pdf_merger import PdfMerger
from .utils.file_handler import is_valid_pdf, validate_output_path

class TestPdfMerger(unittest.TestCase):
    
    def setUp(self):
        self.merger = PdfMerger()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_empty_pdf_list(self):
        """Test merge with empty PDF list"""
        result = self.merger.merge_pdfs([], "output.pdf")
        self.assertFalse(result)
    
    def test_single_pdf_list(self):
        """Test merge with only one PDF (should fail)"""
        result = self.merger.merge_pdfs(["single.pdf"], "output.pdf")
        self.assertFalse(result)
    
    def test_nonexistent_file(self):
        """Test merge with non-existent files"""
        result = self.merger.merge_pdfs(["fake1.pdf", "fake2.pdf"], "output.pdf")
        self.assertFalse(result)

class TestFileHandler(unittest.TestCase):
    
    def test_is_valid_pdf_nonexistent(self):
        """Test PDF validation with non-existent file"""
        self.assertFalse(is_valid_pdf("nonexistent.pdf"))
    
    def test_is_valid_pdf_wrong_extension(self):
        """Test PDF validation with wrong extension"""
        self.assertFalse(is_valid_pdf("document.txt"))
    
    def test_validate_output_path_empty(self):
        """Test output path validation with empty string"""
        is_valid, clean_path, error = validate_output_path("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())
    
    def test_validate_output_path_adds_extension(self):
        """Test that .pdf extension is added automatically"""
        is_valid, clean_path, error = validate_output_path("test")
        self.assertTrue(clean_path.endswith(".pdf"))

if __name__ == '__main__':
    unittest.main()