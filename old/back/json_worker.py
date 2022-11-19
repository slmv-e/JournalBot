import json


def reader() -> dict:
    with open("back/config.json") as f:
        data = json.load(f)
    return data


def writer(login: str, password: str):
    with open("back/config.json", "w") as f:
        data = {
            "email": login,
            "password": password
        }
        json.dump(data, f)
