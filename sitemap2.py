import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3

# Ignore les avertissements SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URLS = [
    "https://openpaye.co/docs/console-de-notifications-dsn",
    "https://openpaye.co/docs/regularisation-dsn",
    "https://openpaye.co/docs/declarations-sociales"
]

def get_article_links(url):
    try:
        response = requests.get(url, verify=False)  # <--- ici on ignore le certificat
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        links = soup.select("a[href^='/docs/']")
        return [
            "https://openpaye.co" + a["href"]
            for a in links
            if a["href"].startswith("/docs/")
        ]
    except Exception as e:
        print(f"Erreur sur {url}: {e}")
        return []

def generate_sitemap(urls):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url in sorted(set(urls)):
        sitemap.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{now}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")
    sitemap.append('</urlset>')
    return "\n".join(sitemap)

def main():
    all_urls = []
    for base_url in BASE_URLS:
        links = get_article_links(base_url)
        all_urls.extend(links)

    if len(all_urls) < 30:
        print(f"Erreur : seulement {len(all_urls)} URLs détectées.")
        return

    sitemap_content = generate_sitemap(all_urls)
    with open("sitemap-docs.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    print("✅ Sitemap généré avec succès.")

if __name__ == "__main__":
    main()
