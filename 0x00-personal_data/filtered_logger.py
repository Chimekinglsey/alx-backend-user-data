#!/usr/bin/env python3
"""0 - REGEX-ING Module"""
import re
from typing import List, Tuple
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum() """
        result = filter_datum(self.fields, self.REDACTION,
                              record.msg, self.SEPARATOR)
        formatted_message = self.FORMAT % {
                                            "name": record.name,
                                            "levelname": record.levelname,
                                            "asctime":
                                            self.formatTime(record,
                                                            self.datefmt),
                                            "message": result
                                        }
        return formatted_message


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates private fields in message """
    for item in fields:
        pattern = rf'{item}=(.*?)\{separator}'
        message = re.sub(pattern,  f' {item}={redaction}{separator}', message)
    return message
