from datetime import datetime, timezone
from tests.fixtures.fixtures_queue import queue_keys, queue_client, queue_health


def test_redis(queue_health):
    assert queue_health["status-length"] == 7
    assert queue_health["complete"] >= 0
    assert queue_health["queued"] >= 0
    assert (
        (
            datetime.now(timezone.utc).replace(tzinfo=None) - queue_health["date-time"]
        ).seconds
        / 60
        / 60
    ) <= 1
