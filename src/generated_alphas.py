
from alter_tree import AlterTree

toolset = AlterTree()
contingency = toolset.contingency_name
# when there is contingency, there will always be contingency_plan node that is empty
planning_node = toolset.contingency_plan['id']
completed_task_list = []
# There should not be a duplicate node ids

# Be sure to notice whether it is problem with assembly parts or agents
def ATV_I_r11_Dropped_screw():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-I_r11_dropped_screw", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-I_r11_dropped_screw", "recovery-notify_human", "atomic", agent='H2', duration=6)
    
    # Step 2: Wait for human to pick up and place the screw back
    toolset.add_node("recovery-I_r11_dropped_screw", "recovery-wait_for_human", "atomic", agent='H2', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()def ATV_m1_unstable_mounting_of_ATV():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-m1_unstable_mounting_of_ATV", "sequential")
    
    # Step 1: Check the mounting of the ATV
    toolset.add_node("recovery-m1_unstable_mounting_of_ATV", "recovery-check_mounting", "atomic", agent='m1', duration=6)
    
    # Step 2: Repair the mounting of the ATV
    toolset.add_node("recovery-m1_unstable_mounting_of_ATV", "recovery-repair_mounting", "atomic", agent='m1', duration=8)
    
    # Export the new HTN
    toolset.export_new_htn()


def ATV_misaligned_frame_to_chassis():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-misaligned_frame_to_chassis", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-misaligned_frame_to_chassis", "recovery-notify_human", "atomic", agent='H2', duration=6)

    # Step 2: Wait for human to realign the frame to the chassis
    toolset.add_node("recovery-misaligned_frame_to_chassis", "recovery-wait_for_human", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()
def ATV_misaligned_frame_to_chassis():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-misaligned_frame_to_chassis", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-misaligned_frame_to_chassis", "recovery-notify_human", "atomic", agent='H2', duration=6)

    # Step 2: Wait for human to resolve the misalignment issue
    toolset.add_node("recovery-misaligned_frame_to_chassis", "recovery-wait_for_alignment_fix", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()
def ATV_A_r1_misaligned_frame_to_chassis():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-misaligned_frame_to_chassis", "sequential")
    
    # Step 1: Unscrew the misaligned frame
    toolset.add_node("recovery-misaligned_frame_to_chassis", "recovery-unscrew_frame", "atomic", agent='A_r1', duration=6)
    
    # Step 2: Realign the frame to the chassis
    toolset.add_node("recovery-misaligned_frame_to_chassis", "recovery-realign_frame", "atomic", agent='A_r1', duration=8)
    
    # Step 3: Rescrew the frame to the chassis
    toolset.add_node("recovery-misaligned_frame_to_chassis", "recovery-rescrew_frame", "atomic", agent='A_r1', duration=8)
    
    # Export the new HTN
    toolset.export_new_htn()
def ATV_dropped_from_m1_mobile_platform():
    toolset.add_node(planning_node, "recovery-ATV_dropped", "sequential")
    toolset.add_node("recovery-ATV_dropped", "recovery-check_for_damage", "atomic", agent='H2', duration=10)
    toolset.export_new_htn()def invalid_path_for_m1_moving_platform():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-invalid_path_m1", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-invalid_path_m1", "recovery-notify_human", "atomic", agent='H2', duration=6)
    
    # Step 2: Wait for human to resolve the invalid path issue for m1
    toolset.add_node("recovery-invalid_path_m1", "recovery-wait_for_path_fix", "atomic", agent='H2', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()
def invalid_motion_plan_for_I_r13_arm():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-invalid_motion_plan_for_I_r13_arm", "sequential")
  
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-invalid_motion_plan_for_I_r13_arm", "recovery-notify_human", "atomic", agent='H2', duration=6)
    
    # Step 2: Wait for human to resolve the motion plan issue
    toolset.add_node("recovery-invalid_motion_plan_for_I_r13_arm", "recovery-wait_for_resolution", "atomic", agent='H2', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()
def A_r1_arm_collided_with_assembly_part():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-collision_arm_assembly", "sequential")
    
    # Step 1: Move the arm away from the assembly part
    toolset.add_node("recovery-collision_arm_assembly", "recovery-move_arm_away", "atomic", agent='A_r1', duration=8)
    
    # Step 2: Check for any damage
    toolset.add_node("recovery-collision_arm_assembly", "recovery-check_for_damage", "atomic", agent='A_r1', duration=6)
    
    #Step 3: Return to the previous step in the HTN
    toolset.export_new_htn()
def human_on_the_way_of_path_m1():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-human_on_the_way_of_path_m1", "sequential")
    
    # Step 1: Notify the human to clear the path
    toolset.add_node("recovery-human_on_the_way_of_path_m1", "recovery-notify_human", "atomic", agent='H2', duration=6)
    
    # Step 2: Wait for the human to clear the path
    toolset.add_node("recovery-human_on_the_way_of_path_m1", "recovery-wait_for_path_clearance", "atomic", agent='m1', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()def m1_mobile_base_collision_with_wall():
    toolset.add_node(planning_node, "recovery-m1_mobile_base_collision_with_wall", "sequential")
    
    # Step 1: Check for any damage or obstruction
    toolset.add_node("recovery-m1_mobile_base_collision_with_wall", "recovery-check_for_damage_or_obstruction", "atomic", agent='m1', duration=6)
    
    # Step 2: Move the mobile base away from the wall
    toolset.add_node("recovery-m1_mobile_base_collision_with_wall", "recovery-move_away_from_wall", "atomic", agent='m1', duration=8)
    
    # Export the new HTN
    toolset.export_new_htn()
def m1_collision_with_human():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-m1_collision_with_human", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-m1_collision_with_human", "recovery-notify_human", "atomic", agent='H2', duration=10)

    # Step 2: Wait for human to resolve the collision
    toolset.add_node("recovery-m1_collision_with_human", "recovery-wait_for_collision_fix", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()

# Call this function to complete the recovery task
def A_r1_collision_with_table():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-A_r1_collision_with_table", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-A_r1_collision_with_table", "recovery-notify_human", "atomic", agent='A_r1', duration=6)

    # Step 2: Wait for human to resolve the collision
    toolset.add_node("recovery-A_r1_collision_with_table", "recovery-wait_for_collision_fix", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()

def A_r1_unreachable_part():
    toolset.add_node(planning_node, "recovery-A_r1_unreachable_part", "sequential")
    toolset.add_node("recovery-A_r1_unreachable_part", "recovery-wait_for_access", "atomic", agent='A_r1', duration=10)
    toolset.add_node("recovery-A_r1_unreachable_part", "recovery-move_to_access", "atomic", agent='A_r1', duration=8)
    toolset.export_new_htn()def A_r1_collided_with_A_r2():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-A_r1_collided_with_A_r2", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-A_r1_collided_with_A_r2", "recovery-notify_human", "atomic", agent='A_r1', duration=6)

    # Step 2: Wait for human to resolve the collision
    toolset.add_node("recovery-A_r1_collided_with_A_r2", "recovery-wait_for_collision_fix", "atomic", agent='A_r1', duration=0)

    # Export the new HTN
    toolset.export_new_htn()
def A_r1_crack_in_outer_frame():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-crack_in_outer_frame", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-crack_in_outer_frame", "recovery-notify_human", "atomic", agent='A_r1', duration=6)

    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-crack_in_outer_frame", "recovery-wait_for_resolution", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()def A_r1_crack_in_ATV_outer_frame():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-crack_in_ATV_outer_frame", "sequential")

    # Step 1: Assess the damage
    toolset.add_node("recovery-crack_in_ATV_outer_frame", "recovery-assess_damage", "atomic", agent='A_r1', duration=6)

    # Step 2: Repair the crack in the outer frame
    toolset.add_node("recovery-crack_in_ATV_outer_frame", "recovery-repair_crack", "atomic", agent='A_r1', duration=10)

    # Export the new HTN
    toolset.export_new_htn()
