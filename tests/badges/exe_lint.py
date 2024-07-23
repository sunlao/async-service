from os import getcwd
from sys import path

path.insert(0, getcwd())

# pylint: disable=C0413
from tests.badges.badges import Badges  # nopep8

Badges().exe_pylint()
