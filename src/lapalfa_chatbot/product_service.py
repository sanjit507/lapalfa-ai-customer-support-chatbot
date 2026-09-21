from lapalfa_chatbot.product_store import load_products, search_products
import requests
import urllib.parse

def live_search_shopify(query: str):
    """Fallback live search from Lapalfa's website."""
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://www.lapalfa.com/search/suggest.json?q={encoded}&resources[type]=product"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        
        results = data.get("resources", {}).get("results", {}).get("products", [])
        products = []
        for p in results[:5]:
            products.append({
                "title": p.get("title"),
                "price": float(p.get("price", 0)) if p.get("price") else None,
                "comparePrice": float(p.get("compare_at_price_max", 0)) if p.get("compare_at_price_max") else None,
                "sku": None,
                "imageUrl": p.get("image"),
                "productUrl": f"https://www.lapalfa.com{p.get('url')}" if p.get("url") else None,
                "inStock": p.get("available", True),
            })
        return products
    except Exception as e:
        print(f"Live search error: {e}")
        return []

def search_product_for_chat(query: str):
    local = search_products(query, limit=5)
    if not local:
        return live_search_shopify(query)
    return local


def check_compatibility(laptop_model: str):

    products = load_products()

    # Normalize: lowercase, strip punctuation except hyphens and dots
    import re
    text = laptop_model.lower().strip()
    text = re.sub(r"[?!,]", "", text)

    results = []

    for product in products:

        searchable_text = " ".join([
            str(product.get("title", "")),
            str(product.get("sku", "")),
            str(product.get("category", "")),
            " ".join(product.get("tags", [])),
            str(product.get("description", "")),
        ]).lower()

        score = 0

        # --- Strategy 1: look for hyphenated model tokens as whole strings ---
        # e.g. "15-de0999nf" stays intact and is searched as-is
        tokens = text.split()
        for token in tokens:
            if len(token) >= 4 and token in searchable_text:
                # Exact model-like tokens (contain digit) score higher
                if re.search(r"\d", token):
                    score += 10
                else:
                    score += 1

        # --- Strategy 2: also try the full phrase without stop words ---
        stop_words = {
            "do", "you", "have", "a", "battery", "for", "the",
            "is", "there", "any", "laptop", "compatible", "with",
            "will", "this", "fit", "does", "suitable", "can", "i",
            "get", "find", "need", "want",
        }
        meaningful_tokens = [
            t for t in tokens
            if t not in stop_words and len(t) >= 3
        ]
        for token in meaningful_tokens:
            if token in searchable_text and token not in tokens:
                score += 2

        if score > 0:
            results.append((score, product))

    # Highest matching products first
    results.sort(key=lambda x: x[0], reverse=True)
    
    local_results = [
        product
        for score, product in results[:5]
    ]
    
    if not local_results:
        # If no local compatible parts found, try searching the live website
        return live_search_shopify(laptop_model)
        
    return local_results