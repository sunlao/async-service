from xform.api.v1.helper.parser import Parser
from xform.api.v1.helper.command import Command
from shared.models.constants import Tags


class Fresh:
    def __init__(self, request):
        self.request = request
        self.command = Command(self.request)

    async def check(self, tag: Tags) -> bool:
        cmd = f"dbt source freshness -s @tag:{tag}"
        run = await self.command.run(cmd)
        out = run.Output
        if run.ReturnCode != 0 and "Database Error" in out and "does not exist" in out:
            return False
        if run.ReturnCode != 0 and "Failure in source" in out:
            return False
        if run.ReturnCode != 0:
            msg = f"Fresh ReturnCode: {run.ReturnCode} Output: {out} Error: {run.Error}"
            raise RuntimeError(msg)
        parsed = Parser(self.request).fresh_results(tag)
        model_cnt = len(parsed.Result)
        fresh_cnt = len([r.Model for r in parsed.Result if r.FreshFlag is True])
        if model_cnt == fresh_cnt and fresh_cnt > 0:
            return True
        return False
