import json
import re
from pathlib import Path


PRODUCT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "products"
    / "products.json"
)


def load_products():
    with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(text):
    """Normalize text for searching."""

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(r"[^a-z0-9]+", " ", text)

    return " ".join(text.split())


def field_to_text(value):
    """
    Convert list/string fields into searchable text.
    """

    if isinstance(value, list):
        return " ".join(str(item) for item in value)

    return str(value or "")


def search_products(query: str, limit: int = 5):

    products = load_products()

    query_normalized = normalize(query)

    results = []

    for product in products:

        name = normalize(product.get("name", ""))

        brand = normalize(product.get("brand", ""))

        category = normalize(product.get("category", ""))

        part_numbers = normalize(
            field_to_text(product.get("part_numbers"))
        )

        compatible_models = normalize(
            field_to_text(product.get("compatible_models"))
        )

        searchable_text = " ".join([
            name,
            brand,
            category,
            part_numbers,
            compatible_models,
        ])

        score = 0

        # --------------------------------
        # Exact product name
        # --------------------------------

        if query_normalized == name:
            score += 100


        # --------------------------------
        # Query appears in product name
        # --------------------------------

        if query_normalized in name:
            score += 50


        # --------------------------------
        # Part number match
        # --------------------------------

        if query_normalized in part_numbers:
            score += 80


        # --------------------------------
        # Compatible model match
        # --------------------------------

        if query_normalized in compatible_models:
            score += 70


        # --------------------------------
        # Individual word matching
        # --------------------------------

        query_words = query_normalized.split()

        for word in query_words:

            if len(word) < 2:
                continue

            if word in name:
                score += 10

            elif word in part_numbers:
                score += 8

            elif word in compatible_models:
                score += 7

            elif word in searchable_text:
                score += 2


        if score > 0:
            results.append((score, product))


    # Highest score first
    results.sort(
        key=lambda item: item[0],
        reverse=True
    )


    return [
        product
        for score, product in results[:limit]
    ]