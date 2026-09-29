"""
Profit Analyzer — Digital Ledger Intelligence
Analyzes farmer's income/expense data and generates actionable insights.
"""
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Benchmark costs per acre (approximate, 2024 rates)
BENCHMARK_COSTS = {
    "wheat": {"seed": 1500, "fertilizer": 3500, "labour": 4000, "irrigation": 2000, "pesticide": 1500, "total": 12500},
    "onion": {"seed": 3000, "fertilizer": 4500, "labour": 8000, "irrigation": 3000, "pesticide": 2000, "total": 20500},
    "cotton": {"seed": 2500, "fertilizer": 5000, "labour": 7000, "irrigation": 3500, "pesticide": 3000, "total": 21000},
    "soybean": {"seed": 2000, "fertilizer": 3000, "labour": 4000, "irrigation": 1500, "pesticide": 1500, "total": 12000},
    "rice": {"seed": 1500, "fertilizer": 4000, "labour": 6000, "irrigation": 3000, "pesticide": 2000, "total": 16500},
    "maize": {"seed": 1200, "fertilizer": 2500, "labour": 3500, "irrigation": 1500, "pesticide": 1000, "total": 9700},
    "default": {"seed": 2000, "fertilizer": 3500, "labour": 5000, "irrigation": 2500, "pesticide": 1500, "total": 14500},
}


def analyze_profit(ledger_entries: List[Dict], crop: Optional[str] = None) -> Dict:
    """
    Analyze ledger entries and generate profit/loss report with suggestions.
    """
    if not ledger_entries:
        return {
            "summary": "No financial data available yet. Start recording your income and expenses in the Ledger section.",
            "total_income": 0,
            "total_expenses": 0,
            "net_profit": 0,
            "profit_margin_percent": 0,
            "top_earning_crop": None,
            "biggest_expense_category": None,
            "cost_reduction_tips": [],
            "revenue_improvement_tips": [],
            "benchmark_comparison": None,
        }

    # Aggregate
    total_income = 0
    total_expenses = 0
    expense_by_category = {}
    income_by_crop = {}
    total_transport = 0
    total_labour = 0
    total_packaging = 0

    for entry in ledger_entries:
        amount = float(entry.get("amount", 0))
        entry_type = entry.get("type", "")
        category = entry.get("category", "Other")
        entry_crop = entry.get("crop", "Unknown")
        transport = float(entry.get("transport_cost", 0))
        labour = float(entry.get("labour_cost", 0))
        packaging = float(entry.get("packaging_cost", 0))

        total_transport += transport
        total_labour += labour
        total_packaging += packaging

        if entry_type == "Income":
            total_income += amount
            income_by_crop[entry_crop] = income_by_crop.get(entry_crop, 0) + amount
        elif entry_type == "Expense":
            total_expenses += amount + transport + labour + packaging
            expense_by_category[category] = expense_by_category.get(category, 0) + amount

    net_profit = total_income - total_expenses
    profit_margin = round((net_profit / total_income * 100), 1) if total_income > 0 else 0
    top_crop = max(income_by_crop, key=income_by_crop.get) if income_by_crop else None
    biggest_expense = max(expense_by_category, key=expense_by_category.get) if expense_by_category else None

    # Cost reduction tips
    tips = []
    if total_transport > total_income * 0.08:
        tips.append(f"Transport costs are high ({round(total_transport/total_income*100, 1)}% of income). Consider group transport with neighboring farmers to split costs.")
    if total_labour > total_income * 0.15:
        tips.append("Labour costs are high. Consider using farm machinery for harvesting — can reduce labour cost by 40%.")
    if total_packaging > total_income * 0.03:
        tips.append("Reduce packaging cost by buying gunny bags in bulk from cooperative society.")
    if biggest_expense == "Fertilizer":
        tips.append("Use soil testing to apply fertilizer only where needed. Can reduce fertilizer cost by 20-30%.")
    if biggest_expense == "Pesticide":
        tips.append("Practice Integrated Pest Management (IPM) to reduce pesticide use by 40-50% while maintaining yield.")
    if not tips:
        tips.append("Your cost structure looks reasonable. Focus on increasing income through better market timing.")

    # Revenue improvement tips
    revenue_tips = []
    if profit_margin < 20:
        revenue_tips.append("Profit margin is below 20%. Consider adding a second crop or intercropping to boost income per acre.")
    revenue_tips.append("Check if your crop qualifies for government MSP procurement — guaranteed better price than market.")
    revenue_tips.append("Grade your produce before selling. Grade A typically fetches 15-25% more than mixed grade.")

    # Benchmark comparison
    benchmark = None
    if crop:
        bench = BENCHMARK_COSTS.get(crop.lower(), BENCHMARK_COSTS["default"])
        benchmark = {
            "crop": crop,
            "your_expenses": total_expenses,
            "benchmark_expenses": bench["total"],
            "difference": total_expenses - bench["total"],
            "status": "Above average" if total_expenses > bench["total"] * 1.2 else (
                "Below average (good)" if total_expenses < bench["total"] * 0.9 else "Near average"
            ),
        }

    logger.info(f"📊 Profit analysis: Income=₹{total_income}, Expenses=₹{total_expenses}, Profit=₹{net_profit} ({profit_margin}%)")

    return {
        "summary": f"Total income: ₹{total_income:,.0f}. Total expenses: ₹{total_expenses:,.0f}. Net profit: ₹{net_profit:,.0f} ({profit_margin}% margin).",
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "profit_margin_percent": profit_margin,
        "transport_cost": total_transport,
        "labour_cost": total_labour,
        "packaging_cost": total_packaging,
        "top_earning_crop": top_crop,
        "top_crop_income": income_by_crop.get(top_crop, 0) if top_crop else 0,
        "biggest_expense_category": biggest_expense,
        "expense_breakdown": expense_by_category,
        "income_by_crop": income_by_crop,
        "cost_reduction_tips": tips,
        "revenue_improvement_tips": revenue_tips,
        "benchmark_comparison": benchmark,
    }
