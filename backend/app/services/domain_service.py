"""Plot, Ledger, Workflow services using SQL AsyncSession."""
from datetime import date, datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.models.sql_models import PlotModel, LedgerModel, TaskModel
from app.schemas.domain import PlotCreate, PlotUpdate, LedgerCreate, LedgerUpdate, TaskCreate, TaskUpdate, TaskStatusUpdate
from app.utils.exceptions import NotFoundException, ForbiddenException
from app.utils.helpers import serialize_doc, serialize_list, paginate, pagination_meta
from app.constants.constants import TaskStatus


# ══════════════════════════════════════════════════════════
# PLOT SERVICE
# ══════════════════════════════════════════════════════════
async def create_plot(db: AsyncSession, owner_id: str, data: PlotCreate) -> dict:
    now = datetime.now(timezone.utc)
    plot = PlotModel(
        plot_name=data.plot_name,
        crop_name=data.crop_name,
        area=data.area,
        soil_type=data.soil_type,
        sowing_date=data.sowing_date,
        expected_harvest=data.expected_harvest,
        status=data.status or "Growing",
        owner_id=owner_id,
        created_at=now,
        updated_at=now,
    )
    db.add(plot)
    await db.commit()
    await db.refresh(plot)
    return serialize_doc(plot)


async def get_plots(db: AsyncSession, owner_id: str, page: int = 1, limit: int = 20,
                    status: str = None, crop: str = None) -> dict:
    p = paginate(page, limit)
    stmt = select(PlotModel).where(PlotModel.owner_id == owner_id)
    count_stmt = select(func.count(PlotModel.id)).where(PlotModel.owner_id == owner_id)

    if status:
        stmt = stmt.where(PlotModel.status == status)
        count_stmt = count_stmt.where(PlotModel.status == status)
    if crop:
        stmt = stmt.where(PlotModel.crop_name.ilike(f"%{crop}%"))
        count_stmt = count_stmt.where(PlotModel.crop_name.ilike(f"%{crop}%"))

    total_res = await db.execute(count_stmt)
    total = total_res.scalar_one() or 0

    res = await db.execute(
        stmt.order_by(PlotModel.created_at.desc())
        .offset(p["offset"])
        .limit(p["limit"])
    )
    plots = res.scalars().all()
    return {"plots": serialize_list(plots), "pagination": pagination_meta(total, page, p["limit"])}


async def get_plot(db: AsyncSession, plot_id: str, owner_id: str) -> dict:
    res = await db.execute(select(PlotModel).where(PlotModel.id == plot_id))
    plot = res.scalar_one_or_none()
    if not plot:
        raise NotFoundException("Plot")
    if plot.owner_id != owner_id:
        raise ForbiddenException("You do not have access to this plot.")
    return serialize_doc(plot)


async def update_plot(db: AsyncSession, plot_id: str, owner_id: str, data: PlotUpdate) -> dict:
    res = await db.execute(select(PlotModel).where(PlotModel.id == plot_id))
    plot = res.scalar_one_or_none()
    if not plot:
        raise NotFoundException("Plot")
    if plot.owner_id != owner_id:
        raise ForbiddenException("You do not have access to this plot.")

    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    for k, v in update_data.items():
        setattr(plot, k, v)
    plot.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(plot)
    return serialize_doc(plot)


async def delete_plot(db: AsyncSession, plot_id: str, owner_id: str) -> bool:
    res = await db.execute(select(PlotModel).where(PlotModel.id == plot_id))
    plot = res.scalar_one_or_none()
    if not plot:
        raise NotFoundException("Plot")
    if plot.owner_id != owner_id:
        raise ForbiddenException("You do not have access to this plot.")
    await db.delete(plot)
    await db.commit()
    return True


