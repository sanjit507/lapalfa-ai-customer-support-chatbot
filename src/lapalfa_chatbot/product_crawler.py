import requests
from typing import List, Dict
import json
from pathlib import Path


BASE_URL = "https://www.lapalfa.com"


def get_products() -> List[Dict]:

    url = f"{BASE_URL}/products.json?limit=250"

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    products = []

    for product in data.get("products", []):

        variants = product.get("variants", [])

        product_data = {
            "id": product.get("id"),
            "title": product.get("title"),
            "handle": product.get("handle"),
            "vendor": product.get("vendor"),
            "product_type": product.get("product_type"),

            "url": (
                f"{BASE_URL}/products/"
                f"{product.get('handle')}"
            ),

            "images": [
                image.get("src")
                for image in product.get("images", [])
                if image.get("src")
            ],

            "variants": []
        }

        for variant in variants:

            product_data["variants"].append({
                "id": variant.get("id"),
                "title": variant.get("title"),
                "sku": variant.get("sku"),
                "price": variant.get("price"),
                "available": variant.get("available"),
            })

        products.append(product_data)

    return products


if __name__ == "__main__":

    products = get_products()

    print(f"Products found: {len(products)}")

    for product in products[:5]:

        print("\n" + "=" * 60)

        print("TITLE:", product["title"])
        print("VENDOR:", product["vendor"])
        print("TYPE:", product["product_type"])
        print("URL:", product["url"])

        for variant in product["variants"]:

            print("SKU:", variant["sku"])
            print("PRICE:", variant["price"])
            print("AVAILABLE:", variant["available"])

if __name__ == "__main__":

    products = get_products()

    print(f"Products found: {len(products)}")

    # Create products directory
    output_dir = Path("data/products")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save products
    output_file = output_dir / "products.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            products,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Products saved to: {output_file}")

    # Show first 5 products
    for product in products[:5]:

        print("\n" + "=" * 60)

        print("TITLE:", product["title"])
        print("VENDOR:", product["vendor"])
        print("TYPE:", product["product_type"])
        print("URL:", product["url"])

        for variant in product["variants"]:

            print("SKU:", variant["sku"])
            print("PRICE:", variant["price"])
            print("AVAILABLE:", variant["available"])            