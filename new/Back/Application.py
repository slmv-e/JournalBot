from dataclasses import dataclass
from threading import Thread
import pandas as pd
from Parse import *
from Handlers.user import *
from Handlers.config import *


@dataclass(kw_only=True)
class Data:
    login: str
    password: str
    students_list: list
    homeworks: list = 0


def main():
    login, password = auth_data_input()
    students_list = student_list_input()

    data = Data(login=login, password=password, students_list=students_list)
    parse_preload_app = App(data=data)
    data.homeworks = parse_preload_app.get_data()
    apps, jobs, result = [], [], {"Name": {}}

    for index in range(len(students_list)):
        result["Name"][index + 1] = students_list[index]

    # multithreading
    for i in range(len(data.homeworks)):
        apps.append(App(data=data))
        process = Thread(target=apps[i].parse, args=(i, ))

        jobs.append(process)
        process.start()

    for proc in jobs:
        proc.join()

    # getting result dict
    for app in apps:
        result.update(app.output)

    # deleting empty columns
    result = {key: value for (key, value) in result.items() if value}

    # save result in .xlsx file
    homework_data = pd.DataFrame(result)
    filename = "HomeworkData.xlsx"
    homework_data.to_excel(f"../{filename}")


if __name__ == "__main__":
    main()
