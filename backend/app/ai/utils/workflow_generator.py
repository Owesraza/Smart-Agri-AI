"""
Workflow Generator
Creates day-by-day harvest-to-sale task workflows for farmers.
"""
import logging
from typing import List, Dict, Optional
from datetime import date, timedelta

logger = logging.getLogger(__name__)

WORKFLOW_TEMPLATES = {
    "wheat": [
        {"day": 1, "task": "Final Moisture Check", "description": "Check wheat moisture content. Should be below 12% before selling. Use moisture meter or send sample to mandi lab.", "duration_hours": 2, "priority": "High"},
        {"day": 1, "task": "Cleaning & Sorting", "description": "Clean wheat to remove stones, chaff, and damaged grains. Higher cleanliness = better price at mandi.", "duration_hours": 4, "priority": "High"},
        {"day": 2, "task": "Bagging & Weighing", "description": "Fill wheat in standard 50kg gunny bags. Accurate weighing prevents disputes at mandi.", "duration_hours": 4, "priority": "High"},
        {"day": 2, "task": "Transport Booking", "description": "Book tractor-trolley or truck. Compare rates — ₹15-25 per quintal typical for 20-50km distance.", "duration_hours": 1, "priority": "Medium"},
        {"day": 3, "task": "Mandi Registration", "description": "Arrive at mandi early (5-6 AM). Register your lot for auction. Keep Aadhaar and land records ready.", "duration_hours": 2, "priority": "High"},
        {"day": 3, "task": "Auction & Sale", "description": "Wait for auction. Negotiate minimum price. Accept price if at or above your target/MSP.", "duration_hours": 4, "priority": "High"},
        {"day": 4, "task": "Payment Collection", "description": "Collect payment from mandi trader. Verify amount. Update your ledger with income.", "duration_hours": 1, "priority": "High"},
    ],
    "onion": [
        {"day": 1, "task": "Sorting & Grading", "description": "Grade onions by size (A, B, C grade). Grade A fetches 20-30% premium. Remove rotten/damaged onions.", "duration_hours": 6, "priority": "High"},
        {"day": 1, "task": "Curing Check", "description": "Ensure onions are properly cured (outer skin dry). Reduces post-harvest losses during transport.", "duration_hours": 1, "priority": "Medium"},
        {"day": 2, "task": "Packing in Mesh Bags", "description": "Pack in 50kg mesh bags allowing ventilation. Label each bag with grade and weight.", "duration_hours": 4, "priority": "High"},
        {"day": 2, "task": "Price Check at Lasalgaon", "description": "Check Lasalgaon APMC price. Compare with Nashik and Pune mandis.", "duration_hours": 1, "priority": "High"},
        {"day": 3, "task": "Early Morning Transport", "description": "Leave by 4 AM to reach Lasalgaon by 6 AM for morning auction slot.", "duration_hours": 2, "priority": "High"},
        {"day": 3, "task": "Auction Sale", "description": "Participate in open auction. Minimum price for Grade A: aim ₹2000+/quintal.", "duration_hours": 3, "priority": "High"},
        {"day": 4, "task": "Payment & Records", "description": "Collect payment (same day in most mandis). Record sale in ledger.", "duration_hours": 1, "priority": "Medium"},
    ],
    "cotton": [
        {"day": 1, "task": "Ginning Quality Check", "description": "Check cotton staple length and trash content. Higher staple length = better price. Aim for moisture below 8%.", "duration_hours": 2, "priority": "High"},
        {"day": 2, "task": "Approach CCI/Trader", "description": "Contact Cotton Corporation of India (CCI) for MSP procurement OR compare private trader prices.", "duration_hours": 2, "priority": "High"},
        {"day": 2, "task": "Pressing & Baling", "description": "Press cotton into standard bales (170kg each). Required for both CCI and private ginning mills.", "duration_hours": 6, "priority": "High"},
        {"day": 3, "task": "Transport to Ginning Mill", "description": "Transport bales to registered ginning mill or CCI center.", "duration_hours": 4, "priority": "High"},
        {"day": 4, "task": "Quality Testing", "description": "HVI (High Volume Instrument) testing at mill. Grade determines price.", "duration_hours": 2, "priority": "High"},
        {"day": 4, "task": "Sale & Payment", "description": "Complete sale. CCI pays via DBT within 72 hours. Private traders pay same day.", "duration_hours": 2, "priority": "High"},
    ],
    "default": [
        {"day": 1, "task": "Quality Assessment", "description": "Check moisture, grading, and quality of your produce. Remove damaged stock.", "duration_hours": 3, "priority": "High"},
        {"day": 1, "task": "Price Research", "description": "Check current prices on AGMARKNET app or call nearby mandis. Compare 2-3 mandis.", "duration_hours": 1, "priority": "High"},
        {"day": 2, "task": "Packaging & Weighing", "description": "Pack in standard bags/containers. Accurate weight prevents disputes.", "duration_hours": 4, "priority": "High"},
        {"day": 2, "task": "Arrange Transport", "description": "Book vehicle. Calculate transport cost vs price difference between mandis.", "duration_hours": 1, "priority": "Medium"},
        {"day": 3, "task": "Sell at Best Mandi", "description": "Arrive early. Complete registration. Participate in auction. Accept fair price.", "duration_hours": 5, "priority": "High"},
        {"day": 4, "task": "Collect Payment & Update Ledger", "description": "Collect and verify payment. Record income, transport costs in your ledger.", "duration_hours": 1, "priority": "Medium"},
    ],
}


def generate_workflow(
    crop: str,
    harvest_date: Optional[str] = None,
    quantity: Optional[float] = None,
    mandi: Optional[str] = None,
    recommendation: str = "SELL",
) -> List[Dict]:
    """Generate a day-by-day workflow for the crop sale process."""
    crop_lower = crop.lower()

    # Get template — exact match or default
    template = None
    for key in WORKFLOW_TEMPLATES:
        if key in crop_lower or crop_lower in key:
            template = WORKFLOW_TEMPLATES[key]
            break
    if not template:
        template = WORKFLOW_TEMPLATES["default"]

    # Calculate dates from harvest date or today
    try:
        start = date.fromisoformat(harvest_date) if harvest_date else date.today()
    except (ValueError, TypeError):
        start = date.today()

    # Add STORE workflow prefix if recommendation is STORE/WAIT
    if recommendation == "STORE":
        store_steps = [
            {"day": 0, "task": "Storage Preparation", "description": f"Clean and dry your storage space. Check for moisture and pests. {crop} needs dry, cool storage.", "duration_hours": 3, "priority": "High"},
            {"day": 0, "task": "MSP Registration", "description": "Visit nearest APMC office to register for government MSP procurement. Carry Aadhaar + land records.", "duration_hours": 2, "priority": "High"},
        ]
        template = store_steps + template

    workflow = []
    for step in template:
        step_date = start + timedelta(days=step["day"])
        workflow.append({
            "day": step["day"] + 1,
            "date": str(step_date),
            "task": step["task"],
            "description": step["description"],
            "priority": step.get("priority", "Medium"),
            "duration_hours": step.get("duration_hours", 2),
            "crop": crop,
            "mandi": mandi or "Nearest APMC",
        })

    logger.info(f"📋 Workflow generated: {len(workflow)} steps for {crop}")
    return workflow