A_r1_crack_in_ATV_outer_frame()def StationB_insufficient_screw():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-insufficient_screw", "sequential")

    # Step 1: Notify the human about the insufficient screw
    toolset.add_node("recovery-insufficient_screw", "recovery-notify_human", "atomic", agent='B_r3', duration=6)

    # Step 2: Wait for human to provide the missing screw
    toolset.add_node("recovery-insufficient_screw", "recovery-wait_for_screw", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()
def StationB_wheel_not_present():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-wheel_not_present", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-wheel_not_present", "recovery-notify_human", "atomic", agent='B_r2', duration=6)

    # Step 2: Wait for human to provide the wheel
    toolset.add_node("recovery-wheel_not_present", "recovery-wait_for_wheel", "atomic", agent='H2', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()
def StationB_Wrong_part_present():
    toolset.add_node(planning_node, "recovery-wrong_part_present", "sequential")
    toolset.add_node("recovery-wrong_part_present", "recovery-remove_wrong_part", "atomic", agent='B_r2', duration=8)
    toolset.add_node("recovery-wrong_part_present", "recovery-replace_with_correct_part", "atomic", agent='B_r2', duration=8)
    toolset.export_new_htn()

def recover_ATV_flat_tire_rear_left_wheel():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-flat_tire_rear_left_wheel", "sequential")

    # Step 1: Remove the flat tire
    toolset.add_node("recovery-flat_tire_rear_left_wheel", "recovery-remove_flat_tire", "atomic", agent='I_r11', duration=10)

    # Step 2: Retrieve a new tire
    toolset.add_node("recovery-flat_tire_rear_left_wheel", "recovery-retrieve_new_tire", "atomic", agent='H2', duration=12)

    # Step 3: Install the new tire
    toolset.add_node("recovery-flat_tire_rear_left_wheel", "recovery-install_new_tire", "atomic", agent='I_r11', duration=10)

    # Export the new HTN
    toolset.export_new_htn()
def recover_incorrect_screw_size():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-incorrect_screw_size", "sequential")
    
    # Step 1: Unscrew the incorrect screw
    toolset.add_node("recovery-incorrect_screw_size", "recovery-unscrew_incorrect_screw", "atomic", agent='I_r12', duration=6)
    
    # Step 2: Check for any damage
    toolset.add_node("recovery-incorrect_screw_size", "recovery-check_for_damage", "atomic", agent='I_r12', duration=6)
    
    # Step 3: Rescrew the correct screw
    toolset.add_node("recovery-incorrect_screw_size", "recovery-rescrew_correct_screw", "atomic", agent='I_r12', duration=8)
    
    # Export the new HTN
    toolset.export_new_htn()
def recover_ATV_engine_part_defective():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-engine_part_defective", "sequential")

    # Step 1: Unscrew the defective part
    toolset.add_node("recovery-engine_part_defective", "recovery-unscrew_defective_part", "atomic", agent='A_r1', duration=6)

    # Step 2: Check for any damage
    toolset.add_node("recovery-engine_part_defective", "recovery-check_for_damage", "atomic", agent='A_r1', duration=6)

    # Step 3: Replace the defective part with a new one
    toolset.add_node("recovery-engine_part_defective", "recovery-replace_defective_part", "atomic", agent='A_H1', duration=8)

    # Export the new HTN
    toolset.export_new_htn()

def whole_cell_power_outage():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-whole_cell_power_outage", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-whole_cell_power_outage", "recovery-notify_human", "atomic", agent='H2', duration=6)

    # Step 2: Wait for human to resolve the power outage
    toolset.add_node("recovery-whole_cell_power_outage", "recovery-wait_for_power_fix", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()

def liquid_spill():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-liquid_spill", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-liquid_spill", "recovery-notify_human", "atomic", agent='H2', duration=6)

    # Step 2: Wait for human to clean the spill
    toolset.add_node("recovery-liquid_spill", "recovery-wait_for_cleanup", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()

def Fire_in_the_cell():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-fire_in_the_cell", "sequential")

    # Step 1: Evacuate the cell and notify the authorities
    toolset.add_node("recovery-fire_in_the_cell", "recovery-evacuate_cell", "atomic", agent='H2', duration=6)
    toolset.add_node("recovery-fire_in_the_cell", "recovery-notify_authorities", "atomic", agent='H2', duration=6)

    # Step 2: Wait for the fire to be extinguished and receive clearance to re-enter the cell
    toolset.add_node("recovery-fire_in_the_cell", "recovery-wait_for_clearance", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()

Fire_in_the_cell()

def earthquake_in_the_cell():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-earthquake_in_the_cell", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-earthquake_in_the_cell", "recovery-notify_superviser", "atomic", agent='H2', duration=6)

    # Step 2: Wait for human to resolve the situation after the earthquake
    toolset.add_node("recovery-earthquake_in_the_cell", "recovery-wait_for_earthquake_resolution", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()def software_hack():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-software_hack", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-software_hack", "recovery-notify_human", "atomic", agent='H2', duration=6)

    # Step 2: Wait for human to resolve the software hack
    toolset.add_node("recovery-software_hack", "recovery-wait_for_hack_fix", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()


def rodent_and_insect():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-rodent_and_insect", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-rodent_and_insect", "recovery-notify_human", "atomic", agent='H2', duration=6)
    
    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-rodent_and_insect", "recovery-wait_for_resolution", "atomic", agent='H2', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()
def war_broke_out_in_the_area():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-war_broke_out", "sequential")

    # Step 1: Notify the human supervisor immediately
    toolset.add_node("recovery-war_broke_out", "recovery-notify_supervisor", "atomic", agent='H2', duration=6)

    # Step 2: Evaluate the situation and assess the necessary actions
    toolset.add_node("recovery-war_broke_out", "recovery-assess_situation", "atomic", agent='H2', duration=60)

    # Step 3: Implement appropriate safety measures for the cell and agents
    toolset.add_node("recovery-war_broke_out", "recovery-implement_safety_measures", "atomic", agent='H2', duration=30)

    # Export the new HTN
    toolset.export_new_htn()def war_broke_out_in_the_area():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-war_broke_out", "sequential")

    # Step 1: Notify all agents to secure their stations
    toolset.add_node("recovery-war_broke_out", "recovery-notify_agents", "atomic", agent=['A_r1', 'A_H1', 'B_r2', 'B_r3', 'B_H2', 'C_r4', 'C_H3', 'C_r5', 'C_H4', 'D_r6', 'D_H4', 'E_r7', 'E_H5', 'F_H6', 'G_r8', 'G_r9', 'H_r10', 'H_H7', 'I_r11', 'I_r12', 'H2', 'J_r13', 'J_H8', 'K_r14', 'K_r15'], duration=10)

    # Step 2: Await further instructions from supervising agent
    toolset.add_node("recovery-war_broke_out", "recovery-await_instructions", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()

war_broke_out_in_the_area()def agent_controller_failure():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-agent_controller_failure", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-agent_controller_failure", "recovery-notify_human", "atomic", agent='H2', duration=6)

    # Step 2: Wait for human to resolve the controller failure
    toolset.add_node("recovery-agent_controller_failure", "recovery-wait_for_controller_fix", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()

# Return the function definition
agent_controller_failure()def human_on_break():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-human_on_break", "sequential")

    # Step 1: Notify the supervisor about the human on break
    toolset.add_node("recovery-human_on_break", "recovery-notify_supervisor", "atomic", agent='H2', duration=6)

    # Step 2: Wait for the human to return from break
    toolset.add_node("recovery-human_on_break", "recovery-wait_for_return", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()

human_on_break()def gripper_stuck():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-gripper_stuck", "sequential")
    
    # Step 1: Unscrew the stuck grips
    toolset.add_node("recovery-gripper_stuck", "recovery-unscrew_grips", "atomic", agent='C_H3', duration=6)
    
    # Step 2: Check for any damage
    toolset.add_node("recovery-gripper_stuck", "recovery-check_for_damage", "atomic", agent='C_H3', duration=6)
    
    # Step 3: Replace the grips with new ones
    toolset.add_node("recovery-gripper_stuck", "recovery-replace_grips", "atomic", agent='C_H3', duration=8)
    
    # Export the new HTN
    toolset.export_new_htn()

# The function 'gripper_stuck' is now complete.
# You can copy this entire function and use it in your code.def A_r1_Software_bug():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-A_r1_Software_bug", "sequential")

    # Step 1: Restart the software
    toolset.add_node("recovery-A_r1_Software_bug", "recovery-restart_software", "atomic", agent='A_r1', duration=6)

    # Step 2: Check for any additional bugs
    toolset.add_node("recovery-A_r1_Software_bug", "recovery-check_for_additional_bugs", "atomic", agent='A_r1', duration=6)

    # Export the new HTN
    toolset.export_new_htn()def A_r1_camera_not_working():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-A_r1_camera_not_working", "sequential")
    
    # Step 1: Check if camera is properly connected
    toolset.add_node("recovery-A_r1_camera_not_working", "recovery-check_camera_connection", "atomic", agent='A_r1', duration=6)
    
    # Step 2: Check for any damage
    toolset.add_node("recovery-A_r1_camera_not_working", "recovery-check_for_damage", "atomic", agent='A_r1', duration=6)
    
    # Step 3: Replace camera with a new one
    toolset.add_node("recovery-A_r1_camera_not_working", "recovery-replace_camera", "atomic", agent='A_r1', duration=8)
    
    # Export the new HTN
    toolset.export_new_htn()

A_r1_camera_not_working()Sure, here is the function for recovering from a mobile platform navigation error:

```python
def mobile_platform_navigation_error():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-mobile_platform_navigation_error", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-mobile_platform_navigation_error", "recovery-notify_human", "atomic", agent='m1', duration=6)

    # Step 2: Wait for human to resolve the navigation error
    toolset.add_node("recovery-mobile_platform_navigation_error", "recovery-wait_for_navigation_fix", "atomic", agent='m1', duration=0)

    # Export the new HTN
    toolset.export_new_htn()
```

Please note that the provided function assumes you have already imported the necessary modules and have the `toolset` variable defined.def power_supply_voltage_low():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-power_supply_voltage_low", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-power_supply_voltage_low", "recovery-notify_human", "atomic", agent='H2', duration=6)

    # Step 2: Wait for human to resolve the voltage issue
    toolset.add_node("recovery-power_supply_voltage_low", "recovery-wait_for_voltage_fix", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()

# Returning the function definition
power_supply_voltage_lowdef I_r12_wheel_screw_stuck():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-wheel_screw_stuck", "sequential")

    # Step 1: Unscrew the stuck wheel screw
    toolset.add_node("recovery-wheel_screw_stuck", "recovery-unscrew_wheel_screw", "atomic", agent='I_r12', duration=6)

    # Step 2: Check for any damage
    toolset.add_node("recovery-wheel_screw_stuck", "recovery-check_for_damage", "atomic", agent='I_r12', duration=6)

    # Step 3: Rescrew the wheel screw
    toolset.add_node("recovery-wheel_screw_stuck", "recovery-rescrew_wheel_screw", "atomic", agent='I_r12', duration=8)

    # Export the new HTN
    toolset.export_new_htn()def cannot_find_Hole_for_screwing():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-cannot_find_hole_for_screwing", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-cannot_find_hole_for_screwing", "recovery-notify_human", "atomic", agent='H2', duration=6)
    
    # Step 2: Wait for human to assist in finding the hole for screwing
    toolset.add_node("recovery-cannot_find_hole_for_screwing", "recovery-wait_for_assistance", "atomic", agent='H2', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()def agent_I_r11_dropped_wheel():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-I_r11_dropped_wheel", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-I_r11_dropped_wheel", "recovery-notify_human", "atomic", agent='I_r11', duration=6)
    
    # Step 2: Wait for the human to pick up the dropped wheel
    toolset.add_node("recovery-I_r11_dropped_wheel", "recovery-wait_for_human", "atomic", agent='I_r11', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()def m1_mobile_platform_unstable_mounting_of_ATV():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-m1_platform_unstable_mounting", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-m1_platform_unstable_mounting", "recovery-notify_human", "atomic", agent='m1', duration=6)
    
    # Step 2: Wait for human to stabilize the mounting of ATV
    toolset.add_node("recovery-m1_platform_unstable_mounting", "recovery-wait_for_stabilization", "atomic", agent='m1', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()def m1_mobile_platform_dropped_atv_from_mobile_platform():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-m1_mobile_platform_dropped_atv", "sequential")
    
    # Step 1: Inspect the ATV for any damage
    toolset.add_node("recovery-m1_mobile_platform_dropped_atv", "recovery-inspect_atv", "atomic", agent='H2', duration=8)
    
    # Step 2: Repair any damage if necessary
    toolset.add_node("recovery-m1_mobile_platform_dropped_atv", "recovery-repair_atv", "atomic", agent='H2', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()def m1_mobile_platform_invalid_part():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-m1_invalid_part", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-m1_invalid_part", "recovery-notify_human", "atomic", agent='m1', duration=6)
    
    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-m1_invalid_part", "recovery-wait_for_resolution", "atomic", agent='m1', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()

m1_mobile_platform_invalid_part()def m1_mobile_platform_invalid_path():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-m1_mobile_platform_invalid_path", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-m1_mobile_platform_invalid_path", "recovery-notify_human", "atomic", agent='m1', duration=6)

    # Step 2: Wait for human to resolve the path issue
    toolset.add_node("recovery-m1_mobile_platform_invalid_path", "recovery-wait_for_path_fix", "atomic", agent='m1', duration=0)

    # Export the new HTN
    toolset.export_new_htn()def I_r11_arm_invalid_motion_plan():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-I_r11_arm_invalid_motion_plan", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-I_r11_arm_invalid_motion_plan", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-I_r11_arm_invalid_motion_plan", "recovery-wait_for_resolution", "atomic", agent='I_r11', duration=0)

    # Export the new HTN
    toolset.export_new_htn()def I_r11_arm_collided_with_assembly_part():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-arm_collision_with_assembly_part", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-arm_collision_with_assembly_part", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Step 2: Wait for human to resolve the collision
    toolset.add_node("recovery-arm_collision_with_assembly_part", "recovery-wait_for_collision_fix", "atomic", agent='I_r11', duration=0)

    # Export the new HTN
    toolset.export_new_htn()def I_r11_arm_collided_with_assembly_part():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-I_r11_arm_collided_with_assembly_part", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-I_r11_arm_collided_with_assembly_part", "recovery-notify_human", "atomic", agent='I_r11', duration=6)
    
    # Step 2: Inspect the assembly part for damage
    toolset.add_node("recovery-I_r11_arm_collided_with_assembly_part", "recovery-inspect_assembly_part", "atomic", agent='I_r11', duration=10)
    
    # Step 3: Notify the monitor when inspection is complete
    toolset.add_node("recovery-I_r11_arm_collided_with_assembly_part", "recovery-notify_monitor", "atomic", agent='I_r11', duration=6)
    
    # Export the new HTN
    toolset.export_new_htn()
    
I_r11_arm_collided_with_assembly_part()def mobile_platform_m1_human_on_the_way_of_path():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-m1_human_on_the_way_of_path", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-m1_human_on_the_way_of_path", "recovery-notify_human", "atomic", agent='m1', duration=6)
    
    # Step 2: Wait for human to clear the path
    toolset.add_node("recovery-m1_human_on_the_way_of_path", "recovery-wait_for_path_clearance", "atomic", agent='m1', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()

mobile_platform_m1_human_on_the_way_of_path()def mobile_platform_m1_mobile_base_collision_with_wall():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-mobile_base_collision_with_wall", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-mobile_base_collision_with_wall", "recovery-notify_human", "atomic", agent='m1', duration=6)

    # Step 2: Wait for human to resolve the collision
    toolset.add_node("recovery-mobile_base_collision_with_wall", "recovery-wait_for_collision_fix", "atomic", agent='m1', duration=0)

    # Export the new HTN
    toolset.export_new_htn()
