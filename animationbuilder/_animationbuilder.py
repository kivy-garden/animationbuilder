# -*- coding: utf-8 -*-

__all__ = ('AnimationBuilder', )


import io
from kivy.compat import PY2
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty

if PY2:
    from collections import Mapping
else:
    from collections.abc import Mapping

import yaml

from ._compiler import Compiler


class AnimationData(EventDispatcher, Mapping):

    locals = ObjectProperty({}, allownone=True)  # Don't replace with DictProperty
    globals = ObjectProperty({}, allownone=True)  # Don't replace with DictProperty

    def __init__(self, database, **kwargs):
        self.compiler = Compiler(database)
        super(AnimationData, self).__init__(**kwargs)
        self.compile = self.compiler.compile
        self.database = database

    def __getitem__(self, key):
        return self.compile(key)

    def __iter__(self):
        return iter(self.database)

    def __len__(self):
        return len(self.database)

    def on_locals(self, __, value):
        self.compiler.locals = value

    def on_globals(self, __, value):
        self.compiler.globals = value


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
