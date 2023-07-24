import json
import os


def write_history(file, time: str, scramble: str, comment="", penalty="none"):

    filename = file

    if filename not in os.listdir("."):
        with open(filename, "w") as file:
            file.write("")

    with open(filename, "r+") as file:
        content = file.readlines()

        try:
            previous_line = content[content.__len__() - 1]
            previous_number = int(previous_line[0])
        except:
            previous_number = 0

        file.write(f"{previous_number + 1}. {time if penalty == 'none' else (f'{time}+' if penalty == '+2' else f'DNF({time})')}, {scramble}{f', [{comment}]' if comment != '' else ''}\n")

def save_config():
    filename = "config.json"

    with open(filename, 'w') as file:
        json.dump({
            "config": {
                "state": 1
            }
        }, file)


def load_config():  # currently does nothing at all
    filename = "config.json"

    if filename not in os.listdir('.'):
        with open(filename, 'w') as file:
            json.dump({
                "config": {
                    "state": 1
                }
            }, file)
            return

    with open(filename, "r") as file:
        try:
            data: dict = json.load(file)
        except json.decoder.JSONDecodeError as e:
            print(repr(e))