import datetime
import os
from functools import reduce


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


def get_aon(file, n=5):

    filename = file

    if filename not in os.listdir("."):
        return "-"

    with open(filename, "r+") as file:
        content = file.readlines()

        if content.__len__() < n:
            return "-"

        time_list = []

        for i in range(n):
            time_list.append((content[content.__len__() + i - n].split(". ")[1]).split(",")[0])

        # this code sucks
        time_list_in_seconds = []

        for t in range(time_list.__len__()):
            time_list_in_seconds.append((t, time_to_seconds(time_list[t]), time_list[t]))

        current_maximum = (0, 0, "")
        current_minimum = (0, 0, "")

        for j in range(time_list_in_seconds.__len__()):
            if time_list_in_seconds[j][1] > current_maximum[1]:
                current_maximum = time_list_in_seconds[j]

            if j == 0:
                current_minimum = time_list_in_seconds[j]
            else:
                if time_list_in_seconds[j][1] < current_minimum[1]:
                    current_minimum = time_list_in_seconds[j]

        time_list.remove(current_minimum[2])
        time_list.remove(current_maximum[2])

        return average_time(time_list)


def time_to_seconds(time_str):

    try:
        time_in_datetime = datetime.datetime.strptime(time_str, "%S.%f")
    except:
        try:
            time_in_datetime = datetime.datetime.strptime(time_str, "%M:%S.%f")
        except:
            try:
                time_in_datetime = datetime.datetime.strptime(time_str, "%H:%M:%S.%f")
            except:
                raise ValueError("Something went wrong with the time format!!!")


    real_time = time_in_datetime.replace(hour=0) - datetime.datetime(1900, 1, 1) # fuck unix
    seconds = real_time.total_seconds()

    return seconds


# ChatGPT moment.. hahaha
def average_time(time_list, roundv=1):
    # Convert all time values to seconds
    time_in_seconds = [time_to_seconds(time) for time in time_list]

    # Calculate the average time in seconds
    average_seconds = sum(time_in_seconds) / len(time_in_seconds)

    # Convert average time to different formats based on hours, minutes, and seconds
    if average_seconds >= 36000:
        # Format: HH:MM:SS.ms
        average_minutes, remainder_seconds = divmod(average_seconds, 60)
        average_hours, average_minutes = divmod(average_minutes, 60)
        average_seconds, average_milliseconds = divmod(remainder_seconds, 1)
        average_milliseconds *= 1000

        return f"{int(average_hours):02d}:{int(average_minutes):02d}:{int(average_seconds):02d}.{int(round(average_milliseconds, -roundv + 1))}"
    elif average_seconds >= 3600:
        # Format: H:MM:SS.ms
        average_minutes, remainder_seconds = divmod(average_seconds, 60)
        average_hours, average_minutes = divmod(average_minutes, 60)
        average_seconds, average_milliseconds = divmod(remainder_seconds, 1)
        average_milliseconds *= 1000

        return f"{int(average_hours)}:{int(average_minutes):02d}:{int(average_seconds):02d}.{int(round(average_milliseconds, -roundv + 1))}"
    elif average_seconds >= 600:
        # Format: HH:MM:SS.ms
        average_minutes, remainder_seconds = divmod(average_seconds, 60)
        average_seconds, average_milliseconds = divmod(remainder_seconds, 1)
        average_milliseconds *= 1000

        return f"{int(average_minutes):02d}:{int(average_seconds):02d}.{int(round(average_milliseconds, -roundv + 1))}"
    elif average_seconds >= 60:
        # Format: M:SS.ms
        average_minutes, remainder_seconds = divmod(average_seconds, 60)
        average_seconds, average_milliseconds = divmod(remainder_seconds, 1)
        average_milliseconds *= 1000

        return f"{int(average_minutes)}:{int(average_seconds):02d}.{int(round(average_milliseconds, -roundv + 1))}"
    elif average_seconds >= 10:
        # Format: MM:SS.ms
        average_seconds, average_milliseconds = divmod(average_seconds, 1)
        average_milliseconds *= 1000

        return f"{int(average_seconds):02d}.{int(round(average_milliseconds, -roundv + 1))}"
    else:
        # Format: S.ms
        average_seconds, average_milliseconds = divmod(average_seconds, 1)
        average_milliseconds *= 1000

        return f"{int(average_seconds)}.{int(round(average_milliseconds, -roundv + 1))}"