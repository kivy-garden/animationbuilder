# -*- coding: utf-8 -*-

__all__ = ('AnimationBuilder', )


import io
from kivy.compat import PY2

if PY2:
    from collections import Mapping
else:
    from collections.abc import Mapping

import yaml

from ._compiler import Compiler


class AnimationData(Mapping):

    def __init__(self, database):
        self.database = database
        self.compile = Compiler(database).compile

    def __getitem__(self, key):
        return self.compile(key)

    def __iter__(self):
        return iter(self.database)

    def __len__(self):
        return len(self.database)


class AnimationBuilder:

    @staticmethod
    def load_file(filepath):
        with io.open(filepath, 'rt', encoding='utf_8') as stream:
            return AnimationBuilder.load_stream(stream)

    @staticmethod
    def load_string(s):
        return AnimationBuilder.load_stream(s)

    @staticmethod
    def load_stream(stream):
        return AnimationData(yaml.load(stream))
