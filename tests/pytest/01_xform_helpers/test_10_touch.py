from pathlib import Path

test_data = Path.cwd() / "tests" / "data" / "xform_runs"
ready = test_data / ".ready.lock"


def test_lifecyle(dbt_request):
    assert not ready.is_file()
    touch = dbt_request.app.state.touch
    touch.execute()
    assert ready.is_file()
    touch.unlink()
    assert not ready.is_file()
