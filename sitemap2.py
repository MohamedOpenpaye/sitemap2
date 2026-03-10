import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin
import sys

BASE_URLS = [
    "https://openpaye.co/docs/console-de-notifications-dsn",
    "https://openpaye.co/docs/regularisation-dsn",
    "https://openpaye.co/docs/declarations-sociales",
]

HEADERS = {
    "User-Agent": "Openpaye Sitemap Generator/1.0"
}

def get_article_links(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        found = set()

        for a in soup.select("a[href]"):
            href = a.get("href", "").strip()
            if href.startswith("/docs/"):
                found.add(urljoin("https://openpaye.co", href))
            elif href.startswith("https://openpaye.co/docs/"):
                found.add(href)

        return sorted(found)

    except Exception as e:
        print(f"Erreur sur {url}: {e}")
        return []

def generate_sitemap(urls):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url in sorted(set(urls)):
        sitemap.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{now}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    sitemap.append("</urlset>")
    return "\n".join(sitemap)

def main():
    all_urls = set(BASE_URLS)

    for base_url in BASE_URLS:
        links = get_article_links(base_url)
        print(f"{base_url} -> {len(links)} liens détectés")
        all_urls.update(links)

    print(f"Total URLs uniques détectées : {len(all_urls)}")

    if len(all_urls) == 0:
        print("Erreur : aucune URL détectée, sitemap non généré.")
        sys.exit(1)

    sitemap_content = generate_sitemap(all_urls)

    output_file = "sitemap-docs.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    print(f"✅ Sitemap généré avec succès : {output_file}")

if __name__ == "__main__":
    main()