return mobile_platform_m1_mobile_base_collision_with_walldef I_r11_collision_with_the_wall():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-I_r11_collision_with_the_wall", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-I_r11_collision_with_the_wall", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Step 2: Wait for human to resolve the collision
    toolset.add_node("recovery-I_r11_collision_with_the_wall", "recovery-wait_for_collision_fix", "atomic", agent='I_r11', duration=0)

    # Export the new HTN
    toolset.export_new_htn()def I_r11_task_unreachable_by_robot():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-I_r11_task_unreachable_by_robot", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-I_r11_task_unreachable_by_robot", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-I_r11_task_unreachable_by_robot", "recovery-wait_for_resolution", "atomic", agent='I_r11', duration=0)

    # Export the new HTN
    toolset.export_new_htn()def I_r11_task_unreachable_by_robot():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-I_r11_task_unreachable", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-I_r11_task_unreachable", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Step 2: Wait for human to make the task reachable
    toolset.add_node("recovery-I_r11_task_unreachable", "recovery-wait_for_task_reachability_fix", "atomic", agent='I_r11', duration=0)

    # Export the new HTN
    toolset.export_new_htn()
def I_r11_part_not_visible():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-part_not_visible", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-part_not_visible", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-part_not_visible", "recovery-wait_for_resolution", "atomic", agent='I_r11', duration=0)

    # Export the new HTN
    toolset.export_new_htn()def I_r11_noticed_crack_in_outer_frame():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-cracked_frame", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-cracked_frame", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Step 2: Wait for human to assess the crack
    toolset.add_node("recovery-cracked_frame", "recovery-assess_crack", "atomic", agent='I_r11', duration=6)

    # Step 3: Determine repair or replacement needed
    toolset.add_node("recovery-cracked_frame", "recovery-repair_or_replace", "parallel")
    toolset.add_node("recovery-repair_or_replace", "recovery-repair_frame", "atomic", agent='I_r11', duration=40)
    toolset.add_node("recovery-repair_or_replace", "recovery-replace_frame", "sequential")
    toolset.add_node("recovery-replace_frame", "recovery-search_for_new_frame", "atomic", agent='I_r11', duration=30)
    toolset.add_node("recovery-replace_frame", "recovery-pick_new_frame", "atomic", agent='I_r11', duration=15)
    toolset.add_node("recovery-replace_frame", "recovery-install_new_frame", "atomic", agent='I_r11', duration=25)

    # Export the new HTN
    toolset.export_new_htn()def I_r11_noticed_wheel_not_present():
    # When the I_r11 agent notices that the wheel is not present, it needs to notify the human for assistance
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-I_r11_noticed_wheel_not_present", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-I_r11_noticed_wheel_not_present", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Export the new HTN
    toolset.export_new_htn()def I_r11_incorrect_size_screw():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-incorrect_size_screw", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-incorrect_size_screw", "recovery-notify_human", "atomic", agent='I_r11', duration=6)
    
    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-incorrect_size_screw", "recovery-wait_for_screw_fix", "atomic", agent='I_r11', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()

