#!/usr/bin/python3

import os
import openai
import yaml

openai.api_key = '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'


class RecoveryGeneration:
    def __init__(self):
        self.dict = None
        print('___initialized GPT recovery Module____')
        self.call_gpt()

    # def get_context(self, cont):
    # # def generate_prompt(self):
    # #     content =
    # #     return content
    # #
    def call_gpt(self):
        """calls gpt model """
        prompt = self.import_prompt_yaml()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input("input prompt")}
                # {"role": "user", "content": "Screw was stuck during screwing. Recover from failure"},

                # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                # {"role": "user", "content": "How do I recover from failure"}
                #
            ],

        )
        answer = response['choices'][0]['message']['content']
        conv = {}
        print(answer)
        # recovery_action = eval(answer)
        # conv["answer"] = recovery_action
        # conv["content"] = prompt

        # print(recovery_action.items())

        new_yaml = f'context: {prompt}\n so far you have generated: {answer}'
        with open('prompt/recovery_generate.yaml', "w") as file:
            yaml.safe_dump(new_yaml, file)

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
