import os
from pathlib import Path
from PyPDF2 import PdfReader


class DocumentLoader:
    """Load and extract text from various file formats in a directory."""

    SUPPORTED_EXTENSIONS = {'.txt', '.md', '.pdf'}

    def __init__(self, data_dir="./data"):
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

    def load_all_documents(self):
        """Load all supported documents from the data directory."""
        all_content = []
        files_loaded = []

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

        combined_text = "\n\n".join(all_content)
        return combined_text, files_loaded

    def _load_file(self, file_path):
        """Load content from a single file based on its extension."""
        ext = file_path.suffix.lower()

        if ext in {'.txt', '.md'}:
            return self._load_text_file(file_path)
        elif ext == '.pdf':
            return self._load_pdf_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _load_text_file(self, file_path):
        """Load plain text or markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _load_pdf_file(self, file_path):
        """Extract text from PDF file."""
        reader = PdfReader(str(file_path))
        text_parts = []

        for page_num, page in enumerate(reader.pages, 1):
            try:
                text = page.extract_text()
                if text.strip():
                    text_parts.append(text)
            except Exception as e:
                print(f"⚠️  Warning: Failed to extract page {page_num} from {file_path.name}: {e}")

        return "\n\n".join(text_parts)
