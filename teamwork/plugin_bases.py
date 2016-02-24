# -*- coding: utf-8 -*-
from __future__ import absolute_import

import elk


class ModePlugin(elk.ElkRole):
    """
    Base role for plugins serving as operational modes for virtual agents
    """

    __require__ = ('add_parser',)
    # add_parser: callable
