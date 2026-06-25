import pytesseract
from PIL import Image
from pathlib import Path
from typing import Dict, Optional, List
import re
import asyncio


class OCREngine:
    """
    OCR engine for extracting text from screenshots.
    """

    def __init__(self, tesseract_path: Optional[str] = None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

        self.supported_languages = ['eng']  # Can be extended: 'spa', 'fra', etc.

    def extract_text(self, image_path: Path, language: str = 'eng') -> Dict:
        """
        Extract text from an image using Tesseract OCR.

        Args:
            image_path: Path to the image file
            language: OCR language (default: 'eng')

        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            # Open image
            image = Image.open(image_path)

            # Extract text with confidence data
            data = pytesseract.image_to_data(
                image,
                lang=language,
                output_type=pytesseract.Output.DICT
            )

            # Extract plain text
            text = pytesseract.image_to_string(image, lang=language)

            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0

            # Count words
            words = [word for word in data['text'] if word.strip()]
            word_count = len(words)

            return {
                'text': text.strip(),
                'word_count': word_count,
                'confidence': avg_confidence / 100.0,  # Normalize to 0-1
                'language': language,
                'raw_data': data,
            }

        except Exception as e:
            return {
                'text': '',
                'word_count': 0,
                'confidence': 0.0,
                'language': language,
                'error': str(e),
            }

    async def extract_text_async(self, image_path: Path, language: str = 'eng') -> Dict:
        """Async version of extract_text"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.extract_text, image_path, language)

    def search_keywords(self, text: str, keywords: List[str], case_sensitive: bool = False) -> List[Dict]:
        """
        Search for keywords in extracted text.

        Args:
            text: Text to search
            keywords: List of keywords to find
            case_sensitive: Whether search is case-sensitive

        Returns:
            List of matches with positions
        """
        matches = []

        if not case_sensitive:
            text_lower = text.lower()
            keywords = [k.lower() for k in keywords]
        else:
            text_lower = text

        for keyword in keywords:
            pattern = re.escape(keyword)
            for match in re.finditer(pattern, text_lower):
                matches.append({
                    'keyword': keyword,
                    'position': match.start(),
                    'context': text[max(0, match.start()-50):match.end()+50],
                })

        return matches

    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text"""
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        return url_pattern.findall(text)

    def extract_domains(self, text: str) -> List[str]:
        """Extract domain names from text"""
        domain_pattern = re.compile(
            r'(?:(?:https?://)?(?:www\.)?)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})'
        )
        matches = domain_pattern.findall(text)
        return list(set(matches))  # Remove duplicates


class OCRProcessor:
    """
    Batch processor for OCR operations with queuing.
    """

    def __init__(self, engine: OCREngine, max_workers: int = 2):
        self.engine = engine
        self.max_workers = max_workers
        self.queue = asyncio.Queue()
        self.workers = []
        self.is_running = False

    async def worker(self):
        """Worker that processes OCR tasks from the queue"""
        while self.is_running:
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                image_path, callback = task

                # Process OCR
                result = await self.engine.extract_text_async(image_path)

                # Call callback with result
                if callback:
                    await callback(image_path, result)

                self.queue.task_done()

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"OCR worker error: {e}")

    async def start(self):
        """Start OCR workers"""
        self.is_running = True
        self.workers = [
            asyncio.create_task(self.worker())
            for _ in range(self.max_workers)
        ]

    async def stop(self):
        """Stop OCR workers"""
        self.is_running = False
        await self.queue.join()
        for worker in self.workers:
            await worker

    async def process(self, image_path: Path, callback=None):
        """
        Add image to OCR processing queue.

        Args:
            image_path: Path to image
            callback: Optional async callback(image_path, result)
        """
        await self.queue.put((image_path, callback))

    def get_queue_size(self) -> int:
        """Get current queue size"""
        return self.queue.qsize()
