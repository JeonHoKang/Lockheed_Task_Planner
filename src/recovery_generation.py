#!/usr/bin/python3

import openai
import yaml
import json
openai.api_key = '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'
import MILP_scheduler
from MILP_scheduler import HtnMilpScheduler


class RecoveryGeneration:
    def __init__(self):
        self.dict = None
        print('___initialized GPT recovery Module____')
        self.call_gpt()
        self.answer = None

    def import_htn(self):
        with open('problem_description/ATV_Assembly/current_ATV_Assembly_Problem.yaml', "r") as data:
            try:
                htn = str(yaml.safe_load(data))
            except yaml.YAMLError as e:
                print(e)
        return htn

    def import_example_policies(self):
        with open('src/recovery_policies_example.py', "r") as file:
            examples = file.read()
        return examples

    def import_user_prompt(self):
        with open('prompt/user_prompt.py', "r") as file:
            user_prompt = file.read()
        return user_prompt

    def import_intro(self):
        with open('prompt/recovery_generate.txt', "r") as file:
            intro = file.read()
        return intro

    def import_problem_description(self):
        with open('problem_description/ATV_Assembly/current_problem_description_ATV.yaml', "r") as data:
            try:
                problem_description = str(yaml.safe_load(data))
            except yaml.YAMLError as e:
                print(e)
        return problem_description
    
    def call_gpt(self):
        """calls gpt model """
        scheduler = HtnMilpScheduler()
        example_policies = self.import_example_policies()
        user_prompt = self.import_user_prompt()
        htn = self.import_htn()
        introduction = self.import_intro()
        problem_description = self.import_problem_description()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "user", "content": introduction},
                {"role": "user", "content": "Current HTN is :" + htn}, # feeds in htn as input,
                {"role": "user", "content": problem_description},
                {"role": "user", "content": "Here is the example: " + example_policies},
                {"role": "user", "content": user_prompt}
            ],

        )
        self.answer = response['choices'][0]['message']['content']
        # dict_answer = json.loads(self.answer)
        conv = {}
        
        print(self.answer)
        with open('src/generated_alphas.py', "a") as file:
            file.write(self.answer)


    def import_prompt_yaml(self):
        """
        imports yaml file
        :return:
        returns the prompt and context from the yaml file
        """
        with open('prompt/recovery_generate.yaml', "r") as data:
            try:
                self.dict = yaml.safe_load(data)
            except yaml.YAMLError as e:
                print(e)
        return self.dict


def main():
    recovery = RecoveryGeneration()


if __name__ == '__main__':
    main()
