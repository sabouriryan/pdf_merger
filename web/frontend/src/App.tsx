import React, { useState, useEffect, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { validateFiles, mergePdfs } from './services/api';
import { FileValidationResult } from './types/api';
import './App.css';

const App: React.FC = () => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [validationResults, setValidationResults] = useState<FileValidationResult[]>([]);
  const [isValidating, setIsValidating] = useState(false);
  const [isMerging, setIsMerging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Drag and drop functionality
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const pdfFiles = acceptedFiles.filter(file => 
      file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
    );
    setSelectedFiles(prev => [...prev, ...pdfFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: true
  });

  // Validate files when they change
  useEffect(() => {
    if (selectedFiles.length === 0) {
      setValidationResults([]);
      return;
    }

    const handleValidation = async () => {
      setIsValidating(true);
      setError(null);

      try {
        const response = await validateFiles(selectedFiles);
        setValidationResults(response.files);
      } catch (err) {
        setError('Failed to validate files. Check if the server is running.');
        console.error(err);
      } finally {
        setIsValidating(false);
      }
    };

    handleValidation();
  }, [selectedFiles]);

  const removeFile = (index: number) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index);
    setSelectedFiles(newFiles);
  };

  const clearAll = () => {
    setSelectedFiles([]);
  };

  const handleMerge = async () => {
    const validFiles = selectedFiles.filter((file) => {
      const validation = validationResults.find(v => v.filename === file.name);
      return validation?.is_valid;
    });

    if (validFiles.length < 2) {
      setError('Please select at least 2 valid PDF files');
      return;
    }

    setIsMerging(true);
    setError(null);

    try {
      const blob = await mergePdfs(validFiles);
      
      // Download the merged PDF
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'merged.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      // Clear files after successful merge
      setSelectedFiles([]);
      setValidationResults([]);
      
    } catch (err) {
      setError('Failed to merge PDFs. Please try again.');
      console.error(err);
    } finally {
      setIsMerging(false);
    }
  };

  const validFileCount = validationResults.filter(v => v.is_valid).length;
  const canMerge = validFileCount >= 2 && !isValidating && !isMerging;

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <header style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h1 style={{ color: '#333', fontSize: '2.5em', marginBottom: '10px' }}>
          📄 PDF Merger
        </h1>
        <p style={{ color: '#666', fontSize: '1.1em' }}>
          Upload multiple PDF files and merge them into one document
        </p>
      </header>

      {/* Drag & Drop Zone */}
      <div
        {...getRootProps()}
        style={{
          border: '3px dashed #4CAF50',
          borderRadius: '12px',
          padding: '40px 20px',
          textAlign: 'center',
          cursor: 'pointer',
          backgroundColor: isDragActive ? '#f0f8f0' : '#fafafa',
          transition: 'all 0.3s ease',
          marginBottom: '20px'
        }}
      >
        <input {...getInputProps()} />
        <div style={{ fontSize: '48px', marginBottom: '10px' }}>📄</div>
        <p style={{ fontSize: '18px', fontWeight: 'bold', margin: '10px 0' }}>
          {isDragActive ? "Drop the PDF files here..." : "Drag & drop PDF files here, or click to select"}
        </p>
        <p style={{ color: '#666', fontSize: '14px' }}>
          Select multiple PDF files to merge into one document
        </p>
      </div>

      {/* File List */}
      {selectedFiles.length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
            <h3 style={{ margin: 0 }}>Selected Files ({selectedFiles.length})</h3>
            <button
              onClick={clearAll}
              style={{
                background: '#ff6b6b',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                padding: '8px 15px',
                cursor: 'pointer'
              }}
            >
              Clear All
            </button>
          </div>

          {selectedFiles.map((file, index) => {
            const validation = validationResults.find(v => v.filename === file.name);
            const isValid = validation?.is_valid;
            
            return (
              <div
                key={index}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '15px',
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  margin: '8px 0',
                  backgroundColor: 
                    isValid === false ? '#ffe6e6' : 
                    isValid === true ? '#e6ffe6' : '#f9f9f9'
                }}
              >
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
                    {file.name}
                  </div>
                  <div style={{ fontSize: '12px', color: '#666' }}>
                    {(file.size / 1024).toFixed(1)} KB
                  </div>
                  {validation && (
                    <div style={{ marginTop: '4px', fontSize: '12px' }}>
                      {validation.is_valid ? (
                        <span style={{ color: '#4CAF50', fontWeight: 'bold' }}>✓ Valid PDF</span>
                      ) : (
                        <span style={{ color: '#f44336', fontWeight: 'bold' }}>✗ {validation.error}</span>
                      )}
                    </div>
                  )}
                  {isValidating && !validation && (
                    <div style={{ marginTop: '4px', fontSize: '12px', color: '#666' }}>
                      🔄 Validating...
                    </div>
                  )}
                </div>
                <button
                  onClick={() => removeFile(index)}
                  style={{
                    background: '#ff4444',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    padding: '8px 12px',
                    cursor: 'pointer'
                  }}
                >
                  Remove
                </button>
              </div>
            );
          })}
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div style={{
          color: '#f44336',
          backgroundColor: '#ffe6e6',
          padding: '15px',
          borderRadius: '8px',
          margin: '20px 0',
          textAlign: 'center'
        }}>
          <strong>{error}</strong>
        </div>
      )}

      {/* Merge Button */}
      {selectedFiles.length > 0 && (
        <div style={{ textAlign: 'center', marginTop: '30px' }}>
          <div style={{ marginBottom: '15px', color: '#666' }}>
            {validFileCount} of {selectedFiles.length} files are valid
          </div>
          
          <button
            onClick={handleMerge}
            disabled={!canMerge}
            style={{
              backgroundColor: canMerge ? '#4CAF50' : '#ccc',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              padding: '15px 40px',
              fontSize: '18px',
              fontWeight: 'bold',
              cursor: canMerge ? 'pointer' : 'not-allowed',
              transition: 'background-color 0.3s ease'
            }}
          >
            {isMerging ? '🔄 Merging...' : `📄 Merge ${validFileCount} PDFs`}
          </button>
        </div>
      )}
    </div>
  );
};

export default App;
