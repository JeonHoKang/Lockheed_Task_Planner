import yaml

with open("problem_description/LM2023_problem/cont_problem_description_LM2023.yaml", "r") as file:
    d = yaml.safe_load(file)
    print(d)
