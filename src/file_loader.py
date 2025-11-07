import os
from pathlib import Path
from PyPDF2 import PdfReader
from typing import Tuple, List, Set


class DocumentLoader:
    """Load and extract text from various file formats in a directory."""

    SUPPORTED_EXTENSIONS: Set[str] = {'.txt', '.md', '.pdf'}

    def __init__(self, data_dir: str = "./data") -> None:
        """
        Initialize document loader with data directory.
        
        Args:
            data_dir: Path to directory containing documents
            
        Raises:
            FileNotFoundError: If data directory does not exist
        """
        self.data_dir: Path = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

    def load_all_documents(self) -> Tuple[str, List[str]]:
        """
        Load all supported documents from the data directory.
        
        Returns:
            Tuple of (combined_text, files_loaded)
            - combined_text: All document content joined with double newlines
            - files_loaded: List of successfully loaded filenames
            
        Raises:
            ValueError: If no valid documents are found
        """
        all_content: List[str] = []
        files_loaded: List[str] = []

        for file_path in sorted(self.data_dir.iterdir()):
            if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    content = self._load_file(file_path)
                    if content.strip():
                        all_content.append(content)
                        files_loaded.append(file_path.name)
                except Exception as e:
                    print(f"⚠️  Warning: Failed to load {file_path.name}: {e}")

        if not all_content:
            raise ValueError(f"No valid documents found in {self.data_dir}")

        combined_text: str = "\n\n".join(all_content)
        return combined_text, files_loaded

    def _load_file(self, file_path: Path) -> str:
        """
        Load content from a single file based on its extension.
        
        Args:
            file_path: Path to the file to load
            
        Returns:
            File content as string
            
        Raises:
            ValueError: If file type is not supported
        """
        ext: str = file_path.suffix.lower()

        if ext in {'.txt', '.md'}:
            return self._load_text_file(file_path)
        elif ext == '.pdf':
            return self._load_pdf_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _load_text_file(self, file_path: Path) -> str:
        """
        Load plain text or markdown file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            File content as string
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _load_pdf_file(self, file_path: Path) -> str:
        """
        Extract text from PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text from all pages, joined with double newlines
        """
        reader = PdfReader(str(file_path))
        text_parts: List[str] = []

        for page_num, page in enumerate(reader.pages, 1):
            try:
                text: str = page.extract_text()
                if text.strip():
                    text_parts.append(text)
            except Exception as e:
                print(f"⚠️  Warning: Failed to extract page {page_num} from {file_path.name}: {e}")

        return "\n\n".join(text_parts)
