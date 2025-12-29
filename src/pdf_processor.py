
"""
PDF Processor Module - Handles PDF download and text extraction
"""

import requests
from pathlib import Path
from typing import Optional
import PyPDF2
import pdfplumber
from bs4 import BeautifulSoup
import utils,traceback


class PDFProcessor:
    """Handles PDF downloading and text extraction"""
    
    def __init__(self, config: dict):
        self.config = config
        self.downloads_dir = Path(config['output']['downloads_dir'])
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        self.subjects_data = utils.load_subjects_data()
        #self.session = requests.Session()
    
    def download_chapter(self, subject: str, chapter: str) -> Path:
        """
        Download chapter PDF from NCERT website
        """
        # Sanitize filename
        safe_subject = subject.replace(' ', '_').replace('/', '_')
        safe_chapter = chapter.replace(' ', '_').replace('/', '_')
        filename = f"{safe_subject}_{safe_chapter}.pdf"
        filepath = self.downloads_dir / filename
        
        # If file already exists and has content, return it
        if filepath.exists() and filepath.stat().st_size > 1000:
            print(f"      Using existing file: {filepath}")
            return filepath
        
        # Try to download from NCERT
        print (f"file not found {filepath}")
        for attempts in range(3):
            try:
                pdf_url = self._get_chapter_url(subject, chapter)
                
                if pdf_url:
                    print(f"      Downloading from: {pdf_url}")
                    response = requests.get(pdf_url, timeout=300, stream=False)
                    
                    if response.status_code == 200:
                        # Save the PDF
                        with open(filepath, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        
                        # Verify download
                        if filepath.stat().st_size > 1000:
                            print(f"      Successfully downloaded: {filepath.stat().st_size} bytes")
                            return filepath
                        else:
                            print(f"      Download failed: file too small attempts {attempts}")
                    else:
                        print(f"      HTTP Error: {response.status_code} attempts {attempts}")
            
            except Exception as e:
                print(f"      Download error: {str(e)} attempts {attempts}")
                traceback.print_exc()
                #raise e
        
        # If download failed, create placeholder
        # if not filepath.exists() or filepath.stat().st_size < 1000:
        #     print(f"      Creating placeholder file (download failed)")
        #     filepath.touch()
        
        return filepath

    def _get_chapter_url(self, subject: str, chapter: str) -> Optional[str]:
        """Get the PDF URL for a specific chapter"""
        
        chapter_num = self.subjects_data[subject]["chapters"].get(chapter)
        if chapter_num:
            return self.subjects_data[subject]["base_url"].format(chapter_num)
        
        # # Handle Science
        # elif subject == "Science":
        #     chapter_num = self.NCERT_PDF_URLS["Science"]["chapters"].get(chapter)
        #     if chapter_num:
        #         return self.NCERT_PDF_URLS["Science"]["base_url"].format(chapter_num)
        
        # # Handle Social Science (multiple books)
        # elif subject == "Social_Science":
        #     for book_name, book_data in self.NCERT_PDF_URLS["Social_Science"].items():
        #         if chapter in book_data["chapters"]:
        #             chapter_num = book_data["chapters"][chapter]
        #             return book_data["base_url"].format(chapter_num)
        
        # # Handle English (multiple books)
        # elif subject == "English":
        #     for book_name, book_data in self.NCERT_PDF_URLS["English"].items():
        #         if chapter in book_data["chapters"]:
        #             chapter_num = book_data["chapters"][chapter]
        #             return book_data["base_url"].format(chapter_num)
        
        return None
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text content from PDF using multiple methods
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            # Return sample content for demo
            return self._get_sample_content()
        
        # Try pdfplumber first (better for complex layouts)
        try:
            return self._extract_with_pdfplumber(pdf_path)
        except Exception:
            pass
        
        # Fallback to PyPDF2
        try:
            return self._extract_with_pypdf2(pdf_path)
        except Exception:
            pass
        
        # Return sample content if extraction fails
        return self._get_sample_content()
    
    def _extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """Extract text using pdfplumber"""
        text_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            max_pages = self.config['pdf'].get('max_pages_per_chapter', 50)
            
            for i, page in enumerate(pdf.pages):
                if i >= max_pages:
                    break
                
                text = page.extract_text()
                if text:
                    text_content.append(text)
        
        return "\\n\\n".join(text_content)
    
    def _extract_with_pypdf2(self, pdf_path: Path) -> str:
        """Extract text using PyPDF2"""
        text_content = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            max_pages = self.config['pdf'].get('max_pages_per_chapter', 50)
            
            for i in range(min(len(pdf_reader.pages), max_pages)):
                page = pdf_reader.pages[i]
                text = page.extract_text()
                if text:
                    text_content.append(text)
        
        return "\\n\\n".join(text_content)
    
    def _get_sample_content(self) -> str:
        """Return sample content for demonstration"""
        return """
        SAMPLE CHAPTER CONTENT
        
        This is sample content from an NCERT textbook chapter.
        In production, this would be replaced with actual extracted content.
        
        Key Concepts:
        1. First major concept with detailed explanation
        2. Second major concept with examples
        3. Third major concept with applications
        
        Important Definitions:
        - Definition 1: Clear explanation
        - Definition 2: Clear explanation
        
        Solved Examples:
        Example 1: Problem statement and solution
        Example 2: Problem statement and solution
        
        Exercise Questions:
        1. Practice question 1
        2. Practice question 2
        3. Practice question 3
        """
