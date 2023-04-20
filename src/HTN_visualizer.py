
"""
Developer: Jeon Ho Kang
Email: jeonhoka@usc.edu
Association: University of Southern California
Center for Advanced Manufacturing

HTN tree visualizer
"""


import collections
import igraph as ig
from igraph import Graph, EdgeSeq
import math
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import sys
from tkinter import ttk
import tkinter as tk
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.widgets import Button, TextBox, CheckButtons
from matplotlib import colors
import matplotlib.pyplot as plt
import time


class HTN_VIS_GUI(object):
    def __init__(self):
        super(HTN_VIS_GUI, self).__init__()
        self.LARGE_FONT = ("Verdana", 12)
        self.NORM_FONT = ("Helvetica", 10)
        self.SMALL_FONT = ("Helvetica", 8)
        self.constraints = ['']
        self.labels = ['0:root']
        self.edge_labels = ['']
        self.num_it = 0
        self.parent = [0]
        self.number_nodes = len(self.labels)
        self.state = False
        self.constraint_state = False
        self.state_added = False
        print('number of nodes:', self.number_nodes)
        # BEGIN Extracting data
        self.root = 0
        self.edges = [[0 for i in range(2)] for j in range(len(self.parent))]
        for i, j in enumerate(self.parent):
            self.edges[i] = [j-1, i+1]
        print(self.edges[1:])
        self.g = Graph(n=self.number_nodes, edges=self.edges[1:])

    def popupmsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("Warning")
        label = ttk.Label(popup, text=msg, font=self.NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
        B1.pack()
        popup.mainloop()

    def submit_labels(self, expression):
        """
        Update the plotted function to the new math *expression*.

        *expression* is a string using "t" as its independent variable, e.g.
        "t ** 3".
        """
        self.state = False
        self.constraint_state = False
        self.state_added = True
        if len(expression) >= 10:
            expression = expression[0:11] + " \n" + expression[11::]
        self.labels.append(expression)
        print(self.labels)

    def submit_parent(self, expression):
        """
        Update the plotted function to the new math *expression*.

        *expression* is a string using "t" as its independent variable, e.g.
        "t ** 3".
        """
        labels = self.labels
        self.constraint_state = False
        self.state = False
        self.state_added = True
        if expression.isnumeric() == False:
            self.popupmsg('not a number')
        elif int(expression) > len(labels):
            self.popupmsg('Value cannot exceed {}'.format(len(labels)))
        elif int(expression) > len(labels)-2:
            self.popupmsg('Parent does not exist')
        else:
            expression = int(expression)
            self.parent.append(expression)
            print(self.parent)

    def submit_constraints(self, expression):
        """
        Update the plotted function to the new math *expression*.

        *expression* is a string using "t" as its independent variable, e.g.
        "t ** 3".
        """
        labels = self.labels
        self.constraint_state = True
        if expression.isnumeric() == True:
            self.popupmsg('Needs String input')
        elif len(expression) >= 1:
            expression = expression[0]
            self.constraints.append(expression)
            print(self.constraints)
        else:
            expression = int(expression)
            self.constraints.append(expression)
            print(self.constraints)

    def delete_element(self, expression):
        labels = self.labels
        edges = self.edges
        parent = self.parent
        self.state = True
        self.constraint_state = False
        self.del_index = []
        if expression.isnumeric() == False:
            self.popupmsg('Needs Integer input')
        elif len(expression) >= self.number_nodes:
            self.popupmsg('Can not exceed current length')
        else:
            expression = int(expression)
        for k in range(len(labels)-1, expression-1, -1):
            print('the number is :', labels)
            print('k :', k)
            del labels[k]
            del parent[k]
            print(edges)
            print(labels)
        for n, m in enumerate(edges):
            if m[0] == int(expression):
                self.del_index.append(n)

            elif m[1] == int(expression):
                self.del_index.append(n)
        for l in reversed(self.del_index):
            del edges[l]
        print(edges)

    def update(self, event):
        global bnext
        global text_box_name1
        global text_box_parent
        global text_box_constraint
        global text_box_delete
        print("Number of ")
        HTN = HTN_Editor()

        if abs(len(self.parent) - len(self.labels)) != 0:
            print(abs(len(self.parent) - len(self.labels)))
            self.popupmsg('Edge needs to be Node-1')
            self.popupmsg('Check the left side of the graph')

        else:
            self.num_it += 1
            self.edge_labels = ["" for z in range(len(self.constraints))]
            print('hit')
            plt.ion()
            # self.popupmsg('Drawing!......')
            self.number_nodes = len(self.labels)
            numbering = range(self.number_nodes)
            if self.state == True:
                print('delete')
            elif self.constraint_state == True:
                print('Constraint')
            elif self.constraint_state == True and self.state_added == True:
                self.labels[self.number_nodes-1] = str(
                    self.number_nodes-1) + ": " + self.labels[self.number_nodes-1]
            else:
                self.labels[self.number_nodes-1] = str(
                    self.number_nodes-1) + ": " + self.labels[self.number_nodes-1]
            self.edges = [[0 for i in range(2)]
                          for j in range(len(self.parent))]
            for i, j in enumerate(self.parent):
                self.edges[i] = [j, i]
            for k in range(len(self.labels)):
                self.labels[k] = str(self.labels[k])
            for n, edge_labels in enumerate(self.constraints):
                if type(edge_labels) != str and edge_labels != 'none':
                    self.edge_labels[n] = ""
                elif edge_labels == "":
                    self.edge_labels[n] = ""
                if edge_labels == 'P' or edge_labels == 'p':
                    self.edge_labels[n] = '||'
                elif edge_labels == 'S' or edge_labels == 's':
                    self.edge_labels[n] = '->'
                elif edge_labels == 'C' or edge_labels == 's':
                    self.edge_labels[n] = '┴'
            print(self.constraints)
            print(self.edge_labels)
            print(self.edges)
            print(self.number_nodes)
            self.fig1, self.ax1 = plt.subplots(figsize=(7, 6))
            self.g = Graph(n=self.number_nodes, edges=self.edges[1:])
            self.fig1.subplots_adjust(bottom=0.3)
            self.fig1.subplots_adjust(left=0.2)
            self.ax1.set_title('HTN Visualizer', fontsize=14)
            print('hit2')
            # Number of nodes as input
            node_name_box1 = self.fig1.add_axes([0.11, 0.05, 0.1, 0.075])
            parent_box = self.fig1.add_axes([0.41, 0.05, 0.1, 0.075])
            constraints_box = self.fig1.add_axes([0.64, 0.05, 0.1, 0.075])
            update_fig = self.fig1.add_axes([0.81, 0.15, 0.1, 0.075])
            delete_el = self.fig1.add_axes([0.81, 0.05, 0.1, 0.075])
            print('hit3')
            bnext = Button(update_fig, 'Update')
            bnext.on_clicked(self.update)
            text_box_name1 = TextBox(
                node_name_box1, "Name: ", textalignment="center")
            text_box_parent = TextBox(parent_box, "Parent(In Number): ",
                                      textalignment="center")
            text_box_constraint = TextBox(constraints_box, "Constraint: ",
                                          textalignment="center")
            text_box_delete = TextBox(
                delete_el, "Delete: ", textalignment='center')
            print('hit4')
            text_box_name1.on_submit(self.submit_labels)
            text_box_parent.on_submit(self.submit_parent)
            text_box_constraint.on_submit(self.submit_constraints)
            text_box_delete.on_submit(self.delete_element)
            layout = self.g.layout("rt", root=[0])
            layout.rotate(-180)
            print('hit5')
            ig.plot(self.g, layout=layout, target=self.ax1, vertex_label=self.labels,
                    vertex_size=0.5,
                    vertex_frame_width=0.0,
                    vertex_color='#AAAAFF',
                    edge_color=['gray'],
                    vertex_label_size=8,
                    edge_label=self.edge_labels,
                    edge_label_size=9,
                    bbox=(300, 300)
                    )
            print('hit6')
            axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                        zeroline=False,
                        showgrid=False,
                        showticklabels=False,
                        )
            print('hit')
            plt.draw()
            print(self.num_it)
        plt.close(1)
        for i in range(self.num_it+1):
            plt.close(i)

    # def delete_index(self, expression):

    #     if expression.isnumeric() == False:
    #         self.popupmsg('Input Robot Index')
    #     elif int(expression) > grid_len:
    #         self.popupmsg('Value cannot exceed {}'.format(len(robot_x)))
    #     else:

    #         expression = int(expression)-1
    #         cmap = colors.ListedColormap(['yellow'])
    #         # ax.pcolor(data, cmap=cmap, edgecolors='k', linewidths=3)
    #         # del robot_x[expression]
    #         # del robot_y[expression]
    #         # del robot_th[expression]
    #         # for i in range(len(robot_x)):
    #         #     ax.arrow(robot_x[i]-0.5, robot_y[i]-0.5, scale*conv_cart_to_ang(robot_th[i])[0],
    #         #              scale*conv_cart_to_ang(robot_th[i])[1], head_width=0.1, color='blue', label='robot{}'.format(i+1))
    #     plt.draw()


