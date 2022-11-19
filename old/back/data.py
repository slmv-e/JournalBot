from dataclasses import dataclass


@dataclass()
class Data:
    login: str
    password: str
    homework_name: str
    count_of_levels: int
    students_list: list
