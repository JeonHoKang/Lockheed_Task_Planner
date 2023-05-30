class Agent:

    def __init__(self, agent_id, agent_type):
        self.agent_id = agent_id
        self.agent_state = "available"  # can be avaialble or busy
        self.agent_type = agent_type
        self.agent_location = None
        self.agent_task = None
        # Agent State
        # Agent Type
        # Agent Location

    def __repr__(self) -> str:
        return self.agent_id + "-"+self.agent_state+":"+str(self.agent_task) + "type: " + self.agent_type
