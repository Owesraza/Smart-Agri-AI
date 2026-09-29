"""
Historical Data Import & Search Service
Features:
- Imports CSV, Excel, and JSON datasets
- Cleans data: handles missing values, removes duplicates, validates dates
- Normalizes crop and district names
- Saves into `historical_prices` table
- Auto-triggers FAISS embedding rebuild for RAG AI integration
"""
import io
import json
import logging
import pandas as pd
from datetime import datetime, date
from typing import Dict, List, Optional, Union, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.models.sql_models import HistoricalPriceModel
from app.services.market_service import normalize_crop_name

logger = logging.getLogger(__name__)


def parse_flexible_date(val: Any) -> Optional[date]:
    """Parse date from various string formats or datetime objects."""
    if isinstance(val, (datetime, date)):
        return val if isinstance(val, date) else val.date()
    if pd.isna(val) or not val:
        return None
    val_str = str(val).strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%b %d, %Y"):
        try:
            return datetime.strptime(val_str, fmt).date()
        except ValueError:
            pass
    return None


async def import_historical_dataset(
    db: AsyncSession,
    file_bytes: bytes,
    filename: str,
    source_name: str = "Imported File",
) -> Dict:
    """
    Parse CSV, Excel, or JSON dataset, clean and normalize data,
    insert into DB, and trigger FAISS RAG index rebuild.
    """
    fn = filename.lower()
    df = None

    try:
        if fn.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif fn.endswith(".xlsx") or fn.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(file_bytes))
        elif fn.endswith(".json"):
            data = json.loads(file_bytes.decode("utf-8"))
            df = pd.DataFrame(data if isinstance(data, list) else [data])
        else:
            return {"success": False, "message": "Unsupported file format. Please upload CSV, Excel, or JSON."}
    except Exception as e:
        logger.error(f"Failed to parse file {filename}: {e}")
        return {"success": False, "message": f"File parsing error: {str(e)}"}

    if df is None or df.empty:
        return {"success": False, "message": "The uploaded file is empty."}

    # Normalize column names to lowercase
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

    # Map column aliases
    crop_col = next((c for c in df.columns if c in ["commodity", "crop", "crop_name", "item"]), None)
    price_col = next((c for c in df.columns if c in ["modal_price", "price", "modal", "rate", "avg_price"]), None)
    date_col = next((c for c in df.columns if c in ["date", "price_date", "record_date", "day"]), None)
    mandi_col = next((c for c in df.columns if c in ["market", "mandi", "market_name", "apmc"]), None)
    district_col = next((c for c in df.columns if c in ["district", "city", "location"]), None)
    state_col = next((c for c in df.columns if c in ["state", "region"]), None)

    if not crop_col or not price_col:
        return {
            "success": False,
            "message": "Required columns missing. File must contain crop/commodity and price/modal_price columns.",
            "detected_columns": list(df.columns)
        }

    # Clean data
    df = df.dropna(subset=[crop_col, price_col])
    df = df.drop_duplicates()

    inserted_count = 0
    skipped_count = 0

    for _, row in df.iterrows():
        try:
            raw_crop = str(row[crop_col]).strip()
            raw_price = float(row[price_col])

            if raw_price <= 0:
                skipped_count += 1
                continue

            crop_norm = normalize_crop_name(raw_crop)
            parsed_date = parse_flexible_date(row[date_col]) if date_col and row[date_col] else date.today()

            obj = HistoricalPriceModel(
                commodity=crop_norm,
                modal_price=raw_price,
                date=parsed_date or date.today(),
                market_name=str(row[mandi_col]).strip() if mandi_col and pd.notna(row[mandi_col]) else None,
                district=str(row[district_col]).strip() if district_col and pd.notna(row[district_col]) else None,
                state=str(row[state_col]).strip() if state_col and pd.notna(row[state_col]) else None,
                source=source_name,
            )
            db.add(obj)
            inserted_count += 1

        except (ValueError, TypeError):
            skipped_count += 1
            continue

    await db.commit()
    logger.info(f"✅ Imported {inserted_count} historical price records from {filename} (skipped {skipped_count})")

    # Auto-trigger FAISS index rebuild so RAG has newest knowledge
    try:
        from app.ai.vector_store.faiss_store import build_index
        build_index(force_rebuild=True)
        logger.info("✅ FAISS RAG index rebuilt with new dataset")
    except Exception as e:
        logger.warning(f"FAISS index rebuild after import warning: {e}")

    return {
        "success": True,
        "filename": filename,
        "inserted_records": inserted_count,
        "skipped_records": skipped_count,
        "total_rows_processed": len(df),
        "faiss_index_rebuilt": True,
    }


async def search_historical_prices(
    db: AsyncSession,
    commodity: str,
    district: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 100,
) -> List[Dict]:
    """Search historical price records with filters."""
    crop_norm = normalize_crop_name(commodity)
    stmt = select(HistoricalPriceModel).where(HistoricalPriceModel.commodity == crop_norm)

    if district:
        stmt = stmt.where(HistoricalPriceModel.district.ilike(f"%{district}%"))
    if start_date:
        stmt = stmt.where(HistoricalPriceModel.date >= start_date)
    if end_date:
        stmt = stmt.where(HistoricalPriceModel.date <= end_date)

    stmt = stmt.order_by(HistoricalPriceModel.date.desc()).limit(limit)
    res = await db.execute(stmt)
    records = res.scalars().all()

    return [
        {
            "id": r.id,
            "commodity": r.commodity,
            "modal_price": r.modal_price,
            "date": str(r.date),
            "market_name": r.market_name,
            "district": r.district,
            "state": r.state,
            "source": r.source,
        }
        for r in records
    ]
