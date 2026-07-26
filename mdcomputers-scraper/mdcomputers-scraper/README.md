# MDComputers Product Scraper

A Python scraper for collecting product details from MDComputers search results for a given search term.

## What it collects
- Product name
- Product URL
- Current price
- Old price (if shown)
- Shipping / stock / badge text when available
- Extra product info shown in the card
- Image URL

## Example target
Search URL pattern:
`https://mdcomputers.in/?route=product/search&search=external+hard+drive`

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```bash
python scraper.py "external hard drive" -o external_hdd.csv --pages 2 --delay 1.5
```

## Output
The script saves the extracted product data to a CSV file.

## Notes
- Keep request volume low and use a delay between requests.
- The website markup may change, so selectors may need adjustment later.
- This script is designed for search result pages, not full category crawling.

## AI usage note
AI was used to speed up the initial scraper structure and README drafting. After that, the parsing logic, CSV schema, CLI arguments, request behavior, and final project packaging were reviewed and adjusted so the result is practical and submission-ready rather than a raw first-pass output.
