import re
import urllib.request
from typing import Dict, Any
from .text_parser import parse_text

def scrape_url(url: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Fetches web content from a URL and extracts clean article text.
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) VeriMorph-Bot/1.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            html = response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return {
            "title": f"Failed URL: {url}",
            "content": f"Failed to fetch content from {url}: {str(e)}",
            "chunks": [],
            "total_words": 0,
            "total_chunks": 0,
            "source_url": url,
            "error": str(e)
        }

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Scraped Article"

    # Strip script and style tags
    clean_html = re.sub(r'<(script|style|noscript|header|footer|nav)[^>]*>.*?</\1>', '', html, flags=re.IGNORECASE | re.DOTALL)
    
    # Extract paragraphs and headers
    paragraphs = re.findall(r'<(?:p|h[1-6]|li)[^>]*>(.*?)</(?:p|h[1-6]|li)>', clean_html, flags=re.IGNORECASE | re.DOTALL)
    
    extracted_lines = []
    for p in paragraphs:
        # Strip all tags
        text = re.sub(r'<[^>]+>', ' ', p)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text.split()) > 4: # Filter navigation crumbs
            extracted_lines.append(text)

    full_text = "\n\n".join(extracted_lines)
    if not full_text:
        # Fallback raw tag stripping
        full_text = re.sub(r'<[^>]+>', ' ', clean_html)
        full_text = re.sub(r'\s+', ' ', full_text).strip()

    parsed = parse_text(full_text)
    parsed["title"] = title
    parsed["source_url"] = url
    return parsed
