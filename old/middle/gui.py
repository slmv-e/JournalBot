import eel
import sys
from raw.back.json_worker import reader, writer
from raw.back.data import Data
from raw.back.homeworks import app


class Application:
    def __init__(self):
        eel.init("front")
        self.data = reader()
        self.email = self.data["email"]
        self.password = self.data["password"]
        Data.login = self.email
        Data.password = self.password

    def start_ui(self):
        eel.hello_line(self.email)
        eel.start("index.html", size=(400, 600))


@eel.expose
def login_and_password_writer(login: str, password: str, checkbox: bool):
    Data.login = login
    Data.password = password
    if checkbox:
        writer(login, password)


@eel.expose
def startApp():
    data = {
        "homework_name": Data.homework_name,
        "levels_cnt": Data.count_of_levels,
        "students": Data.students_list
    }
    app(Data.login, Data.password, data)


@eel.expose
def get_homework_data(hw_name: str, levels_cnt: str, stud_list: str):
    Data.homework_name = hw_name
    Data.count_of_levels = levels_cnt
    Data.students_list = stud_list.split("\n")


@eel.expose
def quit_app():
    sys.exit()


def change_status(status):
    eel.changeStatus(status)


if __name__ == "__main__":
    app = Application()
    app.start_ui()
