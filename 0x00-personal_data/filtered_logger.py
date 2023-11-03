#!/usr/bin/env python3
"""0 - REGEX-ING Module"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates private fields in message """
    for item in fields:
        pattern, replace = rf'{item}.[^\{separator}]*', f'{item}={redaction}'
        message = re.sub(pattern, replace, message)
    return message
