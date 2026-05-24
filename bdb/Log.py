from common.Log import Log as CommonLogger


def Log(message: str, context: dict):
    CommonLogger("BDB", message, context)
