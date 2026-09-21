from lapalfa_chatbot.crawler import fetch_page
from lapalfa_chatbot.parser import extract_text, extract_title


url = "https://www.lapalfa.com/"

html = fetch_page(url)

title = extract_title(html)
text = extract_text(html)

print("TITLE:")
print(title)

print("\nCONTENT:")
print(text[:5000])