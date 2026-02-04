import requests
import json

def search_series(keyword):
    url = f"https://www.bankofcanada.ca/valet/api/v1/series/search"
    params = {"q": keyword}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def main():
    keywords = ["prime", "corra", "bond"]
    for kw in keywords:
        print(f"Searching series for keyword: {kw}")
        results = search_series(kw)
        for series in results.get('series', [])[:5]:
            print(f"Series ID: {series['id']}, Description: {series['description']}")
        print()

if __name__ == "__main__":
    main()
