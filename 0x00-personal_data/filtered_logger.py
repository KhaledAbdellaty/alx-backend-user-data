#!/usr/bin/emnv python3
"""logger"""
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """A function that returns the log message obfuscated:"""
    pattern = r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator),
    repl = r'\g<field>={}'.format(redaction)
    return re.sub(pattern=pattern[0], repl=repl, string=message)
