# -*- coding: utf-8 -*-

__all__ = ('Compiler', )


import ast

from kivy.animation import Animation

from ._exception import AnimationBuilderException


class Compiler:

    def __init__(self, database):
        self.database = {
            key: self.prepare_dictionary(data)
            for key, data in database.items()
        }

    def compile(self, key):
        return self.compile_identifier(key)

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
        return self.compile_identifier(node.id)

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

    def compile_identifier(self, identifier):
        value = self.database.get(identifier)
        if value is None:
            raise AnimationBuilderException(
                "Unknown identifier '{}'".format(identifier))
        data, handler = value
        # print(data, handler)
        return handler(data)

    def compile_simple(self, dictionary):
        return Animation(**dictionary)

    def compile_freestyle(self, dictionary):
        node = dictionary['freestyle']
        anim = self.compile_node(node)
        kwargs = dictionary.copy()
        del kwargs['freestyle']
        for key, value in kwargs.items():
            setattr(anim, key, value)
        return anim

    def compile_sequential(self, dictionary):
        listobj = dictionary['sequential']

        data, handler = listobj[0]
        anim = handler(data)
        for data, handler in listobj[1:]:
            anim += handler(data)

        kwargs = dictionary.copy()
        del kwargs['sequential']
        for key, value in kwargs.items():
            setattr(anim, key, value)
        return anim

    def compile_unsupported(self, data):
        raise AnimationBuilderException(
            "Unsupported data type: " + str(type(data)))

    def prepare_dictionary(self, dictionary):
        # sequential
        sequential = dictionary.get('sequential', None)
        if sequential is not None:
            dictionary['sequential'] = self.prepare_list(sequential)
            return (dictionary, self.compile_sequential, )
        # freestyle
        freestyle = dictionary.get('freestyle', None)
        if freestyle is not None:
            dictionary['freestyle'] = ast.parse(freestyle).body[0]
            return (dictionary, self.compile_freestyle, )
        # simple
        return (dictionary, self.compile_simple)

    def prepare_list(self, listobj):
        return [
            (item, self.compile_identifier, ) if isinstance(item, str)
            else self.prepare_dictionary(item) if isinstance(item, dict)
            else (item, self.compile_unsupported, )
            for item in listobj
        ]
