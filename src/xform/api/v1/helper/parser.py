# edge-allow: open, pathlib
# no safe python objects in Standad lib
from shared.models.constants import DBTTypes, Tags
from shared.models.xform import (
    ParseRunRequest,
    FreshResult,
    FreshResults,
    ParseRunResponse,
    ModelResult,
)


class Parser:
    def __init__(self, request):
        self.time_counter = request.app.state.config_log.TimeCounter
        self.path_run = request.app.state.run_result_path
        self.path_fresh = request.app.state.path_fresh
        # self.path_manifest = request.app.state.run_manifest_path
        self.load = request.app.state.load
        self.lock = request.app.state.lock
        # self.allowed = set("model", "snapshot")

    def _load_doc(self, path) -> dict | None:
        try:
            with path.open("r", encoding="utf-8") as f:
                return self.load(f)
        except Exception:  # pylint: disable=broad-except
            return None

    @staticmethod
    def _run_id(doc) -> str:
        try:
            return doc["metadata"]["env"]["RUN_ID"]
        except Exception:  # pylint: disable=broad-except
            return "dbt not ready yet"

    @staticmethod
    def _name(result: dict[str, object], action_type: DBTTypes) -> str:
        name = {
            DBTTypes.SEED: result.get("unique_id"),
            DBTTypes.FRESH: result.get("unique_id"),
            DBTTypes.RUN: result.get("relation_name"),
        }.get(action_type)
        if name:
            name = (
                name.replace("seed.xform.", "")
                .replace("source.xform.", "")
                .replace("db_aserv", "")
                .replace('"', "")
            ).strip(".")
        return name

    # def _manifest_results(self, doc, tag: Tags) -> list[ManifestResult]:
    #     results = doc.get("xxx")
    #     return [self._run_manifest(result, tag) for result in results]

    def _run_result(
        self, result: dict[str, object], action_type: DBTTypes
    ) -> ModelResult:
        return ModelResult(
            ModelStatus=result.get("status"),
            ExecutionTime=result.get("execution_time"),
            RowsAffected=result.get("adapter_response", {}).get("rows_affected"),
            Name=self._name(result, action_type),
            Failures=result.get("failures"),
        )

    def _run_results(self, doc, action_type: DBTTypes) -> list[ModelResult]:
        results = doc.get("results")
        return [self._run_result(result, action_type) for result in results]

    # def manifest(self, data: ParseManifestRequest) -> ParseManifestResponse:
    #     doc = self._load_doc(self.path_manifest)
    #     nodes = doc.get("nodes")
    #     response =  ParseManifestResponse(
    #         Status=True,
    #         tag=data.TagId,
    #         ManifestResults=self._manifest_results(doc, data.Tag),
    #     )

    def _fresh_result(self, result) -> FreshResult:
        status = str(result.get("status", "")).lower()
        return FreshResult(
            Model=self._name(result, DBTTypes.FRESH), FreshFlag=(status == "pass")
        )

    def fresh_results(self, tag: Tags) -> FreshResults:
        doc = self._load_doc(self.path_fresh)
        doc_results = doc.get("results")
        results = [self._fresh_result(r) for r in doc_results]
        return FreshResults(Tag=tag, Result=tuple(results))

    def run(self, data: ParseRunRequest) -> ParseRunResponse:
        """Parse dbt run results if available by action type"""
        doc = self._load_doc(self.path_run)
        run_id = self._run_id(doc)
        if data.RunId == run_id:
            response = ParseRunResponse(
                Status=True,
                RunId=data.RunId,
                Command=doc.get("args", {}).get("invocation_command"),
                RunResults=self._run_results(doc, data.ActionType),
                Duration=doc.get("elapsed_time"),
            )
            self.lock.release()
            return response
        return ParseRunResponse(Status=False)
