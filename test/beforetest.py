# -*- coding: utf-8 -*-

import sys
import os.path
import kivy.resources

SEARCH_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SEARCH_PATH)
kivy.resources.resource_add_path(SEARCH_PATH)
