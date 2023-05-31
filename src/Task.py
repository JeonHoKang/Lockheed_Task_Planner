class Task:

    def __init__(self, task_id, agents_model, duration_model):
        self.task_id = task_id
        self.agent_id = agents_model
        self.duration_model = duration_model
        # for agent in range(len(agent_id)):
        #     self.duration_model['agent'] =
        self.task_state = 'unattempted'
        self.agent_types = None
        self.task_agent_uncertainty_models = {}
        self.max_time = None
        self.nominal_duration = None

        self.det_next_state = None  # Used in State representation
        self.expected_task_duration = None  # Used in State representation
        self.hidden_expected_task_duration = None
        # Task State unattempted, inprogress, completed, failed
        # Agent Type
        # Task Gen transiton function
        # Task Start , end time
        self.contingency_model = None
        self.start_time = None
        self.finish_time = None
        self.agent = None

    def __repr__(self) -> str:
        if self.task_state == "unattempted":
            exp_next_state = ''
            robot = ''
        elif self.task_state != 'inprogress':
            exp_next_state = ''
            robot = self.agent
        else:
            exp_next_state = '->E:' + self.det_next_state + \
                "(" + str(self.expected_task_duration) + ")"
            robot = self.agent
        return self.task_id + ':' + str(self.task_state) + exp_next_state + ':' + robot

    def set_task_state(self, state):
        if state not in ['unattempted', "inprogress", 'succeeded', 'failed']:
            raise Exception
        self.task_state = state
