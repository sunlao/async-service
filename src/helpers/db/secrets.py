from os import getenv
from os import environ
from logging import debug
from dotenv import load_dotenv


class Secrets:
    def _local_db_secrets(self, p_user_context: str) -> None:
        if getenv("ENV", "false") == "test":
            load_dotenv()
        return {
            "HOST": environ["DB_HOST"],
            "USER": f"{environ['APP_CODE']}_{p_user_context.value}".lower(),
            "PASSWORD": environ[f"DB_{p_user_context.value}_PWD"],
            "DB_NAME": environ["DB_NAME"],
            "ENGINE": "postgres",
            "PORT": environ["DB_PORT"],
        }

    def db(self, p_user_context: str):
        if getenv("ENV", "false") in ["test", "github"]:
            secrets = self._local_db_secrets(p_user_context)
            safe_secrets = {k: v for k, v in secrets.items() if k != "PASSWORD"}
            debug("safe_secrets: %s", safe_secrets)
            return secrets
        return None
