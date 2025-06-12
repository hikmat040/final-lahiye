import requests
from datetime import datetime
import time

# GitHub Personal Access Token (istəyə bağlıdır, amma tövsiyə olunur)
GITHUB_TOKEN = ""

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.text-match+json"
}

# Axtarış üçün açar sözlər – bunları istəyə uyğun artıra bilərsən
SEARCH_TERMS = [
    "vulnerable CMS", "old version CMS", "site.php", "config.php password",
    "wp-config.php", "admin login", "php mysql_connect", "Drupal 7.0", "Joomla 1.5",
    "eval(base64_decode(", "str_rot13(gzinflate(base64_decode("
]

# GitHub API URL
GITHUB_SEARCH_URL = "https://api.github.com/search/code"

# Axtarış funksiyası
def search_github_code(query, max_pages=3):
    results = []
    for page in range(1, max_pages + 1):
        params = {
            "q": query,
            "per_page": 10,
            "page": page
        }

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Searching page {page} for '{query}'...")

        response = requests.get(GITHUB_SEARCH_URL, headers=HEADERS, params=params)

        if response.status_code == 200:
            items = response.json().get("items", [])
            for item in items:
                result = {
                    "name": item.get("name"),
                    "repo": item.get("repository", {}).get("full_name"),
                    "html_url": item.get("html_url")
                }
                results.append(result)
        else:
            print(f"[-] Error: {response.status_code} — {response.text}")
            break

        time.sleep(2)  # Rate limit-ə düşməmək üçün

    return results

# Əsas funksiya
def main():
    all_results = []

    for term in SEARCH_TERMS:
        results = search_github_code(term)
        if results:
            print(f"[+] {len(results)} result(s) found for '{term}'")
            all_results.extend(results)
        else:
            print(f"[!] No results for '{term}'")

    print("\n-- Toplam nəticələr --")
    for r in all_results:
        print(f"[{r['repo']}] - {r['name']} → {r['html_url']}")

if __name__ == "__main__":
    main()

