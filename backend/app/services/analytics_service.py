"""Analytics service — aggregates from SQL for charts and KPIs."""
from datetime import datetime, timezone, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract, and_
from app.models.sql_models import PlotModel, LedgerModel, TaskModel
from app.services.domain_service import ensure_baseline_ledger_entries


async def get_monthly_profit(db: AsyncSession, owner_id: str, year: int = None) -> list:
    year = year or datetime.now(timezone.utc).year

    # Extract month from LedgerModel.date
    stmt = (
        select(
            extract('month', LedgerModel.date).label("month"),
            LedgerModel.type,
            func.coalesce(func.sum(LedgerModel.amount), 0.0).label("total")
        )
        .where(
            and_(
                LedgerModel.owner_id == owner_id,
                extract('year', LedgerModel.date) == year
            )
        )
        .group_by(extract('month', LedgerModel.date), LedgerModel.type)
        .order_by("month")
    )
    res = await db.execute(stmt)
    results = res.fetchall()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly = {m: {"month": m, "income": 0.0, "expenses": 0.0, "profit": 0.0} for m in months}

    for month_num, l_type, total in results:
        if month_num and 1 <= int(month_num) <= 12:
            m_name = months[int(month_num) - 1]
            if l_type == "Income":
                monthly[m_name]["income"] = float(total)
            else:
                monthly[m_name]["expenses"] = float(total)

    for m in monthly.values():
        m["profit"] = m["income"] - m["expenses"]

    return list(monthly.values())


async def get_crop_summary(db: AsyncSession, owner_id: str) -> list:
    stmt = (
        select(
            LedgerModel.crop,
            func.coalesce(func.sum(LedgerModel.amount), 0.0).label("total_income"),
            func.count(LedgerModel.id).label("count")
        )
        .where(
            and_(
                LedgerModel.owner_id == owner_id,
                LedgerModel.crop.isnot(None),
                LedgerModel.type == "Income"
            )
        )
        .group_by(LedgerModel.crop)
        .order_by(func.sum(LedgerModel.amount).desc())
    )
    res = await db.execute(stmt)
    results = res.fetchall()

    return [
        {"crop": crop, "total_income": float(tot), "transactions": int(cnt)}
        for crop, tot, cnt in results if crop
    ]


async def get_dashboard_stats(db: AsyncSession, owner_id: str) -> dict:
    # Total & active plots
    tp_res = await db.execute(select(func.count(PlotModel.id)).where(PlotModel.owner_id == owner_id))
    total_plots = tp_res.scalar_one() or 0

    ap_res = await db.execute(select(func.count(PlotModel.id)).where(
        and_(PlotModel.owner_id == owner_id, PlotModel.status.in_(["Growing", "Harvesting"]))
    ))
    active_plots = ap_res.scalar_one() or 0

    # Tasks
    pt_res = await db.execute(select(func.count(TaskModel.id)).where(
        and_(TaskModel.owner_id == owner_id, TaskModel.status == "Pending")
    ))
    pending_tasks = pt_res.scalar_one() or 0

    ct_res = await db.execute(select(func.count(TaskModel.id)).where(
        and_(TaskModel.owner_id == owner_id, TaskModel.status == "Completed")
    ))
    completed_tasks = ct_res.scalar_one() or 0

    # Financial summary
    fin_res = await db.execute(
        select(
            LedgerModel.type,
            func.coalesce(func.sum(LedgerModel.amount), 0.0).label("total")
        )
        .where(LedgerModel.owner_id == owner_id)
        .group_by(LedgerModel.type)
    )
    fin = fin_res.fetchall()

    income = 0.0
    expense = 0.0
    for l_type, tot in fin:
        if l_type == "Income":
            income = float(tot)
        elif l_type == "Expense":
            expense = float(tot)

    return {
        "total_plots": total_plots,
        "active_plots": active_plots,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "total_income": income,
        "total_expenses": expense,
        "net_profit": income - expense,
        "profit_margin": round((income - expense) / income * 100, 1) if income > 0 else 0,
    }
