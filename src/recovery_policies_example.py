from alter_tree import AlterTree

toolset = AlterTree()
contingency = toolset.contingency_name
# when there is contingency, there will always be contingency_plan node that is empty
planning_node = toolset.contingency_plan['id']
completed_task_list = []
# There should not be a duplicate node ids

# Be sure to notice whether it is problem with assembly parts or agents
def recover_ATV_defective_rear_left_wheel():
    # add a node to planning node
    toolset.add_node(planning_node, "recovery-defective_rear_left_wheel", "sequential")
    toolset.add_node("recovery-defective_rear_left_wheel", "recovery-unscrew_operation", "sequential")
    # This screw is for the ATV which robot is performing
    toolset.add_node("recovery-unscrew_operation", "recovery-unscrew_rear_left_wheel_screw1", "atomic", agent='I_r12', duration=6)
    toolset.add_node("recovery-unscrew_operation", "recovery-unscrew_rear_left_wheel_screw2", "atomic", agent='I_r12', duration=8)
    toolset.add_node("recovery-unscrew_operation", "recovery-unscrew_rear_left_wheel_screw3", "atomic", agent='I_r12', duration=8)
    toolset.add_node("recovery-defective_rear_left_wheel", "recovery-remove_rear_left_wheel", "atomic", agent='I_r12', duration=8)
    toolset.add_node("recovery-defective_rear_left_wheel", "recovery-new_wheel", "sequential")
    toolset.add_node("recovery-new_wheel", "recovery-search_new_wheel", "atomic", agent='I_r12', duration=8)
    toolset.add_node("recovery-new_wheel", "recovery-pick_new_wheel", "atomic", agent='I_r12', duration=7)
    toolset.add_node("recovery-new_wheel", "recovery-place_new_wheel", "atomic", agent='I_r12', duration=7)
    toolset.add_node("recovery-defective_rear_left_wheel", "recovery-resrew_operation", "sequential")
    toolset.add_node("recovery-resrew_operation", "recovery-rescrew_rear_left_wheel_screw1", "atomic", agent='I_r12', duration=6)
    toolset.add_node("recovery-resrew_operation", "recovery-rescrew_rear_left_wheel_screw2", "atomic", agent='I_r12', duration=6)
    toolset.add_node("recovery-resrew_operation", "recovery-rescrew_rear_left_wheel_screw3", "atomic", agent='I_r12', duration=6)
    toolset.export_new_htn()


def ATV_assembly_screw1_stuck():
    # screw is stuck so it should be reattempted
    toolset.add_node(planning_node, "recovery-ATV_assembly_screw1_stuck", "sequential")
    toolset.add_node("recovery-ATV_assembly_screw1_stuck", "recovery-unscrew_screw1", "atomic", agent='I_r12', duration=4)
    toolset.add_node("recovery-ATV_assembly_screw1_stuck", "recovery-rescrew_screw1", "atomic", agent='I_r12', duration=6)
    toolset.export_new_htn()


def broken_ATV_upper_cover():
    toolset.add_node(planning_node, "recovery-broken_upper_body_frame", "sequential")
    toolset.add_node("recovery-broken_upper_body_frame", "recovery-remove_broken_pieces", "atomic", agent="G_r9", duration=6)
    toolset.add_node("recovery-broken_upper_body_frame", "recovery-new_upper_body_frame", "sequential")
    toolset.add_node("recovery-new_upper_body_frame", "recovery-search_for_new_part", "atomic", agent="G_r9", duration=6)
    toolset.add_node("recovery-new_upper_body_frame", "recovery-pick_new_part", "atomic", agent="G_r9", duration=6)
    toolset.export_new_htn()


def agent_J_r13_motor_defective():
    # This is a agent's problem which human should resolve
    toolset.add_node(planning_node, "recovery-agent_motor_defective", "sequential")
    toolset.add_node("recovery-agent_motor_defective", "recovery-wait_for_repair", "atomic", agent="J_r13", duration=6)
    # Notice that human from the same cell J is resolving the issue for J_r13
    toolset.add_node("recovery-agent_motor_defective", "recovery-replacement", "sequential")
    # agent is human because human is recovering J_r13 from contingency
    toolset.add_node("recovery-replacement", "recovery-repair_motor", "atomic", agent="J_H8", duration=70)
    toolset.add_node("recovery-replacement", "recovery-notify_monitor_of_completion", "atomic", agent="J_H8", duration=6)
    toolset.export_new_htn()

def agent_J_r13_software_malfunction():
    # This is a agent's problem which human should resolve
    toolset.add_node(planning_node, "recovery-agent_J_r13_software_malfunction", "sequential")
    # Human resolves any malfuction with the agent or bug with software
    toolset.add_node("recovery-agent_J_r13_software_malfunction", "recovery-restart_computer", "atomic", agent="H2", duration=6)
    # Human resolves any malfuction with the agent or bug with software
    toolset.add_node("recovery-agent_motor_defective", "recovery-notify_monitor", "atomic", agent="H2", duration=6)
    toolset.export_new_htn()

def A_r1_recovered():
    toolset.set_agent_state("A_r1", 'available')

