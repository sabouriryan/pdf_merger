export interface FileValidationResult {
  filename: string;
  is_valid: boolean;
  size: number;
  size_kb: number;
  error: string | null;
}

export interface ValidationResponse {
  files: FileValidationResult[];
}