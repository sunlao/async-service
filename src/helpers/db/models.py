import enum


class DatabaseUserContext(enum.Enum):
    APP = "APP"
    DATA = "DATA"


class DatabaseConnectionProfile:
    def __init__(
        self,
        HOST: str,
        USER: str,
        PASSWORD: str,
        DB_NAME: str,
        PORT: int,
        ENGINE: str = "postgres",
    ):
        self.ENGINE = ENGINE
        self.HOST = HOST
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.DB_NAME = DB_NAME
        self.PORT = PORT
