from db.connection import get_connection

_BASE_QUERY = """
    SELECT
        p.address,
        p.city,
        s.name        AS status,
        p.price,
        p.description
    FROM property p
    INNER JOIN status_history sh ON sh.property_id = p.id
    INNER JOIN status s ON s.id = sh.status_id
    WHERE sh.id = (
        SELECT MAX(sh2.id)
        FROM status_history sh2
        WHERE sh2.property_id = p.id
    )
    AND s.name IN ('pre_venta', 'en_venta', 'vendido')
"""


def get_properties(filters: dict) -> list[dict]:
    """Query properties with their current status, applying optional filters."""
    clauses: list[str] = []
    params: list = []

    if "year" in filters:
        clauses.append("AND p.year = %s")
        params.append(filters["year"])

    if "city" in filters:
        clauses.append("AND LOWER(p.city) = %s")
        params.append(filters["city"])

    if "status" in filters:
        clauses.append("AND s.name = %s")
        params.append(filters["status"])

    query = _BASE_QUERY + " ".join(clauses)

    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()
