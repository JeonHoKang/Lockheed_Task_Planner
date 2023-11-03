
from alter_tree import AlterTree

toolset = AlterTree()
contingency = toolset.contingency_name
# when there is contingency, there will always be contingency_plan node that is empty
planning_node = toolset.contingency_plan['id']
completed_task_list = []
# There should not be a duplicate node ids

def agent_under_maintanance():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-agent_under_maintanance", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-agent_under_maintanance", "recovery-wait_for_maintanance", "atomic", agent='A_r1', duration=6)

    # Step 2: Wait for human to realign the frame to the chassis
    toolset.add_node("recovery-agent_under_maintanance", "recovery-notify_monitor_completion", "atomic", agent='H2', duration=10)

    # Export the new HTN
    toolset.export_new_htn()


def agent_under_maintanance():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-agent_under_maintanance", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-agent_under_maintanance", "recovery-wait_for_maintanance", "atomic", agent='A_r1', duration=6)

    # Step 2: Wait for human to realign the frame to the chassis
    toolset.add_node("recovery-agent_under_maintanance", "recovery-notify_monitor_completion", "atomic", agent='H2', duration=10)

    # Export the new HTN
    toolset.export_new_htn()

def A_r1_agent_controller_failure():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-agent_controller_failure", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-agent_controller_failure", "recovery-check_agent_controller", "atomic", agent='A_r1', duration=6)

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-agent_controller_failure", "recovery-controller_replacement", "atomic", agent='A_r1', duration=6)

    # Step 2: Wait for human to realign the frame to the chassis
    toolset.add_node("recovery-agent_under_maintanance", "recovery-notify_monitor_completion", "atomic", agent='H2', duration=10)

    # Export the new HTN
    toolset.export_new_htn()

def human_on_break():
    toolset.set_agent_state("A_r1", 'unavailable')

def gripper_stuck():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-gripper_stuck", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-gripper_stuck", "recovery-release_gripper", "atomic", agent='A_r1',
                     duration=6)

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-agent_controller_failure", "recovery-check_for_error", "atomic", agent='A_H1',
                     duration=6)

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-agent_controller_failure", "recovery-check_gripper_functionality", "atomic", agent='A_H1',
                     duration=6)
    # Step 2: Wait for human to realign the frame to the chassis
    toolset.add_node("recovery-agent_controller_failure", "recovery-notify_monitor_completion", "atomic", agent='A_r1',
                     duration=10)

    # Export the new HTN
    toolset.export_new_htn()

def overheated_actuator():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-overheated_actuator", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-overheated_actuator", "recovery-notify_monitor", "atomic", agent='A_r1',
                     duration=6)

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-overheated_actuator", "recovery-resolve_actuator_issue", 'sequential')

    toolset.add_node("recovery-resolve_actuator_issue", "recovery-check_for_error", "atomic", agent='A_H1',
                     duration=6)

    toolset.add_node("recovery-resolve_actuator_issue", "recovery-reset_actuator", "atomic", agent='A_H1',
                     duration=10)
    toolset.add_node("recovery-overheated_actuator", "recovery-notify_monitor_for_completion", "atomic", agent='A_H1',
                     duration=6)

    # Export the new HTN
    toolset.export_new_htn()


def communication_delay():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-communication_delay", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-communication_delay", "recovery-notify_monitor", "atomic", agent='A_r1',
                     duration=6)

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-communication_delay", "recovery-resolve_comm_error", 'sequential')

    toolset.add_node("recovery-resolve_comm_error", "recovery-check_for_error", "atomic", agent='A_H1',
                     duration=6)

    toolset.add_node("recovery-resolve_comm_error", "recovery-restart_computer", "atomic", agent='A_H1',
                     duration=10)
    toolset.add_node("recovery-overheated_actuator", "recovery-notify_monitor_for_completion", "atomic", agent='A_H1',
                     duration=6)

    # Export the new HTN
    toolset.export_new_htn()

def I_r12_wheel_screw_stuck():
    toolset.add_node(planning_node, "recovery-I_r12_wheel_screw_stuck", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-I_r12_wheel_screw_stuck", "recovery-unscrew_wheel_screw", "atomic", agent='I_r12',
                     duration=6)

    toolset.add_node("recovery-unscrew_wheel_screw", "recovery-check_for_damage", "atomic", agent='I_r12',
                     duration=6)

    toolset.add_node("recovery-resolve_comm_error", "recovery-rescrew_wheel", "atomic", agent='I_r12',
                     duration=10)


    # Export the new HTN
    toolset.export_new_htn()

