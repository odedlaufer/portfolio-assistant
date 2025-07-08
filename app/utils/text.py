import unicodedata


def ascii_only(text: str) -> str:
    """Remove non-ASCII characters (like emojis, symbols, etc.)"""
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
