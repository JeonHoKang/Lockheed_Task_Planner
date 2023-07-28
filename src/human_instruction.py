#!/usr/bin/python3

import os
import openai
import yaml

openai.api_key = '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'


class HumanInstruction:
    def __init__(self):
        self.dict = None
        print('___initialized GPT recovery Module____')
        self.call_gpt()

    def import_example_policies(self):
        with open('src/recovery_policies_example.py', "r") as file:
            examples = file.read()
            print("check")
        return examples


    def call_gpt(self):
        """calls gpt model """
        prompt = self.import_prompt_yaml()
        example_policies = self.import_example_policies()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": example_policies},
                {"role": "user", "content": "recovery-dropped_main_body : r1 has dropped a part during pick and place of the ATV main body frame. r1 will search\
                for a part and see if it is reachable which will take 5.\
                Let us say that it is reachable. Then r1 will re-pick the part which will take 3.\
                Then r1 will place it on the table b1 which will take 6."}
            ]
        )
        answer = response['choices'][0]['message']['content']
        print(answer)
        # recovery_action = eval(answer)
        # conv["answer"] = recovery_action
        # conv["content"] = prompt

        # print(recovery_action.items())

        with open('src/recovery_policies_example.py', "a") as file:
            file.write(answer)

    def import_prompt_yaml(self):
        """
        imports yaml file
        :return:
        returns the prompt and context from the yaml file
        """
        with open('prompt/human_instruction.yaml', "r") as data:
            try:
                self.dict = yaml.safe_load(data)
            except yaml.YAMLError as e:
                print(e)
        return self.dict


def main():
    recovery = HumanInstruction()


if __name__ == '__main__':
    main()