I_r11_incorrect_size_screw()def I_r11_notifed_installed_engine_failure():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-I_r11_notification_installed_engine_failure", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-I_r11_notification_installed_engine_failure", "recovery-notify_human", "atomic", agent='I_r11', duration=6)
    
    # Step 2: Wait for human to resolve the failure
    toolset.add_node("recovery-I_r11_notification_installed_engine_failure", "recovery-wait_for_engine_failure_fix", "atomic", agent='I_r11', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()def I_r11_realized_ATV_installed_engine_failure():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-ATV_installed_engine_failure", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-ATV_installed_engine_failure", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Step 2: Wait for human to resolve the engine failure
    toolset.add_node("recovery-ATV_installed_engine_failure", "recovery-wait_for_engine_fix", "atomic", agent='I_r11', duration=0)

    # Export the new HTN
    toolset.export_new_htn()def I_r11_realized_ATV_installed_engine_failure():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-installed_engine_failure", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-installed_engine_failure", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Step 2: Wait for human to resolve the engine failure
    toolset.add_node("recovery-installed_engine_failure", "recovery-replace_engine", "atomic", agent='I_r11', duration=120)

    # Export the new HTN
    toolset.export_new_htn()def I_r11_realized_ATV_installed_engine_failure():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-ATV_installed_engine_failure", "sequential")
    
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-ATV_installed_engine_failure", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-ATV_installed_engine_failure", "recovery-wait_for_resolution", "atomic", agent='I_r11', duration=0)

    # Export the new HTN
    toolset.export_new_htn()# Recovery plan for I_r11_defective_engine_on_ATV_Assembly:

