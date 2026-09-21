import json
import re
from pathlib import Path
from typing import List, Dict


# =========================================================
# Product file
# =========================================================

PRODUCT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "products"
    / "products.json"
)


# =========================================================
# Load products
# =========================================================

def load_products() -> List[Dict]:

    if not PRODUCT_FILE.exists():
        raise FileNotFoundError(
            f"Product file not found: {PRODUCT_FILE}"
        )

    with open(
        PRODUCT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# =========================================================
# Normalize text
# =========================================================

def normalize_text(text: str) -> str:

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s.-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# Search products
# =========================================================

def search_products(
    query: str,
    limit: int = 5
) -> List[Dict]:

    products = load_products()

    query_text = normalize_text(query)

    STOP_WORDS = {
        "a", "an", "the", "and", "or", "but", "is", "are", "am", "was", "were", 
        "do", "does", "did", "have", "has", "had", "for", "with", "about", 
        "to", "of", "in", "on", "at", "by", "from", "up", "down", "out",
        "it", "this", "that", "these", "those", "my", "your", "his", "her", "its", "our", "their",
        "i", "you", "he", "she", "we", "they", "me", "him", "us", "them",
        "can", "could", "shall", "should", "will", "would", "may", "might", "must",
        "need", "want", "find", "get", "looking", "search", "please", "plz", "pls",
        "any", "some", "all", "there", "here", "where", "when", "how", "what", "which",
        "who", "whom", "whose", "why", "whether", "if", "then", "else", "not", "no", "yes",
        "ok", "okay", "thanks", "thank", "hello", "hi", "hey",
        # Keep laptop out of query words if possible to prevent excessive matching
        "laptop", "computer", "pc", "device", "machine"
    }

    query_words = set(query_text.split()) - STOP_WORDS

    results = []

    for product in products:

        title = normalize_text(
            product.get("title", "")
        )

        brand = normalize_text(
            product.get("brand", "")
        )

        category = normalize_text(
            product.get("category", "")
        )

        sku = normalize_text(
            product.get("sku", "")
        )

        tags = normalize_text(
            " ".join(
                product.get("tags", [])
            )
        )

        description = normalize_text(
            product.get("description", "")
        )

        # Everything that can be searched
        searchable_text = " ".join([
            title,
            brand,
            category,
            sku,
            tags,
            description
        ])

        searchable_words = set(
            searchable_text.split()
        )

        # -------------------------------------------------
        # Score
        # -------------------------------------------------

        score = 0

        # Exact title match
        if query_text in title:
            score += 100

        # Exact SKU match
        if query_text in sku:
            score += 90

        # Exact category match
        if query_text in category:
            score += 80

        # Exact brand match
        if query_text == brand:
            score += 70

        # Word matching
        matching_words = (
            query_words & searchable_words
        )

        score += len(matching_words) * 10

        if score < 30:
            continue

        result = {
            "id": product.get("id"),
            "sku": product.get("sku"),
            "title": product.get("title"),
            "brand": product.get("brand"),
            "category": product.get("category"),
            "price": product.get("price"),
            "comparePrice": product.get("comparePrice"),
            "imageUrl": product.get("imageUrl"),
            "productUrl": product.get("productUrl"),
            "tags": product.get("tags", []),
            "description": product.get("description"),
            "inStock": product.get("inStock", False),
            "_score": score
        }

        results.append(result)

    # Highest score first
    results.sort(
        key=lambda product: product["_score"],
        reverse=True
    )

    return results[:limit]


# =========================================================
# Test
# =========================================================

if __name__ == "__main__":

    print("Loading products from:")
    print(PRODUCT_FILE)

    products = load_products()

    print(
        f"Total products: {len(products)}"
    )

    query = input(
        "\nSearch product: "
    )

    results = search_products(
        query
    )

    print(
        f"\nFound {len(results)} matching products."
    )

    for product in results:

        print(
            "\n" + "=" * 70
        )

        print(
            "SCORE:",
            product["_score"]
        )

        print(
            "TITLE:",
            product["title"]
        )

        print(
            "BRAND:",
            product["brand"]
        )

        print(
            "CATEGORY:",
            product["category"]
        )

        print(
            "SKU:",
            product["sku"]
        )

        print(
            "PRICE:",
            f"₹{product['price']}"
        )

        print(
            "COMPARE PRICE:",
            f"₹{product['comparePrice']}"
        )

        print(
            "AVAILABLE:",
            product["inStock"]
        )

        print(
            "PRODUCT URL:",
            product["productUrl"]
        )

        print(
            "IMAGE URL:",
            product["imageUrl"]
        )