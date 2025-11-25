from shutil import copyfile
from pathlib import Path
from xform.api.v1.helper.parser import Parser
from shared.models.constants import Tags


test_data = Path.cwd() / "tests" / "data" / "xform_runs"
not_fresh = test_data / "notfresh-sources.json"
fresh = test_data / "fresh-sources.json"
target = test_data / "sources.json"
models = ["raw.iso_country", "raw.iso_subdivision", "raw.cities"]


def test_fresh(dbt_request):
    copyfile(fresh, target)
    tag = Tags.NATAL
    parser = Parser(dbt_request)
    results = parser.fresh_results(tag)
    assert results.Tag == tag
    model_cnt = len(results.Result)
    fresh_cnt = len([r.Model for r in results.Result if r.FreshFlag is True])
    assert model_cnt > 0
    assert fresh_cnt > 0
    assert model_cnt == fresh_cnt
    for r in results.Result:
        assert r.Model in models


def test_not_fresh(dbt_request):
    copyfile(not_fresh, target)
    tag = Tags.NATAL
    parser = Parser(dbt_request)
    results = parser.fresh_results(tag)
    assert results.Tag == tag
    model_cnt = len(results.Result)
    fresh_cnt = len([r.Model for r in results.Result if r.FreshFlag is True])
    assert model_cnt > 0
    assert fresh_cnt == 0
    assert model_cnt != fresh_cnt
    for r in results.Result:
        assert r.Model in models
