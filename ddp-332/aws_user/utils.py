# -*- coding: utf-8 -*-

"""Utilities for aws_user."""


import random


def gen_random_string(size, chars):
    """Generate random suffix for names."""
    return ''.join(random.choice(chars) for _ in range(size))
