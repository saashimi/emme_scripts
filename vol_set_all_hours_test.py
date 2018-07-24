"""
Run this test file from a cygwin window on a server that contains the 
INRO python API.
"""

import vol_set_all_hours


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4