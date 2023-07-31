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


def r1_under_maintanance():
    toolset.set_agent_state("r1", 'unavailable')


def r1_recovered():
    toolset.set_agent_state("r1", 'available')

def r3_not_available(agent):
    toolset.set_agent_state("r3", 'unavailable')

def recovery_part_collision():
    toolset.add_node(planning_node, "recovery-part_collision", "sequential")
    toolset.add_node("recovery-part_collision", "recovery-move_away", "atomic", agent="r1", duration=10, order_number=0)
    toolset.add_node("recovery-part_collision", "recovery-check_damage", "atomic", agent="H", duration=6, order_number=1)
    toolset.add_node("recovery-part_collision", "recovery-reattempt_motion", "atomic", agent="r1", duration=12, order_number=2)
    toolset.export_new_htn()

def recovery_screw_not_found():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-screw_not_found", "sequential")
    
    # Step 1: Search for the missing screw
    toolset.add_node("recovery-screw_not_found", "recovery-search_screw", "sequential")
    toolset.add_node("recovery-search_screw", "recovery-scan_workspace", "atomic", agent='H', duration=6, order_number=0)
    toolset.add_node("recovery-search_screw", "recovery-notify_monitor", "atomic", agent='H', duration=6, order_number=1)
    
    # Step 2: Insert a new screw
    toolset.add_node("recovery-screw_not_found", "recovery-insert_new_screw", "atomic", agent='r1', duration=8, order_number=1)
    
    # Export the new HTN
    toolset.export_new_htn()


def recovery_damaged_part():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-damaged_part", "sequential")
    
    # Step 1: Remove the damaged part
    toolset.add_node("recovery-damaged_part", "recovery-remove_damaged_part", "atomic", agent='r2', duration=6, order_number=0)
    
    # Step 2: Check the damage
    toolset.add_node("recovery-damaged_part", "recovery-check_damage", "atomic", agent='H', duration=6, order_number=1)
    
    # Step 3: Replace with a new part
    toolset.add_node("recovery-damaged_part", "recovery-replace_part", "atomic", agent='r1', duration=8, order_number=2)
    
    # Export the new HTN
    toolset.export_new_htn()


def recovery_task_collision():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-task_collision", "sequential")
    
    # Step 1: Move away from the collision spot
    toolset.add_node("recovery-task_collision", "recovery-move_away", "atomic", agent='r1', duration=10, order_number=0)
    
    # Step 2: Retry the motion
    toolset.add_node("recovery-task_collision", "recovery-reattempt_motion", "atomic", agent='r1', duration=12, order_number=1)
    
    # Export the new HTN
    toolset.export_new_htn()


def recovery_Human_on_break():
    toolset.set_agent_state("H", 'unavailable')
    # code to handle recovery task when human agent is on break
