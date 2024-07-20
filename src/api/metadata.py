def info():
    name = "Information"
    description = """GET:
- information about FastAPI Status"""
    return {"name": name, "description": description}


def tags():
    return [
        info(),
    ]
