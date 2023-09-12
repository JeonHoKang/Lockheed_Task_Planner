import yaml
import collections
from tree_toolset import TreeToolSet
from Agent import Agent
from contingency_manager import ContingencyManager
from MILP_scheduler import HtnMilpScheduler

class AlterTree:
    """ LLM can call these methods to alter the htn tree"""

    def __init__(self):
        """
        Initialize AlterTree

        Parameters
            None

        """

        # import
        self.htn_dict = self.load_current_htn()
        self.task_model_dict = self.load_current_task_model()
        htn_dict = self.htn_dict
        task_model_dict = self.task_model_dict
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
        contingency_handling = ContingencyManager()
        # contingency_handling.set_problem_dir(problem_dir)
        self.contingency_name = contingency_handling.contingency_name
        self.contingency_plan = {'id': f'recovery-contingency_action-{self.contingency_name}', 'type': 'sequential',
                                 'children': []}
        contingency_node = TreeToolSet().search_tree(
            htn_dict, self.contingency_name)
        contingency_handling.split_contingency_and_normal(
            htn_dict, contingency_node, self.contingency_plan)
        print('initialized')

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

    def add_node(self, parent_id, child_id, child_type, agent=None, duration=None, order_number=0):
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
            agent (str)
                if the type is atomic, input which agent will be performing the task
            duration (int)
                if the type is atomic, also input what the duration for the agent will be
            order_number (int)
                defaults to 0.
                from left to right, order number of the new child node.
        """
        assert type(order_number) == int, "order number should be integer"
        assert child_id not in self.list_node_ids, "no duplicate names"
        # child_id = f'recovery-{child_id}'
        htn_dictionary = self.htn_dict
        task_model_dictionary = self.task_model_dict
        input_order_number = order_number
        node_type = type

        def insert_child(dictionary_htn, target_id, node_added_id, type_child, insert_order=0):
            if type_child == 'atomic':
                new_element = {'id': node_added_id, 'type': type_child, 'agent': [agent]}
                self.add_agent_model(child_id, agent, duration)
            else:
                new_element = {'id': node_added_id, 'type': type_child, 'children': []}
            if dictionary_htn['id'] == target_id:
                if 'children' not in dictionary_htn:
                    dictionary_htn['children'] = []
                    del dictionary_htn['agent']
                    dictionary_htn['type'] = node_type
                    dictionary_htn['children'].append(new_element)
                else:
                    if len(dictionary_htn['children']) < insert_order:
                        print("exceeds the number of children - Defaulting to first child")
                        dictionary_htn['children'].append(new_element)
                    else:
                        dictionary_htn['children'].append(new_element)

            else:
                if 'children' in dictionary_htn:
                    for child in dictionary_htn['children']:
                        insert_child(child, target_id, node_added_id, type_child, insert_order)

        insert_child(htn_dictionary, parent_id, child_id, child_type, insert_order=0)

    def add_agent_model(self, node_id, agent_id, agent_duration):
        """
        AddAgentModel

        Parameters
        parent_id:
        agent_id:
        agent_duration:
        """
        task_model = self.task_model_dict
        task_model[node_id] = {'agent_model': [agent_id],
                               'duration_model': {agent_id: {'id': 'det', 'mean': agent_duration}}}
        print("Inputting task model")

    def set_agent_state(self, agent_id, availability):
        """
        sets the agent state to avaiable or unavailable

        Parameters
            agent_id (str)
            availability (str)
                available
                unavailable

        """
        Agent(agent_id).set_agent_state(availability)

    def export_new_htn(self):
        """
        Exports the newly altered HTN to yaml file format for permanent storage

        safe_dict_yaml_export

        Parameters
        export_dictionary:
        problem_dir:
        file_name:
        """
        task_model_file = "problem_description/ATV_Assembly/current_task_model_ATV.yaml"
        htn_file = "problem_description/ATV_Assembly/current_ATV_Assembly_Problem.yaml"
        print('-----created------')
        print(htn_file)
        print(task_model_file)
        with open(htn_file, 'w') as file1:
            yaml.safe_dump(self.htn_dict, file1, sort_keys=False)
        with open(task_model_file, 'w') as file2:
            yaml.safe_dump(self.task_model_dict, file2, sort_keys=False)
