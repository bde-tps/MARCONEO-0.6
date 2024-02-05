"""
hardware.py

Defines some hardware abstractions that are used in the application.
"""

def key_to_number(buffer = "") -> int:
    """
    Converts a string to an integer.
    """
    LUT = {
        '&': '1',
        'é': '2',
        '"': '3',
        "'": '4',
        '(': '5',
        '-': '6',
        'è': '7',
        '_': '8',
        'ç': '9',
        'à': '0'
    }
    trans_table = str.maketrans(LUT)
    try:
        id_in_buffer = int(buffer.translate(trans_table))
    except ValueError:
        return None
    return id_in_buffer