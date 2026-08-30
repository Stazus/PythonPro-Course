from pathlib import Path


REPORT_FILE = Path("zadanie20/cost_report.md")

INSTANCES = [
    {
        "instance_id": "i-001",
        "state": "running",
        "running_hours": 720,
        "cpu_usage": 12,
        "hourly_cost": 0.05,
        "reserved_hourly_cost": 0.03,
        "attached_volumes": 1,
    },
    {
        "instance_id": "i-002",
        "state": "running",
        "running_hours": 180,
        "cpu_usage": 65,
        "hourly_cost": 0.08,
        "reserved_hourly_cost": 0.05,
        "attached_volumes": 2,
    },
    {
        "instance_id": "i-003",
        "state": "stopped",
        "running_hours": 50,
        "cpu_usage": 0,
        "hourly_cost": 0.04,
        "reserved_hourly_cost": 0.025,
        "attached_volumes": 2,
    },
    {
        "instance_id": "i-004",
        "state": "running",
        "running_hours": 744,
        "cpu_usage": 18,
        "hourly_cost": 0.10,
        "reserved_hourly_cost": 0.06,
        "attached_volumes": 1,
    },
]


def calculate_reserved_savings(instance):
    current_cost = (
        instance["running_hours"]
        * instance["hourly_cost"]
    )

    reserved_cost = (
        instance["running_hours"]
        * instance["reserved_hourly_cost"]
    )

    savings = current_cost - reserved_cost

    return current_cost, reserved_cost, savings


def analyze_instances():
    recommendations = []

    for instance in INSTANCES:
        if (
            instance["state"] == "running"
            and instance["running_hours"] >= 700
            and instance["cpu_usage"] < 30
        ):
            current_cost, reserved_cost, savings = (
                calculate_reserved_savings(instance)
            )

            recommendations.append(
                {
                    "type": "reserved_instance",
                    "instance_id": instance["instance_id"],
                    "cpu_usage": instance["cpu_usage"],
                    "current_cost": current_cost,
                    "reserved_cost": reserved_cost,
                    "savings": savings,
                }
            )

        if (
            instance["state"] == "stopped"
            and instance["attached_volumes"] > 0
        ):
            recommendations.append(
                {
                    "type": "unused_volumes",
                    "instance_id": instance["instance_id"],
                    "volumes": instance["attached_volumes"],
                }
            )

    return recommendations


def generate_markdown_report(recommendations):
    lines = [
        "# Cloud Cost Optimization Report",
        "",
        "## Recommendations",
        "",
    ]

    if not recommendations:
        lines.append("Brak rekomendacji.")
    else:
        for recommendation in recommendations:
            if recommendation["type"] == "reserved_instance":
                lines.extend(
                    [
                        (
                            f"### Instance "
                            f"{recommendation['instance_id']}"
                        ),
                        "",
                        (
                            f"- CPU usage: "
                            f"{recommendation['cpu_usage']}%"
                        ),
                        (
                            f"- Current cost: "
                            f"${recommendation['current_cost']:.2f}"
                        ),
                        (
                            f"- Reserved cost: "
                            f"${recommendation['reserved_cost']:.2f}"
                        ),
                        (
                            f"- Estimated savings: "
                            f"${recommendation['savings']:.2f}"
                        ),
                        (
                            "- Recommendation: migrate to "
                            "Reserved Instance."
                        ),
                        "",
                    ]
                )

            elif recommendation["type"] == "unused_volumes":
                lines.extend(
                    [
                        (
                            f"### Instance "
                            f"{recommendation['instance_id']}"
                        ),
                        "",
                        "- State: stopped",
                        (
                            f"- Attached volumes: "
                            f"{recommendation['volumes']}"
                        ),
                        (
                            "- Recommendation: verify whether "
                            "attached volumes are still needed."
                        ),
                        "",
                    ]
                )

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Raport zapisano do: {REPORT_FILE}")


def main():
    recommendations = analyze_instances()
    generate_markdown_report(recommendations)


if __name__ == "__main__":
    main()
