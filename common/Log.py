from common.Temporal import iso8601


def Log(source: str, message: str, context: dict):
    print(
        f"[{iso8601()}][{source}]: {message}",
        context
    )
