#!/usr/bin/env python3
"""0 - REGEX-ING Module"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates private fields in message """
    for item in fields:
        message = re.sub(rf'{item}.[^\{separator}]*',
                         f'{item}={redaction}', message)
    return message
