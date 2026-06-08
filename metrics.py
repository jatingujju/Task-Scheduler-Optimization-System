from collections import defaultdict


def calculate_kpis(schedule, resources):
    """
    Returns:
    {
        on_time_percent,
        total_lateness_hours,
        resource_utilization
    }
    """

    total_tasks = len(schedule)

    if total_tasks == 0:
        return {
            "on_time_percent": 0,
            "total_lateness_hours": 0,
            "resource_utilization": {}
        }

    on_time_tasks = 0
    total_lateness = 0

    resource_busy_hours = defaultdict(int)

    # -----------------------------
    # Task KPIs
    # -----------------------------

    for task in schedule:

        finish_time = task["end"]
        deadline = task["deadline"]

        lateness = max(0, finish_time - deadline)

        total_lateness += lateness

        if lateness == 0:
            on_time_tasks += 1

        duration = finish_time - task["start"]

        resource_busy_hours[
            task["resource_id"]
        ] += duration

    on_time_percent = (
        on_time_tasks / total_tasks
    ) * 100

    # -----------------------------
    # Resource Utilization
    # -----------------------------

    utilization = {}

    for resource in resources:

        rid = resource["resource_id"]

        available_hours = (
            resource["shift_end"]
            - resource["shift_start"]
        )

        busy_hours = resource_busy_hours[rid]

        util = 0

        if available_hours > 0:
            util = (
                busy_hours / available_hours
            ) * 100

        utilization[rid] = round(util, 2)

    return {
        "on_time_percent": round(
            on_time_percent, 2
        ),
        "total_lateness_hours": total_lateness,
        "resource_utilization": utilization
    }