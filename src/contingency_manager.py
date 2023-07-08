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
        self.contingency_name = 'p1_scew_bolt_for_rear_left_wheel3'
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
        operations_list  = set()
        contingency_list = ["broken_upper_body_frame", "engine_leaking"]
        contingency_planning_node['id'] = 'contingency_plan'
        contingency_planning_node['type'] = 'sequential'
        contingency_planning_node['children'] = []
        enm_notification_node['id'] = 'recovery-notify_execution_monitor'
        enm_notification_node['type'] = 'atomic'
        enm_notification_node['agent'] = ['H']
        for cont in contingency_list:
            current_contingency_policy = dict_policies[cont]
            contingency_policy_list.append(current_contingency_policy)
            operations_list.add(current_contingency_policy['operation_id'])
        policy_in_order = self.search_hierarchy(operations_list)
        for task in list(policy_in_order.values()):
            for item in contingency_policy_list:
                if task.id[3:] == item['operation_id']:
                    contingency_planning_node['children'].append(item['policy'])
        original_task = copy.deepcopy(self.contingency_node)
        original_task['id'] = 'recovery-' + self.contingency_node['id'][3:]
        contingency_planning_node['children'].append(enm_notification_node)
        contingency_planning_node['children'].append(original_task)
        return contingency_planning_node

    def search_hierarchy(self, handling_list):
        def check_parent_type(contingency_list):
            joined_policy = {}
            original_node1 = copy.deepcopy(contingency_list[0])
            original_node2 = copy.deepcopy(contingency_list[1])
            while contingency_list[0].is_root != True:
                if contingency_list[0].parent == contingency_list[1].parent:
                    source_node = contingency_list[0].parent # check for commmon parent and check for its type
                    source_child_node = source_node.children
                # set to parent
                    index1 = source_child_node.index(contingency_list[0])
                    index2 = source_child_node.index(contingency_list[1])
                    joined_policy[index1] = original_node1
                    joined_policy[index2] = original_node2
                    joined_policy = dict(sorted(joined_policy.items()))
                    break
                contingency_list[0] = contingency_list[0].parent
                contingency_list[1] = contingency_list[1].parent
            return joined_policy
        
        contingency_product = []
        for task in handling_list: # task in operations that went wrong
            for descent in self.product_htn_anytree.descendants:
                if descent.id[3:] == task:
                    contingency_product.append(descent)
        ordered_policy = check_parent_type(contingency_product)
        return ordered_policy

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
