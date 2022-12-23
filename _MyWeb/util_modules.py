# -*- coding: utf-8 -*-
"""
Util Module of MyWeb

@author: kiera
"""
# 產生隨機字串
def get_random_str(len=8):
    import string
    import random

    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(len))