def I_r11_defective_engine_on_ATV_Assembly():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-defective_engine_on_ATV_Assembly", "sequential")
    
    # Step 1: Unscrew the defective engine
    toolset.add_node("recovery-defective_engine_on_ATV_Assembly", "recovery-unscrew_defective_engine", "atomic", agent='I_r11', duration=8)
    
    # Step 2: Remove the defective engine
    toolset.add_node("recovery-defective_engine_on_ATV_Assembly", "recovery-remove_defective_engine", "atomic", agent='I_r11', duration=6)
    
    # Step 3: Search for a new engine
    toolset.add_node("recovery-defective_engine_on_ATV_Assembly", "recovery-search_new_engine", "atomic", agent='I_r11', duration=10)
    
    # Step 4: Pick up the new engine
    toolset.add_node("recovery-defective_engine_on_ATV_Assembly", "recovery-pick_new_engine", "atomic", agent='I_r11', duration=6)
    
    # Step 5: Insert the new engine on chassis
    toolset.add_node("recovery-defective_engine_on_ATV_Assembly", "recovery-insert_new_engine_on_chassis", "atomic", agent='I_r11', duration=8)
    
    # Export the new HTN
    toolset.export_new_htn()

# Call the function to add the recovery plan to the HTN
I_r11_defective_engine_on_ATV_Assembly()def I_r11_defective_wheel_flat_tire ():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-defective_wheel_flat_tire", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-defective_wheel_flat_tire", "recovery-notify_human", "atomic", agent='I_r11', duration=10)

    # Step 2: Wait for human to replace the wheel
    toolset.add_node("recovery-defective_wheel_flat_tire", "recovery-replace_wheel", "atomic", agent='H2', duration=6)

    # Export the new HTN
    toolset.export_new_htn()def I_r11_suspension_not_present():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-I_r11_suspension_not_present", "sequential")
    
    # Step 1: Notify the human for assistance in finding the suspension
    toolset.add_node("recovery-I_r11_suspension_not_present", "recovery-notify_human", "atomic", agent='I_r11', duration=6)
    
    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-I_r11_suspension_not_present", "recovery-search_for_suspension", "atomic", agent='I_r11', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()def I_r11_wrong_part_present():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-wrong_part_present", "sequential")
    
    # Step 1: Remove the wrong part
    toolset.add_node("recovery-wrong_part_present", "recovery-remove_wrong_part", "atomic", agent='I_r11', duration=6)
    
    # Step 2: Search and pick the correct part
    toolset.add_node("recovery-wrong_part_present", "recovery-search_correct_part", "atomic", agent='I_r11', duration=8)
    toolset.add_node("recovery-wrong_part_present", "recovery-pick_correct_part", "atomic", agent='I_r11', duration=6)
    
    # Step 3: Place and fasten the correct part
    toolset.add_node("recovery-wrong_part_present", "recovery-place_correct_part", "atomic", agent='I_r11', duration=6)
    toolset.add_node("recovery-wrong_part_present", "recovery-fasten_correct_part", "atomic", agent='I_r12', duration=8)
    
    # Export the new HTN
    toolset.export_new_htn()def I_r11_wheel_defective_rim_dent():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-wheel_defective_rim_dent", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-wheel_defective_rim_dent", "recovery-notify_human", "atomic", agent='I_r11', duration=6)

    # Step 2: Wait for human to inspect the wheel
    toolset.add_node("recovery-wheel_defective_rim_dent", "recovery-inspect_wheel", "atomic", agent='I_r11', duration=6)

    # Step 3: Repair the dent on the wheel
    toolset.add_node("recovery-wheel_defective_rim_dent", "recovery-repair_dent", "atomic", agent='I_r11', duration=8)

    # Export the new HTN
    toolset.export_new_htn()
