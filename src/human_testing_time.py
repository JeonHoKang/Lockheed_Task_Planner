
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