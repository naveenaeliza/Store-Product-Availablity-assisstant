import re

REMOVE_PATTERNS = [
    r"\bnear me\b",
    r"\bnearby\b",
    r"\bclosest\b",
    r"\bavailable\b",
    r"\bin stock\b",
    r"\bwhere can i buy\b",
    r"\bwhere do i buy\b",
    r"\bbuy\b",
    r"\bfind\b",
    r"\bsearch\b",
    r"\bshow me\b",
    r"\bstore\b"
]

def extract_product(query: str) -> str:
    query = query.lower()

    for pattern in REMOVE_PATTERNS:
        query = re.sub(pattern, "", query)

    query = re.sub(r"[^\w\s]", " ", query)
    query = re.sub(r"\s+", " ", query).strip()

    return query