from pprint import pprint
from typing import Any


def pretty_print(msg: list[dict[str, Any]], indent: int = 4):
   print()
   pprint(msg, indent=indent)

