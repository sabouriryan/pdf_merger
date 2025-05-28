import os
from pathlib import Path

def is_valid_pdf(file_path):
    """
    Check if the provided file path is a valid PDF file.
    
    Args:
        file_path (str): Path to the file to check
        
    Returns:
        bool: True if file exists and appears to be a PDF
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return False
            
        # Check file extension
        if not file_path.lower().endswith('.pdf'):
            return False
            
        # Check if file is readable and has some content
        if os.path.getsize(file_path) == 0:
            return False
            
        # Try to read the PDF header
        with open(file_path, 'rb') as f:
            header = f.read(4)
            if header != b'%PDF':
                return False
                
        return True
        
    except Exception:
        return False

def validate_output_path(output_path):
    """
    Validate and prepare output path.
    
    Args:
        output_path (str): Desired output file path
        
    Returns:
        tuple: (is_valid, clean_path, error_message)
    """
    try:
        # Clean the path
        clean_path = output_path.strip().strip('"\'')
        
        if not clean_path:
            return False, "", "Output path cannot be empty"
            
        # Add .pdf extension if missing
        if not clean_path.lower().endswith('.pdf'):
            clean_path += '.pdf'
            
        # Check if we can write to the directory
        output_dir = os.path.dirname(clean_path)
        if output_dir:
            try:
                os.makedirs(output_dir, exist_ok=True)
            except OSError:
                return False, clean_path, f"Cannot create directory: {output_dir}"
            
        return True, clean_path, ""
            
    except Exception as e:
        return False, output_path, f"Invalid output path: {str(e)}"

def get_file_info(file_path):
    """
    Get information about a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        dict: File information
    """
    try:
        stat = os.stat(file_path)
        return {
            'size': stat.st_size,
            'size_kb': round(stat.st_size / 1024, 1),
            'name': os.path.basename(file_path),
            'exists': True
        }
    except OSError:
        return {
            'size': 0,
            'size_kb': 0,
            'name': os.path.basename(file_path) if file_path else '',
            'exists': False
        }