def r3_not_available(agent):
    toolset.set_agent_state("r3", 'unavailable')

def recovery_ATV_trunk_missing():
    # trunk is missing
    toolset.add_node(planning_node, "recovery-trunk_missing", "sequential")
    toolset.add_node("recovery-trunk_missing", "recovery-notify_monitor", "atomic", agent="I_r11", duration=10)
    toolset.add_node("recovery-trunk_missing", "recovery-new_trunk_skeleton", "sequential")
    toolset.add_node("recovery-new_trunk_skeleton", "recovery-wait_for_new_part", "atomic", agent="I_r11", duration=12)
    # human gets the new part
    toolset.add_node("recovery-new_trunk_skeleton", "recovery-retrieve_new_trunk", "atomic", agent="H2", duration=12)
    toolset.add_node("recovery-new_trunk_skeleton", "recovery-locate_new_part", "atomic", agent="I_r11", duration=12)
    toolset.export_new_htn()

def recovery_ATV_handle_bolt3_missing():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-handle_bolt3_missing", "sequential")
    # human retrieves new part
    # robot only notifies human
    toolset.add_node("recovery-handle_bolt3_missing", "recovery-notify_human_for_new_bolt", "atomic", agent='G_r8', duration=6)
    toolset.add_node("recovery-search_screw", "recovery-notify_monitor", "atomic", agent='G_r8', duration=6)
    toolset.export_new_htn()


def shorted_ATV_battery():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-shorted_battery", "sequential")
    
    # Step 1: Remove the damaged part
    toolset.add_node("recovery-shorted_battery", "recovery-move_to_contingency_cell_for_undo", "atomic", agent='m1', duration=6, order_number=0)
    
    # Step 2: Check the damage
    toolset.add_node("recovery-shorted_battery", "recovery-shorted_battery_undo", "atomic", agent='contingency_H', duration=6, order_number=1)
    
    # Step 3: Replace with a new part
    toolset.add_node("recovery-shorted_battery", "recovery-return_to_battery_cell", "atomic", agent='m1', duration=8, order_number=2)
    
    # Export the new HTN
    toolset.export_new_htn()

def recovery_mobile_platform_m1_wheel_stuck():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-m1_wheel_stuck", "sequential")
  
    # Step 1: Unscrew the stuck wheel
    toolset.add_node("recovery-m1_wheel_stuck", "recovery-unscrew_wheel", "atomic", agent='H2', duration=8)
    
    # Step 2: Check for any damage
    toolset.add_node("recovery-m1_wheel_stuck", "recovery-check_for_damage", "atomic", agent='H2', duration=6)
    
    # Step 3: Replace the wheel with a new one
    toolset.add_node("recovery-m1_wheel_stuck", "recovery-replace_wheel", "atomic", agent='H2', duration=8)
    
    # Export the new HTN
    toolset.export_new_htn()
def recovery_mobile_platform_m1_navigation_error():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-m1_navigation_error", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-m1_navigation_error", "recovery-notify_human", "atomic", agent='m1', duration=6)
    
    # Step 2: Wait for human to resolve the navigation error
    toolset.add_node("recovery-m1_navigation_error", "recovery-wait_for_navigation_fix", "atomic", agent='m1', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()
def ATV_chassis_screw_stuck():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-chassis_screw_stuck", "sequential")
    
    # Step 1: Unscrew the stuck chassis screw
    toolset.add_node("recovery-chassis_screw_stuck", "recovery-unscrew_chassis_screw", "atomic", agent='A_r1', duration=6)
    
    # Step 2: Check for any damage
    toolset.add_node("recovery-chassis_screw_stuck", "recovery-check_for_damage", "atomic", agent='A_r1', duration=6)
    
    # Step 3: Rescrew the chassis screw
    toolset.add_node("recovery-chassis_screw_stuck", "recovery-rescrew_chassis_screw", "atomic", agent='A_r1', duration=8)
    
    # Export the new HTN
    toolset.export_new_htn()

def m1_collision_with_human():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-m1_collision_with_human", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-m1_collision_with_human", "recovery-notify_human", "atomic", agent='m1', duration=10)

    # Step 2: Wait for human to resolve the collision
    toolset.add_node("recovery-m1_collision_with_human", "recovery-wait_for_collision_fix", "atomic", agent='m1', duration=0)

    # Export the new HTN
    toolset.export_new_htn()

def A_r1_collision_with_table():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-A_r1_collision_with_table", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-A_r1_collision_with_table", "recovery-notify_human", "atomic", agent='A_r1', duration=6)

    # Step 2: Wait for human to resolve the collision
    toolset.add_node("recovery-A_r1_collision_with_table", "recovery-wait_for_collision_fix", "atomic", agent='A_r1', duration=0)

    # Export the new HTN
    toolset.export_new_htn()
def whole_cell_power_outage():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-whole_cell_power_outage", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-whole_cell_power_outage", "recovery-notify_superviser", "atomic", agent='H2', duration=6)

    # Step 2: Wait for human to resolve the power outage
    toolset.add_node("recovery-whole_cell_power_outage", "recovery-wait_for_power_fix", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()