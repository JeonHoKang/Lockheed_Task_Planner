#!/usr/bin/python3

import openai
import yaml
import json
openai.api_key = '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'
import MILP_scheduler
from MILP_scheduler import HtnMilpScheduler
import json

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
        """
        imports yaml file
        :return:
        returns the prompt and context from the yaml file
        """
        with open('prompt/contingency_policies.yaml', "r") as data:
            try:
                self.dict = str(yaml.safe_load(data))
                print(self.dict)
            except yaml.YAMLError as e:
                print(e)
        return self.dict

    def import_user_prompt(self):
        with open('prompt/user_prompt.py', "r") as file:
            user_prompt = file.read()
        return user_prompt

    def import_intro(self):
        with open('prompt/recovery_generate2.txt', "r") as file:
            intro = file.read()
        return intro
    
    
    def call_gpt(self):
        """calls gpt model """
        scheduler = HtnMilpScheduler()
        example_policies = self.import_example_policies()
        user_prompt = self.import_user_prompt()
        htn = self.import_htn()
        introduction = self.import_intro()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "user", "content": introduction},
                {"role": "user", "content": "Here is the htn: " + htn}, # feeds in htn as input,
                {"role": "user", "content": "Here is the example: " + example_policies},
                {"role": "user", "content": "Here is the contingency. Generate recovery for \\"
                                            "I_r11_overheated_actuator : Complete this dictionary only"}
            ],

        )
        print("Generating_answer")
        self.answer = response['choices'][0]['message']['content']
        # dict_answer = json.loads(self.answer)
        conv = {}
        
        print(self.answer)
        with open('prompt/generation_method2.yaml', "a") as file:
            yaml.dump(eval(self.answer), file, sort_keys=False, Dumper=NoTagNoQuotesDumper)



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

class NoTagNoQuotesDumper(yaml.Dumper):
    """
    Export yaml file in the desired format - without string tag etc
    """

    def represent_data(self, data):
        if isinstance(data, tuple):
            return self.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)
        return super().represent_data(data)

    def represent_scalar(self, tag, value, style=None):
        if style is None:
            style = self.default_style
        if tag == 'tag:yaml.org,2002:str' and '\n' in value:
            style = '|'
        return super().represent_scalar(tag, value, style)

def main():
    recovery = RecoveryGeneration()


if __name__ == '__main__':
    main()
