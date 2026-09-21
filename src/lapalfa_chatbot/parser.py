from bs4 import BeautifulSoup


def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Remove elements that are not useful for knowledge retrieval
    for element in soup([
        "script",
        "style",
        "noscript",
        "nav",
        "header",
        "footer",
        "form",
    ]):
        element.decompose()

    # Prefer the main content area
    main = soup.find("main")

    if main:
        content = main
    else:
        content = soup.body

    if content is None:
        return ""

    text = content.get_text(separator="\n")

    # Clean whitespace
    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    if soup.title:
        return soup.title.get_text(strip=True)

    return ""