def rodent_present():
    toolset.add_node(planning_node, "recovery-rodent_present", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-rodent_present", "recovery-notify_human", "atomic", agent='I_r12',
                     duration=6)

    toolset.add_node("recovery-notify_human", "recovery-resolve_issue", "atomic", agent='I_r12',
                     duration=6)


    # Export the new HTN
    toolset.export_new_htn()


def fire_in_cell_B():
    toolset.add_node(planning_node, "recovery-fire_in_cell_B", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-fire_in_cell_B", "recovery-notify_human", "atomic", agent='I_r12',
                     duration=6)

    toolset.add_node("recovery-fire_in_cell_B", "recovery-examine_fire", "atomic", agent='I_r12',
                     duration=6)

    toolset.add_node("recovery-fire_in_cell_B", "recovery-small_fire_then_put_out_fire", "atomic", agent='I_r12',
                     duration=6)
    toolset.add_node("recovery-fire_in_cell_B", "recovery-inspect_and_notify_monitor", "atomic", agent='I_r12',
                     duration=6)
    # Export the new HTN
    toolset.export_new_htn()

def crak_in_the_outer_frame():
    toolset.add_node(planning_node, "recovery-crak_in_the_outer_frame", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-crak_in_the_outer_frame", "recovery-inspect_crack", "atomic", agent='A_r2',
                     duration=6)

    toolset.add_node("recovery-crak_in_the_outer_frame", "recovery-replace_part", "atomic", agent='A_r2',
                     duration=6)

    toolset.add_node("recovery-crak_in_the_outer_frame", "recovery-search_new_part", "atomic", agent='A_r2',
                     duration=6)
    toolset.add_node("recovery-crak_in_the_outer_frame", "recovery-pick_new_part", "atomic", agent='A_r2',
                     duration=6)
    toolset.add_node("recovery-crak_in_the_outer_frame", "recovery-notify_monitor", "atomic", agent='A_r2',
                     duration=6)
    # Export the new HTN
    toolset.export_new_htn()

def incorrect_screw_size ():
    toolset.add_node(planning_node, "recovery-incorrect_screw_size", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-incorrect_screw_size", "recovery-remove_incorrect_screw", "atomic", agent='A_r2',
                     duration=6)

    toolset.add_node("recovery-incorrect_screw_size", "recovery-replace_incorrect_screw", "atomic", agent='H2',
                     duration=6)

    toolset.add_node("recovery-incorrect_screw_size", "recovery-new_screw", "sequential")

    toolset.add_node("recovery-new_screw", "recovery-locate_new_screw", "atomic", agent='A_r2',
                     duration=6)
    toolset.add_node("recovery-new_screw", "recovery-repick_correct_screw", "atomic", agent='A_r2',
                     duration=6)
    toolset.add_node("recovery-incorrect_screw_size", "recovery-notify_monitor", "atomic", agent='A_r2',
                     duration=6)
    # Export the new HTN
    toolset.export_new_htn()

def engine_leaking ():
    toolset.add_node(planning_node, "recovery-engine_leaking", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-engine_leaking", "recovery-undo_engine_from_assembly", "atomic", agent='A_r2',
                     duration=6)

    toolset.add_node("recovery-engine_leaking", "recovery-pick_faulty_engine", "atomic", agent='A_r2',
                     duration=6)
    toolset.add_node("recovery-engine_leaking", "recovery-set_aside_faulty_engine", "atomic", agent='A_r2',
                     duration=6)
    toolset.add_node("recovery-engine_leaking", "recovery-new_engine", "atomic", agent='A_r2',
                     duration=6)

    toolset.add_node("recovery-new_engine", "recovery-locate_new_engine", "atomic", agent='A_r2',
                     duration=6)

    toolset.add_node("recovery-new_engine", "recovery-pick_new_engine", "atomic", agent='A_r2',
                     duration=6)
    toolset.add_node("recovery-new_engine", "recovery-notify_monitor", "atomic", agent='A_r2',
                     duration=6)
    # Export the new HTN
    toolset.export_new_htn()