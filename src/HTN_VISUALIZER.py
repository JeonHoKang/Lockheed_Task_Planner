from asyncio import get_child_watcher
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import igraph as ig
from igraph import Graph, EdgeSeq
from tkinter import ttk
import tkinter as tk
import matplotlib.pyplot as plt
import sys
from matplotlib.figure import Figure
import plotly.graph_objects as go
import Lockheed_task_planner
import anytree
from anytree import AnyNode, PostOrderIter
from anytree.exporter import DictExporter
from anytree import RenderTree  # just for nice printing
from anytree.importer import DictImporter
import numpy as np

_RENDER_CMD = ['dot']
_FORMAT = 'png'
# print(data['children'][0]['children'][0]['children'][0])


def recui(htn):
    if "children" in htn:
        parent = htn['id']
        children = htn["children"]
        child_list = []
        for child in children:
            child_list.append(recui(child))
        return child_list
    else:
        return htn["id"]


class HTN_vis(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.n_vertices = 1
        self.edges = []
        self.color_list = []
        self.constraint_list = []
        self.node_ids = []
        self.render_node_to_edges()
        self.g = Graph(self.n_vertices, self.edges)
        self.labels = []
        for i in range(self.n_vertices):
            print(i)
            self.g.vs[i]["label"] = f"{i}"
            self.g.vs[i]["name"] = f"{i}: {self.node_ids[i]} - constraint/node type: {self.constraint_list[i]}"
            self.labels.append(self.g.vs[i]["name"])
        self.fig = Figure(figsize=(100, 600))
        self.fig.set_size_inches(15, 50)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setFixedSize(10000, 800)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ax = self.fig.add_subplot(111)
        self.plot()
        self.parent_node = QtWidgets.QLineEdit('Parent')
        self.label = QtWidgets.QLineEdit('label')
        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.add_node_gui)
        self.delete_node = QtWidgets.QLineEdit('delete')
        self.delete_submit = QtWidgets.QPushButton("Delete")
        self.delete_submit.clicked.connect(self.del_node_gui)
        self.list_widget = QtWidgets.QListWidget()
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        list_scroll_area = QtWidgets.QScrollArea()
        list_scroll_area.setWidgetResizable(True)
        list_scroll_area.setWidget(self.list_widget)
        layout0 = QtWidgets.QVBoxLayout()
        layout1 = QtWidgets.QHBoxLayout()
        layout0.addWidget(list_scroll_area)
        self.list_widget.addItems(self.labels)
        # layout1.addWidget(self.canvas)
        scroll_area.setWidget(self.canvas)
        layout1.addWidget(scroll_area)
        layout2 = QtWidgets.QVBoxLayout()
        layout2.addWidget(self.toolbar)
        layout2.addWidget(self.parent_node)
        layout2.addWidget(self.label)
        layout2.addWidget(self.submit_button)
        layout3 = QtWidgets.QVBoxLayout()
        layout3.addWidget(self.delete_node)
        layout3.addWidget(self.delete_submit)
        container = QtWidgets.QWidget()
        container.setLayout(layout0)
        container.layout().addLayout(layout1)
        container.layout().addLayout(layout2)
        container.layout().addLayout(layout3)
        # Add the Matplotlib canvas to the PyQt window
        self.setCentralWidget(container)

    def render_node_to_edges(self):
        """Create nodes, edges, colors and constraint lists based on the dictionary using the class method"""
        self.scheduler = Lockheed_task_planner.HtnMilpScheduler()
        self.scheduler.set_dir("problem_description/LM2023_problem/")
        self.scheduler.import_problem("problem_description_LM2023.yaml")
        self.scheduler.create_task_model()
        self.htn = self.scheduler.import_htn()
        self.htn_dict = self.scheduler.dict
        self.pairs_with_name, self.pairs_with_full_node = dfs(self.htn_dict)
        self.name_node, self.edge_list = create_dict_from_list(
            self.pairs_with_name)
        self.id_sequence = create_dict_list_from_pairs(self.pairs_with_full_node)
        self.id_seqence_list = list(self.id_sequence.values())
        for i in range(len(self.id_seqence_list)):
            self.node_ids.append(self.id_seqence_list[i]['id'])
            self.constraint_list.append(self.id_seqence_list[i]['type'])
            if self.constraint_list[i] == 'atomic':
                self.color_list.append('red')
            else:
                self.color_list.append('yellow')
        self.edges = self.edge_list
        self.n_vertices = len(self.node_ids)

    def trace(self, root):
        # builds a set of all nodes and edges in a graph
        nodes, edges = set(), set()

        def build(v):
            if v not in nodes:
                nodes.add(v)
                for child in v._children:
                    edges.add((child, v))
                    build(child)
        build(root)
        return nodes, edges

    def plot(self):
        # self.g = Graph(self.n_vertices, self.edges)
        self.g["title"] = "HTN"
        layout = self.g.layout("rt", root=[0])
        layout.rotate(-180)
        layout.fit_into((20000, 30000))

        # layout.scale(5000)
        ig.plot(
            self.g,
            layout=layout,
            target=self.ax,
            vertex_size=100,
            showlegend=False,
            vertex_color=self.color_list,
            vertex_label_size=9
        )
        self.canvas.draw()

    def add_node_gui(self):
        self.ax.clear()
        user_input_parent = self.parent_node.text()
        if user_input_parent.isalpha():
            print('string')
            pass
        else:
            user_input_parent = int(user_input_parent)
            if user_input_parent > self.n_vertices-1:
                pass
            self.n_vertices += 1
            print('number of vertices', self.n_vertices)
            # self.edges.append((user_input_parent, self.n_vertices-1))
            # self.labels.append(self.label.text())
            self.g.add_vertices(1)
            self.g.add_edges([(user_input_parent, self.n_vertices-1)])
            self.g.vs[self.n_vertices -
                      1]["label"] = f"{self.n_vertices-1}"
            self.g.vs[self.n_vertices -
                      1]["name"] = f"{self.n_vertices-1}: {self.label.text()}"
            self.labels.append(self.g.vs[self.n_vertices -
                                         1]["name"])
            self.node_ids.append(self.g.vs[self.n_vertices -
                                           1]["name"])
            self.color_list[user_input_parent] = 'yellow'
            self.color_list.append('red')
            self.list_widget.clear()
            print(self.labels)
            self.list_widget.addItems(self.labels)
            edge_list = self.g.get_edgelist()
            vertex_list = self.g.vs
            # print the resulting list of dictionaries
            print('vertex: ', list(vertex_list))
            print('edge: ', edge_list)
        self.plot()

    def del_node_gui(self):
        self.ax.clear()
        user_delete = self.delete_node.text()
        if user_delete.isalpha():
            print('string')
            pass
        else:
            user_delete = int(user_delete)
            if user_delete > self.n_vertices-1:
                pass
            # self.g.delete_edges(user_delete)
            self.g.delete_vertices(user_delete)
            edge_list = self.g.get_edgelist()
            vertex_list = self.g.vs
            self.n_vertices -= 1
            # print the resulting list of dictionaries
            print('vertex: ', list(vertex_list))
            print('edge_list: ', edge_list)
            self.node_ids.pop(user_delete)
            self.color_list.pop(user_delete)
        self.labels = []
        for i in range(self.n_vertices):
            print(i)
            self.g.vs[i]["label"] = f"{i}"
            self.g.vs[i]["name"] = f"{i}: {self.node_ids[i]} - constraint/node type: {self.constraint_list[i]}"
            self.labels.append(self.g.vs[i]["name"])
            print('current labels:', self.labels)
        self.list_widget.clear()
        self.list_widget.addItems(self.labels)
        self.plot()


