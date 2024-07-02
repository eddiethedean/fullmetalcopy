def add_driver(url: str, driver: str) -> str:
    start, middle, end = url.split(':')
    return f"{start}+{driver}:{middle}:{end}"