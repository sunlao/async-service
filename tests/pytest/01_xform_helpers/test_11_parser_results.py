from shutil import copyfile
from pathlib import Path
from xform.api.v1.helper.parser import Parser
from shared.models.constants import DBTTypes
from shared.models.xform import ParseRunRequest


test_data = Path.cwd() / "tests" / "data" / "xform_runs"
seed = test_data / "seed-run_results.json"
run = test_data / "run-run_results.json"
target = test_data / "run_results.json"


def test_seed(dbt_request):
    copyfile(seed, target)
    run_id = "35c5ae52-4c7b-4b06-9cd9-a738249585c1"
    data = ParseRunRequest(RunId=run_id, ActionType=DBTTypes.SEED)
    names = ["body", "body_type", "house", "point_type", "sign"]
    count = {"body": 14, "body_type": 3, "house": 12, "point_type": 2, "sign": 12}
    dur = {
        "body": 0.1964883804321289,
        "body_type": 0.20395541191101074,
        "house": 0.2076106071472168,
        "point_type": 0.2153937816619873,
        "sign": 0.05132746696472168,
    }
    parser = Parser(dbt_request)
    results = parser.run(data)
    assert results.Status is True
    assert results.RunId == run_id
    assert results.Command == "dbt seed"
    assert results.Duration == 0.5715122222900391
    run_results = results.RunResults
    assert len(run_results) == len(names)
    for row in run_results:  # pylint: disable=not-an-iterable
        assert row.ModelStatus == "success"
        assert row.Failures is None
        assert row.ExecutionTime == dur[row.Name]
        assert row.RowsAffected == count[row.Name]
        assert row.Name in names


def test_run(dbt_request):
    copyfile(run, target)
    run_id = "9dfc1925-d305-41a8-9cf2-bc576300bdb4"
    data = ParseRunRequest(RunId=run_id, ActionType=DBTTypes.RUN)
    names = ["working.location"]
    count = {"working.location": 52552}
    dur = {"working.location": 0.25722503662109375}
    parser = Parser(dbt_request)
    results = parser.run(data)
    assert results.Status is True
    assert results.RunId == run_id
    assert results.Command == "dbt run --select tag:natal"
    assert results.Duration == 0.5167360305786133
    run_results = results.RunResults
    assert len(run_results) == len(names)
    for row in run_results:  # pylint: disable=not-an-iterable
        assert row.ModelStatus == "success"
        assert row.Failures is None
        assert row.ExecutionTime == dur[row.Name]
        assert row.RowsAffected == count[row.Name]
        assert row.Name in names
