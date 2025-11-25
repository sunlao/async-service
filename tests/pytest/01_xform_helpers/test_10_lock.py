from pathlib import Path
from time import sleep

test_data = Path.cwd() / "tests" / "data" / "xform_runs"
lock_file = test_data / ".dbt.lock"


def test_lifecyle(dbt_request):
    # dbt lock is initialized at api edge
    lock = dbt_request.app.state.lock
    # lock never exists at startup
    assert not lock_file.is_file()
    assert lock.acquire() is True
    assert lock_file.is_file()
    # can't aquire a lock if already locked
    assert lock.acquire() is False
    print("\n**** sleep 5 second for test lock_expiration of 4 seconds to expire")
    sleep(5)
    # can aquire a lock if locked aged out
    assert lock.acquire() is True
    lock.release()
    assert not lock_file.is_file()
