# edge-allow: open, pathlib
# no safe python objects in Standad lib
from errno import EEXIST


class Lock:
    """Create a lock for DBT to assert only one dbt execution can happen
    at a time. Locks Age out after 30 minutes.  For AsyncServ it is
    assumed all dbt jobs will complete after 30 minutes. Locks are relased on
    start up and shut down
    """

    def __init__(self, cntx):
        self.lock_path = cntx.lock_path
        self.time = cntx.time
        self.os = cntx.os
        self.now = cntx.config_log.Now
        self.lock_expiration = cntx.lock_expiration

    def _open(self) -> bool:
        """Attempt to create a conventional atomic lock file via open flags.
        - O_CREAT: create if doesn't exist
          - Raises EEXIST which is handled: Returns False
        - O_EXCL: Exclusive create
        - O_CLOEXEC: prevent fd descriptor leakage extreme edge case
        """
        flags = self.os.O_CREAT | self.os.O_EXCL | getattr(self.os, "O_CLOEXEC", 0)
        try:
            fd = self.os.open(self.lock_path, flags)
            self.os.close(fd)
            return True
        except OSError as e:
            if e.errno == EEXIST:
                return False
            raise

    def _check(self, age: float) -> bool:
        """Check Lock Expiratioin
        - True: Remove lock and retry acquisition
        - False: Locked"""
        if age > self.lock_expiration:
            try:
                self.lock_path.unlink()
            except FileNotFoundError:
                pass
            return self.acquire()
        return False

    def acquire(self) -> bool:
        """Attempt Lock aquistion
        - True: acquired
        - False: locked"""
        if self._open():
            return True
        try:
            mtime = self.lock_path.stat().st_mtime
            age = self.time() - mtime
        except FileNotFoundError:
            return self._open()
        return self._check(age)

    def release(self) -> None:
        """Release Lock"""
        try:
            self.lock_path.unlink()
        except FileNotFoundError:
            pass