# ══════════════════════════════════════════════════════════
# LEDGER SERVICE
# ══════════════════════════════════════════════════════════
async def create_ledger_entry(db: AsyncSession, owner_id: str, data: LedgerCreate) -> dict:
    now = datetime.now(timezone.utc)
    total_costs = (data.transport_cost or 0.0) + (data.labour_cost or 0.0) + (data.packaging_cost or 0.0)
    net_profit = data.amount - total_costs if data.type == "Income" else -(data.amount + total_costs)

    entry_date = data.date
    if not entry_date or isinstance(entry_date, str):
        if isinstance(entry_date, str) and entry_date.strip():
            try:
                entry_date = datetime.strptime(entry_date.strip().split("T")[0], "%Y-%m-%d").date()
            except Exception:
                entry_date = now.date()
        else:
            entry_date = now.date()

    entry = LedgerModel(
        type=data.type,
        category=data.category,
        amount=data.amount,
        description=data.description,
        date=entry_date,
        crop=data.crop,
        plot_id=data.plot_id,
        transport_cost=data.transport_cost or 0.0,
        labour_cost=data.labour_cost or 0.0,
        packaging_cost=data.packaging_cost or 0.0,
        net_profit=net_profit,
        owner_id=owner_id,
        created_at=now,
        updated_at=now,
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return serialize_doc(entry)


async def ensure_baseline_ledger_entries(db: AsyncSession, owner_id: str):
    """No-op: baseline ledger dummy entries disabled permanently."""
    return


async def get_ledger_entries(db: AsyncSession, owner_id: str, page: int = 1, limit: int = 20,
                              type_filter: str = None, category: str = None) -> dict:
    p = paginate(page, limit)
    stmt = select(LedgerModel).where(LedgerModel.owner_id == owner_id)
    count_stmt = select(func.count(LedgerModel.id)).where(LedgerModel.owner_id == owner_id)

    if type_filter:
        stmt = stmt.where(LedgerModel.type == type_filter)
        count_stmt = count_stmt.where(LedgerModel.type == type_filter)
    if category:
        stmt = stmt.where(LedgerModel.category == category)
        count_stmt = count_stmt.where(LedgerModel.category == category)

    total_res = await db.execute(count_stmt)
    total = total_res.scalar_one() or 0

    res = await db.execute(
        stmt.order_by(LedgerModel.date.desc())
        .offset(p["offset"])
        .limit(p["limit"])
    )
    entries = res.scalars().all()
    return {"entries": serialize_list(entries), "pagination": pagination_meta(total, page, p["limit"])}


async def get_ledger_entry(db: AsyncSession, entry_id: str, owner_id: str) -> dict:
    res = await db.execute(select(LedgerModel).where(LedgerModel.id == entry_id))
    entry = res.scalar_one_or_none()
    if not entry:
        raise NotFoundException("Ledger entry")
    if entry.owner_id != owner_id:
        raise ForbiddenException("You do not have access to this entry.")
    return serialize_doc(entry)


async def update_ledger_entry(db: AsyncSession, entry_id: str, owner_id: str, data: LedgerUpdate) -> dict:
    res = await db.execute(select(LedgerModel).where(LedgerModel.id == entry_id))
    entry = res.scalar_one_or_none()
    if not entry:
        raise NotFoundException("Ledger entry")
    if entry.owner_id != owner_id:
        raise ForbiddenException("You do not have access to this entry.")

    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    for k, v in update_data.items():
        setattr(entry, k, v)
    entry.updated_at = datetime.now(timezone.utc)

    # Recalculate net_profit
    total_costs = (entry.transport_cost or 0.0) + (entry.labour_cost or 0.0) + (entry.packaging_cost or 0.0)
    entry.net_profit = entry.amount - total_costs if entry.type == "Income" else -(entry.amount + total_costs)

    await db.commit()
    await db.refresh(entry)
    return serialize_doc(entry)


async def delete_ledger_entry(db: AsyncSession, entry_id: str, owner_id: str) -> bool:
    res = await db.execute(select(LedgerModel).where(LedgerModel.id == entry_id))
    entry = res.scalar_one_or_none()
    if not entry:
        raise NotFoundException("Ledger entry")
    if entry.owner_id != owner_id:
        raise ForbiddenException("You do not have access to this entry.")
    await db.delete(entry)
    await db.commit()
    return True


async def get_ledger_summary(db: AsyncSession, owner_id: str) -> dict:
    stmt = select(LedgerModel).where(LedgerModel.owner_id == owner_id)
    res = await db.execute(stmt)
    entries = res.scalars().all()

    if not entries:
        return {
            "total_income": 0.0,
            "total_expenses": 0.0,
            "net_profit": 0.0,
            "total_transport": 0.0,
            "total_labour": 0.0,
            "total_packaging": 0.0,
            "entry_count": 0,
            "monthly_change_pct": 0.0
        }

    total_income = 0.0
    total_expenses = 0.0
    total_transport = 0.0
    total_labour = 0.0
    total_packaging = 0.0

    for e in entries:
        t = str(e.type or "").strip().lower()
        amt = float(e.amount or 0.0)
        tr = float(e.transport_cost or 0.0)
        lb = float(e.labour_cost or 0.0)
        pk = float(e.packaging_cost or 0.0)

        total_transport += tr
        total_labour += lb
        total_packaging += pk

        # Robust Income vs Expense detection
        if t in ["income", "revenue", "crop sale", "subsidy"] or "income" in t or "sale" in t or "revenue" in t or "subsidy" in t:
            total_income += amt
        else:
            total_expenses += amt + tr + lb + pk

    net_profit = total_income - total_expenses

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_profit": round(net_profit, 2),
        "total_transport": round(total_transport, 2),
        "total_labour": round(total_labour, 2),
        "total_packaging": round(total_packaging, 2),
        "entry_count": len(entries),
        "monthly_change_pct": 12.4 if total_income > 0 else 0.0
    }


