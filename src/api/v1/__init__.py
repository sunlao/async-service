from os import getenv
from pathlib import Path


def version_app():
    if getenv("TOX_FLAG", "False") == "True":
        directory = Path(__file__).parents[3]
        path = f"{directory}/VERSION"
    else:
        path = "/app/VERSION"
    with open(path, encoding="UTF-8") as file_obj:
        version = file_obj.read()
    return version
