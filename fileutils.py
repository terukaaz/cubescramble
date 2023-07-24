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
            previous_number = int(previous_line.split(".")[0])
        except:
            previous_number = 0

        file.write(f"{previous_number + 1}. {time if penalty == 'none' else (f'{time}+' if penalty == '+2' else f'DNF({time})')}, {scramble}{f', [{comment}]' if comment != '' else ''}\n")