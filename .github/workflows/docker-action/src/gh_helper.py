
import os
import requests

class GitHub_Helper:

    def __init__(self, token: str, org: str = None, repo: str = None):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }
        self.org = org
        self.repo = repo
    
    def get_cache(self, key: str = None):
        if not self.org or not self.repo:
            raise ValueError("Organization and repository must be specified.")
        
        url = f"{self.base_url}/repos/{self.org}/{self.repo}/actions/caches"
        response = requests.get(url, headers=self.headers)

        print(response.json())
        for cache in response.json().get("actions_caches", []):
            if cache["key"].lower() == key.lower():
                return cache

