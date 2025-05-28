# PDF Merger Tool

This project provides a simple command-line tool to merge multiple PDF documents into a single PDF file. It is designed to be user-friendly and efficient, utilizing Python for implementation.

## Features

- Merge multiple PDF files into one.
- Validate PDF file paths before merging.
- Easy to use command-line interface.

## Installation

To get started, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd pdf-merger
pip install -r requirements.txt
```

## Usage

Run the application using the following command:

```bash
python src/main.py
```

You will be prompted to enter the paths of the PDF files you wish to merge. After entering the paths, the merged PDF will be created in the same directory.

## File Structure

- `src/main.py`: Entry point of the application.
- `src/pdf_merger.py`: Contains the `PdfMerger` class for merging PDFs.
- `src/utils/file_handler.py`: Utility functions for file operations.
- `tests/test_pdf_merger.py`: Unit tests for the merging functionality.
- `requirements.txt`: Lists the required dependencies.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.