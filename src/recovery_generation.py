#!/usr/bin/python3

import openai
import yaml
import json
openai.api_key = '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'
from MILP_scheduler import HtnMilpScheduler

class RecoveryGeneration:
    def __init__(self):
        self.dict = None
        print('___initialized GPT recovery Module____')
        self.user_prompt = input("input prompt: ")
        self.call_gpt(self.user_prompt)
        self.answer = None
    # def get_context(self, cont):
    # # def generate_prompt(self):
    # #     content =
    # #     return content
    # #
    def call_gpt(self, user_prompt):
        """calls gpt model """
        scheduler = HtnMilpScheduler()
        prompt = self.import_prompt_yaml()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_prompt},
                {"role": "user", "content": f'{scheduler.multi_product_dict}'},
                # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                # {"role": "user", "content": "How do I recover from failure"}
                #
            ],

        )
        self.answer = response['choices'][0]['message']['content']
        dict_answer = json.loads(self.answer)
        conv = {}
        # print(answer)
        # recovery_action = eval(answer)
        # conv["answer"] = recovery_action
        # conv["content"] = prompt

        # print(recovery_action.items())
        new_yaml = dict_answer
        print(dict_answer)
        # new_yaml = f'context: {prompt}\n so far you have generated: {self.answer}'
        with open(f'answer/{user_prompt}.yaml', "w") as file:
            yaml.dump(new_yaml, file)

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
