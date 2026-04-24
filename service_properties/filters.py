VALID_STATUSES = frozenset({"pre_venta", "en_venta", "vendido"})


def parse_filters(body: dict) -> dict:
    """Parse and validate optional query filters from the request body."""
    filters = {}

    if "year" in body:
        year = body["year"]
        if not isinstance(year, int) or isinstance(year, bool):
            raise ValueError("'year' must be an integer")
        filters["year"] = year

    if "city" in body:
        city = body["city"]
        if not isinstance(city, str) or not city.strip():
            raise ValueError("'city' must be a non-empty string")
        filters["city"] = city.strip().lower()

    if "status" in body:
        status = body["status"]
        if status not in VALID_STATUSES:
            raise ValueError(
                f"'status' must be one of: {', '.join(sorted(VALID_STATUSES))}"
            )
        filters["status"] = status

    return filters
