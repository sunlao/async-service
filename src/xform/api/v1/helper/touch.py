# edge-allow: open, pathlib
# no safe python objects in Standad lib
from errno import EEXIST
from shared.models.constants import TouchStatuses
from shared.models.xform import TouchResponse


class Touch:
    def __init__(self, cntx):
        self.ready_path = cntx.ready_path
        self.os = cntx.os

    def execute(self) -> TouchResponse:
        """Create the ready file once, atomically."""
        try:
            fd = self.os.open(
                self.ready_path,
                self.os.O_CREAT | self.os.O_EXCL | self.os.O_WRONLY,
            )
            self.os.close(fd)
            return TouchResponse(Status=TouchStatuses.NEW)
        except OSError as e:
            if e.errno == EEXIST:
                return TouchResponse(Status=TouchStatuses.EXIST)
            raise

    def unlink(self) -> None:
        try:
            self.ready_path.unlink()
        except FileNotFoundError:
            pass
