from service_properties.repository import get_properties


def list_properties(filters: dict) -> list[dict]:
    """Return properties visible to the public, applying optional filters."""
    return get_properties(filters)
