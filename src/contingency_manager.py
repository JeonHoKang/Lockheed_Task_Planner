import copy
import yaml
import anytree
from anytree import AnyNode, PostOrderIter, find_by_attr
# from anytree.exporter import DictExporter
# from anytree import RenderTree  # just for nice printing
from anytree.importer import DictImporter
# from anytree.exporter import DictExporter
import Lockheed_task_scheduler

# Load the YAML file
# ------- While ROS node is running ------


class ContingencyManager(object):
    def __init__(self):
        super().__init__()
        self.contingency = True
        contingency_occur = 1
        # print(data['children'][0]['children'][0]['children'][0])
        scheduler = Lockheed_task_scheduler.HtnMilpScheduler()
        self.problem_dir = "problem_description/ATV_Assembly/"
        problem = "problem_description_ATV.yaml"
        self.policies_file = "contingency_policies.yaml"
        scheduler.set_dir(self.problem_dir)
        scheduler.import_problem(problem)
        scheduler.create_task_model()
        htn = scheduler.import_htn()
        self.htn_object = scheduler.task_object
        self.contingency_name = 'p1_pick_upper_body_frame'
        self.htn_dict = scheduler.multi_product_dict
        self.product_htn_anytree = scheduler.multi_product_htn
        self.contingency_node = self.search_tree(
            self.htn_dict, self.contingency_name)
        self.contingency_plan = self.geneate_contingency_plan()
        self.Add_Handle_Node(
            self.htn_dict, self.contingency_node, self.contingency_plan)
        self.generate_task_model()
        self.contingency_htn_dict = self.htn_dict
        self.yaml_export()

    def search_tree(self, dictionary, node_id):
        if dictionary['id'] == node_id:
            contingency_node = dictionary
            return contingency_node
        else:
            res = []
            if 'children' in dictionary:
                for child in dictionary['children']:
                    parent = dictionary
                    res.append(self.search_tree(child, node_id))
            else:
                return None

            for element in res:
                if element:
                    return element

    def import_policies(self, policy_yaml):
        """Imports a problem description"""
        # Get the directory where problem is located
        file_dir = self.problem_dir + policy_yaml
        # open the file directory
        with open(file_dir, 'r') as stream:
            try:
                # load the yaml file
                # Converts yaml document to python object
                policies_dict = yaml.safe_load(stream)
                print('')
            # Printing dictionary
            except yaml.YAMLError as dict_e:
                print(dict_e)
        return policies_dict

    def geneate_contingency_plan(self):
        contingency_planning_node = {}
        dict_policies = self.import_policies(self.policies_file)
        current_contingency_policy = {}
        contingency_policy_list = []
        enm_notification_node = {}
        abort_current_task = {}
        operations_list  = set()
        merged_policy = {}
        contingency_list = ["broken_upper_body_frame", "engine_leaking", "rear_left_wheel_screw1_stuck"]
        # contingency_list = ["broken_upper_body_frame"]
        contingency_planning_node['id'] = 'contingency_plan'
        contingency_planning_node['type'] = 'parallel'
        contingency_planning_node['children'] = []
        enm_notification_node['id'] = 'recovery-notify_execution_monitor'
        enm_notification_node['type'] = 'atomic'
        enm_notification_node['agent'] = ['H']
        # abort current task is to free and abort from the node that does not add value to the assembly
        abort_current_task['id'] = f'recovery-abort_task_{self.contingency_node["id"][3:]}'
        abort_current_task['type'] = 'atomic'
        abort_current_task['agent'] = self.contingency_node['agent']
        contingency_planning_node['children'].append(abort_current_task)
        for cont in contingency_list:
            current_contingency_policy = dict_policies[cont]
            contingency_policy_list.append(current_contingency_policy)
            operations_list.add(current_contingency_policy['operation_id'])
        contingency_product = self.search_anytree_node(operations_list) # get Anynode object of the operation
        if len(contingency_list) > 1: # if it is an occurance of multi-layer contingency
            policy_in_order = self.search_hierarchy(contingency_product)
        else: # if it is an occurance of single contingency
            policy_in_order = {1: contingency_product[0]}

        for common_parent, task_list in list(policy_in_order.items()):
            for item in contingency_policy_list:
                for task in task_list: #________You need to finally merge the tasks____________________
                    if common_parent.type != 'sequential' and task.id[3:] == item['operation_id']:
                        merged_policy['id'] = f'Contingency_{common_parent.type}'
                        merged_policy['type'] = common_parent.type
                        merged_policy['children'] = []
                        merged_policy['children'].append(item['policy'])
                    # elif common_parent.type == 'sequential' and task.id[3:] == item['operation_id']:
                    #     merged_policy['id'] = item['id']
                    #     merged_policy['type'] = common_parent.type
                    #     merged_policy['children'].append(item['policy'])
        contingency_planning_node['children'].append(merged_policy)
        original_task = copy.deepcopy(self.contingency_node)
        original_task['id'] = 'recovery-' + self.contingency_node['id'][3:]
        contingency_planning_node['children'].append(enm_notification_node)
        contingency_planning_node['children'].append(original_task)
        return contingency_planning_node

    def search_anytree_node(self, nodes):
        """Check for nodes within a tree"""
        contingency_product = []   
        for task in nodes:
            for descent in self.product_htn_anytree.descendants:
                if descent.id[3:] == task:
                    contingency_product.append(descent)
        return contingency_product
    
    def search_hierarchy(self, contingency_product):
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
        joined_policy = {}
        original_node = []
        contingency_in_order = []
        for i in range(len(contingency_product)):
            original_node.append({'node':copy.deepcopy(contingency_product[i])})
        for node in original_node:
            node['len_anc'] = node['node'].depth
        original_node_sorted = sorted(original_node, key=lambda x: x['len_anc'])
        print('original_node')
        check_in_order_dfs(self.product_htn_anytree, contingency_product, contingency_in_order)
        for i in range(len(contingency_in_order)):
            for j in range(i+1, len(contingency_in_order)):
                parent_type = check_for_common_parent(contingency_in_order[i],contingency_in_order[j])
                joined_policy[parent_type] = [contingency_in_order[i],contingency_in_order[j]]
        return joined_policy

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

    def yaml_export(self):
        # exporter = DictExporter()
        # htn_dict = exporter.export(self.htn_dict)
        # Save the updated data to the YAML file
        with open("problem_description/ATV_Assembly/problem_description_ATV.yaml", "r") as file:
            yaml_dict = yaml.safe_load(file)
            yaml_dict['num_tasks'] = yaml_dict['num_tasks'] + \
                len(self.contingency_plan['children'])-1
            yaml_dict['agents'] = yaml_dict['agents']
            yaml_dict['task_model_id'] = 'cont_task_model_ATV.yaml'
            yaml_dict['htn_model_id'] = 'cont_ATV_Assembly_htn.yaml'
        with open('problem_description/ATV_Assembly/cont_ATV_Assembly_htn.yaml', 'w') as file:
            yaml.safe_dump(self.htn_dict, file, sort_keys=False)

        with open('problem_description/ATV_Assembly/cont_problem_description_ATV.yaml', 'w') as file:
            yaml.safe_dump(yaml_dict, file, sort_keys=False)

    def generate_task_model(self):
        with open("problem_description/ATV_Assembly/task_model_ATV.yaml", "r") as file:
            task_model_dict = yaml.safe_load(file)
            # list_task_models = list(task_model_dict.keys())
            # for i, tasks in enumerate(list_task_models):
            #     if tasks == self.contingency_name:
            #         task_model_dict['']
            contingency_plan_anytree = DictImporter().import_(self.contingency_plan)
            contingency_leaf = list(anytree.PostOrderIter(contingency_plan_anytree, filter_=lambda node: node.is_leaf))
            for task_nodes in contingency_leaf:
                    task_model_dict[task_nodes.id] = {'agent_model':
                                                        task_nodes.agent}
                    for agent in task_nodes.agent:
                        task_model_dict[task_nodes.id]['duration_model'] = {
                            agent: {'id': 'det', 'mean': 9}}
        with open('problem_description/ATV_Assembly/cont_task_model_ATV.yaml', 'w') as file:
            yaml.safe_dump(task_model_dict, file)
    

def main():
    contingency_handling = ContingencyManager()

    print('-------initialized contingency manager-------')


if __name__ == '__main__':
    main()