class HTN_Editor(object):
    """HTN editor"""

    def __init__(self):
        super(HTN_Editor, self).__init__()
        # Read file
        self.labels = HTN_VIS_GUI().labels
        self.edge_labels = HTN_VIS_GUI().edge_labels
        self.parent = HTN_VIS_GUI().parent

    def plot(self):
        GUI = HTN_VIS_GUI()
        g = GUI.g
        self.fig, self.ax = plt.subplots(figsize=(7, 6))
        self.fig.subplots_adjust(bottom=0.3)
        self.fig.subplots_adjust(left=0.2)
        self.ax.set_title('HTN Visualizer', fontsize=14)
        # Number of nodes as input
        node_name_box = self.fig.add_axes([0.11, 0.05, 0.1, 0.075])
        parent_box = self.fig.add_axes([0.41, 0.05, 0.1, 0.075])
        constraints_box = self.fig.add_axes([0.64, 0.05, 0.1, 0.075])
        update_fig = self.fig.add_axes([0.81, 0.15, 0.1, 0.075])
        bnext = Button(update_fig, 'Update')
        bnext.on_clicked(GUI.update)
        text_box_name = TextBox(
            node_name_box, "Name: ", textalignment="center")
        text_box_parent = TextBox(parent_box, "Parent(In Number): ",
                                  textalignment="center")
        text_box_constraint = TextBox(constraints_box, "Constraint: ",
                                      textalignment="center")
        text_box_name.on_submit(GUI.submit_labels)
        text_box_parent.on_submit(GUI.submit_parent)
        text_box_constraint.on_submit(GUI.submit_constraints)
        layout = g.layout("rt", root=[0])
        layout.rotate(-180)
        ig.plot(g, layout=layout, target=self.ax, vertex_label=self.labels,
                vertex_size=0.5,
                vertex_frame_width=0.0,
                vertex_color='#AAAAFF',
                edge_color=['gray'],
                vertex_label_size=8,
                edge_label=self.edge_labels,
                edge_label_size=9,
                bbox=(300, 300)
                )
        axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    )

        plt.show()


def main():
    try:
        print('----HTN diagram printer ----')

        visualizer = HTN_Editor()
        visualizer.plot()
        # Create the Qt Application
        # Create and show the form

    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()
