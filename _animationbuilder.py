# -*- coding: utf-8 -*-

__all__ = ('AnimationBuilder', )


import io
# import ast
import collections.abc

import yaml
from kivy.animation import Animation


class AnimationData(collections.abc.Mapping):

    def __init__(self, database):
        self._database = database

    def __getitem__(self, key):
        data = self._database[key]
        if 'compound' in data:
            raise NotImplementedError("compound animation ain't implemented yet.")
        else:
            return Animation(**data)

    def __iter__(self):
        return iter(self._database)

    def __len__(self):
        return len(self._database)


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


# def iterate_recur(node, indent=''):
#     print(indent, node, sep='')
#     if hasattr(node, 'id'):
#         print(indent, '  id=', node.id, sep='')
#     if isinstance(node, ast.Num):
#         print(indent, '  n=', node.n, sep='')
#     for item in ast.iter_child_nodes(node):
#         iterate_recur(item, indent=indent+'  ')

# r = ast.parse(ANIM_DATA)
# iterate_recur(r)
# print(dir(r))
# for item in ast.iter_child_nodes(r):
#     print(item)
# for item in ast.iter_fields(r):
#     print(item)