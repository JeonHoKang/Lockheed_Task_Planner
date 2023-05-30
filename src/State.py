class State(object):
    def __init__(self) -> None:
        self.task_states = None  # Dictionary with id as task id
        self.current_executing_tasks = {}  # Dictionary with id as task id, and agent as
        self.agent_states = None
        self.time = 0
        self.htn = None
        self.contingency_tasks = []
        self.original_htn = None

    def __repr__(self) -> str:
        return "Task state: " + str(self.task_states) + "\nCurrent Actions:" + str(self.current_executing_tasks) + "\nAgent States:" + str(self.agent_states)
