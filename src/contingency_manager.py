import copy
import yaml
# import anytree
# from anytree import AnyNode, PostOrderIter, find_by_attr
# from anytree.exporter import DictExporter
# from anytree import RenderTree  # just for nice printing
# from anytree.importer import DictImporter
# from anytree.exporter import DictExporter
import Lockheed_task_scheduler

# Load the YAML file
# ------- While ROS node is running ------


class Contingency_Manager(object):
    def __init__(self):
        super().__init__()
        self.contingency = False
        contingency_occur = 1
        # print(data['children'][0]['children'][0]['children'][0])
        scheduler = Lockheed_task_scheduler.HtnMilpScheduler()
        scheduler.set_dir("problem_description/ATV_Assembly/")
        scheduler.import_problem("problem_description_ATV.yaml")
        scheduler.create_task_model()
        htn = scheduler.import_htn()
        self.contingency_name = 'p1_scew_bolt_for_rear_left_wheel3'
        self.htn_dict = scheduler.multi_product_dict
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

    def geneate_contingency_plan(self):
        contingency_planning_node = {}
        contingency_planning_node['id'] = 'contingency_plan'
        contingency_planning_node['type'] = 'sequential'
        
        protocol1 = {}
        protocol2 = {}
        protocol3 = {}
        protocol4 = {}
        protocol5 = {}
        protocol6 = {}
        protocol7 = {}
        protocol8 = {}
        protocol9 = {}
        protocol10 = {}
        original_task = copy.deepcopy(self.contingency_node)
        contingency_planning_node['children'] = [
            protocol1, protocol2, protocol3, protocol4, original_task]
        original_task['id'] = 'recovery-' + self.contingency_node['id'][3:]
        protocol1['id'] = 'recovery-unscrew_operation'
        protocol1['type'] = 'parallel'
        protocol1['children'] = [protocol5,protocol6,protocol7]
        protocol2['id'] = 'recovery-remove_rear_left_wheel'
        protocol2['type'] = 'atomic'
        protocol2['agent'] = ['r2']
        protocol3['id'] = 'recovery-rescrew_operation'
        protocol3['type'] = 'parallel'
        protocol3['children'] = [protocol8,protocol9,protocol10]
        protocol4['id'] = 'recovery-notify execution monitor'
        protocol4['type'] = 'atomic'
        protocol4['agent'] = ['H1']
        protocol5['id'] = 'recovery-unscrew_rear_left_wheel_screw1'
        protocol5['type'] = 'atomic'
        protocol5['agent'] = ['r3']
        protocol6['id'] = 'recovery-unscrew_rear_left_wheel_screw1'
        protocol6['type'] = 'atomic'
        protocol6['agent'] = ['r3']
        protocol7['id'] = 'recovery-unscrew_rear_left_wheel_screw1'
        protocol7['type'] = 'atomic'
        protocol7['agent'] = ['r3']
        protocol8['id'] = 'recovery-unscrew_rear_left_wheel_screw1'
        protocol8['type'] = 'atomic'
        protocol8['agent'] = ['r3']
        protocol9['id'] = 'recovery-unscrew_rear_left_wheel_screw1'
        protocol9['type'] = 'atomic'
        protocol9['agent'] = ['r3']
        protocol10['id'] = 'recovery-unscrew_rear_left_wheel_screw1'
        protocol10['type'] = 'atomic'
        protocol10['agent'] = ['r3']
        return contingency_planning_node

    def Add_Handle_Node(self, htn_dictionary, failed_task, contingency_plan):

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
            for task_nodes in self.contingency_plan['children']:
                if task_nodes['type'] == 'atomic':
                    task_model_dict[task_nodes['id']] = {'agent_model':
                                                        task_nodes['agent']}
                for agent in task_nodes['agent']:
                    task_model_dict[task_nodes['id']]['duration_model'] = {
                        agent: {'id': 'det', 'mean': 6}}
        with open('problem_description/ATV_Assembly/cont_task_model_ATV.yaml', 'w') as file:
            yaml.safe_dump(task_model_dict, file)


def main():
    contingency_handling = Contingency_Manager()

    print('-------initialized contingency manager-------')


if __name__ == '__main__':
    main()
