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
        print('start')

    def set_dir(self, dir):
        """Sets the problem instance directory"""
        self.problem_dir = dir

    def import_problem(self, prob_description_yaml):
        file_dir = self.problem_dir + prob_description_yaml
        print(file_dir)
        with open(file_dir, 'r') as stream:
            try:
                # Converts yaml document to python object
                self.problem_description = yaml.safe_load(stream)

            # Printing dictionary
                print(self.problem_description)
            except yaml.YAMLError as e:
                print(e)

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
        num_products = 2
        children = []
        for p in range(num_products):
            child = DictImporter().import_(dict)
            if p > 0:
                for node in PostOrderIter(child):
                    node.id = 'p{}_'.format(p+1) + node.id
            children.append(child)
        print(children)
        # htn = DictImporter().import_(dict)
        # htn2 = DictImporter().import_(dict)
        root = AnyNode(id="TASK_ROOT", type='parallel', children=children)
        # root.children = AnyNode(id="toy_prob", type='independent')
        self.htn_model = root
        if print_htn:
            print(RenderTree(root))

        return self.htn_model


def main():
    scheduler = HtnMilpScheduler()
    scheduler.set_dir("problem_description/toy_problem/")
    scheduler.import_problem("problem_description_toy.yaml")
    scheduler.import_htn()


if __name__ == '__main__':
    main()
