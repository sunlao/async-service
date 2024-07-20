from os import getenv
from datetime import datetime
from redis import StrictRedis


class Client:
    def __init__(self):
        self.queue = StrictRedis(
            host=getenv("REDIS_HOST", "localhost"),
            port=int(getenv("REDIS_PORT", "6379")),
            decode_responses=True,
            charset="utf-8",
        )

    def keys(self):
        return [
            key.replace("arq:result:", "")
            for key in self.queue.scan_iter("arq:result:*")
        ]

    def health(self):
        status = self.queue.get("arq:queue:health-check")
        status_list = status.split(" ")
        year = datetime.today().strftime("%Y")
        date_time = f"{year}-{status_list[0]} {status_list[1]}"
        return {
            "status-length": len(status_list),
            "date-time": datetime.strptime(date_time, "%Y-%b-%d %H:%M:%S"),
            "complete": int(status_list[2].lstrip("j_complete=")),
            "queued": int(status_list[6].lstrip("queued=")),
        }
