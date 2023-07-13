from asyncio import get_child_watcher
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import igraph as ig
from igraph import Graph, EdgeSeq
import matplotlib.pyplot as plt
import sys
from matplotlib.figure import Figure
import MILP_scheduler
from anytree import AnyNode, PostOrderIter
from anytree.exporter import DictExporter
from anytree import RenderTree  # just for nice printing
from anytree.importer import DictImporter
import numpy as np
from tree_toolset import TreeToolSet
import yaml

_RENDER_CMD = ['dot']
_FORMAT = 'png'


class HTN_vis(QtWidgets.QMainWindow):
    ''' Visualize HTN based on the tree structured dictionary'''

    def __init__(self):
        super().__init__()
        self.n_vertices = 1
        self.edges = []
        self.color_list = []
        self.constraint_list = []
        self.node_ids = []
        self.radio_options = ['sequential',
                              'parallel', 'independent', 'atomic'] # options of node types
        self.parent_radio_options = ['sequential', 'parallel', 'independent'] 
        scheduler = MILP_scheduler.HtnMilpScheduler()
        
        self.contingency_state = scheduler.contingency
        self.problem_dir = "problem_description/ATV_Assembly/"
        
        if scheduler.initial_run:
            htn_dir = self.problem_dir + "ATV_Assembly_Problem.yaml"
            with open(htn_dir, "r") as data:
                try:
                    self.htn_dict = yaml.safe_load(data)
                except yaml.YAMLError as e:
                    print(e)
        else:
            contingency_name = scheduler.contingency_name
            scheduler.set_dir(self.problem_dir)
            scheduler.import_problem("current_problem_description_ATV.yaml")
            scheduler.create_task_model()
            self.htn = scheduler.import_htn()
            # main htn dictionary
            self.htn_dict = scheduler.multi_product_dict # input
            self.contingency_node = TreeToolSet().search_tree(self.htn_dict, contingency_name) 
        
        self.render_node_to_edges(self.htn_dict)
        # declare first igraph instance
        self.g = Graph(self.n_vertices, self.edges)
        self.labels = []
        for i in range(self.n_vertices):
            print(i)
            self.g.vs[i]["label"] = f"T{i}"
            self.g.vs[i]["name"] = f"T{i}: {self.node_ids[i]} - type: {self.constraint_list[i]}"
            self.labels.append(self.g.vs[i]["name"])
        self.fig = plt.figure(figsize=(110, 40), dpi=100)
        # self.fig.set_size_inches(40, 80)
        self.fig.set_size_inches(50, 90) # for qt6
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setFixedSize(3000, 1000) # comment this out when using with mac
        self.toolbar = NavigationToolbar(self.canvas, self) # self is to satisfy parent argument
        self.ax = self.fig.add_subplot(111)
        self.plot()
        self.sub_container = QtWidgets.QWidget()
        self.sub_main_layout = QtWidgets.QHBoxLayout(self.sub_container)
        # First parent node input container
        self.parent_node_container = QtWidgets.QWidget()
        self.text_layout_1 = QtWidgets.QVBoxLayout(self.parent_node_container)
        self.text_label1 = QtWidgets.QLabel(
            'Parent Node: ', self.parent_node_container)
        self.parent_node = QtWidgets.QLineEdit()
        self.parent_node.setPlaceholderText('Parent in integer number')
        self.text_layout_1.addWidget(self.text_label1)
        self.text_layout_1.addWidget(self.parent_node)
        # end of container maker
        self.label_container = QtWidgets.QWidget()
        self.text_layout_2 = QtWidgets.QVBoxLayout(self.label_container)
        self.text_label2 = QtWidgets.QLabel(
            'Task Node name: ', self.parent_node_container)
        self.label = QtWidgets.QLineEdit()
        self.label.setPlaceholderText('Name of the node')
        self.text_layout_2.addWidget(self.text_label2)
        self.text_layout_2.addWidget(self.label)
        # End of container
        self.node_type_container = QtWidgets.QWidget()
        self.text_layout_3 = QtWidgets.QVBoxLayout(self.node_type_container)
        self.text_label3 = QtWidgets.QLabel(
            'New node type: ', self.node_type_container)
        self.button_group1 = QtWidgets.QButtonGroup()
        self.text_layout_3.addWidget(self.text_label3)
        self.child_type_radio = []
        for idx, option in enumerate(self.radio_options):
            self.select_child_type = QtWidgets.QRadioButton(option)
            self.child_type_radio.append(self.select_child_type)
            self.text_layout_3.addWidget(self.select_child_type)
            self.button_group1.addButton(self.select_child_type, idx)
        # End of container
        self.parent_type_container = QtWidgets.QWidget()
        # self.parent_type_container.setFixedSize(100, 400)
        self.text_layout_4 = QtWidgets.QVBoxLayout(self.parent_type_container)
        self.text_label4 = QtWidgets.QLabel(
            'Parent node type: ', self.parent_type_container)
        self.text_layout_4.addWidget(self.text_label4)
        self.button_group2 = QtWidgets.QButtonGroup()
        self.parent_type_radio = []
        for idx, option in enumerate(self.parent_radio_options):
            self.select_parent_type = QtWidgets.QRadioButton(option)
            self.parent_type_radio.append(self.select_parent_type)
            self.text_layout_4.addWidget(self.select_parent_type)
            self.button_group2.addButton(self.select_parent_type, idx)
        # End of container
        self.agent_type_container = QtWidgets.QWidget()
        self.text_layout_5 = QtWidgets.QVBoxLayout(self.agent_type_container)
        self.text_label5 = QtWidgets.QLabel(
            'Agent name: ', self.agent_type_container)
        self.agent_type = QtWidgets.QLineEdit()
        self.agent_type.setPlaceholderText(
            'if atomic, input agent id')
        self.text_layout_5.addWidget(self.text_label5)
        self.text_layout_5.addWidget(self.agent_type)
        # End of container

        self.agent_duration_container = QtWidgets.QWidget()
        self.text_layout_5_1 = QtWidgets.QVBoxLayout(self.agent_duration_container)
        self.text_label5_1 = QtWidgets.QLabel(
            'Agent duration model: ', self.agent_duration_container)
        self.agent_duration = QtWidgets.QLineEdit()
        self.agent_duration.setPlaceholderText(
            'if atomic, input agent duration')
        self.text_layout_5_1.addWidget(self.text_label5_1)
        self.text_layout_5_1.addWidget(self.agent_duration)
        # End of container

        self.order_number_container = QtWidgets.QWidget()
        self.text_layout_6 = QtWidgets.QVBoxLayout(self.order_number_container)
        self.text_label6 = QtWidgets.QLabel(
            'Children Order Index from 0 : ', self.order_number_container)
        self.order_number = QtWidgets.QLineEdit()
        self.order_number.setPlaceholderText(
            'From left to right(0~)')
        self.text_layout_6.addWidget(self.text_label6)
        self.text_layout_6.addWidget(self.order_number)
        # End of container
        self.delete_node_container = QtWidgets.QWidget()
        self.text_layout_7 = QtWidgets.QHBoxLayout(self.delete_node_container)
        self.text_label7 = QtWidgets.QLabel(
            'Delete node: ', self.delete_node_container)
        self.delete_node = QtWidgets.QLineEdit()
        self.delete_node.setPlaceholderText(
            'Delete node in integer')
        self.text_layout_7.addWidget(self.text_label7)
        self.text_layout_7.addWidget(self.delete_node)
        # End of container

        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.add_node_gui)
        self.delete_submit = QtWidgets.QPushButton("Delete")
        self.delete_submit.clicked.connect(self.del_node_gui)
        self.list_widget = QtWidgets.QListWidget()
        list_scroll_area = QtWidgets.QScrollArea()
        list_scroll_area.setWidgetResizable(True)
        list_scroll_area.setWidget(self.list_widget)
        layout0 = QtWidgets.QHBoxLayout()
        layout1 = QtWidgets.QHBoxLayout()
        layout0.addWidget(list_scroll_area)
        self.list_widget.addItems(self.labels)
        # layout1.addWidget(self.canvas)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.canvas)
        # scroll_area.setWidgetResizable(True)
        list_scroll_area.setFixedWidth(200)
        scroll_area.setFixedWidth(1300)
        layout1.addWidget(scroll_area)
        layout2 = QtWidgets.QVBoxLayout()
        layout2.addWidget(self.toolbar)
        layout2.addWidget(self.parent_node_container)
        layout2.addWidget(self.parent_type_container)
        layout2.addWidget(self.label_container)
        layout2.addWidget(self.node_type_container)
        layout2.addWidget(self.order_number_container)
        layout2.addWidget(self.agent_type_container)
        layout2.addWidget(self.agent_duration_container)
        layout2.addWidget(self.submit_button)
        layout2.setContentsMargins(0, 0, 0, 0)
        layout2.addWidget(self.delete_node_container)
        layout2.addWidget(self.delete_submit)
        self.order_number_container.setFixedWidth(190)
        container = QtWidgets.QWidget()
        container.setLayout(layout0)
        container.layout().addLayout(layout1)
        container.layout().addLayout(layout2)
        # Add the Matplotlib canvas to the PyQt window
        self.setCentralWidget(container)

    def render_node_to_edges(self, htn_dict):
        """Create nodes, edges, colors and constraint lists based on the dictionary using the class method"""
        self.pairs_with_name, self.pairs_with_full_node = TreeToolSet().create_pairs_with_dfs(htn_dict)
        self.name_node, self.edge_list = TreeToolSet().create_dict_from_list(
            self.pairs_with_name)
        self.id_sequence = TreeToolSet().create_dict_list_from_pairs(
            self.pairs_with_full_node)
        self.id_seqence_list = list(self.id_sequence.values())
        self.node_ids = []
        self.constraint_list = []
        self.color_list = []
        for i in range(len(self.id_seqence_list)):
            self.node_ids.append(self.id_seqence_list[i]['id'])
            self.constraint_list.append(self.id_seqence_list[i]['type'])
            if self.constraint_list[i] != 'atomic':
                self.color_list.append('yellow')
            else:
                self.color_list.append('cyan')
        if self.contingency_state and self.contingency_node in self.id_seqence_list:
            self.color_list[self.id_seqence_list.index(
                self.contingency_node)] = 'red'
        self.edges = self.edge_list
        self.n_vertices = len(self.node_ids)

    def plot(self):
        """
        Plotting functionality
        """
        # general style configuration
        self.g["title"] = "HTN"
        layout = self.g.layout("rt", root=[0])
        layout.rotate(-180)

        # layout.scale(5000)
        ig.plot(
            self.g,
            layout=layout,
            target=self.ax,
            vertex_size=0.6,
            showlegend=False,
            vertex_color=self.color_list,
            vertex_label_size=9,
            margin=50,
            line_width=0.5,
            marker_size=1
        )

        self.canvas.draw()

    def add_node_gui(self):
        self.ax.clear()
        user_input_parent = self.parent_node.text()
        for index, radio_button in enumerate(self.child_type_radio):
            if radio_button.isChecked():
                child_selected_index = index
                break

        for index, radio_button in enumerate(self.parent_type_radio):
            if radio_button.isChecked():
                parent_selected_index = index
                break
        parent_node_type = self.parent_radio_options[parent_selected_index]
        self.child_node_type = self.radio_options[child_selected_index]
        order_child = self.order_number.text()

        if user_input_parent.isalpha() or order_child.isalpha():
            print('string')
            pass
        else:
            user_input_parent = int(user_input_parent)
            if user_input_parent > self.n_vertices-1:
                pass
            # self.n_vertices += 1
            print('number of vertices', self.n_vertices)
            user_new_node = {}
            if TreeToolSet().search_tree(self.htn_dict, self.label.text()) is not None: # search if id already exists
                user_new_node['id'] = f'{self.label.text()}_duplicate'  # automatically add new label
            else:
                user_new_node['id'] = self.label.text() # let user pick 
            user_new_node['type'] = self.child_node_type # new node is child node type selected
            if user_new_node['type'] != 'atomic': # if not atomic
                user_new_node['children'] = [] # need to have children
            else:
                user_new_node['agent'] = self.agent_type.text() # let it be agent
            self.id_sequence[self.n_vertices-1] = user_new_node
            target_id = self.id_seqence_list[user_input_parent]['id']
            parent_input_node_type = parent_node_type
            TreeToolSet().insert_element(self.htn_dict, target_id, parent_input_node_type,
                           user_new_node, order_child)
            TreeToolSet().dict_yaml_export(self.htn_dict, self.problem_dir, "ATV_Assembly_Problem.yaml")
            self.render_node_to_edges(self.htn_dict)
            self.g = Graph(self.n_vertices, self.edges)
            self.labels = []
            for i in range(self.n_vertices):
                self.g.vs[i]["label"] = f"T{i}"
                self.g.vs[i]["name"] = f"T{i}: {self.node_ids[i]} - type: {self.constraint_list[i]}"
                self.labels.append(self.g.vs[i]["name"])
            self.list_widget.clear()
            self.list_widget.addItems(self.labels)
        self.add_task_model()
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
            TreeToolSet().delete_element(
                self.htn_dict, self.id_seqence_list[user_delete]['id'])
            TreeToolSet().dict_yaml_export(self.htn_dict, self.problem_dir, "ATV_Assembly_Problem.yaml")
            self.render_node_to_edges(self.htn_dict)
            self.g = Graph(self.n_vertices, self.edges)
            self.labels = []
            for i in range(self.n_vertices):
                self.g.vs[i]["label"] = f"T{i}"
                self.g.vs[i]["name"] = f"T{i}: {self.node_ids[i]} - type: {self.constraint_list[i]}"
                self.labels.append(self.g.vs[i]["name"])
            self.list_widget.clear()
            self.list_widget.addItems(self.labels)
        self.plot()

    def add_task_model(self):
        if self.child_node_type == 'atomic':
            with open("problem_description/ATV_Assembly/task_model_ATV.yaml", "r") as file:
                task_model_dict = yaml.safe_load(file)
                print(task_model_dict)
                task_model_dict[self.label.text()] = {'agent_model': [self.agent_type.text()], 'duration_model': {}}
                task_model_dict[self.label.text()]['duration_model'][self.agent_type.text()] = {'id': 'det', 'mean': int(self.agent_duration.text())}
            print(task_model_dict)
            TreeToolSet().safe_dict_yaml_export(task_model_dict, self.problem_dir, "task_model_ATV.yaml")
    
    # def delete_task_model(self):
    #     with open("problem_description/ATV_Assembly/task_model_ATV.yaml", "r") as file:
    #         task_model_dict = yaml.safe_load(file)
    #         print(task_model_dict)
        # TreeToolSet().safe_dict_yaml_export(task_model_dict, self.problem_dir, "cont_task_model_ATV.yaml")
def main():
    app = QtWidgets.QApplication(sys.argv)
    htn = HTN_vis()
    htn.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
