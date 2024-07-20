from src.helpers.db.sql.hello import Hello


class Query:
    def get(self, p_name: str) -> str:
        # add SQL classes below to integrate sql with db init
        if p_name.startswith("hello"):
            sql = Hello().get(p_name)
            return sql
        return None
