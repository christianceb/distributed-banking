import time
import datetime


def unix_timestamp_s() -> int:
    return int(time.time())

def unix_timestamp_to_iso8601(ts: int) -> str:
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')

def iso8601() -> str:
    return datetime.datetime.now().replace(microsecond=0).isoformat()