def dfs(start):
    visited = []  # Set to track visited vertices
    edges = []
    stack = [start]  # Stack to keep track of vertices to visit
    type_list = []
    full_id = []
    while stack:
        vertex = stack.pop()  # Pop a vertex from the stack

        if vertex["id"] not in visited:
            print(vertex["id"])  # Process the vertex (in this case, print it)
            visited.append(vertex["id"])  # Mark the vertex as visited
            # Add adjacent vertices to the stack
            if "children" in vertex:
                for child in reversed(vertex["children"]):
                    stack.append(child)
                    edges.append((vertex["id"], child["id"]))
                    full_id.append((vertex, child))
    return edges, full_id


def create_dict_from_list(pairs):
    local_dict = {}
    name_id_dict = {}
    latest_id = -1
    index_list = []
    for pair in pairs:
        parent = pair[0]
        child = pair[1]
        child_id = 0
        parent_id = 0
        if parent not in name_id_dict:
            latest_id += 1
            local_dict[latest_id] = parent
            parent_id = latest_id
            name_id_dict[parent] = parent_id

        else:
            parent_id = name_id_dict[parent]

        if child not in name_id_dict:
            latest_id += 1
            local_dict[latest_id] = child
            child_id = latest_id
            name_id_dict[child] = child_id
        else:
            child_id = name_id_dict[child]

        index_list.append((parent_id, child_id))

    return local_dict, index_list

def create_dict_list_from_pairs(pairs):
    local_dict = {}
    name_id_dict = {}
    latest_id = -1
    index_list = []
    for pair in pairs:
        parent = pair[0]
        child = pair[1]
        child_id = 0
        parent_id = 0
        if parent['id'] not in name_id_dict:
            latest_id += 1
            local_dict[latest_id] = parent
            parent_id = latest_id
            name_id_dict[parent['id']] = parent_id
        else:
            parent_id = name_id_dict[parent['id']]

        if child['id'] not in name_id_dict:
            latest_id += 1
            local_dict[latest_id] = child
            child_id = latest_id
            name_id_dict[child['id']] = child_id
        else:
            child_id = name_id_dict[child['id']]

        index_list.append((parent_id, child_id))

    return local_dict



def main():
    app = QtWidgets.QApplication(sys.argv)
    htn = HTN_vis()
    htn.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
