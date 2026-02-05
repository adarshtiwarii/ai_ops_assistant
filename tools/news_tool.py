"""
News Tool
Integrates with NewsAPI to fetch latest news articles
"""

import requests
import os
from typing import Dict, Any, Optional
from .base_tool import BaseTool


class NewsTool(BaseTool):
    """NewsAPI integration tool"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/top-headlines"
    
    @property
    def name(self) -> str:
        return "news_fetch"
    
    @property
    def description(self) -> str:
        return "Fetch latest news headlines on any topic or from any country. Returns news articles with titles, descriptions, sources, and URLs. Use this for current events, news, or trending topics."
    
    def execute(self, query: Optional[str] = None, country: str = "us", max_results: int = 5) -> Dict[str, Any]:
        """
        Fetch latest news articles
        
        Args:
            query: Search query (optional)
            country: Country code (us, gb, in, etc.)
            max_results: Maximum number of articles
            
        Returns:
            Dict with success status and news data
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "NEWS_API_KEY not configured. Get free API key from https://newsapi.org",
                "data": None
            }
        
        try:
            params = {
                "apiKey": self.api_key,
                "pageSize": max_results
            }
            
            if query:
                params["q"] = query
            else:
                params["country"] = country
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                
                for article in data.get("articles", [])[:max_results]:
                    articles.append({
                        "title": article.get("title"),
                        "description": article.get("description", "No description"),
                        "source": article.get("source", {}).get("name", "Unknown"),
                        "author": article.get("author", "Unknown"),
                        "url": article.get("url"),
                        "published_at": article.get("publishedAt")
                    })
                
                return {
                    "success": True,
                    "data": {
                        "total_results": data.get("totalResults", 0),
                        "articles": articles
                    }
                }
            
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Invalid NewsAPI key",
                    "data": None
                }
            
            elif response.status_code == 426:
                return {
                    "success": False,
                    "error": "NewsAPI upgrade required (free tier limitations)",
                    "data": None
                }
            
            else:
                return {
                    "success": False,
                    "error": f"News API error: {response.status_code}",
                    "data": None
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "News API request timed out",
                "data": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"News tool error: {str(e)}",
                "data": None
            }
