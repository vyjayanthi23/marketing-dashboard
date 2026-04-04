import json
import random
from datetime import datetime, timedelta

random.seed(datetime.now().toordinal())  # different values each day, stable within a day

CAMPAIGNS = [
    {"name": "Spring Sale 2026", "channel": "Email", "status": "Active"},
    {"name": "Product Launch - Pro Plan", "channel": "Social", "status": "Active"},
    {"name": "Weekly Newsletter", "channel": "Email", "status": "Active"},
    {"name": "Re-engagement Campaign", "channel": "Email", "status": "Paused"},
    {"name": "Brand Awareness Q2", "channel": "Display", "status": "Active"},
]


def generate_daily_trend(base_reach, days=7):
    trend = []
    for i in range(days):
        date = (datetime.today() - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d")
        value = int(base_reach * random.uniform(0.75, 1.25))
        trend.append({"date": date, "reach": value})
    return trend


def generate_campaign(campaign):
    reach = random.randint(8_000, 80_000)
    impressions = int(reach * random.uniform(1.5, 3.0))
    clicks = int(reach * random.uniform(0.03, 0.12))
    conversions = int(clicks * random.uniform(0.08, 0.20))
    open_rate = round(random.uniform(0.18, 0.42), 3) if campaign["channel"] == "Email" else None
    ctr = round(clicks / impressions, 4) if impressions > 0 else 0

    return {
        **campaign,
        "reach": reach,
        "impressions": impressions,
        "clicks": clicks,
        "conversions": conversions,
        "open_rate": open_rate,
        "ctr": ctr,
        "daily_trend": generate_daily_trend(reach),
    }


def generate_summary(campaigns):
    active = [c for c in campaigns if c["status"] == "Active"]
    total_reach = sum(c["reach"] for c in active)
    total_impressions = sum(c["impressions"] for c in active)
    total_clicks = sum(c["clicks"] for c in active)
    total_conversions = sum(c["conversions"] for c in active)
    avg_ctr = round(total_clicks / total_impressions, 4) if total_impressions > 0 else 0

    return {
        "total_reach": total_reach,
        "total_impressions": total_impressions,
        "total_clicks": total_clicks,
        "total_conversions": total_conversions,
        "avg_ctr": avg_ctr,
        "active_campaigns": len(active),
    }


def main():
    campaigns = [generate_campaign(c) for c in CAMPAIGNS]
    summary = generate_summary(campaigns)

    output = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": summary,
        "campaigns": campaigns,
    }

    with open("data/metrics.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Generated metrics.json at {output['generated_at']}")


if __name__ == "__main__":
    main()
