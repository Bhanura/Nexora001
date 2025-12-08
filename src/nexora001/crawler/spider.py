"""
Scrapy spider for crawling websites with chunking and embedding generation.
"""

import scrapy
from scrapy.http import Response
from typing import Generator, Optional
from urllib.parse import urljoin, urlparse
import sys
from pathlib import Path

# Add parent to path for imports
sys.path. insert(0, str(Path(__file__).parent. parent. parent))

from nexora001. storage.mongodb import MongoDBStorage
from nexora001.processors.chunker import TextChunker
from nexora001.processors.embeddings import EmbeddingGenerator, EmbeddingProvider


class Nexora001Spider(scrapy. Spider):
    """
    Spider for crawling websites and extracting text content with embeddings.
    
    Usage:
        scrapy crawl nexora001 -a start_url=https://example.com -a max_depth=2
    """
    
    name = "nexora001"
    
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 1.0,
        'COOKIES_ENABLED': False,
        'TELNETCONSOLE_ENABLED': False,
        'LOG_LEVEL': 'INFO',
    }
    
    def __init__(
        self,
        start_url: str = None,
        max_depth: int = 2,
        follow_links: bool = True,
        enable_embeddings: bool = True,
        chunk_size: int = 500,
        *args,
        **kwargs
    ):
        """
        Initialize the spider.
        
        Args:
            start_url: The URL to start crawling from
            max_depth: Maximum crawl depth (default: 2)
            follow_links: Whether to follow internal links (default: True)
            enable_embeddings: Whether to generate embeddings (default: True)
            chunk_size: Size of text chunks (default: 500)
        """
        super().__init__(*args, **kwargs)
        
        if not start_url:
            raise ValueError("start_url is required")
        
        self.start_urls = [start_url]
        self.max_depth = int(max_depth)
        self.follow_links = follow_links in [True, 'True', 'true', '1']
        self.enable_embeddings = enable_embeddings in [True, 'True', 'true', '1']
        self.chunk_size = int(chunk_size)
        self.allowed_domains = [urlparse(start_url).netloc]
        
        # Statistics
        self.pages_crawled = 0
        self. documents_created = 0
        self.chunks_created = 0
        
        # Initialize components
        self.storage = MongoDBStorage()
        self.chunker = TextChunker(chunk_size=self.chunk_size, chunk_overlap=50)
        
        # Initialize embedding generator if enabled
        self.embedding_generator = None
        if self.enable_embeddings:
            try:
                self.logger.info("Initializing embedding generator...")
                self.embedding_generator = EmbeddingGenerator(
                    provider=EmbeddingProvider.SENTENCE_TRANSFORMERS
                )
                self.logger.info(f"✓ Embeddings enabled (dimension: {self.embedding_generator.get_dimension()})")
            except Exception as e:
                self.logger.warning(f"Failed to initialize embeddings: {e}")
                self. logger.warning("Continuing without embeddings...")
                self.enable_embeddings = False
        
        self.logger.info(f"Spider initialized:")
        self.logger.info(f"  Start URL: {start_url}")
        self.logger.info(f"  Max depth: {self.max_depth}")
        self.logger.info(f"  Follow links: {self.follow_links}")
        self.logger. info(f"  Embeddings: {self.enable_embeddings}")
        self.logger.info(f"  Chunk size: {self.chunk_size}")
    
    def parse(self, response: Response, depth: int = 0) -> Generator:
        """
        Parse a web page and extract content. 
        
        Args:
            response: Scrapy response object
            depth: Current crawl depth
        """
        self.logger.info(f"Crawling [{depth}/{self.max_depth}]: {response.url}")
        
        # Check if already crawled
        if self.storage.url_exists(response.url):
            self.logger.info(f"  Skipping (already crawled): {response.url}")
            return
        
        # Extract text content
        content = self._extract_text(response)
        
        if not content or len(content. strip()) < 100:
            self.logger.warning(f"  Little/no content found: {response.url}")
            return
        
        # Extract title
        title = self._extract_title(response)
        
        self.logger.info(f"  Title: {title}")
        self.logger.info(f"  Content length: {len(content)} chars")
        
        # Chunk the content
        chunks = self. chunker.chunk_text(
            content,
            metadata={
                "source_url": response.url,
                "title": title
            }
        )
        
        self.logger.info(f"  Created {len(chunks)} chunks")
        
        # Process and store chunks
        stored_count = 0
        for chunk in chunks:
            try:
                chunk_text = chunk['text']
                chunk_index = chunk['chunk_index']
                total_chunks = chunk['total_chunks']
                
                # Generate embedding if enabled
                embedding = None
                if self.enable_embeddings and self.embedding_generator:
                    try:
                        embedding = self. embedding_generator.generate_embedding(chunk_text)
                    except Exception as e:
                        self.logger.warning(f"  Failed to generate embedding for chunk {chunk_index}: {e}")
                
                # Store in MongoDB
                if embedding:
                    doc_id = self.storage.store_document_with_embedding(
                        content=chunk_text,
                        embedding=embedding,
                        source_url=response.url,
                        source_type="web",
                        title=title,
                        chunk_index=chunk_index,
                        total_chunks=total_chunks,
                        metadata={
                            "depth": depth,
                            "chunk_char_count": chunk['char_count']
                        }
                    )
                else:
                    doc_id = self.storage.store_document(
                        content=chunk_text,
                        source_url=response.url,
                        source_type="web",
                        title=title,
                        metadata={
                            "depth": depth,
                            "chunk_index": chunk_index,
                            "total_chunks": total_chunks,
                            "chunk_char_count": chunk['char_count']
                        }
                    )
                
                stored_count += 1
                self.chunks_created += 1
                
            except Exception as e:
                self.logger.error(f"  ✗ Failed to store chunk {chunk_index}: {e}")
                continue
        
        self.pages_crawled += 1
        self.documents_created += stored_count
        
        self. logger.info(f"  ✓ Stored {stored_count} chunks")
        
        # Follow links if enabled and depth allows
        if self.follow_links and depth < self.max_depth:
            links = response.css('a::attr(href)'). getall()
            internal_links = [
                urljoin(response.url, link)
                for link in links
                if self._is_internal_link(link, response.url)
            ]
            
            self.logger.info(f"  Found {len(internal_links)} internal links")
            
            for link in internal_links[:10]:  # Limit to 10 links per page
                yield scrapy.Request(
                    link,
                    callback=self. parse,
                    cb_kwargs={'depth': depth + 1},
                    dont_filter=False
                )
    
    def _extract_text(self, response: Response) -> str:
        """
        Extract clean text from HTML.
        
        Args:
            response: Scrapy response
            
        Returns:
            Extracted text content
        """
        # Remove script and style elements
        for element in response.css('script, style, nav, header, footer'):
            element.root.drop_tree()
        
        # Extract text from main content areas
        text_parts = []
        
        # Try to find main content area
        main_selectors = [
            'main ::text',
            'article ::text',
            '. content ::text',
            '#content ::text',
            'body ::text'
        ]
        
        for selector in main_selectors:
            texts = response.css(selector).getall()
            if texts:
                text_parts = texts
                break
        
        # Clean and join text
        cleaned_text = ' '.join(
            text.strip()
            for text in text_parts
            if text. strip()
        )
        
        return cleaned_text
    
    def _extract_title(self, response: Response) -> str:
        """Extract page title."""
        # Try different title sources
        title = (
            response.css('title::text').get() or
            response.css('h1::text').get() or
            response.css('meta[property="og:title"]::attr(content)').get() or
            response.url
        )
        
        return title. strip() if title else response.url
    
    def _is_internal_link(self, link: str, base_url: str) -> bool:
        """
        Check if a link is internal (same domain).
        
        Args:
            link: The link to check
            base_url: The base URL
            
        Returns:
            True if link is internal
        """
        if not link or link.startswith('#') or link.startswith('javascript:'):
            return False
        
        # Make absolute
        absolute_link = urljoin(base_url, link)
        link_domain = urlparse(absolute_link). netloc
        base_domain = urlparse(base_url).netloc
        
        return link_domain == base_domain
    
    def closed(self, reason):
        """Called when spider closes."""
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Spider finished: {reason}")
        self.logger.info(f"Pages crawled: {self.pages_crawled}")
        self.logger.info(f"Chunks created: {self.chunks_created}")
        self.logger.info(f"Documents stored: {self.documents_created}")
        self.logger.info(f"{'='*60}\n")
        
        self.storage.close()