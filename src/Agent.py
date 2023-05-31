class Agent:

    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.agent_state = "available"  # can be avaialble or busy
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

    def __repr__(self) -> str:
        return self.agent_id + "-"+self.agent_state+":"+str(self.agent_task) + "type: " + self.agent_type
