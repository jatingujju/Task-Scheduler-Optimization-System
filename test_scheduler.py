import pytest

from scheduler import greedy_scheduler
from cp_sat_scheduler import cp_sat_scheduler


# =====================================================
# TEST DATA
# =====================================================

@pytest.fixture
def sample_tasks():

    return [
        {
            "task_id": "T1",
            "duration": 2,
            "deadline": 12,
            "priority": 10,
            "required_skill": "Backend",
            "dependencies": []
        },
        {
            "task_id": "T2",
            "duration": 3,
            "deadline": 18,
            "priority": 8,
            "required_skill": "Backend",
            "dependencies": ["T1"]
        },
        {
            "task_id": "T3",
            "duration": 2,
            "deadline": 15,
            "priority": 7,
            "required_skill": "Frontend",
            "dependencies": []
        }
    ]


@pytest.fixture
def sample_resources():

    return [
        {
            "resource_id": "R1",
            "skill": "Backend",
            "shift_start": 9,
            "shift_end": 18
        },
        {
            "resource_id": "R2",
            "skill": "Frontend",
            "shift_start": 9,
            "shift_end": 17
        }
    ]


# =====================================================
# HELPERS
# =====================================================

def schedule_to_map(schedule):

    return {
        item["task_id"]: item
        for item in schedule
    }


def validate_dependency_order(schedule):

    plans = schedule_to_map(schedule)

    assert plans["T2"]["start"] >= plans["T1"]["end"]


def validate_skill_matching(schedule, resources, tasks):

    resource_skill = {
        r["resource_id"]: r["skill"]
        for r in resources
    }

    task_skill = {
        t["task_id"]: t["required_skill"]
        for t in tasks
    }

    for item in schedule:

        assert (
            resource_skill[item["resource_id"]]
            ==
            task_skill[item["task_id"]]
        )


def validate_shift_windows(schedule, resources):

    resource_map = {
        r["resource_id"]: r
        for r in resources
    }

    for item in schedule:

        resource = resource_map[
            item["resource_id"]
        ]

        assert (
            item["start"]
            >=
            resource["shift_start"]
        )

        assert (
            item["end"]
            <=
            resource["shift_end"]
        )


# =====================================================
# GREEDY TESTS
# =====================================================

def test_greedy_dependency_order(
    sample_tasks,
    sample_resources
):

    schedule = greedy_scheduler(
        sample_tasks,
        sample_resources
    )

    validate_dependency_order(
        schedule
    )


def test_greedy_skill_matching(
    sample_tasks,
    sample_resources
):

    schedule = greedy_scheduler(
        sample_tasks,
        sample_resources
    )

    validate_skill_matching(
        schedule,
        sample_resources,
        sample_tasks
    )


def test_greedy_shift_feasibility(
    sample_tasks,
    sample_resources
):

    schedule = greedy_scheduler(
        sample_tasks,
        sample_resources
    )

    validate_shift_windows(
        schedule,
        sample_resources
    )


# =====================================================
# CP-SAT TESTS
# =====================================================

def test_cpsat_dependency_order(
    sample_tasks,
    sample_resources
):

    schedule = cp_sat_scheduler(
        sample_tasks,
        sample_resources
    )

    validate_dependency_order(
        schedule
    )


def test_cpsat_skill_matching(
    sample_tasks,
    sample_resources
):

    schedule = cp_sat_scheduler(
        sample_tasks,
        sample_resources
    )

    validate_skill_matching(
        schedule,
        sample_resources,
        sample_tasks
    )


def test_cpsat_shift_feasibility(
    sample_tasks,
    sample_resources
):

    schedule = cp_sat_scheduler(
        sample_tasks,
        sample_resources
    )

    validate_shift_windows(
        schedule,
        sample_resources
    )