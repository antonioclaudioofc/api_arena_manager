def normalize_string(value: str):
    if not value:
        return value

    return value.strip().lower()
