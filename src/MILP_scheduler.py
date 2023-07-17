""""
Contributors:

Jeon Ho Kang
Neel Dhanaraj

Task allocation problem

"""
import os.path
import copy
import itertools
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ortools.sat.python import cp_model
import matplotlib.pyplot as plt
import yaml
import anytree
from anytree import RenderTree  # just for nice printing
from anytree.importer import DictImporter
from Agent import Agent
from Task import Task
from tree_toolset import TreeToolSet


class HtnMilpScheduler:
    """
    Uses MILP to generate schedule
    """

    def __init__(self) -> None:
        self.task_object = None
        self.current_problem_description = None
        self.multi_product_htn = None
        self.all_diff_constraints = []
        self.model = None
        self.durations = []
        self.starts = []
        self.ends = []
        self.objective = None
        self.solver = cp_model.CpSolver()
        self.makespan = None
        self.start_var = None
        self.task_start_vars = None
        self.task_end_vars = None
        self.task_interval_vars = None
        self.problem_description = None
        self.problem_dir = None
        self.num_products = 1
        self.agent_team_model = {}
        self.multi_product_dict = {}
        self.initial_run = False
        self.current_problem = "problem_description/ATV_Assembly/current_problem_description_ATV.yaml"
        if os.path.isfile(self.current_problem):
            self.initial_run = False
        else:
            self.initial_run = True
        self.contingency = True
        if self.initial_run is True:
            self.contingency = False
        self.contingency_name = 'p1_pick_rear_frame'
        self.contingency_node = None
        self.unavailable_agent_bool = False
        self.unavailable_agent = 'r1'
        self.sorted_assignment = {}

    def set_dir(self, problem_dir):
        """Sets the problem instance directory"""
        self.problem_dir = problem_dir

    def import_problem(self, prob_description_yaml):
        """Imports a problem description"""

        # Get the directory where problem is located
        file_dir = self.problem_dir + prob_description_yaml
        # open the file directory
        with open(file_dir, 'r') as stream:
            try:
                # load the yaml file
                # Converts yaml document to python object
                self.problem_description = yaml.safe_load(stream)
            # Printing dictionary
            except yaml.YAMLError as dict_e:
                print(dict_e)
        if self.initial_run:
            self.current_problem_description = copy.deepcopy(self.problem_description)
            self.current_problem_description["htn_model_id"] = "current_ATV_Assembly_Problem.yaml"
            self.current_problem_description["task_model_id"] = "current_task_model_ATV.yaml"
            TreeToolSet().dict_yaml_export(self.current_problem_description, self.problem_dir,
                                           "current_problem_description_ATV.yaml")

    def load_agent_model(self):
        """Loads agent model from yaml file"""
        agents = self.problem_description['agents']
        agents.append('X')
        for agent_id in agents:
            self.agent_team_model[agent_id] = Agent(
                agent_id)
        self.agent_team_model['X'].set_agent_state('unavailable')

    def create_task_model(self):
        """Creates a task model with the existing HTN"""
        self.load_agent_model()
        task_model_yaml = self.problem_description["task_model_id"]
        file_dir = self.problem_dir + task_model_yaml
        task_model = {}
        with open(file_dir, 'r') as stream:
            try:
                # Converts yaml document to python object
                task_model1 = yaml.safe_load(stream)
                # for ease of manipulation convert the task model1 to the list
                list_task_model = list(task_model1)
            except yaml.YAMLError as e:
                print(e)

            if self.initial_run:
                TreeToolSet().dict_yaml_export(task_model1, self.problem_dir,
                                               "current_task_model_ATV.yaml")  # create current file for future
            for product in range(self.num_products):
                for i in range(len(task_model1)):
                    # just indexing how long this is
                    cur_leaf_node = product * \
                                    len(task_model1) + (i + 1)
                    if cur_leaf_node <= len(task_model1):
                        if list_task_model[i][:8] == 'recovery':
                            task_model[list_task_model[i]] = {}
                        else:
                            task_model['p1_' +
                                       list_task_model[i]] = {}
                    elif cur_leaf_node > len(task_model1):
                        if list_task_model[i][:8] == 'recovery':
                            task_model[list_task_model[i]] = {}
                        else:
                            task_model['p{}_'.format(
                                product + 1) + list_task_model[i]] = {}
            for i in range(self.num_products):
                for c, agents in enumerate(task_model1):
                    task_model_index = (c + 1) + len(task_model1) * i
                    if list_task_model[c][:8] == 'recovery':
                        task_model[list_task_model[c]
                        ] = task_model1[list_task_model[c]]
                    else:
                        task_model["p{}_".format(i + 1)
                                   + list_task_model[c]] = task_model1[list_task_model[c]]

        self.task_object = self.create_task_object(task_model)

    def create_task_object(self, tasks):
        '''
        Creates a class object task for each task models
        '''
        task_model = {}
        for key, value in tasks.items():
            task_id = key
            agent_model = value['agent_model']
            duration_model = value['duration_model']
            task_model[key] = Task(task_id, agent_model, duration_model)
        return task_model

    def visualize(self, t_assignment):
        window = tk.Tk()
        window.title("Gant Chart - Multi-Robot SChedule")
        frame = ttk.Frame(window, width=200)
        frame.pack(pady=10)
        # Create the graph frame
        graph_frame = ttk.Frame(frame)
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        fig, gnt = plt.subplots(figsize=(200, 5))
        fig.set_figwidth(60)
        # delcare colors for the charts
        blue = 'tab:blue'
        brown = 'tab:brown'
        orange = 'tab:orange'
        pink = 'tab:pink'
        green = 'tab:green'
        gray = 'tab:gray'
        red = 'tab:red'
        olive = 'tab:olive'
        purple = 'tab:purple'
        cyan = 'tab:cyan'
        # Create a list of colors
        list_colors = [blue, orange, pink,
                       green, gray, red, olive, purple, cyan, brown]
        color_idx = 0
        # x step size
        x_step = 25
        # First y-tick
        first_y_tick = 15
        # y-tick gap
        # init ticks and lable
        list_ytick_labels = []
        list_yticks = []
        # init xtick with value 0
        xticks = [0]
        minimized_factor = 3
        x_limit = self.horizon
        # Setting X-axis limits
        gnt.set_xlim(0, x_limit)

        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('seconds since start')
        gnt.set_ylabel('agent')
        # fig.set_figheight(10)
        # fig.set_figwidth(500``)
        # Setting ticks on y-axis
        for i in range(int(x_limit / x_step)):
            xticks.append(i * x_step)
        gnt.set_xticks(xticks)

        # Labelling tickes of y-axis

        # Setting graph attribute
        gnt.grid(True)
        y_tick_gap = 10
        list_labels = []
        task_index = 1
        # Declaring a bar in schedule
        for c, agent in enumerate(self.agent_id):  # for count and agent names
            # plot bar chart
            for assignment in t_assignment[agent]:
                for task, (start, end) in assignment.items():
                    if color_idx >= 9:
                        color_idx = 0
                    duration = end - start
                    gnt.broken_barh([(start, duration)], (10 * (c + 1), 9),
                                    facecolors=(list_colors[color_idx]))
                    font_size = 6
                    gnt.text((start + end) / 2, 10 * (c + 1) + 4.5,
                             f'T{task_index}', ha='center', va='center', fontsize=font_size)

                    list_labels.append(task)
                    task_index += 1
                    color_idx += 1
            # append to the y ticks
            list_ytick_labels.append(agent)
            list_yticks.append(first_y_tick + y_tick_gap * c)

        gnt.set_title('Task Assignment')
        # se final ytick
        list_yticks.append(first_y_tick + y_tick_gap * len(list_ytick_labels))
        gnt.set_yticklabels(list_ytick_labels)
        gnt.set_yticks(list_yticks)
        # Setting Y-axis limits
        gnt.set_ylim(0, list_yticks[len(list_yticks) - 1])

        listbox_frame = ttk.Frame(frame)
        listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar2 = ttk.Scrollbar(
            listbox_frame, orient=tk.HORIZONTAL)
        scrollbar2.pack(side=tk.BOTTOM, fill=tk.X)

        # listbox_font = Font(size=12)
        listbox = tk.Listbox(
            listbox_frame, yscrollcommand=scrollbar.set, xscrollcommand=scrollbar2.set, font='Aerial', width=20)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=listbox.yview)
        # Configure the scrollbar to work with the listbox
        scrollbar2.config(command=listbox.xview)

        for i, label in enumerate(list_labels):
            listbox.insert(tk.END, f"{i + 1}: {label}")
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        scrollbar_canvas = tk.Scrollbar(
            frame, orient=tk.HORIZONTAL, command=canvas.get_tk_widget().xview)
        canvas.get_tk_widget().configure(xscrollcommand=scrollbar_canvas.set)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH,
                                    expand=True)
        scrollbar_canvas.pack(fill=tk.X, side=tk.BOTTOM)
        canvas.get_tk_widget().configure(scrollregion=canvas.get_tk_widget().bbox("all"))

        if self.initial_run:
            plt.savefig("gant.png")
        else:
            plt.savefig("current_gant.png")

        # Add the Scrollbar to the window
        def on_window_close():
            window.quit()

        window.protocol("WM_DELETE_WINDOW", on_window_close)
        window.mainloop()

    def import_htn(self, print_htn=True):  # HTN import
        def edit_tree(dictionary, product_num):
            dictionary['id'] = f"p{product_num}_{dictionary['id']}"
            if 'children' in dictionary:
                for child in dictionary['children']:
                    edit_tree(child, product_num)

        combined_dict = {}
        htn_model_yaml = self.problem_description["htn_model_id"]  # HTN id
        file_dir = self.problem_dir + htn_model_yaml  # directory + htn_model
        with open(file_dir, "r") as data:
            try:
                self.dict = yaml.safe_load(data)
            except yaml.YAMLError as e:
                print(e)
        num_products = self.num_products
        children = []

        if self.initial_run:
            self.multi_product_dict = {}
            self.multi_product_dict['id'] = 'Multi_Product_Assembly'
            self.multi_product_dict['type'] = 'independent'
            self.multi_product_dict['children'] = []
            for p in range(num_products):
                product_htn = copy.deepcopy(self.dict)
                edit_tree(product_htn, p + 1)
                self.multi_product_dict['children'].append(product_htn)
                # For multi-product formulation, we introduce a task root at the highest
                # hiararchy
                self.multi_product_htn = DictImporter().import_(self.multi_product_dict)

            TreeToolSet().dict_yaml_export(self.multi_product_dict, self.problem_dir,
                                           "current_ATV_Assembly_Problem.yaml")
        else:
            self.multi_product_htn = DictImporter().import_(self.dict)  # to avoid duplicating p1
            self.multi_product_dict = self.dict
        if print_htn:
            print(RenderTree(self.multi_product_htn))
        return self.multi_product_htn

    def generate_sequential_task_constraints(self, atomic_action_groups):
        model = self.model
        starts = self.task_start_vars
        ends = self.task_end_vars

        while len(atomic_action_groups) > 1:
            prior_atomic_actions = atomic_action_groups[0]
            subsequent_atomic_actions = atomic_action_groups[1]

            for s_action in subsequent_atomic_actions:
                s_id = s_action.id
                for p_action in prior_atomic_actions:
                    p_id = p_action.id
                    model.Add(starts[s_id] >= ends[p_id])
            atomic_action_groups.pop(0)

    def generate_multiproduct_task_contrasints(self, atomic_action_groups1, atomic_action_groups2):
        '''
        This comstraint generates a constraint to go from product1 to product2
        '''
        model = self.model
        starts = self.task_start_vars
        ends = self.task_end_vars
        self.preserved2 = []
        # while len(atomic_action_groups2) >= 0:
        product1_atomic_actions = atomic_action_groups1
        subsequent_atomic_actions = atomic_action_groups2
        for s_action in subsequent_atomic_actions:
            s_id = s_action.id
            s_parent = s_action.parent.id
            for p_action in product1_atomic_actions:
                p_id = p_action.id
                p_parent = p_action.parent.id
                if p_parent[3::] == s_parent[3::]:
                    model.Add(starts[s_id] >= ends[p_id])

    def generate_independent_task_constraints(self, atomic_action_groups):
        model = self.model
        intervals = self.task_interval_vars
        count = 0
        atomic_action_groups_sorted = sorted(
            atomic_action_groups, key=lambda x: len(x))
        count = 0
        while len(atomic_action_groups_sorted) > 1:
            group = atomic_action_groups_sorted.pop()
            flattened_nodes = list(itertools.chain(
                *atomic_action_groups_sorted))
            for node1 in group:
                for node2 in flattened_nodes:
                    model.AddNoOverlap(
                        [intervals[node1.id], intervals[node2.id]])
                    count = count + 1

    def create_task_network(self):
        htn = self.multi_product_htn
        multi_product_index = 0
        if htn is None:
            raise Exception("no htn loaded")

        constraint_nodes = []
        constraint_nodes.append(htn)
        atomic_action_groups1 = [[] for i in range(self.num_products)]
        while constraint_nodes:
            node = constraint_nodes.pop(0)
            node_children = node.children
            atomic_action_groups = []
            for node_child in node_children:
                if node_child.type == "atomic":
                    atomic_action_groups.append([node_child])
                    for i in range(self.num_products):
                        # Meaning it is the first product
                        if node_child.id[1:2] == str(i + 1):
                            atomic_action_groups1[i].append(
                                node_child)
                else:
                    constraint_nodes.append(node_child)
                    atomic_action_groups.append(
                        (list(anytree.PostOrderIter(node_child, filter_=lambda node: node.is_leaf))))

            if node.type == "parallel":
                continue
            elif node.type == "sequential":
                self.generate_sequential_task_constraints(atomic_action_groups)
            elif node.type == "independent":
                self.generate_independent_task_constraints(
                    atomic_action_groups)
            else:
                raise Exception(
                    "Unknown node type encountered in HTN:" + node.type)
        # If we have only two products wo only check once
        for k in range(self.num_products):
            # hence it will be num_products
            if k == 0:  # and skip 0 to check only once
                continue
            else:
                for j in range(self.num_products + multi_product_index):
                    if j == 0:  # and skip 0 to check only once
                        continue
                    else:
                        self.generate_multiproduct_task_contrasints(
                            atomic_action_groups1[k - 1], atomic_action_groups1[k - 1 + j])
                multi_product_index -= 1

    def set_dependencies_by_dfs(self, start):
        visited = []  # Set to track visited vertices
        edges = []
        stack = [start]  # Stack to keep track of vertices to visit
        type_list = []
        full_id = []
        while stack:
            vertex = stack.pop()  # Pop a vertex from the stack

            if vertex.id not in visited:
                # Process the vertex (in this case, print it)
                visited.append(vertex.id)  # Mark the vertex as visited

                # Add adjacent vertices to the stack
                if vertex.is_leaf != True:
                    for child in reversed(vertex.children):
                        stack.append(child)
                else:
                    self.task_object[vertex.id].set_task_state('infeasible')

    def set_dependencies_infeasible(self, node):
        list_siblings = list(node.parent.children)
        idx = list_siblings.index(node) + 1
        parent = node.parent
        child = node
        while parent.is_root != True:
            if parent.type == 'sequential':
                parent_siblings = list(parent.children)
                parent_idx = parent_siblings.index(child) + 1
                for element in parent_siblings[parent_idx:len(parent_siblings)]:
                    if "contingency" in element.id:
                        continue
                    if element.is_leaf:
                        self.task_object[element.id].set_task_state(
                            'infeasible')
                    else:
                        self.set_dependencies_by_dfs(element)
            child = parent
            parent = parent.parent

    def generate_model(self):
        if self.problem_description == None:
            raise Exception("No problem description imported")
        else:
            prob = self.problem_description
        self.model = cp_model.CpModel()
        task_object = self.task_object
        task_list = list(self.task_object.keys())
        htn_nodes = list(anytree.PostOrderIter(self.multi_product_htn))
        ### Create Task Assignment Agent Decision Variables ###
        agent_decision_variables = {}  # agent Decision Variables
        agent_dur_constraints = {}
        task_sched_vars = {}
        self.task_start_vars = {}
        self.task_end_vars = {}
        self.task_interval_vars = {}
        agent_start_vars = {}
        agent_end_vars = {}
        agent_interval_vars = {}
        agent_makespan_vars = {}
        agent_teams = list(self.agent_team_model.keys())
        for agent in agent_teams:
            agent_decision_variables[agent] = {}
            agent_dur_constraints[agent] = {}
            agent_start_vars[agent] = {}
            agent_end_vars[agent] = {}
            agent_interval_vars[agent] = {}

        if self.contingency:
            self.task_object[self.contingency_name].set_task_state('failed')
            self.contingency_node = self.task_object[self.contingency_name]
        if self.unavailable_agent_bool:
            self.agent_team_model[self.unavailable_agent].set_agent_state(
                'unavailable')

        # self.task_object['p1_Pick_and_Place_Top_Panel'].set_task_state(
        #     'succeeded')
        # print(self.task_object['p1_Pick_and_Place_Top_Panel'].task_state)

        def find_contingency_nodes(unavailable_agent):
            contingency_nodes = []
            for node in htn_nodes:
                if node.type != 'atomic':
                    continue
                if self.contingency_name != '':
                    if node.id == self.contingency_name:
                        contingency_nodes.append(node)
                if self.unavailable_agent_bool:
                    if unavailable_agent in node.agent:
                        contingency_nodes.append(node)
            return contingency_nodes

        if self.contingency or self.unavailable_agent_bool:
            contingency_node_list = find_contingency_nodes(
                self.unavailable_agent)
            # From the found contingency list move upward on tree to set all the children infeasible
            for node in contingency_node_list:
                self.set_dependencies_infeasible(node)

        for task in task_list:
            for agent in agent_teams:
                if agent not in task_object[task].agent_id:
                    continue
                if self.agent_team_model[agent].agent_state == 'available' and self.task_object[
                    task].task_state == 'unattempted':
                    agent_decision_variables[agent][task] = self.model.NewBoolVar(
                        'x' + agent + '[' + task + ']')
        # Create Start End Duration Interval Variables

        starts = []
        ends = []
        intervals = []

        # calculate the horizon for the entire plan
        self.horizon = 0
        for task in task_object.keys():
            dur = 0
            for agent, agent_dur_model in self.task_object[task].duration_model.items():
                task_dur = max(dur, agent_dur_model['mean'])
            self.horizon = self.horizon + task_dur

        # Task varriables
        for task in task_object.keys():
            # Define Main Start End , Duration and interval variables
            start = self.model.NewIntVar(0, self.horizon, 'start_' + task)
            duration = self.model.NewIntVar(
                0, self.horizon, 'duration_' + task)
            self.durations.append(duration)
            end = self.model.NewIntVar(0, self.horizon, 'end_' + task)
            starts.append(copy.deepcopy(start))
            self.task_start_vars[task] = start
            ends.append(end)
            self.task_end_vars[task] = end
            interval = self.model.NewIntervalVar(
                start, duration, end, 'interval_' + task)
            task_sched_vars[task] = copy.deepcopy([start, duration, end])
            intervals.append(interval)
            self.task_interval_vars[task] = interval
            for agent in prob["agents"]:
                if agent not in self.task_object[task].duration_model.keys():
                    continue
                if self.agent_team_model[agent].agent_state == 'unavailable':
                    continue
                if self.task_object[task].task_state != 'unattempted':
                    continue
                agent_dur_constraints[agent][task] = self.model.Add(
                    self.task_object[task].duration_model[agent]['mean'] == duration).OnlyEnforceIf(
                    agent_decision_variables[agent][task])
                agent_start_vars[agent][task] = self.model.NewIntVar(
                    0, self.horizon, 'start_on_' + task + agent)
                agent_end_vars[agent][task] = self.model.NewIntVar(
                    0, self.horizon, 'end_on_' + task + agent)
                agent_interval_vars[agent][task] = self.model.NewOptionalIntervalVar(agent_start_vars[agent][task],
                                                                                     duration,
                                                                                     agent_end_vars[agent][task],
                                                                                     agent_decision_variables[agent][
                                                                                         task],
                                                                                     'interval_on_' + task + agent)

                self.model.Add(agent_start_vars[agent][task] == start).OnlyEnforceIf(
                    agent_decision_variables[agent][task])

        for agent in prob["agents"]:
            self.model.AddNoOverlap(list(agent_interval_vars[agent].values()))

        # self.create_task_network_constraints(self.model,starts,ends)
        self.create_task_network()

        # Define Makespace variable
        t = self.model.NewIntVar(0, self.horizon, 't')
        s = self.model.NewIntVar(0, 100000000000, 's')
        self.start_var = s
        o = self.model.NewIntVar(0, 100000000000, 'o')

        self.objective = o
        self.makespan = t
        self.model.AddMaxEquality(t, ends)
        self.model.Add(s == sum(starts))
        self.model.Add(o == 10 * t + s)
        self.objective = o
        self.makespan = t

        #### Define Objective ####
        self.model.Minimize(o)
        for task in self.task_object.keys():
            for agent in self.task_object[task].agent_id:
                if self.task_object[task].task_state != 'unattempted' or self.agent_team_model[
                    agent].agent_state != 'available':
                    continue
                else:
                    self.all_diff_constraints.append(self.model.Add(sum(
                        [agent_decision_variables[agent][task] for agent in self.task_object[task].agent_id]) == 1))

        #### Create Solver and Solve ####
        solver = self.solver
        solver.parameters.num_search_workers = len(self.agent_team_model)
        solver.parameters.max_time_in_seconds = 12
        status = solver.Solve(self.model)

        if status == cp_model.OPTIMAL:
            print("optimal solution")
            print(solver.Value(self.makespan))
            print(solver.WallTime())
        elif status == cp_model.FEASIBLE:
            print("solution is feasible")
            print(solver.Value(self.makespan))
            print(solver.WallTime())
        else:
            print("no solution found")

        t_assignment = {}
        visual_t_assignment = {}
        self.agent_id = []
        self.task_id = []
        for agent_id, tasks in agent_decision_variables.items():
            self.agent_id.append(agent_id)
            visual_t_assignment[agent_id] = []
            t_assignment[agent_id] = {}

        task_count = 0
        for agent_id, tasks in agent_decision_variables.items():
            for task_id, vars in tasks.items():
                if solver.Value(agent_decision_variables[agent_id][task_id]) == 1:
                    val = agent_id
                    self.task_id.append(task_id)
                    t_assignment[val][task_id] = {}
                    t_assignment[val][task_id]["StarttoEnd"] = list(
                        [solver.Value(self.task_start_vars[task_id]), solver.Value(
                            self.task_end_vars[task_id])])
                    visual_t_assignment[val].append(
                        {task_id: (solver.Value(self.task_start_vars[task_id]), solver.Value(
                            self.task_end_vars[task_id]))})
                prev_task = task_id
        sorted_t_assignment = {}
        for agent in self.agent_id:
            assignment = visual_t_assignment[agent]
            sorted_t_assignment[agent] = sorted(
                assignment, key=lambda x: list(x.values())[0][0])
        self.export_yaml(sorted_t_assignment)
        self.visualize(sorted_t_assignment)

    def export_yaml(self, t_assignment):
        task_allocation = t_assignment
        i = 1
        schedule_yaml = {}
        for agent, assignment in task_allocation.items():
            schedule_yaml[agent] = {}
            for element in assignment:
                for task, (start, end) in element.items():
                    schedule_yaml[agent][i] = {}
                    schedule_yaml[agent][i][task] = {
                        'start': start, 'end': end}
                    i += 1
            if schedule_yaml[agent] == {}:
                schedule_yaml[agent] = 'None Scheduled yet'

        if self.initial_run:
            TreeToolSet().dict_yaml_export(schedule_yaml, self.problem_dir, "initial_visualize_helper_text.yaml")
        else:
            TreeToolSet().dict_yaml_export(schedule_yaml, self.problem_dir, "current_visualize_helper_text.yaml")

        self.export_schedule_text(t_assignment)

    def export_schedule_text(self, t_assignment):
        """
        Format ROS service
        - id 
        - agent
        - order that the agent is performing the task
        - sequential constraint id

        """
        task_allocation = t_assignment
        # print(task_allocation)
        schedule_yaml = []
        for agent, assignment in list(task_allocation.items()):
            for count, assign in enumerate(assignment):
                for task, (start, end) in assign.items():
                    schedule_yaml.append({
                        'task_id': task, 'agent': agent, 'agent_specific_order': count + 1,
                        'sequential_dependencies': '', 'start': start, 'end': end})

        schedule_yaml = sorted(
            schedule_yaml, key=lambda x: x['start'])

        prev_schedule = None
        for i, schedule in enumerate(schedule_yaml):
            if prev_schedule is None:
                prev_schedule = schedule_yaml[i]
            elif schedule['start'] >= prev_schedule['end']:
                schedule['sequential_dependencies'] = prev_schedule['task_id']
                prev_schedule = schedule_yaml[i]

        if self.initial_run:
            TreeToolSet().dict_yaml_export(schedule_yaml, self.problem_dir, "initial_task_allocation.yaml")
        else:
            TreeToolSet().dict_yaml_export(schedule_yaml, self.problem_dir, "current_task_allocation.yaml")


def main():
    """
    Main 
    """
    scheduler = HtnMilpScheduler()
    if scheduler.contingency:
        scheduler.set_dir("problem_description/ATV_Assembly/")
        scheduler.import_problem("current_problem_description_ATV.yaml")
    else:
        scheduler.set_dir("problem_description/ATV_Assembly/")
        scheduler.import_problem("problem_description_ATV.yaml")
    scheduler.create_task_model()
    scheduler.import_htn()
    print('--------Initialized-------------')
    scheduler.generate_model()


if __name__ == '__main__':
    main()
