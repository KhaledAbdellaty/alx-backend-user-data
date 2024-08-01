#!/usr/bin/emnv python3
"""logger"""
import re
from typing import List
import logging
import os
import mysql


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """A function that returns the log message obfuscated."""
    pattern = r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator),
    repl = r'\g<field>={}'.format(redaction)
    return re.sub(pattern=pattern[0], repl=repl, string=message)


def get_logger():
    """A function that log PII fields."""
    logger = logging.getLogger('User_data')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db():
    """"A function that returns a connector to the database object"""
    credentials = {
        'user': os.getenv('PERSONAL_DATA_DB_USERNAME', "root"),
        'password': os.getenv('PERSONAL_DATA_DB_PASSWORD', ""),
        'host': os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        'database': os.getenv("PERSONAL_DATA_DB_NAME", "")
    }
    connector = mysql.connector.connect(
        host=credentials['host'],
        user=credentials['user'],
        password=credentials['password'],
        database=credentials['database'],
        port=3306
    )
    return connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """A function that filter values in incoming
        log records using filter_datum
        """
        message = super(RedactingFormatter, self).format(record)
        filtered = filter_datum(self.fields,
                                self.REDACTION, message, self.SEPARATOR)
        return filtered
