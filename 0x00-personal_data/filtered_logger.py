#!/usr/bin/env python3
"""0 - REGEX-ING Module"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Basic login function """
    for specifics in fields:
        message = re.sub(rf"{specifics}=(.*?)\{separator}",
                         f'{specifics}={redaction}{separator}', message)
    return message