# -*- coding: utf-8 -*-

__all__ = ('prepare_for_compile', 'compile', )


import ast

from kivy.animation import Animation

from ._exception import AnimationBuilderException


class Compiler:

    def __init__(self, database):
        self.database = database

    def BinOp(self, node):
        operator = node.op.__class__.__name__
        handler = getattr(self, operator, None)
        if handler is None:
            raise AnimationBuilderException(
                "Unknown operator '{}'".format(operator))
        else:
            return handler(node.left, node.right)

    def Add(self, left_node, right_node):
        return self.compile_node(left_node) + self.compile_node(right_node)

    def BitAnd(self, left_node, right_node):
        return self.compile_node(left_node) & self.compile_node(right_node)

    def Expr(self, node):
        return self.compile_node(node.value)

    def Name(self, node):
        data = self.database.get(node.id)
        if data is None:
            raise AnimationBuilderException(
                "Unknown identifier '{}'".format(node.id))
        return self.compile_data(data)
        if 'compound' in data:
            return self.compile(data['compound'])
        else:
            return Animation(**data)

    def Call(self, node):
        func_name = node.func.id
        handler = getattr(self, 'Call_' + func_name, None)
        if handler is None:
            raise AnimationBuilderException(
                "Unknown function '{}'".format(func_name))
        return handler(node)

    def Call_sleep(self, node):
        return Animation(duration=node.args[0].n)

    def compile_node(self, node):
        node_name = node.__class__.__name__
        handler = getattr(self, node_name, None)
        if handler is None:
            raise AnimationBuilderException(
                "Unknown node '{}'".format(node_name))
        else:
            return handler(node)

    def compile_data(self, data):
        node = data.get('compound')
        if node is None:
            return Animation(**data)
        anim = self.compile_node(node)
        kwargs = data.copy()
        del kwargs['compound']
        for key, value in kwargs.items():
            setattr(anim, key, value)
        return anim


def prepare_for_compile(database):
    for data in database.values():
        s = data.get('compound')
        if s is not None:
            data['compound'] = ast.parse(s).body[0]


def compile(key, database):
    return Compiler(database).compile_data(database[key])
