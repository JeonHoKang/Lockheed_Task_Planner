""""
Contributors:

Jeon Ho Kang
Neel Dhanaraj

Task allocation problem

"""


from pyexpat import model
from sched import scheduler
from tkinter import Variable
from xml.sax.handler import DTDHandler
from ortools.linear_solver import pywraplp
import numpy as np
from ortools.sat.python import cp_model
import copy
import matplotlib.pyplot as plt
from collections import OrderedDict
import itertools
import yaml
import anytree
from anytree import AnyNode, PostOrderIter
from anytree.exporter import DictExporter
from anytree import RenderTree  # just for nice printing
from anytree.importer import DictImporter
import matplotlib.pyplot as plt


class HtnMilpScheduler(object):
    def __init__(self) -> None:
        self.htn_model = None
        self.all_diff_constraints = []
        self.h_dur_constraints = []
        self.r_dur_constraints = []
        self.h_durations = None
        self.r_durations = None
        self.task_spec = None
        self.model = None
        self.agent_d_vars = None
        self.num_tasks = None
        self.durations = []
        self.starts = []
        self.ends = []
        self.objective = None
        self.makespans = []
        self.solver = cp_model.CpSolver()
        self.makespan = None
        self.start_var = None
        self.task_start_vars = None
        self.task_end_vars = None
        self.task_interval_vars = None
        self.problem_description = None
        self.htn_model = None
        self.problem_dir = None
        self.num_products = 1

    def set_dir(self, dir):
        """Sets the problem instance directory"""
        self.problem_dir = dir

    def import_problem(self, prob_description_yaml):
        # Get the directory where problem is located
        file_dir = self.problem_dir + prob_description_yaml
        # open the file directory
        with open(file_dir, 'r') as stream:
            try:
                # load the yaml file
                # Converts yaml document to python object
                self.problem_description = yaml.safe_load(stream)
            # Printing dictionary
            except yaml.YAMLError as e:
                print(e)

    def create_task_model(self):
        """Creates a task model with the existing HTN"""
        task_model_yaml = self.problem_description["task_model_id"]
        file_dir = self.problem_dir + task_model_yaml
        self.task_model = {}
        with open(file_dir, 'r') as stream:
            try:
                # Converts yaml document to python object
                self.task_model1 = yaml.safe_load(stream)
                # for ease of manipulation convert the task model1 to the list
                self.list_task_model1 = list(self.task_model1)
                for product in range(self.num_products):
                    for i in range(len(self.task_model1)):
                        cur_leaf_node = (product)*len(self.task_model1)+(i+1)
                        if cur_leaf_node <= len(self.task_model1):
                            self.task_model['p1_' +
                                            self.list_task_model1[i]] = {}
                        elif cur_leaf_node > len(self.task_model1):
                            self.task_model['p{}_'.format(
                                product+1)+self.list_task_model1[i]] = {}
                for i in range(self.num_products):
                    for c, agents in enumerate(self.task_model1):
                        task_model_index = (c+1)+len(self.task_model1)*(i)
                        self.task_model["p{}_".format(i+1)
                                        + self.list_task_model1[c]] = self.task_model1[self.list_task_model1[c]]

            except yaml.YAMLError as e:
                print(e)

    def visualize(self, t_assignment):
        fig, gnt = plt.subplots(figsize=(60, 10))
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
        x_step = 15
        # First y-tick
        first_y_tick = 15
        # y-tick gap
        y_tick_gap = 10
        # init ticks and lable
        list_ytick_labels = []
        list_yticks = []
        # init xtick with value 0
        xticks = [0]
        minimized_factor = 3
        x_limit = self.horizon-self.horizon/minimized_factor
        # Setting X-axis limits
        gnt.set_xlim(0, x_limit)

        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('seconds since start')
        gnt.set_ylabel('agent')
        # fig.set_figheight(10)
        # fig.set_figwidth(500``)
        # Setting ticks on y-axis
        for i in range(int(x_limit/x_step)):
            xticks.append(i*x_step)
        gnt.set_xticks(xticks)

        # Labelling tickes of y-axis

        # Setting graph attribute
        gnt.grid(True)

        print('t_assignment', t_assignment)
        # Declaring a bar in schedule
        for c, agent in enumerate(self.agent_id):  # for count and agent names
            # plot bar chart
            if color_idx >= 9:
                color_idx = 0
            gnt.broken_barh(t_assignment[agent], (10*(c+1), 9),
                            facecolors=(list_colors))
            # append to the y ticks
            list_ytick_labels.append(agent)
            list_yticks.append(first_y_tick+y_tick_gap*c)
            color_idx += 2
        # se final ytick
        list_yticks.append(first_y_tick+y_tick_gap*len(list_ytick_labels))
        gnt.set_yticklabels(list_ytick_labels)
        gnt.set_yticks(list_yticks)
        # Setting Y-axis limits
        gnt.set_ylim(0, list_yticks[len(list_yticks)-1])
        plt.savefig("gantt1.png")
        plt.show()

    def import_htn(self, print_htn=True):  # HTN import
        combined_dict = {}
        htn_model_yaml = self.problem_description["htn_model_id"]  # HTN id
        file_dir = self.problem_dir + htn_model_yaml  # directory + htn_model
        print(file_dir)
        with open(file_dir, "r") as data:
            try:
                dict = yaml.safe_load(data)
            except yaml.YAMLError as e:
                print(e)
        num_products = self.num_products
        children = []
        for p in range(num_products):
            child = DictImporter().import_(dict)
            for node in PostOrderIter(child):
                node.id = 'p{}_'.format(p+1) + node.id
            children.append(child)
        # For multi-product formulation, we introduce a task root at the highest
        # hiararchy
        root = AnyNode(id="TASK_ROOT", type='parallel', children=children)
        
        self.htn_model = root
        if print_htn:
            print(RenderTree(root))
        return self.htn_model

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
        htn = self.htn_model
        multi_product_index = 0
        if htn == None:
            raise Exception("no htn loaded")

        constraint_nodes = []

        constraint_nodes.append(htn)
        atomic_action_groups1 = [[] for i in range(self.num_products)]
        while constraint_nodes:
            node = constraint_nodes.pop(0)
            print("node:", node)
            node_children = node.children
            print("node:", node_children)
            atomic_action_groups = []
            for node_child in node_children:
                if node_child.type == "atomic":
                    atomic_action_groups.append([node_child])
                    for i in range(self.num_products):
                        # Meaning it is the first product
                        if node_child.id[1:2] == str(i+1):
                            atomic_action_groups1[i].append(
                                node_child)
                else:
                    constraint_nodes.append(node_child)
                    atomic_action_groups.append(
                        (list(anytree.PostOrderIter(node_child, filter_=lambda node: node.is_leaf))))

            if node.type == "parallel":
                continue
            elif node.type == "sequential":
                print("seq")
                self.generate_sequential_task_constraints(atomic_action_groups)
            elif node.type == "independent":
                self.generate_independent_task_constraints(
                    atomic_action_groups)
            else:
                raise Exception(
                    "Unknown node type encountered in HTN:" + node.type)
        print('moment of truth')
        print(atomic_action_groups1)
        print(np.shape(atomic_action_groups1))
        # If we have only two products wo only check once
        for k in range(self.num_products):
            # hence it will be num_products
            if k == 0:  # and skip 0 to check only once
                continue
            else:
                for j in range(self.num_products+multi_product_index):
                    if j == 0:  # and skip 0 to check only once
                        continue
                    else:
                        self.generate_multiproduct_task_contrasints(
                            atomic_action_groups1[k-1], atomic_action_groups1[k-1+j])
                        print('a')
                        print(k-1)
                        print('b')
                        print(k-1+j)
                        input()
                multi_product_index -= 1

    def generate_model(self):
        self.model = cp_model.CpModel()
        if self.problem_description == None:
            raise Exception("No problem description imported")
        else:
            prob = self.problem_description

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
        for agent in prob["agents"]:
            agent_decision_variables[agent] = {}
            agent_dur_constraints[agent] = {}
            agent_start_vars[agent] = {}
            agent_end_vars[agent] = {}
            agent_interval_vars[agent] = {}

        for task in self.task_model.keys():

            for agent in prob["agents"]:
                if agent not in self.task_model[task]["agent_model"]:
                    continue
                agent_decision_variables[agent][task] = self.model.NewBoolVar(
                    'x' + agent + '[' + task + ']')
                print(agent_decision_variables[agent][task])

        # Create Start End Duration Interval Variables

        starts = []
        ends = []
        intervals = []

        self.horizon = 0
        for task in self.task_model.keys():
            dur = 0
            for agent, agent_dur_model in self.task_model[task]["duration_model"].items():
                print(agent_dur_model)
                task_dur = max(dur, agent_dur_model['mean'])
            self.horizon = self.horizon+task_dur
        print("Horizon : ", self.horizon)

        for task in self.task_model.keys():

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
                if agent not in self.task_model[task]["duration_model"].keys():
                    continue
                agent_dur_constraints[agent][task] = self.model.Add(
                    self.task_model[task]["duration_model"][agent]["mean"] == duration).OnlyEnforceIf(agent_decision_variables[agent][task])
                # print(self.task_model[task]["duration_model"][agent]["mean"])

                agent_start_vars[agent][task] = self.model.NewIntVar(
                    0, self.horizon, 'start_on_' + task + agent)
                agent_end_vars[agent][task] = self.model.NewIntVar(
                    0, self.horizon, 'end_on_' + task + agent)
                agent_interval_vars[agent][task] = self.model.NewOptionalIntervalVar(agent_start_vars[agent][task], duration, agent_end_vars[agent][task],
                                                                                     agent_decision_variables[agent][task],
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
        self.model.Add(o == 10*t+s)
        self.objective = o
        self.makespan = t
        #### Define Objective ####
        self.model.Minimize(o)
        for task in self.task_model.keys():
            print([agent_decision_variables[agent][task]
                  for agent in self.task_model[task]["agent_model"]])
            self.all_diff_constraints.append(self.model.Add(sum(
                [agent_decision_variables[agent][task] for agent in self.task_model[task]["agent_model"]]) == 1))

        #### Create Solver and Solve ####
        solver = self.solver
        solver.parameters.num_search_workers = 8
        solver.parameters.max_time_in_seconds = 10
        status = solver.Solve(self.model)

        if status == cp_model.OPTIMAL:
            print("here")
            print(solver.Value(self.makespan))
            print(solver.WallTime())
        elif status == cp_model.FEASIBLE:
            print(solver.Value(self.makespan))
            print(solver.WallTime())
        else:
            print("no solution found")

        t_assignment = {}
        visual_t_assignmnent = {}
        self.agent_id = []
        self.task_id = []
        for agent_id, tasks in agent_decision_variables.items():
            self.agent_id.append(agent_id)
            visual_t_assignmnent[agent_id] = []
            t_assignment[agent_id] = {}

        task_count = 0
        for agent_id, tasks in agent_decision_variables.items():
            for task_id, vars in tasks.items():
                # print(agent_decision_variables[agent_id][task_id])
                if solver.Value(agent_decision_variables[agent_id][task_id]) == 1:
                    val = agent_id
                    self.task_id.append(task_id)
                    t_assignment[val][task_id] = {}
                    t_assignment[val][task_id]["StarttoEnd"] = list([solver.Value(self.task_start_vars[task_id]), solver.Value(
                        self.task_end_vars[task_id])])
                    visual_t_assignmnent[val].append((solver.Value(self.task_start_vars[task_id]), solver.Value(
                        self.task_end_vars[task_id])-solver.Value(self.task_start_vars[task_id])))
                    # assigned_items = t_assignment[val][task_id]["StarttoEnd"][0]
            # if t_assignment[
            #         print(val, ':', t_assignment[val][task_id]["StarttoEnd"])

                    #     if t_assignment[val][task_id]["StarttoEnd"][length][0] < t_assignment[val][task_id]["StarttoEnd"][length+1][0]:
                    #         new_element = t_assignment[val][task_id]["StarttoEnd"][length]
                    #         next_element = t_assignment[val][task_id]["StarttoEnd"][length+1]
                    #         t_assignment[val][task_id]["StarttoEnd"][length] =  next_element
                    #         t_assignment[val][task_id]["StarttoEnd"][length+1] = new_element
        print('task', self.task_id)
        self.visualize(visual_t_assignmnent)
        self.export_yaml(t_assignment)
        print(t_assignment)

    def export_yaml(self, t_assignment):
        task_allocation = {}
        task_allocation = t_assignment
        print(task_allocation)
        with open(r'{}\toy_task_allocation.yaml'.format(self.problem_dir), 'w') as file:
            documents = yaml.dump(task_allocation, file, sort_keys=False)


def main():
    scheduler = HtnMilpScheduler()
    scheduler.set_dir("problem_description/toy_problem/")
    scheduler.import_problem("problem_description_toy.yaml")
    scheduler.create_task_model()
    scheduler.import_htn()
    print('--------model created-------------')
    scheduler.generate_model()


if __name__ == '__main__':
    main()
