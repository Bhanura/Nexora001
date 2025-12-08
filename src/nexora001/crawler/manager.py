"""
Crawler manager for running Scrapy spiders programmatically. 
"""

import sys
from pathlib import Path
from typing import Optional
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent. parent. parent))

from nexora001. crawler.spider import Nexora001Spider
from nexora001.crawler import settings as crawler_settings


class CrawlerManager:
    """Manages web crawling operations."""
    
    def __init__(self):
        """Initialize the crawler manager."""
        self.process: Optional[CrawlerProcess] = None
    
    def crawl_url(
        self,
        url: str,
        max_depth: int = 2,
        follow_links: bool = True,
        use_playwright: bool = False  # NEW PARAMETER
    ) -> dict:
        """
        Crawl a URL and store content in MongoDB.
        
        Args:
            url: The URL to crawl
            max_depth: Maximum crawl depth
            follow_links: Whether to follow internal links
            use_playwright: Whether to use Playwright for JavaScript rendering
            
        Returns:
            Dictionary with crawl statistics
        """
        # Create crawler settings
        settings = {
            'ROBOTSTXT_OBEY': crawler_settings. ROBOTSTXT_OBEY,
            'CONCURRENT_REQUESTS': crawler_settings.CONCURRENT_REQUESTS,
            'DOWNLOAD_DELAY': crawler_settings. DOWNLOAD_DELAY,
            'COOKIES_ENABLED': crawler_settings.COOKIES_ENABLED,
            'TELNETCONSOLE_ENABLED': crawler_settings.TELNETCONSOLE_ENABLED,
            'DEFAULT_REQUEST_HEADERS': crawler_settings.DEFAULT_REQUEST_HEADERS,
            'HTTPCACHE_ENABLED': crawler_settings. HTTPCACHE_ENABLED,
            'HTTPCACHE_DIR': crawler_settings.HTTPCACHE_DIR,
            'LOG_LEVEL': 'INFO',
        }
        
        # Add Playwright settings if enabled
        if use_playwright:
            settings['DOWNLOAD_HANDLERS'] = crawler_settings.DOWNLOAD_HANDLERS
            settings['PLAYWRIGHT_BROWSER_TYPE'] = crawler_settings.PLAYWRIGHT_BROWSER_TYPE
            settings['PLAYWRIGHT_LAUNCH_OPTIONS'] = crawler_settings.PLAYWRIGHT_LAUNCH_OPTIONS
            settings['TWISTED_REACTOR'] = crawler_settings. TWISTED_REACTOR
        
        # Create process
        self.process = CrawlerProcess(settings)
        
        # Add spider
        self.process.crawl(
            Nexora001Spider,
            start_url=url,
            max_depth=max_depth,
            follow_links=follow_links,
            use_playwright=use_playwright  # PASS NEW PARAMETER
        )
        
        # Start crawling (blocking)
        self.process.start()
        
        return {
            "status": "completed",
            "url": url,
            "max_depth": max_depth,
            "playwright_enabled": use_playwright  # ADDED TO RESPONSE
        }


def crawl_website(
    url: str,
    max_depth: int = 2,
    follow_links: bool = True,
    use_playwright: bool = False  # NEW PARAMETER
):
    """
    Convenience function to crawl a website. 
    
    Args:
        url: URL to crawl
        max_depth: Maximum depth
        follow_links: Whether to follow links
        use_playwright: Whether to use Playwright for JavaScript rendering
        
    Returns:
        Dictionary with crawl statistics
    """
    manager = CrawlerManager()
    return manager.crawl_url(url, max_depth, follow_links, use_playwright)