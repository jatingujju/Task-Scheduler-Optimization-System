from collections import defaultdict, deque
import heapq


def greedy_scheduler(tasks, resources):
    """
    tasks: list of dicts
    resources: list of dicts

    Returns:
        schedule list
    """

    # Build dependency graph
    graph = defaultdict(list)
    indegree = defaultdict(int)

    task_map = {}

    for task in tasks:
        task_map[task["task_id"]] = task
        indegree[task["task_id"]] = 0

    for task in tasks:
        for dep in task.get("dependencies", []):
            graph[dep].append(task["task_id"])
            indegree[task["task_id"]] += 1

    # Resource availability
    resource_available = {}

    for r in resources:
        resource_available[r["resource_id"]] = r["shift_start"]

    # Ready queue
    ready = []

    for task in tasks:
        if indegree[task["task_id"]] == 0:
            heapq.heappush(
                ready,
                (
                    task["deadline"],      # earliest deadline first
                    -task["priority"],     # higher priority first
                    task["task_id"]
                )
            )

    finish_times = {}
    schedule = []

    while ready:

        _, _, task_id = heapq.heappop(ready)

        task = task_map[task_id]

        dependency_finish = 0

        for dep in task.get("dependencies", []):
            dependency_finish = max(
                dependency_finish,
                finish_times[dep]
            )

        best_resource = None
        best_start = float("inf")

        for resource in resources:

            if resource["skill"] != task["required_skill"]:
                continue

            start_time = max(
                dependency_finish,
                resource_available[resource["resource_id"]]
            )

            end_time = start_time + task["duration"]

            if end_time <= resource["shift_end"]:

                if start_time < best_start:
                    best_start = start_time
                    best_resource = resource

        if best_resource is None:
            continue

        start_time = best_start
        end_time = start_time + task["duration"]

        resource_available[
            best_resource["resource_id"]
        ] = end_time

        finish_times[task_id] = end_time

        lateness = max(
            0,
            end_time - task["deadline"]
        )

        schedule.append({
            "task_id": task_id,
            "resource_id": best_resource["resource_id"],
            "start": start_time,
            "end": end_time,
            "deadline": task["deadline"],
            "lateness": lateness
        })

        for nxt in graph[task_id]:
            indegree[nxt] -= 1

            if indegree[nxt] == 0:
                nxt_task = task_map[nxt]

                heapq.heappush(
                    ready,
                    (
                        nxt_task["deadline"],
                        -nxt_task["priority"],
                        nxt
                    )
                )

    return schedule