def cell_water_leak():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-cell_water_leak", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-cell_water_leak", "recovery-notify_human", "atomic", agent='H2', duration=6)

    # Step 2: Wait for human to resolve the water leak
    toolset.add_node("recovery-cell_water_leak", "recovery-fix_water_leak", "atomic", agent='H2', duration=0)

    # Export the new HTN
    toolset.export_new_htn()

    # Return the function name and definition
    return cell_water_leakdef cell_rodent_appeared ():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-cell_rodent_appeared", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-cell_rodent_appeared", "recovery-notify_human", "atomic", agent='m1', duration=10)

    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-cell_rodent_appeared", "recovery-resolve_issue", "atomic", agent='m1', duration=0)

    # Export the new HTN
    toolset.export_new_htn()def cell_bird_appeared():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-bird_appeared", "sequential")
  
    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-bird_appeared", "recovery-notify_human", "atomic", agent='m1', duration=6)
    
    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-bird_appeared", "recovery-wait_for_human", "atomic", agent='m1', duration=0)
    
    # Export the new HTN
    toolset.export_new_htn()def fire_in_the_cell_G():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-fire_in_the_cell_G", "sequential")
    
    # Step 1: Notify the human for the fire
    toolset.add_node("recovery-fire_in_the_cell_G", "recovery-notify_human", "atomic", agent='G_r8', duration=6)
    
    # Step 2: Evacuate the cell
    toolset.add_node("recovery-fire_in_the_cell_G", "recovery-evacuate_cell", "atomic", agent='G_H9', duration=12)
    
    # Step 3: Call for emergency help
    toolset.add_node("recovery-fire_in_the_cell_G", "recovery-call_emergency", "atomic", agent='G_H9', duration=6)
    
    # Export the new HTN
    toolset.export_new_htn()def cell_A_desk_broken():
    # Add a node to the planning node
    toolset.add_node(planning_node, "recovery-cell_A_desk_broken", "sequential")

    # Step 1: Notify the human for assistance
    toolset.add_node("recovery-cell_A_desk_broken", "recovery-notify_human", "atomic", agent='H2', duration=6)

    # Step 2: Wait for human to resolve the issue
    toolset.add_node("recovery-cell_A_desk_broken", "recovery-repair_desk", "atomic", agent='H_H7', duration=15)