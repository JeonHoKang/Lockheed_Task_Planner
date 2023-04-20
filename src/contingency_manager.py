import yaml
import Lockheed_task_planner
import anytree
from anytree import AnyNode, PostOrderIter, find_by_attr
from anytree.exporter import DictExporter
from anytree import RenderTree  # just for nice printing
from anytree.importer import DictImporter
from anytree.exporter import DictExporter


# Load the YAML file
# ------- While ROS node is running ------

contingency_occur = 1

# print(data['children'][0]['children'][0]['children'][0])
scheduler = Lockheed_task_planner.HtnMilpScheduler()
scheduler.set_dir("problem_description/LM2023_problem/")
scheduler.import_problem("problem_description_LM2023.yaml")
scheduler.create_task_model()
htn = scheduler.import_htn()


contingency_name = 'p1_Screw1_Right_P_C1_1_Screw'
if contingency_name == 'p1_Screw1_Right_P_C1_1_Screw':
    # Node = []
    for node in PostOrderIter(htn, filter_=lambda n: n.id in (contingency_name)):
        contingency_parent = node.parent
        print(contingency_parent)
        children_of_cont_parent = contingency_parent.children
        print(len(children_of_cont_parent))

        Contingency_handle = AnyNode(
            id='contingency_handler', type='sequential', parent=contingency_parent)
        contingency_node = node
        contingency_node.parent = Contingency_handle
        original_tasks = AnyNode(
            id='original tasks', type=contingency_parent.type, parent=contingency_parent)
        cont_child_arr = []
        for children_of_cont in children_of_cont_parent:
            children_of_cont.parent = original_tasks
            if children_of_cont == contingency_node:
                print('True')
                protocol1 = AnyNode(
                    id='p1_motion_planning', type='atomic', agent=['r3'], parent=Contingency_handle)
                protocol2 = AnyNode(
                    id='p1_repick_crew', type='atomic', agent=['r3'], parent=Contingency_handle)
                protocol3 = AnyNode(
                    id='p1_reattempt_screwing', type='atomic', agent=['r3'], parent=Contingency_handle)
                protocol4 = AnyNode(
                    id='p1_revert_back', type='atomic', agent=['r3'], parent=Contingency_handle)
                contingency_node.parent = Contingency_handle
elif contingency_name == 'p1_Pick_and_Place_Right_Panel':
    # Node = []
    for node in PostOrderIter(htn, filter_=lambda n: n.id in (contingency_name)):
        contingency_parent = node.parent
        print(contingency_parent)
        children_of_cont_parent = contingency_parent.children
        print(len(children_of_cont_parent))

        Contingency_handle = AnyNode(
            id='contingency_handler', type='sequential', parent=contingency_parent)
        contingency_node = node
        contingency_node.parent = Contingency_handle
        original_tasks = AnyNode(
            id='original tasks', type=contingency_parent.type, parent=contingency_parent)
        cont_child_arr = []
        for children_of_cont in children_of_cont_parent:
            children_of_cont.parent = original_tasks
            if children_of_cont == contingency_node:
                print('True')
                protocol1 = AnyNode(
                    id='p1_locate_panel', type='atomic', agent=['r1'], parent=Contingency_handle)
                protocol2 = AnyNode(
                    id='p1_pick_panel', type='atomic', agent=['r1'], parent=Contingency_handle)
                protocol3 = AnyNode(
                    id='p1_place_panel', type='atomic', agent=['r1'], parent=Contingency_handle)
                protocol4 = AnyNode(
                    id='p1_re-pick_panel', type='atomic', agent=['r1'], parent=Contingency_handle)
                contingency_node.parent = Contingency_handle

exporter = DictExporter()
htn_tree = RenderTree(htn)
htn_dict = exporter.export(htn)
print(htn_tree)

print('HTN contingency manager done')
# Save the updated data to the YAML file
with open("problem_description/LM2023_problem/problem_description_LM2023.yaml", "r") as file:
    yaml_dict = yaml.safe_load(file)
    yaml_dict['num_tasks'] = yaml_dict['num_tasks'] + \
        len(Contingency_handle.children)-1
    yaml_dict['agents'] = yaml_dict['agents']
    yaml_dict['task_model_id'] = 'cont_task_model_LM2023.yaml'
    yaml_dict['htn_model_id'] = 'cont_LM2023_htn.yaml'
    print(yaml_dict)
    input()
with open('problem_description/LM2023_problem/cont_LM2023_htn.yaml', 'w') as file:
    yaml.safe_dump(htn_dict, file, sort_keys=False)

with open('problem_description/LM2023_problem/cont_problem_description_LM2023.yaml', 'w') as file:
    yaml.safe_dump(yaml_dict, file, sort_keys=False)

with open("problem_description/LM2023_problem/task_model_LM2023.yaml", "r") as file:
    yaml_model = yaml.safe_load(file)
    yaml_model[protocol1.id[3::]] = {'agent_model': [
        protocol1.agent[0]], 'duration_model': {protocol1.agent[0]: {'id': 'det', 'mean': 4}}}
    yaml_model[protocol2.id[3::]] = {'agent_model': [
        protocol2.agent[0]], 'duration_model': {protocol2.agent[0]: {'id': 'det', 'mean': 4}}}
    yaml_model[protocol3.id[3::]] = {'agent_model': [
        protocol3.agent[0]], 'duration_model': {protocol3.agent[0]: {'id': 'det', 'mean': 4}}}
    yaml_model[protocol4.id[3::]] = {'agent_model': [
        protocol4.agent[0]], 'duration_model': {protocol4.agent[0]: {'id': 'det', 'mean': 4}}}
    # print(yaml_model[protocol4.id])
    # yaml_model[protocol1.id] = ['r3']
    # print(yaml_model)
with open('problem_description/LM2023_problem/cont_task_model_LM2023.yaml', 'w') as file:
    yaml.safe_dump(yaml_model, file)
