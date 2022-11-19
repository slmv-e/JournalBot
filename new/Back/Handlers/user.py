def auth_data_input() -> tuple:
    login = str(input(" - Type login: "))
    password = str(input(" - Type password: "))
    if int(input('If data is correct type "1", else "0": ')) != 1:
        return auth_data_input()
    return login, password


def student_list_input() -> list:
    students = []
    print(' - Type student names in column (to stop writing press "Enter" two times):')
    while (student_name := str(input())) != "":
        students.append(student_name)
    print(' - Students list successfully appended')
    return students
