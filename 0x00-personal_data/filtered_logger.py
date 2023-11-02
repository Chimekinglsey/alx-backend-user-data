#!/usr/bin/env python3
"""0 - REGEX-ING"""
import re
from typing import List


def filter_datum(field: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates private fields in message """
    for item in field:
        pattern = rf'{item}={redaction}{separator}'
        message = re.sub(item, pattern, message)
    return message
