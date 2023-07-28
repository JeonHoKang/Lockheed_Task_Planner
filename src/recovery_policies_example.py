from alter_tree import AlterTree

toolset = AlterTree()
contingency = toolset.contingency_name
# when there is contingency, there will always be contingency_plan node that is empty
planning_node = toolset.contingency_plan['id']
completed_task_list = []
# There should not be a duplicate node ids

def recover_screw_stuck():
    # add a node to planning node
    toolset.add_node(planning_node, "recovery-screw_stuck", "sequential")
    # screw stuck
    toolset.add_node("recovery-screw_stuck", "recovery-unscerw", "atomic", agent='r3', duration=6, order_number=0)
    toolset.add_node("recovery-screw_stuck", "recovery-rescrew", "atomic", agent='r3', duration=8, order_number=1)
    toolset.export_new_htn()


def dropped_part():
    toolset.add_node(planning_node, "recovery-dropped_part", "sequential")
    toolset.add_node("recovery-dropped_part", "recovery-search_dropped_part", "sequential")
    toolset.add_node("recovery-search_dropped_part", "recovery-scan_the_workspace", "atomic", agent='r2', duration=6,
                     order_number=0)
    toolset.add_node("recovery-search_dropped_part", "recovery-notify_monitor", "atomic", agent='r2', duration=6,
                     order_number=1)
    toolset.export_new_htn()


def engine_failure():
    toolset.add_node(planning_node, "recovery-engine_failure", "sequential")
    toolset.add_node("recovery-engine_failure", "recovery-undo_completed_tasks", "atomic", agent="H", duration=6, order_number=0)
    toolset.add_node("recovery-engine_failure", "recovery-get_new_engine", "sequential", order_number=1)
    toolset.add_node("recovery-get_new_engine", "recovery-search_current_workspace", "atomic", agent="r1", duration=6, order_number=0)
    toolset.add_node("recovery-get_new_engine", "recovery-locate_new_engine", "atomic", agent="r1", duration=6, order_number=1)
    toolset.add_node("recovery-get_new_engine", "recovery-pick_new_engine", "atomic", agent="r1", duration=6, order_number=2)
    toolset.add_node("recovery-get_new_engine", "recovery-insert_new_engine", "atomic", agent="r1", duration=8, order_number=3)
    toolset.add_node("recovery-engine_failure", "recovery-redo_completed_task_engine", "atomic", agent="H", duration=6, order_number=2)


def agent_under_maintanance(agent):
    toolset.set_agent_state(agent, 'unavailable')


def agent_recovered(agent):
    toolset.set_agent_state(agent, 'available')


def part_missing():
    toolset.add_node(planning_node, "recovery-part_missing", "sequential")
    toolset.add_node("recovery-part_missing", "recovery-notify_human", "atomic", agent="r2", duration=6,
                     order_number=0)
    toolset.add_node("recovery-part_missing", "recovery-wait_for_part", "atomic", agent="r2", duration=6, order_number=1)
    toolset.add_node("recovery-part_missing", "")

def recovery_dropped_main_body():
    toolset.add_node(planning_node, "recovery-dropped_main_body", "sequential")
    toolset.add_node("recovery-dropped_main_body", "recovery-search_part", "sequential")
    toolset.add_node("recovery-search_part", "recovery-check_reachability", "atomic", agent='r1', duration=5,
                     order_number=0)
    toolset.add_node("recovery-search_part", "recovery-repick_part", "atomic", agent='r1', duration=3, order_number=1)
    toolset.add_node("recovery-dropped_main_body", "recovery-place_on_table", "atomic", agent='r1', duration=6,
                     table='b1', order_number=2)
    toolset.export_new_htn()