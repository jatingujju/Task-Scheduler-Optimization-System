from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
from datetime import datetime

from scheduler import greedy_scheduler
from cp_sat_scheduler import cp_sat_scheduler
from metrics import calculate_kpis

app = FastAPI(
    title="Task Scheduler Optimization System"
)

# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect(
    "scheduler.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    engine TEXT,
    input_data TEXT,
    result_data TEXT
)
""")

conn.commit()

# =====================================================
# MODELS
# =====================================================

class Task(BaseModel):
    task_id: str
    duration: int
    deadline: int
    priority: int
    required_skill: str
    dependencies: Optional[List[str]] = []


class Resource(BaseModel):
    resource_id: str
    skill: str
    shift_start: int
    shift_end: int


class SolveRequest(BaseModel):
    engine: str
    tasks: List[Task]
    resources: List[Resource]


class WhatIfRequest(BaseModel):
    engine: str
    tasks: List[Task]
    resources: List[Resource]

    add_task: Optional[Task] = None

    resource_update: Optional[Resource] = None


# =====================================================
# LOGGING
# =====================================================

def log_run(engine, payload, result):

    cursor.execute(
        """
        INSERT INTO runs
        (
            timestamp,
            engine,
            input_data,
            result_data
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            datetime.now().isoformat(),
            engine,
            json.dumps(payload),
            json.dumps(result)
        )
    )

    conn.commit()


# =====================================================
# SOLVER HELPER
# =====================================================

def run_solver(engine, tasks, resources):

    if engine.lower() == "cp-sat":
        schedule = cp_sat_scheduler(
            tasks,
            resources
        )
    else:
        schedule = greedy_scheduler(
            tasks,
            resources
        )

    kpis = calculate_kpis(
        schedule,
        resources
    )

    return {
        "schedule": schedule,
        "kpis": kpis
    }


# =====================================================
# /solve
# =====================================================

@app.post("/solve")
def solve(request: SolveRequest):

    tasks = [
        t.dict()
        for t in request.tasks
    ]

    resources = [
        r.dict()
        for r in request.resources
    ]

    result = run_solver(
        request.engine,
        tasks,
        resources
    )

    log_run(
        request.engine,
        request.dict(),
        result
    )

    return result


# =====================================================
# /whatif
# =====================================================

@app.post("/whatif")
def whatif(request: WhatIfRequest):

    tasks = [
        t.dict()
        for t in request.tasks
    ]

    resources = [
        r.dict()
        for r in request.resources
    ]

    # -----------------------------
    # Add New Task
    # -----------------------------

    if request.add_task:

        tasks.append(
            request.add_task.dict()
        )

    # -----------------------------
    # Update Resource Shift
    # -----------------------------

    if request.resource_update:

        updated = request.resource_update.dict()

        for idx, resource in enumerate(resources):

            if (
                resource["resource_id"]
                == updated["resource_id"]
            ):
                resources[idx] = updated
                break

    result = run_solver(
        request.engine,
        tasks,
        resources
    )

    log_run(
        f"whatif-{request.engine}",
        request.dict(),
        result
    )

    return result


# =====================================================
# RUN HISTORY
# =====================================================

@app.get("/runs")
def runs():

    rows = cursor.execute(
        """
        SELECT
            id,
            timestamp,
            engine
        FROM runs
        ORDER BY id DESC
        """
    ).fetchall()

    return rows


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health():

    return {
        "status": "running"
    }