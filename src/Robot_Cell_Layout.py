from tkinter import ttk
import tkinter as tk
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.widgets import Button, TextBox, CheckButtons
import math
import numpy as np
from matplotlib import colors
from matplotlib import pyplot as plt


grid_len = 10

data = [[0]*grid_len]*grid_len


robot_x = []
robot_y = []
robot_th = []

scale = 0.25
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Warning")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def conv_cart_to_ang(angle):
    if angle == 0:
        angle = 0.00001
    else:
        angle = angle
    dx = 1*math.cos(angle*(math.pi/180))
    dy = 1*math.sin(angle*(math.pi/180))
    return [dx, dy]


def submit_x(expression):
    """
    Update the plotted function to the new math *expression*.

    *expression* is a string using "t" as its independent variable, e.g.
    "t ** 3".
    """

    if expression.isnumeric() == False:
        popupmsg('not a number')
    elif int(expression) > grid_len:
        popupmsg('Value cannot exceed {}'.format(grid_len))
    else:
        expression = int(expression)
        robot_x.append(expression)
        plt.text(0.02, 0.6, 'x : {}'.format(robot_x), fontsize=7,
                 transform=plt.gcf().transFigure)

    print(robot_x)


def submit_y(expression):
    """
    Update the plotted function to the new math *expression*.

    *expression* is a string using "t" as its independent variable, e.g.
    "t ** 3".
    """
    if expression.isnumeric() == False:
        popupmsg('not a number')
    elif int(expression) > grid_len:
        popupmsg('Value cannot exceed {}'.format(grid_len))
    else:
        expression = int(expression)
        robot_y.append(expression)
        plt.text(0.02, 0.7, 'y : {}'.format(robot_y), fontsize=7,
                 transform=plt.gcf().transFigure)

    print(robot_y)


def submit_theta(expression):
    """
    Update the plotted function to the new math *expression*.

    *expression* is a string using "t" as its independent variable, e.g.
    "t ** 3".
    """
    if expression.isnumeric() == False:
        popupmsg('not a number')
    else:
        expression = int(expression)
        robot_th.append(expression)
        plt.text(0.02, 0.8, 'theta : {}'.format(robot_th), fontsize=7,
                 transform=plt.gcf().transFigure)

    print(robot_th)


def delete_index(expression):

    if expression.isnumeric() == False:
        popupmsg('Input Robot Index')
    elif int(expression) > grid_len:
        popupmsg('Value cannot exceed {}'.format(len(robot_x)))
    else:

        expression = int(expression)-1
        cmap = colors.ListedColormap(['yellow'])
        ax.pcolor(data, cmap=cmap, edgecolors='k', linewidths=3)
        del robot_x[expression]
        del robot_y[expression]
        del robot_th[expression]
        for i in range(len(robot_x)):
            ax.arrow(robot_x[i]-0.5, robot_y[i]-0.5, scale*conv_cart_to_ang(robot_th[i])[0],
                     scale*conv_cart_to_ang(robot_th[i])[1], head_width=0.1, color='blue', label='robot{}'.format(i+1))
    plt.draw()
    # plt.text(0.02, 0.6, 'x : {}'.format(robot_x), fontsize=7,
    #          transform=plt.gcf().transFigure)
    # plt.text(0.02, 0.7, 'y : {}'.format(robot_y), fontsize=7,
    #          transform=plt.gcf().transFigure)
    # plt.text(0.02, 0.8, 'theta : {}'.format(robot_th), fontsize=7,
    #          transform=plt.gcf().transFigure)


fig, ax = plt.subplots(figsize=(7, 6))
fig.subplots_adjust(bottom=0.3)
fig.subplots_adjust(left=0.2)
ax.set_title('Robot Cell Layout', fontsize=14)
cmap = colors.ListedColormap(['yellow'])
ax.pcolor(data, cmap=cmap, edgecolors='k', linewidths=3)


class Index:
    ind = 0

    def next(self, event):
        self.ind += 1
        print("Number of Robots Added is : ", self.ind)
        if abs(len(robot_x) - len(robot_y)) >= 1 or abs(len(robot_x) - len(robot_th)) >= 1 or abs(len(robot_y) - len(robot_th)) >= 1:
            popupmsg('All three value entries need to match')
            popupmsg('Check the left side of the graph')
        else:
            for i in range(len(robot_x)):
                ax.arrow(robot_x[i]-0.5, robot_y[i]-0.5, scale*conv_cart_to_ang(robot_th[i])[0],
                         scale*conv_cart_to_ang(robot_th[i])[1], head_width=0.1, color='blue', label='robot{}'.format(i+1))
                # if robot_th[i] >= 180:
                #     ax.text(robot_x[i]-0.95, robot_y[i]-0.3,
                #             'robot{}'.format(i+1), color='blue', fontsize='medium')
                # else:
                #     ax.text(robot_x[i]-0.95, robot_y[i]-0.8,
                #             'robot{}'.format(i+1), color='blue', fontsize='medium')

        plt.draw()


callback = Index()

delRobot = fig.add_axes([0.81, 0.05, 0.1, 0.075])
update_fig = fig.add_axes([0.81, 0.15, 0.1, 0.075])
del_Robot = TextBox(delRobot, 'Del: ', textalignment="center")
bnext = Button(update_fig, 'Update')
axbox_x = fig.add_axes([0.11, 0.05, 0.1, 0.075])
axbox_y = fig.add_axes([0.31, 0.05, 0.1, 0.075])
axbox_th = fig.add_axes([0.64, 0.05, 0.1, 0.075])
bnext.on_clicked(callback.next)
text_box_x = TextBox(axbox_x, "Robot X: ", textalignment="center")
text_box_y = TextBox(axbox_y, "Robot Y: ", textalignment="center")
text_box_th = TextBox(axbox_th, "Robot Angle(Degree): ",
                      textalignment="center")
del_Robot.on_submit(delete_index)
text_box_x.on_submit(submit_x)
text_box_y.on_submit(submit_y)
text_box_th.on_submit(submit_theta)
plt.show()
