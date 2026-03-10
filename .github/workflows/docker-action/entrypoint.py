#!/usr/bin/env python3
import hashlib
import os
import requests

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
        + requests.compat.urlencode(query)
    )

    print(f"{lookup_url}")

    # headers = {
    #     "Authorization": f"Bearer {token}",
    #     "Accept": "application/json;api-version=6.0-preview.1",
    # }

    # try:
    #     response = requests.get(lookup_url, headers=headers)
    #     response.raise_for_status()
    #     payload = response.json()
    # except requests.exceptions.HTTPError as e:
    #     if e.response.status_code in (204, 404):
    #         print("No cache found.")
    #         return False
    #     raise

if __name__ == "__main__":
    main()

# def restore_github_actions_cache(
#     key: str,
#     path: str,
#     restore_keys: list[str] | None = None,
#     version: str | None = None,
# ) -> bool:
#     """
#     Restore a GitHub Actions cache archive (similar to actions/cache/restore).

#     Returns True if a cache was found and extracted, False otherwise.

#     Notes:
#     - This only works inside a GitHub Actions runner.
#     - It relies on ACTIONS_RUNTIME_TOKEN and ACTIONS_CACHE_URL.
#     """
#     restore_keys = restore_keys or []

#     token = os.getenv("ACTIONS_RUNTIME_TOKEN")
#     cache_url = os.getenv("ACTIONS_CACHE_URL")
#     if not token or not cache_url:
#         raise RuntimeError(
#             "Missing ACTIONS_RUNTIME_TOKEN or ACTIONS_CACHE_URL. "
#             "This function must run inside a GitHub Actions job."
#         )

#     keys = ",".join([key] + restore_keys)
#     query = {"keys": keys}
#     if version:
#         query["version"] = version

#     # GitHub cache service lookup endpoint used by actions/cache.
#     lookup_url = (
#         cache_url.rstrip("/")
#         + "/_apis/artifactcache/cache?"
#         + urllib.parse.urlencode(query)
#     )

#     req = urllib.request.Request(
#         lookup_url,
#         headers={
#             "Authorization": f"Bearer {token}",
#             "Accept": "application/json;api-version=6.0-preview.1",
#         },
#         method="GET",
#     )

#     try:
#         with urllib.request.urlopen(req) as resp:
#             payload = json.loads(resp.read().decode("utf-8"))
#     except urllib.error.HTTPError as e:
#         if e.code in (204, 404):
#             return False
#         raise

#     archive_url = payload.get("archiveLocation") or payload.get("archive_location")
#     if not archive_url:
#         return False

#     os.makedirs(path, exist_ok=True)

#     with tempfile.TemporaryDirectory() as tmp:
#         archive_file = os.path.join(tmp, "cache.tzst")
#         with urllib.request.urlopen(
#             urllib.request.Request(
#                 archive_url,
#                 headers={"Authorization": f"Bearer {token}"},
#                 method="GET",
#             )
#         ) as src, open(archive_file, "wb") as dst:
#             shutil.copyfileobj(src, dst)

#         # Most GitHub cache archives are tar+zstd.
#         subprocess.run(
#             ["tar", "--zstd", "-xf", archive_file, "-C", path],
#             check=True,
#         )

#     return True

# hit = restore_github_actions_cache(
#     key=os.environ["GITHUB_WORKFLOW"], 
#     path="./data/example.db",           
# )
# print(f"cache hit: {hit}")