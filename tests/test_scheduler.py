from smart_factory_mrs.simulation import FactorySimulation


def test_urgent_task_gets_inserted_and_assigned():
    simulation = FactorySimulation()
    simulation.scheduler.reschedule(simulation.time)

    logs = simulation.apply_event("3")

    assert any("urgent task inserted" in line for line in logs)
    urgent = next(task for task in simulation.scheduler.tasks if task.product == "X")
    assert urgent.assigned_robot is not None


def test_sequence_change_moves_v3_before_v2():
    simulation = FactorySimulation()

    simulation.apply_event("1")
    order = {
        task.product: task.sequence_index
        for task in simulation.scheduler.tasks
        if task.product in {"V1", "V2", "V3"}
    }

    assert order["V1"] < order["V3"] < order["V2"]
