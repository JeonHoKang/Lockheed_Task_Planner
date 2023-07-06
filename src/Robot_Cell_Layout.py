import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from tkinter import ttk
import tkinter as tk
import matplotlib.animation as animation
from matplotlib.widgets import Button, TextBox, CheckButtons
import math
import numpy as np
from matplotlib import colors
from matplotlib import pyplot as plt
from matplotlib.patches import Circle


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.list_radio = []
        self.grid_len = 10
        self.data = [[0]*self.grid_len]*self.grid_len
        # Create a Matplotlib figure
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setFixedSize(1000, 1000)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])
        self.cmap = colors.ListedColormap(['yellow'])
        self.ax.pcolor(self.data, cmap=self.cmap, edgecolors='k', linewidths=3)
        # self.ax.scatter(self.x, self.y)
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])
        self.ax.set_title('Robot Cell Layout', fontsize=14)
        # Add a button to trigger an update
        self.reachability = QtWidgets.QLineEdit('Value ranging from 0-2')
        self.button_group = QtWidgets.QButtonGroup()
        self.robot_reachability = []
        # self.x_input.returnPressed.connect(self.process_input)
        # Add a button to trigger an update
        # self.y_input.returnPressed.connect(self.process_input)
        # self.submit_button = QtWidgets.QPushButton("Submit")
        # self.submit_button.clicked.connect(self.process_input)
        # Set up the initial plot
        self.x = []
        self.y = []
        self.theta = []
        self.robots = []
        # Create and add radio buttons dynamically based on the list of options

        self.ax.scatter(self.x, self.y)
        layout1 = QtWidgets.QHBoxLayout()
        layout1.addWidget(self.canvas)
        self.layout2 = QtWidgets.QVBoxLayout()
        self.layout2.addWidget(self.reachability)
        self.layout3 = QtWidgets.QVBoxLayout()
        for idx, option in enumerate(self.robots):
            self.select_robot = QtWidgets.QRadioButton(option)
            self.layout3.addWidget(self.select_robot)
            self.button_group.addButton(self.select_robot, idx)
        self.button_group.buttonClicked[int].connect(self.process_input)
        # self.layout2.addWidget(self.submit_button)
        container = QtWidgets.QWidget()
        container.setLayout(layout1)
        container.layout().addLayout(self.layout2)
        container.layout().addLayout(self.layout3)
        # Add the Matplotlib canvas to the PyQt window
        self.setCentralWidget(container)
        self.canvas.mpl_connect("button_press_event", self.manipulate_point)

    def process_input(self, id):
        # Get the user input and do something with it
        selected_option = self.robots[id]
        print("Selected Option:", selected_option)
        robot_index = id
        robot_reach = self.reachability.text()
        if robot_reach == '':
            pass
        else:
            robot_reach = float(robot_reach)
            for i in range(id+1):
                self.robot_reachability.append(0)
            print('lenght dfsdf', self.robot_reachability)
            self.robot_reachability[id] = robot_reach
            self.circle = Circle(
                (self.x[robot_index], self.y[robot_index]), self.robot_reachability[robot_index], edgecolor='red', facecolor='None')
            self.ax.add_patch(self.circle)
            self.canvas.draw()
            print(f"theta input: {robot_reach}")
            print('xandy', self.x[robot_index], 'and', self.y[robot_index])
            print('reachability', self.robot_reachability[robot_index])

    def conv_cart_to_ang(self, angle):
        if angle == 0:
            angle = 0.00001
        else:
            angle = angle
        dx = 1*math.cos(angle*(math.pi/180))
        dy = 1*math.sin(angle*(math.pi/180))
        return [dx, dy]

    def append(self, x1, y1):
        self.x.append(x1)
        self.y.append(y1)

    def remove(self, x_idx, y_idx):
        self.x.pop(x_idx)
        self.y.pop(y_idx)

    def add_robot_radio(self):
        self.robots.append(f'robot{len(self.ordered_list_xy)+1}')
        # for idx, option in enumerate(self.robots):
        self.select_robot = QtWidgets.QRadioButton(
            self.robots[len(self.robots)-1])
        self.list_radio.append(self.select_robot)
        self.layout3.addWidget(self.select_robot)
        self.button_group.addButton(
            self.select_robot, len(self.robots)-1)

    # def delete_robot_radio(self):
    #     self.robots.pop(f'robot{len(self.ordered_list_xy)+1}')
    #     # for idx, option in enumerate(self.robots):
    #     self.select_robot = QtWidgets.QRadioButton(
    #         self.robots[len(self.robots)-1])
    #     self.layout3.addWidget(self.select_robot)
    #     self.button_group.deleteLater(
    #         self.select_robot, len(self.robots)-1)

    def manipulate_point(self, event):
        x, y = event.xdata, event.ydata
        offset = 0.5
        x_point, y_point = math.floor(x)+offset, math.floor(y)+offset
        self.ordered_list_xy = []
        # data_xy = {}
        # for data in ordered_list_xy:
        #     data_xy['coordinate'] = data
        xy_input = [x_point, y_point]
        for i in range(len(self.x)):
            self.ordered_list_xy.append([self.x[i], self.y[i]])
        print(self.ordered_list_xy)
        if len(self.x) > 0:
            if xy_input in self.ordered_list_xy:
                idx = self.ordered_list_xy.index(xy_input)
                # self.robot_reachability.pop[idx]
                print('--=------==----')
                for i in range(len(self.list_radio)):
                    print(self.list_radio[i].text())
                print('delete node', self.list_radio[idx].text(), '-----', idx)
                self.remove(idx, idx)
                self.layout3.removeWidget(self.list_radio[idx])
                self.list_radio[idx].setParent(None)
                self.list_radio.pop(idx)
            else:
                print('the list constains it but not of same xy')
                self.append(x_point, y_point)
                self.add_robot_radio()
        else:
            self.append(x_point, y_point)
            self.add_robot_radio()

            print('x and y: ', self.x, ' and ', self.y)
            print('x1 and y1: ', x_point, ' and ', y_point)

        cmap = self.cmap
        # self.ax.pcolor(self.data, cmap=cmap, edgecolors='k', linewidths=3)
        self.ax.scatter(self.x, self.y, s=50, c='b')
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])
        self.ax.set_title('Robot Cell Layout', fontsize=14)
        self.canvas.draw()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
