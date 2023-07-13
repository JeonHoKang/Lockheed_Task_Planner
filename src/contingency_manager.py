import copy
import yaml
import anytree
from anytree import AnyNode, PostOrderIter, find_by_attr
from anytree.importer import DictImporter
import MILP_scheduler
from tree_toolset import TreeToolSet
# Load the YAML file
# ------- While ROS node is running ------


class ContingencyManager:
    """
    Alters HTN to handle contingencies reactively.

    """
    def __init__(self):
        super().__init__()
        self.contingency = False # set whether contingency has occured
        
    def set_problem_dir(self, directory):
        self.problem_dir = directory

    def import_policies(self, policy_yaml):
        """Imports a problem description"""
        # Get the directory where problem is located
        file_dir = self.problem_dir + policy_yaml
        # open the file directory
        with open(file_dir, 'r') as stream:
            try:
                # load the yaml file
                # Converts yaml document to python object
                self.policies_dict = yaml.safe_load(stream)
                print('')
            # Printing dictionary
            except yaml.YAMLError as dict_e:
                print(dict_e)

    def geneate_contingency_plan(self, anytree_htn, contingency_node):
        contingency_planning_node = {}
        dict_policies = self.policies_dict
        current_contingency_policy = {}
        contingency_policy_list = []
        enm_notification_node = {}
        abort_current_task = {}
        operations_list  = set()
        merged_policy = {}
        second_merged_policy = {}
        third_merged_policy = {}
        check_different_constraint = []
        # contingency_list = ["broken_upper_body_frame", "engine_leaking", "rear_left_wheel_screw1_stuck"]
        # contingency_list = ["trunk_skeleton_missing", "engine_leaking", "rear_left_wheel_screw1_stuck"] 
        # contingency_list = ["handle_bolt3_missing", "engine_leaking", "defective_front_right_wheel"]            
        contingency_list = ["broken_upper_body_frame", "engine_leaking", "defective_front_right_wheel"]            
        # contingency_list = ["broken_upper_body_frame", "rear_left_wheel_screw1_stuck"]
        # contingency_list = ["broken_upper_body_frame"]
        contingency_planning_node['id'] = 'recovery-contingency_plan'
        contingency_planning_node['type'] = 'sequential'
        contingency_planning_node['children'] = []
        enm_notification_node['id'] = 'recovery-notify_execution_monitor'
        enm_notification_node['type'] = 'atomic'
        enm_notification_node['agent'] = ['H']
        # abort current task is to free and abort from the node that does not add value to the assembly
        abort_current_task['id'] = f'recovery-abort_task_{contingency_node["id"][3:]}'
        abort_current_task['type'] = 'atomic'
        abort_current_task['agent'] = contingency_node['agent']
        contingency_planning_node['children'].append(abort_current_task)
        operation_policy_pair = {}
        for cont in contingency_list:
            current_contingency_policy = dict_policies[cont]
            contingency_policy_list.append(current_contingency_policy)
            current_operation_id = current_contingency_policy['operation_id']
            operations_list.add(current_operation_id)
            operation_policy_pair[current_operation_id] = current_contingency_policy['policy']
        contingency_product = self.search_anytree_node(anytree_htn, operations_list) # get Anynode object of the operation
        if len(contingency_list) > 2: # if it is an occurance of multi-layer contingency
            policy_in_order = self.search_hierarchy(anytree_htn, contingency_product)
            prev_parent_policy = None
            prev_policy_pair = None
            for i in range(len(policy_in_order)):
                if i+1 < len(policy_in_order): # how many policies should we be able to handle?
                    print(f'{i}---->{i+1} {policy_in_order[i]["parent"].type == policy_in_order[i+1]["parent"].type}')
                    check_different_constraint.append(policy_in_order[i]["parent"].type == policy_in_order[i+1]["parent"].type)
            if check_different_constraint[0] and check_different_constraint[1]:
                merged_policy['id'] = f'recovery-multi_{policy_in_order[0]["parent"].id[3:]}'
                merged_policy['type'] = policy_in_order[0]["parent"].type
                merged_policy['children'] = []
                for policy in list(operation_policy_pair.values()):
                    merged_policy["children"].append(policy)
            if check_different_constraint[0] == False and check_different_constraint[1] == True:
                second_merged_policy["id"] = f'recovery-multi_{policy_in_order[0]["parent"].id}'
                second_merged_policy["type"] = policy_in_order[0]["parent"].type
                second_merged_policy["children"] = []
                for policy in policy_in_order[0]["policies"]:
                    second_merged_policy['children'].append(operation_policy_pair[policy.id[3:]])
                merged_policy['id'] = f'recovery-{policy_in_order[2]["parent"].id}'
                merged_policy['type'] = policy_in_order[2]["parent"].type
                merged_policy['children'] = [second_merged_policy]
                merged_policy["children"].append(operation_policy_pair[policy_in_order[len(policy_in_order)-1]["policies"][1].id[3:]])
            elif check_different_constraint[0] == True and check_different_constraint[1] == False:
                merged_policy['id'] = f'recovery-{policy_in_order[0]["parent"].id[3:]}'
                merged_policy['type'] = policy_in_order[0]["parent"].type
                merged_policy['children'] = [operation_policy_pair[policy_in_order[0]['policies'][0].id[3:]]]
                second_merged_policy["id"] = f'recovery-multi_{policy_in_order[2]["parent"].id[3:]}'
                second_merged_policy["type"] = policy_in_order[2]["parent"].type
                second_merged_policy["children"] = []
                for policy in policy_in_order[len(policy_in_order)-1]["policies"]:
                    second_merged_policy['children'].append(operation_policy_pair[policy.id[3:]])
                merged_policy['children'].append(second_merged_policy)
            print("merged_")
        elif len(contingency_list) == 2:
            policy_in_order = self.search_hierarchy(anytree_htn, contingency_product)
            recovery_policy_pair = policy_in_order[0]["policies"]
            merged_policy['id'] = f'recovery-{policy_in_order[0]["parent"].id}'
            merged_policy['type'] = policy_in_order[0]["parent"].type
            merged_policy['children'] = []
            for policy in recovery_policy_pair:
                for item in contingency_policy_list:
                    if policy.id[3:] == item['operation_id']:
                        merged_policy['children'].append(item['policy'])
        elif len(contingency_list) == 1: # if it is an occurance of single contingency
            for item in contingency_policy_list:
                if contingency_product[0].id[3:] == item['operation_id']:
                    merged_policy = item['policy']

        contingency_planning_node['children'].append(merged_policy)
        original_task = copy.deepcopy(contingency_node)
        original_task['id'] = 'recovery-' + contingency_node['id'][3:]
        contingency_planning_node['children'].append(enm_notification_node)
        contingency_planning_node['children'].append(original_task)
        return contingency_planning_node

    def search_anytree_node(self, anytree_htn, nodes):
        """Check for nodes within a tree"""
        contingency_product = []   
        for task in nodes:
            for descent in anytree_htn.descendants:
                if descent.id[3:] == task:
                    contingency_product.append(descent)
        return contingency_product
    
    def search_hierarchy(self, anytree_htn, contingency_product):
        """ Checks the type of common parent shared by multiple contingency"""
        def check_in_order_dfs(node, target_names, result_list):
            if node is None:
                return

            for child in node.children:
                check_in_order_dfs(child, target_names, result_list)

            if node in target_names:
                result_list.append(node)
            
        def check_for_common_parent(node1, node2):
            flag = False # found flag to break out of the loop
            shallower_node = node1
            deeper_node = node2
            reset_to_original = copy.deepcopy(deeper_node)
            # for each ancestors of the higher node
            for ancestor in list(reversed(shallower_node.ancestors)): # is revered because of ordering from lower to high
                while deeper_node.is_root != True: # check each one of the parent of deeper node
                    if deeper_node.parent.id == ancestor.id: # if found
                        flag = True # flag that will break all loops
                        source_node = deeper_node.parent # check for commmon parent and check for its type
                        source_child_node = source_node.children
                    deeper_node = deeper_node.parent
                deeper_node = reset_to_original
                if flag: # if found then also break the for loop
                    break
            return source_node
        # common_parent_list = set()
        joined_policy_list = []
        original_node = []
        contingency_in_order = []
        for i in range(len(contingency_product)):
            original_node.append({'node':copy.deepcopy(contingency_product[i])})
        for node in original_node:
            node['len_anc'] = node['node'].depth
        original_node_sorted = sorted(original_node, key=lambda x: x['len_anc'])
        print('original_node')
        check_in_order_dfs(anytree_htn, contingency_product, contingency_in_order)
        for i in range(len(contingency_in_order)):
            for j in range(i+1, len(contingency_in_order)):
                joined_policy = {}
                parent_node = check_for_common_parent(contingency_in_order[i],contingency_in_order[j])
                joined_policy['policies'] = [contingency_in_order[i],contingency_in_order[j]]
                joined_policy['parent'] = parent_node
                print(f'{i}--->{j}{joined_policy["parent"].type}')
                joined_policy_list.append(joined_policy)

        return joined_policy_list

    def Add_Handle_Node(self, htn_dictionary, failed_task, contingency_plan):
        """Adds the handling nodes into the current contingency"""
        def insert_element(dictionary, failed_task, contingency_plan, parent=None):
            target_node = failed_task
            if dictionary['id'] == target_node['id']:
                input_order_number = parent['children'].index(target_node)
                input_order_number += 1
                parent['children'].insert(
                    input_order_number, contingency_plan)
            else:
                if 'children' in dictionary:
                    for child in dictionary['children']:
                        parent = dictionary
                        insert_element(child, failed_task,
                                       contingency_plan, parent)
        insert_element(htn_dictionary, failed_task,
                       contingency_plan)

    def yaml_export(self,htn_dict, contingency_plan):

        # Save the updated data to the YAML file
        with open("problem_description/ATV_Assembly/problem_description_ATV.yaml", "r") as file:
            yaml_dict = yaml.safe_load(file)
            yaml_dict['num_tasks'] = yaml_dict['num_tasks'] + \
                len(contingency_plan['children'])-1
            yaml_dict['agents'] = yaml_dict['agents']
            yaml_dict['task_model_id'] = 'cont_task_model_ATV.yaml'
            yaml_dict['htn_model_id'] = 'cont_ATV_Assembly_htn.yaml'
        TreeToolSet().safe_dict_yaml_export(htn_dict, self.problem_dir, "current_ATV_Assembly_htn.yaml")
        TreeToolSet().safe_dict_yaml_export(yaml_dict, self.problem_dir, "current_problem_description_ATV.yaml")

    def generate_task_model(self, contingency_task_plan):
        with open("problem_description/ATV_Assembly/task_model_ATV.yaml", "r") as file:
            task_model_dict = yaml.safe_load(file)
            contingency_plan_anytree = DictImporter().import_(contingency_task_plan)
            contingency_leaf = list(anytree.PostOrderIter(contingency_plan_anytree, filter_=lambda node: node.is_leaf))
            for task_nodes in contingency_leaf:
                    task_model_dict[task_nodes.id] = {'agent_model':
                                                        task_nodes.agent}
                    for agent in task_nodes.agent:
                        task_model_dict[task_nodes.id]['duration_model'] = {
                            agent: {'id': 'det', 'mean': 9}}
        TreeToolSet().safe_dict_yaml_export(task_model_dict, self.problem_dir, "task_model_ATV.yaml")
    

def main():
    scheduler = MILP_scheduler.HtnMilpScheduler() # imports scheduler
    problem_dir = "problem_description/ATV_Assembly/"
    problem = "current_problem_description.yaml"
    policies_file = "contingency_policies.yaml"
    scheduler.set_dir(problem_dir)
    scheduler.import_problem(problem)
    scheduler.create_task_model()
    scheduler.import_htn()
    htn_dict = scheduler.multi_product_dict
    product_htn_anytree = scheduler.multi_product_htn
    contingency_handling = ContingencyManager()
    contingency_handling.set_problem_dir(problem_dir)
    contingency_handling.import_policies(policies_file)
    contingency_name = 'p1_scew_bolt_for_rear_left_wheel1'
    contingency_node = TreeToolSet().search_tree(
        htn_dict, contingency_name)
    contingency_plan = contingency_handling.geneate_contingency_plan(product_htn_anytree,contingency_node)
    contingency_handling.Add_Handle_Node(
        htn_dict, contingency_node, contingency_plan)
    contingency_handling.generate_task_model(contingency_plan) # export task_model to yaml file
    contingency_handling.yaml_export(htn_dict, contingency_plan) # Export yaml file
    print('-------initialized contingency manager-------')


if __name__ == '__main__':
    main()
