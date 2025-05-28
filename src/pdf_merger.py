import os
from PyPDF2 import PdfMerger as PyPDFMerger
from utils.file_handler import is_valid_pdf

class PdfMerger:
    def __init__(self):
        self.merger = None

    def merge_pdfs(self, pdf_list, output_path):
        """
        Safely merge multiple PDF files into a single PDF.
        
        Args:
            pdf_list (list): List of PDF file paths to merge
            output_path (str): Path where the merged PDF will be saved
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate inputs
            if not pdf_list:
                print("❌ Error: No PDF files provided")
                return False
                
            if len(pdf_list) < 2:
                print("❌ Error: Need at least 2 PDF files to merge")
                return False

            # Validate all files before starting
            for pdf_file in pdf_list:
                if not os.path.exists(pdf_file):
                    print(f"❌ Error: File '{pdf_file}' does not exist")
                    return False
                    
                if not is_valid_pdf(pdf_file):
                    print(f"❌ Error: '{pdf_file}' is not a valid PDF file")
                    return False

            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                except OSError as e:
                    print(f"❌ Error: Cannot create output directory: {e}")
                    return False

            # Initialize merger
            self.merger = PyPDFMerger()

            # Add each PDF to the merger
            for i, pdf_file in enumerate(pdf_list, 1):
                try:
                    print(f"📄 Adding file {i}/{len(pdf_list)}: {os.path.basename(pdf_file)}")
                    self.merger.append(pdf_file)
                except Exception as e:
                    print(f"❌ Error adding '{pdf_file}': {e}")
                    self._cleanup()
                    return False

            # Write the merged PDF
            try:
                with open(output_path, 'wb') as output_file:
                    self.merger.write(output_file)
                print(f"✅ Successfully created: {output_path}")
                
            except Exception as e:
                print(f"❌ Error writing output file: {e}")
                self._cleanup()
                return False

            # Clean up
            self._cleanup()
            return True

        except Exception as e:
            print(f"❌ Unexpected error during merge: {str(e)}")
            self._cleanup()
            return False

    def _cleanup(self):
        """Clean up resources"""
        if self.merger:
            try:
                self.merger.close()
            except:
                pass
            self.merger = None