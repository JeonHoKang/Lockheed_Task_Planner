import os
import yaml
class Agent:

    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.agent_state = "available"  # can be avaialble or unavailable
        self.agent_location = None
        self.agent_task = None
        # Agent State
        # Agent Type
        # Agent Location

    def set_agent_state(self, state):
        if self.agent_state not in ['available', 'unavailable']:
            raise Exception
        else:
            self.agent_state = state
            # current problem
            current_problem = "problem_description/ATV_Assembly/current_problem_description_ATV.yaml"
            if os.path.isfile(current_problem):
                with open(current_problem, 'r') as stream:
                    try:
                        # load the yaml file
                        # Converts yaml document to python object
                        problem_description = yaml.safe_load(stream)
                        problem_description['agents'][self.agent_id] = state
                        # print('agent model update')
                    # Printing dictionary
                    except yaml.YAMLError as dict_e:
                        print(dict_e)
                with open(current_problem, 'w') as file:
                    yaml.dump(problem_description, file, sort_keys=False)

    def __repr__(self) -> str:
        return f'Agent(id={self.agent_id}, state={self.agent_state})'
