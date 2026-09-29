"""Plot, Ledger, Workflow, Market, Weather, Analytics schemas."""
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Union
from datetime import date, datetime
from app.constants.constants import PlotStatus, LedgerType, LedgerCategory, TaskType, TaskStatus, TaskPriority


# ── Plot Schemas ───────────────────────────────────────────
class PlotCreate(BaseModel):
    plot_name: Optional[str] = Field(default=None, max_length=100)
    crop_name: Optional[str] = Field(default=None, max_length=100)
    name: Optional[str] = Field(default=None, max_length=100)
    crop: Optional[str] = Field(default=None, max_length=100)
    area: float = Field(..., gt=0, description="Area in acres")
    soil_type: Optional[str] = None
    sowing_date: Optional[date] = None
    expected_harvest: Optional[date] = None
    status: str = Field(default=PlotStatus.GROWING)

    @model_validator(mode="before")
    @classmethod
    def set_name_and_crop(cls, data):
        if isinstance(data, dict):
            if "name" in data and not data.get("plot_name"):
                data["plot_name"] = data["name"]
            if "crop" in data and not data.get("crop_name"):
                data["crop_name"] = data["crop"]
            if not data.get("plot_name"):
                data["plot_name"] = "Field Plot"
            if not data.get("crop_name"):
                data["crop_name"] = "Wheat"
        return data

    @field_validator("status")
    @classmethod
    def check_status(cls, v):
        if v not in PlotStatus.ALL:
            return PlotStatus.GROWING
        return v


class PlotUpdate(BaseModel):
    plot_name: Optional[str] = Field(None, max_length=100)
    crop_name: Optional[str] = Field(None, max_length=100)
    area: Optional[float] = Field(None, gt=0)
    soil_type: Optional[str] = None
    health: Optional[str] = None
    sowing_date: Optional[date] = None
    expected_harvest: Optional[date] = None
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def check_status(cls, v):
        if v and v not in PlotStatus.ALL:
            return PlotStatus.GROWING
        return v


class PlotResponse(BaseModel):
    id: str
    plot_name: str
    crop_name: str
    area: float
    soil_type: Optional[str] = None
    sowing_date: Optional[date] = None
    expected_harvest: Optional[date] = None
    status: str
    owner_id: str
    created_at: datetime
    updated_at: datetime


# ── Ledger Schemas ─────────────────────────────────────────
class LedgerCreate(BaseModel):
    type: str = Field(default="Expense", description="Income or Expense")
    category: str = Field(default="Fertilizer")
    amount: float = Field(..., gt=0)
    description: str = Field(default="Transaction Record", min_length=1)
    date: Optional[Union[date, str]] = None
    crop: Optional[str] = None
    plot_id: Optional[str] = None
    transport_cost: Optional[float] = Field(default=0.0)
    labour_cost: Optional[float] = Field(default=0.0)
    packaging_cost: Optional[float] = Field(default=0.0)

    @model_validator(mode="before")
    @classmethod
    def sanitize_ledger_fields(cls, data):
        if isinstance(data, dict):
            if data.get("plot_id") == "":
                data["plot_id"] = None
            if not data.get("crop"):
                data["crop"] = "Wheat"
            if not data.get("type"):
                data["type"] = "Expense"
            if not data.get("category"):
                data["category"] = "Fertilizer"
            if not data.get("description"):
                data["description"] = "Farm Transaction"

            dt = data.get("date")
            if not dt or dt == "":
                data["date"] = None
            elif isinstance(dt, str):
                try:
                    data["date"] = dt.split("T")[0]
                except Exception:
                    data["date"] = None

            for num_field in ["amount", "transport_cost", "labour_cost", "packaging_cost"]:
                val = data.get(num_field)
                if val is not None and val != "":
                    try:
                        data[num_field] = float(val)
                    except Exception:
                        data[num_field] = 0.0 if num_field != "amount" else 1.0
        return data

    @field_validator("type")
    @classmethod
    def check_type(cls, v):
        if v not in LedgerType.ALL:
            return "Expense"
        return v

    @field_validator("category")
    @classmethod
    def check_category(cls, v):
        if not v:
            return "Other"
        return str(v)


class LedgerUpdate(BaseModel):
    type: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    date: Optional[date] = None
    crop: Optional[str] = None
    plot_id: Optional[str] = None
    transport_cost: Optional[float] = Field(None, ge=0)
    labour_cost: Optional[float] = Field(None, ge=0)
    packaging_cost: Optional[float] = Field(None, ge=0)


class LedgerResponse(BaseModel):
    id: str
    type: str
    category: str
    amount: float
    description: str
    date: date
    crop: Optional[str] = None
    plot_id: Optional[str] = None
    transport_cost: float = 0.0
    labour_cost: float = 0.0
    packaging_cost: float = 0.0
    net_profit: Optional[float] = None
    owner_id: str
    created_at: datetime
    updated_at: datetime


class LedgerSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_profit: float
    total_transport: float
    total_labour: float
    total_packaging: float
    entry_count: int


# ── Workflow Schemas ───────────────────────────────────────
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    task_type: Optional[str] = Field(default=TaskType.OTHER)
    category: Optional[str] = Field(default=None)
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[date] = None
    priority: str = Field(default=TaskPriority.MEDIUM)
    plot_id: Optional[str] = None
    crop: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def set_task_type(cls, data):
        if isinstance(data, dict):
            if "category" in data and not data.get("task_type"):
                data["task_type"] = data["category"]
            if not data.get("task_type") or data.get("task_type") not in TaskType.ALL:
                data["task_type"] = TaskType.OTHER
        return data

    @field_validator("priority")
    @classmethod
    def check_priority(cls, v):
        if v not in TaskPriority.ALL:
            return TaskPriority.MEDIUM
        return v


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    task_type: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[str] = None
    plot_id: Optional[str] = None
    crop: Optional[str] = None


class TaskStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def check_status(cls, v):
        if v not in TaskStatus.ALL:
            return TaskStatus.PENDING
        return v


class TaskResponse(BaseModel):
    id: str
    title: str
    task_type: str
    description: Optional[str] = None
    status: str
    due_date: Optional[date] = None
    priority: str
    plot_id: Optional[str] = None
    crop: Optional[str] = None
    owner_id: str
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
