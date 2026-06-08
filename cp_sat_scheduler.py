from ortools.sat.python import cp_model


def cp_sat_scheduler(tasks, resources):
    """
    tasks:
    {
        task_id,
        duration,
        deadline,
        priority,
        required_skill,
        dependencies
    }

    resources:
    {
        resource_id,
        skill,
        shift_start,
        shift_end
    }
    """

    model = cp_model.CpModel()

    horizon = max(r["shift_end"] for r in resources)

    task_vars = {}
    intervals_by_resource = {}

    for r in resources:
        intervals_by_resource[r["resource_id"]] = []

    # --------------------------------------------------
    # Create optional intervals
    # --------------------------------------------------

    for task in tasks:

        task_id = task["task_id"]

        start_vars = {}
        end_vars = {}
        presence_vars = {}

        eligible_resources = []

        for resource in resources:

            if resource["skill"] != task["required_skill"]:
                continue

            eligible_resources.append(resource)

            rid = resource["resource_id"]

            presence = model.NewBoolVar(
                f"presence_{task_id}_{rid}"
            )

            start = model.NewIntVar(
                resource["shift_start"],
                resource["shift_end"],
                f"start_{task_id}_{rid}"
            )

            end = model.NewIntVar(
                resource["shift_start"],
                resource["shift_end"],
                f"end_{task_id}_{rid}"
            )

            interval = model.NewOptionalIntervalVar(
                start,
                task["duration"],
                end,
                presence,
                f"interval_{task_id}_{rid}"
            )

            model.Add(
                end <= resource["shift_end"]
            ).OnlyEnforceIf(presence)

            start_vars[rid] = start
            end_vars[rid] = end
            presence_vars[rid] = presence

            intervals_by_resource[rid].append(interval)

        task_vars[task_id] = {
            "start": start_vars,
            "end": end_vars,
            "presence": presence_vars
        }

        model.Add(
            sum(presence_vars.values()) == 1
        )

    # --------------------------------------------------
    # Resource conflicts
    # --------------------------------------------------

    for rid, intervals in intervals_by_resource.items():
        model.AddNoOverlap(intervals)

    # --------------------------------------------------
    # Precedence constraints
    # --------------------------------------------------

    for task in tasks:

        task_id = task["task_id"]

        for dep in task.get("dependencies", []):

            dep_data = task_vars[dep]
            cur_data = task_vars[task_id]

            dep_finish = model.NewIntVar(
                0,
                horizon,
                f"finish_{dep}_{task_id}"
            )

            cur_start = model.NewIntVar(
                0,
                horizon,
                f"startdep_{dep}_{task_id}"
            )

            model.AddMaxEquality(
                dep_finish,
                list(dep_data["end"].values())
            )

            model.AddMinEquality(
                cur_start,
                list(cur_data["start"].values())
            )

            model.Add(cur_start >= dep_finish)

    # --------------------------------------------------
    # Weighted lateness objective
    # --------------------------------------------------

    lateness_terms = []

    for task in tasks:

        task_id = task["task_id"]

        finish_var = model.NewIntVar(
            0,
            horizon,
            f"finish_{task_id}"
        )

        model.AddMaxEquality(
            finish_var,
            list(task_vars[task_id]["end"].values())
        )

        lateness = model.NewIntVar(
            0,
            horizon,
            f"lateness_{task_id}"
        )

        model.Add(
            finish_var - task["deadline"] <= lateness
        )

        model.Add(lateness >= 0)

        weight = task["priority"]

        lateness_terms.append(
            lateness * weight
        )

    model.Minimize(sum(lateness_terms))

    # --------------------------------------------------
    # Solve
    # --------------------------------------------------

    solver = cp_model.CpSolver()

    status = solver.Solve(model)

    schedule = []

    if status in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE
    ):

        for task in tasks:

            task_id = task["task_id"]

            for rid, presence in task_vars[task_id]["presence"].items():

                if solver.Value(presence):

                    schedule.append({
                        "task_id": task_id,
                        "resource_id": rid,
                        "start": solver.Value(
                            task_vars[task_id]["start"][rid]
                        ),
                        "end": solver.Value(
                            task_vars[task_id]["end"][rid]
                        )
                    })

    return schedule