import os
import sys
from pdf_merger import PdfMerger
from utils.file_handler import is_valid_pdf, validate_output_path, get_file_info

def print_header():
    """Print application header"""
    print("=" * 60)
    print("                   PDF MERGER TOOL")
    print("=" * 60)
    print("Safely combine multiple PDF files into one document")
    print()

def get_pdf_files():
    """
    Safely get PDF file paths from user with validation.
    
    Returns:
        list: List of valid PDF file paths
    """
    while True:
        print("📁 Enter PDF file paths to merge:")
        print("   (separate multiple files with commas)")
        print("   (or drag and drop files here)")
        
        user_input = input("\n> ").strip()
        
        if not user_input:
            print("❌ Please provide at least one PDF file path.\n")
            continue
            
        # Parse file paths
        raw_paths = [path.strip().strip('"\'') for path in user_input.split(',')]
        valid_paths = []
        errors = []
        
        for path in raw_paths:
            if not path:
                continue
                
            if not os.path.exists(path):
                errors.append(f"File not found: {path}")
            elif not is_valid_pdf(path):
                errors.append(f"Not a valid PDF: {path}")
            else:
                valid_paths.append(path)
        
        if errors:
            print("\n❌ Found issues:")
            for error in errors:
                print(f"   • {error}")
            print()
            continue
            
        if len(valid_paths) < 2:
            print("❌ Please provide at least 2 PDF files to merge.\n")
            continue
            
        # Show selected files
        print(f"\n✅ Found {len(valid_paths)} valid PDF files:")
        total_size = 0
        for i, path in enumerate(valid_paths, 1):
            info = get_file_info(path)
            total_size += info['size']
            print(f"   {i}. {info['name']} ({info['size_kb']} KB)")
        
        print(f"\n📊 Total size: {round(total_size / 1024, 1)} KB")
        
        confirm = input("\nProceed with these files? (y/n): ").lower()
        if confirm in ['y', 'yes']:
            return valid_paths
        print()

def get_output_path():
    """
    Safely get output file path from user.
    
    Returns:
        str: Valid output file path
    """
    while True:
        print("\n💾 Enter output file name:")
        output_input = input("> ").strip()
        
        is_valid, clean_path, error_msg = validate_output_path(output_input)
        
        if not is_valid:
            print(f"❌ {error_msg}")
            continue
            
        # Check if file exists and ask for confirmation
        if os.path.exists(clean_path):
            print(f"⚠️  File '{clean_path}' already exists.")
            overwrite = input("Overwrite? (y/n): ").lower()
            if overwrite not in ['y', 'yes']:
                continue
                
        return clean_path

def main():
    """Main application function with comprehensive error handling"""
    try:
        print_header()
        
        # Get input files
        pdf_files = get_pdf_files()
        
        # Get output path
        output_path = get_output_path()
        
        # Perform merge
        print(f"\n🔄 Merging {len(pdf_files)} PDF files...")
        print(f"📁 Output: {output_path}")
        print()
        
        merger = PdfMerger()
        success = merger.merge_pdfs(pdf_files, output_path)
        
        if success:
            # Show results
            output_info = get_file_info(output_path)
            print(f"\n🎉 SUCCESS!")
            print(f"📄 Created: {output_info['name']}")
            print(f"📊 Size: {output_info['size_kb']} KB")
            print(f"📍 Location: {os.path.abspath(output_path)}")
        else:
            print(f"\n💥 FAILED to merge PDF files.")
            print("Please check the error messages above and try again.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⛔ Operation cancelled by user.")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        print("Please try again or report this issue.")
        sys.exit(1)

if __name__ == "__main__":
    main()