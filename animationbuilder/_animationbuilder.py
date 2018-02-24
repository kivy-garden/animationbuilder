# -*- coding: utf-8 -*-

__all__ = ('AnimationBuilder', )


import io
import collections.abc

import yaml

from ._compiler import compile, prepare_for_compile


class AnimationData(collections.abc.Mapping):

    def __init__(self, database):
        self.database = database

    def __getitem__(self, key):
        return compile(key, self.database)

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
        database = yaml.load(stream)
        prepare_for_compile(database)
        return AnimationData(database)
