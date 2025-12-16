FORBIDDEN_KEYWORDS = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "UNION",
    "JOIN",
    ";",
]

WHITELIST_TABLES = {"MARA", "MARC", "EKKO", "EKPO", "MBEW"}


def validate_query(req):
    if req.table.upper() not in WHITELIST_TABLES:
        raise ValueError(f"Table {req.table} is not allowed")

    where = (req.where or "").upper()
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in where:
            raise ValueError(f"Forbidden keyword detected: {keyword}")
