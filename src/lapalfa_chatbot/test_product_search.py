# pyrefly: ignore [missing-import]
from product_search import search_products


query = input("Search product: ")

results = search_products(query)

print("\nRESULTS:")
print("=" * 70)

for product in results:
    print(f"Name: {product['name']}")
    print(f"Brand: {product.get('brand')}")
    print(f"Category: {product.get('category')}")
    print(f"Price: Rs.{product.get('price')}")

    print(
        f"Part Numbers: "
        f"{', '.join(product.get('part_numbers', []))}"
    )

    print(f"URL: {product.get('url')}")

    print("-" * 70)