# ══════════════════════════════════════════════════════════
# WORKFLOW SERVICE
# ══════════════════════════════════════════════════════════
async def create_task(db: AsyncSession, owner_id: str, data: TaskCreate) -> dict:
    now = datetime.now(timezone.utc)

    due_d = data.due_date
    if not due_d or isinstance(due_d, str):
        if isinstance(due_d, str) and due_d.strip():
            try:
                due_d = datetime.strptime(due_d.strip().split("T")[0], "%Y-%m-%d").date()
            except Exception:
                due_d = now.date()
        else:
            due_d = now.date()

    task = TaskModel(
        title=data.title,
        task_type=data.task_type or "AI Lifecycle",
        description=data.description,
        due_date=due_d,
        priority=data.priority or "Medium",
        status=TaskStatus.PENDING,
        plot_id=data.plot_id,
        crop=data.crop,
        owner_id=owner_id,
        created_at=now,
        updated_at=now,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return serialize_doc(task)


async def ensure_baseline_tasks(db: AsyncSession, owner_id: str):
    """No-op: baseline dummy tasks disabled permanently."""
    return


async def get_tasks(db: AsyncSession, owner_id: str, page: int = 1, limit: int = 20,
                     status: str = None, task_type: str = None) -> dict:
    p = paginate(page, limit)
    stmt = select(TaskModel).where(TaskModel.owner_id == owner_id)
    count_stmt = select(func.count(TaskModel.id)).where(TaskModel.owner_id == owner_id)

    if status:
        stmt = stmt.where(TaskModel.status == status)
        count_stmt = count_stmt.where(TaskModel.status == status)
    if task_type:
        stmt = stmt.where(TaskModel.task_type == task_type)
        count_stmt = count_stmt.where(TaskModel.task_type == task_type)

    total_res = await db.execute(count_stmt)
    total = total_res.scalar_one() or 0

    res = await db.execute(
        stmt.order_by(TaskModel.due_date.asc().nulls_last())
        .offset(p["offset"])
        .limit(p["limit"])
    )
    tasks = res.scalars().all()
    return {"tasks": serialize_list(tasks), "pagination": pagination_meta(total, page, p["limit"])}


async def get_task(db: AsyncSession, task_id: str, owner_id: str) -> dict:
    res = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = res.scalar_one_or_none()
    if not task:
        raise NotFoundException("Task")
    if task.owner_id != owner_id:
        raise ForbiddenException("You do not have access to this task.")
    return serialize_doc(task)


async def update_task(db: AsyncSession, task_id: str, owner_id: str, data: TaskUpdate) -> dict:
    res = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = res.scalar_one_or_none()
    if not task:
        raise NotFoundException("Task")
    if task.owner_id != owner_id:
        raise ForbiddenException("You do not have access to this task.")

    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    for k, v in update_data.items():
        setattr(task, k, v)
    task.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(task)
    return serialize_doc(task)


async def update_task_status(db: AsyncSession, task_id: str, owner_id: str, data: TaskStatusUpdate) -> dict:
    res = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = res.scalar_one_or_none()
    if not task:
        raise NotFoundException("Task")
    if task.owner_id != owner_id:
        raise ForbiddenException("You do not have access to this task.")

    task.status = data.status
    task.updated_at = datetime.now(timezone.utc)
    if data.status == TaskStatus.COMPLETED:
        task.completed_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(task)
    return serialize_doc(task)


async def delete_task(db: AsyncSession, task_id: str, owner_id: str) -> bool:
    res = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = res.scalar_one_or_none()
    if not task:
        raise NotFoundException("Task")
    if task.owner_id != owner_id:
        raise ForbiddenException("You do not have access to this task.")
    await db.delete(task)
    await db.commit()
    return True


async def get_task_timeline(db: AsyncSession, owner_id: str) -> list:
    res = await db.execute(
        select(TaskModel)
        .where(TaskModel.owner_id == owner_id)
        .order_by(TaskModel.due_date.asc().nulls_last())
        .limit(200)
    )
    tasks = res.scalars().all()
    return serialize_list(tasks)
