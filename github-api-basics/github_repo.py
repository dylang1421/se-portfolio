import requests  # third-party library that makes HTTP requests simple

BASE_URL = "https://api.github.com"
OWNER = "dylang1421"
REPO = "se-portfolio"  # this repo doesn't exist, so you'll see an error message

# --- Part 1: the same call you made with curl: GET /repos/{owner}/{repo} ---
response = requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO}")

print("Status:", response.status_code)
print("Requests left this hour:", response.headers["x-ratelimit-remaining"])

if response.status_code == 200:
    repo = response.json()
    print(f"\n{repo['full_name']}")
    print(f"  Description: {repo['description']}")
    print(f"  Language:    {repo['language']}")
    print(f"  Topics:      {', '.join(repo['topics'])}")
    print(f"  Created:     {repo['created_at']}")
else:
    # .get() returns None instead of raising a KeyError if the key is missing
    print("Request failed:", response.status_code, response.json().get("message"))

# --- Part 2: a list endpoint with query parameters, plus error handling ---
# Pass params as a dictionary; requests builds the ?sort=...&per_page=... for you
params = {"sort": "updated", "per_page": 5}
response = requests.get(f"{BASE_URL}/users/{OWNER}/repos", params=params)

print("\nMost recently updated repos:")
if response.status_code == 200:
    for r in response.json():  # the body is a list of dicts, just like your deals.csv
        print(f"  - {r['name']} ({r['language']}), updated {r['updated_at'][:10]}")
else:
    print("Request failed:", response.status_code, response.json().get("message"))