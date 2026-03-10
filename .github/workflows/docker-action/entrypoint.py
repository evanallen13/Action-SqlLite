#!/usr/bin/env python3
import hashlib
import os
import urllib.request
import urllib.parse
import urllib.error
import json

def main(): 
    token = os.getenv("ACTIONS_RUNTIME_TOKEN")
    cache_url = os.getenv("ACTIONS_CACHE_URL")
    key = os.getenv("INPUT_KEY", "DefaultKey")
    path = os.getenv("CACHE_PATH", "./data")
    print(f"ACTIONS_CACHE_URL: {cache_url}")
    print(f"Key: {key}")
    if not token or not cache_url or not key:
        raise RuntimeError(
            "Missing ACTIONS_RUNTIME_TOKEN or ACTIONS_CACHE_URL or key. "
            "This function must run inside a GitHub Actions job."
        )
    
    restore_keys = []
    version = hashlib.sha256(key.encode()).hexdigest()
    keys = ",".join([key] + restore_keys)
    query = {"keys": keys}
    if version:
        query["version"] = version

    lookup_url = (
        cache_url.rstrip("/")
        + "/_apis/artifactcache/cache?"
        + urllib.parse.urlencode(query)
    )

    req = urllib.request.Request(
        lookup_url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json;api-version=6.0-preview.1",
        },
        method="GET",
    )

    print("Requesting cache lookup...")

    print("Response --------------------")
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read()
            print(body)
            payload = json.loads(body.decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code in (204, 400, 404):
            print(f"Cache not found (HTTP {e.code})")
            return False
        raise

    archive_url = payload.get("archiveLocation") or payload.get("archive_location")
    print(f"Archive URL: {archive_url}")
    if not archive_url:
        return False

    os.makedirs(path, exist_ok=True)

if __name__ == "__main__":
    main()

