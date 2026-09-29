import datetime as dt_module
from typing import Any
import math


def model_to_dict(obj: Any) -> dict:
    """Convert SQLAlchemy model instance or dict to dictionary."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        d = {}
        for k, v in obj.items():
            if isinstance(v, (dt_module.datetime, dt_module.date)):
                d[k] = v.isoformat()
            else:
                d[k] = v
        return d
    # Handle SQLAlchemy model instance
    result = {}
    if hasattr(obj, "__table__"):
        for column in obj.__table__.columns:
            val = getattr(obj, column.name)
            if isinstance(val, (dt_module.datetime, dt_module.date)):
                result[column.name] = val.isoformat()
            else:
                result[column.name] = val
        return result
    return dict(obj)


def serialize_doc(doc: Any) -> dict:
    """Serialize model object or dict into API response dictionary."""
    if doc is None:
        return None
    d = model_to_dict(doc)
    if "_id" in d and "id" not in d:
        d["id"] = str(d.pop("_id"))
    return d


def serialize_list(docs: list) -> list[dict]:
    """Serialize a list of SQLAlchemy model instances or dicts."""
    return [serialize_doc(doc) for doc in docs]


def paginate(page: int, limit: int) -> dict:
    """Calculate skip/limit for SQL pagination."""
    page = max(1, page)
    limit = min(max(1, limit), 100)  # Cap at 100
    offset = (page - 1) * limit
    return {"offset": offset, "limit": limit}


def pagination_meta(total: int, page: int, limit: int) -> dict:
    """Build pagination metadata for response."""
    total_pages = math.ceil(total / limit) if limit else 1
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }


def success_response(data: Any = None, message: str = "Success", meta: dict = None) -> dict:
    """Standard success response envelope."""
    response = {"success": True, "message": message, "data": data}
    if meta:
        response["meta"] = meta
    return response
