"""
GitHub Tool
Integrates with GitHub API to search repositories and fetch information
"""

import requests
import os
from typing import Dict, Any, Optional
from .base_tool import BaseTool


class GitHubTool(BaseTool):
    """GitHub API integration tool"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    @property
    def name(self) -> str:
        return "github_search"
    
    @property
    def description(self) -> str:
        return "Search GitHub repositories, get repository details, stars, descriptions, and owner information. Use this for finding open-source projects, checking repository popularity, or getting project information."
    
    def execute(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Search GitHub repositories
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            Dict with success status and repository data
        """
        try:
            # Search repositories
            search_url = f"{self.base_url}/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": max_results
            }
            
            response = requests.get(
                search_url, 
                headers=self.headers, 
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                repositories = []
                
                for repo in data.get("items", [])[:max_results]:
                    repositories.append({
                        "name": repo.get("name"),
                        "full_name": repo.get("full_name"),
                        "description": repo.get("description", "No description"),
                        "stars": repo.get("stargazers_count", 0),
                        "forks": repo.get("forks_count", 0),
                        "language": repo.get("language", "Unknown"),
                        "url": repo.get("html_url"),
                        "owner": repo.get("owner", {}).get("login")
                    })
                
                return {
                    "success": True,
                    "data": {
                        "total_count": data.get("total_count", 0),
                        "repositories": repositories
                    }
                }
            
            elif response.status_code == 403:
                return {
                    "success": False,
                    "error": "GitHub API rate limit exceeded. Add GITHUB_TOKEN for higher limits.",
                    "data": None
                }
            
            else:
                return {
                    "success": False,
                    "error": f"GitHub API error: {response.status_code}",
                    "data": None
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "GitHub API request timed out",
                "data": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"GitHub tool error: {str(e)}",
                "data": None
            }
