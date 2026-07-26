import argparse
import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mdcomputers.in/"
SEARCH_URL = BASE_URL + "?route=product/search&search={query}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}


def extract_text(node):
    return node.get_text(" ", strip=True) if node else ""


def parse_product(card):
    name_tag = card.select_one(".caption h4 a") or card.select_one("h4 a")
    current_price_tag = card.select_one(".price")
    special_tag = card.select_one(".price-new")
    old_tag = card.select_one(".price-old")
    image_tag = card.select_one("img")
    shipping_tag = None

    badges = [extract_text(x) for x in card.select(".label, .badge, .product-label")]
    meta_parts = [extract_text(x) for x in card.select(".caption p")]

    current_price = ""
    old_price = ""
    if special_tag:
        current_price = extract_text(special_tag)
        old_price = extract_text(old_tag)
    elif current_price_tag:
        price_text = extract_text(current_price_tag)
        lines = [part.strip() for part in price_text.split("₹") if part.strip()]
        if len(lines) >= 2:
            old_price = "₹" + lines[0]
            current_price = "₹" + lines[-1]
        elif len(lines) == 1:
            current_price = "₹" + lines[0]
        else:
            current_price = price_text

    link = urljoin(BASE_URL, name_tag.get("href", "")) if name_tag else ""
    image = urljoin(BASE_URL, image_tag.get("src", "")) if image_tag else ""

    return {
        "name": extract_text(name_tag),
        "product_url": link,
        "current_price": current_price,
        "old_price": old_price,
        "shipping_or_stock": shipping_tag or (badges[0] if badges else ""),
        "extra_info": " | ".join([part for part in meta_parts if part]),
        "image_url": image,
    }


def scrape_search(search_term, delay=1.0, max_pages=1):
    session = requests.Session()
    session.headers.update(HEADERS)
    results = []

    for page in range(1, max_pages + 1):
        params = {
            "route": "product/search",
            "search": search_term,
            "page": page,
        }
        response = session.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select(".product-layout") or soup.select(".product-grid")

        if not cards:
            break

        page_items = [parse_product(card) for card in cards]
        page_items = [item for item in page_items if item["name"]]
        if not page_items:
            break

        results.extend(page_items)
        time.sleep(delay)

    return results


def save_csv(rows, output_file):
    fieldnames = [
        "name",
        "product_url",
        "current_price",
        "old_price",
        "shipping_or_stock",
        "extra_info",
        "image_url",
    ]
    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Scrape MDComputers product search results")
    parser.add_argument("search_term", help="Search term, e.g. 'external hard drive'")
    parser.add_argument("-o", "--output", default="mdcomputers_products.csv", help="Output CSV filename")
    parser.add_argument("--pages", type=int, default=1, help="Number of search result pages to scrape")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests in seconds")
    args = parser.parse_args()

    rows = scrape_search(args.search_term, delay=args.delay, max_pages=args.pages)
    save_csv(rows, args.output)
    print(f"Saved {len(rows)} products to {args.output}")


if __name__ == "__main__":
    main()
