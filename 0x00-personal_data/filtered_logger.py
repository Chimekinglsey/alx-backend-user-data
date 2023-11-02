#!/usr/bin/env python3
"""0 - REGEX-ING"""
import re
from typing import List


def filter_datum(field: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates private fields in message """
    for item in field:
        pattern = rf'{item}.[^{separator}]+'
        message = re.sub(pattern, f'{item}={redaction}', message)
    return message
