# Task Scheduler Optimization System

## Overview

The Task Scheduler Optimization System is a Data Structures and Algorithms (DSA) project designed to optimize task assignment and execution across available resources. The system supports dependency-aware scheduling, skill-based resource allocation, shift window constraints, KPI analytics, and schedule optimization using both Greedy and Constraint Programming (CP-SAT) approaches.

The project simulates real-world workforce and resource scheduling scenarios commonly found in software development, manufacturing, logistics, cloud computing, and project management systems.

---

## Objectives

* Schedule tasks efficiently across available resources.
* Respect task dependencies.
* Match tasks with appropriately skilled resources.
* Ensure tasks fit within resource shift windows.
* Minimize lateness and improve utilization.
* Compare heuristic and optimization-based scheduling approaches.
* Provide KPI analytics and scheduling insights.

---

## Features

### Greedy Scheduling Engine

* Priority-based scheduling
* Earliest deadline consideration
* Dependency-aware execution
* Fast schedule generation

### CP-SAT Optimization Engine

* Built using Google OR-Tools
* Constraint Programming optimization
* Resource assignment optimization
* Weighted lateness minimization

### Dependency Management

* Directed dependency graph
* Precedence constraints
* Topological execution ordering

### Skill-Based Resource Allocation

Tasks are assigned only to resources possessing the required skills.

### Shift Window Constraints

Resources can only perform tasks during their defined shift timings.

### KPI Analytics

The system computes:

* On-Time Completion Percentage
* Total Lateness Hours
* Resource Utilization Percentage

### What-If Analysis

Evaluate scheduling changes by:

* Adding new tasks
* Modifying resource shifts
* Re-running optimization

### SQLite Run Logging

Every scheduling run is automatically logged for future analysis.

### Automated Testing

Validation of:

* Dependency order
* Skill matching
* Shift-window feasibility

---

## System Architecture

```text
                FastAPI Backend
                       │
        ┌──────────────┼──────────────┐
        │                             │
        ▼                             ▼
 Greedy Scheduler            CP-SAT Scheduler
        │                             │
        └──────────────┬──────────────┘
                       ▼
                Schedule Plan
                       │
                       ▼
                 KPI Analytics
                       │
                       ▼
                SQLite Logging
```

## DSA Concepts Used

### Graphs

Used for dependency management between tasks.

### Topological Ordering

Ensures dependent tasks execute in valid order.

### Priority Queue (Heap)

Used by the Greedy Scheduler for efficient task selection.

### Greedy Algorithms

Used to generate fast scheduling solutions.

### Constraint Satisfaction

Implemented using OR-Tools CP-SAT Solver.

### Hash Maps

Used for task lookup and resource mapping.

---

## Project Structure

```text
Task-Scheduler-Optimization-System/
│
├── app.py
├── scheduler.py
├── cp_sat_scheduler.py
├── metrics.py
├── test_scheduler.py
├── requirements.txt
├── README.md
├── scheduler.db
│
├── data/
│   ├── tasks.csv
│   └── resources.csv
│
└── screenshots/
    ├── api_home.png
    ├── solve_success.png
    ├── health_endpoint.png
    ├── runs_endpoint.png
    └── test_results.png
```

---

## API Endpoints

### POST /solve

Generates a schedule using either:

* Greedy Scheduler
* CP-SAT Scheduler

Returns:

* Schedule Plan
* KPI Metrics

---

### POST /whatif

Performs schedule simulation by:

* Adding tasks
* Modifying shifts
* Re-optimizing schedules

---

### GET /runs

Displays historical scheduling runs stored in SQLite.

---

### GET /health

Health-check endpoint.

Example:

```json
{
  "status": "running"
}
```

---

## KPI Metrics

### On-Time Completion %

Percentage of tasks completed before deadlines.

### Total Lateness Hours

Total delay accumulated across all tasks.

### Resource Utilization %

Measures how effectively resources are being utilized.

---

## Sample Tasks CSV

```csv
task_id,task_name,duration,deadline,priority,required_skill,dependencies
T1,Database Setup,4,12,9,Backend,
T2,Frontend Design,3,15,7,Frontend,
T3,API Development,5,20,10,Backend,T1
T4,Testing,2,18,6,QA,T3
```

---

## Sample Resources CSV

```csv
resource_id,resource_name,skill,shift_start,shift_end
R1,Alice,Backend,9,18
R2,Bob,Frontend,9,18
R3,Charlie,QA,9,18
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Task-Scheduler-Optimization-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start FastAPI:

```bash
uvicorn app:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Running Tests

```bash
pytest test_scheduler.py -v
```

Expected Output:

```text
6 passed
```

---

## Optimization Settings

### Objective

Weighted Lateness Minimization

### Constraints

* Dependency Constraints
* Skill Constraints
* Shift Window Constraints

### Solver Configuration

* Timeout: 10 Seconds
* Search Workers: 4
* Priority-Based Weighting

---

## Test Results

Validated Successfully:

* Dependency Order
* Skill Matching
* Shift Feasibility
* Greedy Scheduler Correctness
* CP-SAT Scheduler Correctness

---

## Applications

This system can be applied to:

* Workforce Scheduling
* Manufacturing Planning
* Software Project Management
* Cloud Resource Scheduling
* Logistics Operations
* Maintenance Planning

---

## Future Enhancements

### 1. Calendar and PTO Integration

Integrate employee calendars and leave schedules.

Features:

* Vacation tracking
* Holiday management
* Resource availability forecasting

---

### 2. Multi-Skill Task Scheduling

Support tasks requiring multiple skills and multiple resources simultaneously.

Example:

* Backend
* Database
* DevOps

---

### 3. Setup and Changeover Times

Account for preparation time before task execution.

Useful in:

* Manufacturing
* Deployment pipelines
* Production systems

---

### 4. Travel Time Constraints

Include travel duration between task locations.

Useful in:

* Field services
* Logistics
* Delivery scheduling

---

### 5. Time-Dependent Penalties

Apply increasing penalties as lateness grows.

Benefits:

* Better deadline management
* Improved prioritization

---

### 6. Rolling Horizon Re-Optimization

Continuously update schedules when:

* New tasks arrive
* Deadlines change
* Resources become unavailable

This enables real-time scheduling and adaptive planning.

---

## Author

Jatin Gujarathi

B.Tech Mechanical Engineering

Task Scheduler Optimization System – DSA Project
