import yaml
from tree_toolset import TreeToolSet
import collections


class AlterTree:
    """ LLM can call these methods to alter the htn tree"""

    # Get required components for the assembly

    def __init__(self):
        """
        Initialize AlterTree

        Parameters
            None

        """

        # import
        htn_dict = self.load_current_htn()
        task_model_dict = self.load_current_task_model()

        self.htn_dict = htn_dict
        self.task_model_dict = task_model_dict
        print(htn_dict)
        print(task_model_dict)
        print("___Initialized HTN Alter Tree___")
        self.pairs_with_name, self.pairs_with_full_node = TreeToolSet().create_pairs_with_dfs(htn_dict)
        self.name_node, self.edge_list = TreeToolSet().create_dict_from_list(
            self.pairs_with_name)
        self.id_sequence = TreeToolSet().create_dict_list_from_pairs(
            self.pairs_with_full_node)
        self.id_sequence_list = list(self.id_sequence.values())
        self.list_node_ids = set()
        for node in self.id_sequence_list:
            self.list_node_ids.add(node['id'])
        print('id_sequence_list')

    def load_current_htn(self):
        """
        Loads current HTN to alter
        Parameters
            None

        Returns
            Dictionary of the current htn
        """

        # Imports the yaml file of the problem
        with open("problem_description/ATV_Assembly/current_ATV_Assembly_Problem.yaml", "r") as file:
            current_htn_dict = yaml.safe_load(file)
        return current_htn_dict

    def load_current_task_model(self):
        """
        Loads the current task model of the assembly
        Parameters:
            None

        Returns:
            Dictionary oof the current task model
        """

        with open("problem_description/ATV_Assembly/current_task_model_ATV.yaml", "r") as file:
            current_task_model_dict = yaml.safe_load(file)
        return current_task_model_dict

    def add_node(self, parent_id, child_id, child_type, order_number=0):
        """
        AddNode

        Parameters
            parent_id (str)
                id of the parent to insert new child.
            child_id (str)
                id of the new node that user needs to be appended to parent_id.
            child_type (str)
                among "independent", "parallel", "sequential"
                independent constraint: order does not matter but cannot be worked on together.
                parallel constraint: can be worked on together in any order.
                sequential constraint: need to be in order from left node to the right node.
            order_number (int)
                defaults to 0.
                from left to right, order number of the new child node.
        """
        assert type(order_number) == int, "order number should be integer"
        assert child_id not in self.list_node_ids, "no duplicate names"
        assert parent_id in self.list_node_ids, "parent id needs to be present"
        child_id = f'recovery-{child_id}'
        htn_dictionary = self.htn_dict
        task_model_dictionary = self.task_model_dict
        input_order_number = order_number
        node_type = type

        def insert_child(htn_dictionary, target_id, node_added_id, type_child, insert_order=0):
            if type_child == 'atomic':
                new_element = {'id': node_added_id, 'type': type_child, 'agent': []}
            else:
                new_element = {'id': node_added_id, 'type': type_child, 'children': []}
            if htn_dictionary['id'] == target_id:
                if 'children' not in htn_dictionary:
                    htn_dictionary['children'] = []
                    del htn_dictionary['agent']
                    htn_dictionary['type'] = node_type
                    htn_dictionary['children'].append(new_element)
                else:
                    if len(htn_dictionary['children']) + 1 < insert_order:
                        print("exceeds the number of children - Defaulting to first child")
                        insert_order = 0
                    else:
                        htn_dictionary['children'].insert(insert_order, new_element)

            else:
                if 'children' in htn_dictionary:
                    for child in htn_dictionary['children']:
                        insert_child(child, target_id, node_added_id, type_child, insert_order)
        insert_child(htn_dictionary, parent_id, child_id, child_type, insert_order=0)

    def add_agent_model(self, parent_id, agent_id, agent_duration):
        """
        AddAgentModel

        Parameters
        parent_id:
        agent_id:
        agent_duration:
        """
        pass

    def safe_dict_yaml_export(self, export_dictionary, problem_dir, file_name):
        """
        Expoorts the newly altered HTN to yaml file format for permanent storage

        safe_dict_yaml_export

        Parameters
        export_dictionary:
        problem_dir:
        file_name:
        """
        file_dir = problem_dir + file_name
        print('-----created------')
        print(file_dir)
        with open(file_dir, 'w') as file:
            yaml.safe_dump(export_dictionary, file, sort_keys=False)
