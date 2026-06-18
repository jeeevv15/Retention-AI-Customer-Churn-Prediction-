from typing import Dict, Any, List, Tuple


RULES: List[Tuple[str, callable, str]] = [
    (
        "high_monthly_charges",
        lambda c: float(c.get("MonthlyCharges", 0)) > 75,
        "💰 Offer a 15% loyalty discount on monthly plan",
    ),
    (
        "low_tenure",
        lambda c: int(c.get("tenure", 99)) < 12,
        "🤝 Assign dedicated onboarding assistance & check-in calls",
    ),
    (
        "month_to_month",
        lambda c: str(c.get("Contract", "")).lower() == "month-to-month",
        "📅 Promote annual or two-year subscription plan with incentives",
    ),
    (
        "high_support_calls",
        lambda c: int(c.get("SupportCalls", 0)) > 4,
        "🎧 Assign dedicated premium support representative",
    ),
    (
        "fiber_optic",
        lambda c: str(c.get("InternetService", "")).lower() == "fiber optic",
        "🌐 Offer a complimentary service upgrade or speed boost",
    ),
    (
        "no_online_security",
        lambda c: str(c.get("OnlineSecurity", "")).lower() == "no",
        "🔒 Bundle online security at no extra charge for first 3 months",
    ),
    (
        "senior_citizen",
        lambda c: int(c.get("SeniorCitizen", 0)) == 1,
        "👴 Enroll in senior care program with priority support",
    ),
    (
        "electronic_check",
        lambda c: "electronic check" in str(c.get("PaymentMethod", "")).lower(),
        "💳 Offer auto-pay setup with a $5/month billing discount",
    ),
    (
        "no_tech_support",
        lambda c: str(c.get("TechSupport", "")).lower() == "no",
        "🛠️  Offer free TechSupport add-on for 6 months",
    ),
    (
        "paperless_billing",
        lambda c: str(c.get("PaperlessBilling", "")).lower() == "yes",
        "📧 Send personalised re-engagement email series",
    ),
]

DEFAULT_RECS = [
    "📞 Schedule a proactive retention call within 48 hours",
    "🎁 Send a loyalty rewards offer via email",
]


def get_recommendations(customer_dict: dict, prob: float) -> List[str]:
    recs = []
    for _, condition, action in RULES:
        try:
            if condition(customer_dict):
                recs.append(action)
        except Exception:
            pass
    if not recs:
        recs = DEFAULT_RECS
    if prob >= 0.65 and len(recs) < 3:
        recs.append("🚨 Escalate to senior retention specialist immediately")
    return recs
