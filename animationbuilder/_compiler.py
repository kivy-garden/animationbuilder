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

    def compile_simple_dictionary(self, dictionary):
        return Animation(**dictionary)

    def compile_ast_dictionary(self, dictionary):
        node = dictionary['builder_internal_ast']
        anim = self.compile_node(node)
        kwargs = dictionary.copy()
        del kwargs['builder_internal_ast']
        for key, value in kwargs.items():
            setattr(anim, key, value)
        return anim

    def compile_list_dictionary(self, dictionary):
        listobj = dictionary['builder_internal_list']

        data, handler = listobj[0]
        anim = handler(data)
        for data, handler in listobj[1:]:
            anim += handler(data)

        kwargs = dictionary.copy()
        del kwargs['builder_internal_list']
        for key, value in kwargs.items():
            setattr(anim, key, value)
        return anim

    def prepare_dictionary(self, dictionary):
        compound = dictionary.pop('compound', None)
        if compound is None:
            return (dictionary, self.compile_simple_dictionary, )
        elif isinstance(compound, str):
            dictionary['builder_internal_ast'] = ast.parse(compound).body[0]
            return (dictionary, self.compile_ast_dictionary, )
        elif isinstance(compound, (list, tuple, )):
            dictionary['builder_internal_list'] = self.prepare_list(compound)
            return (dictionary, self.compile_list_dictionary, )
        else:
            raise AnimationBuilderException("'compound' must be string or list.")

    def prepare_list(self, listobj):
        return [
            (item, self.compile_identifier, ) if isinstance(item, str)
            else self.prepare_dictionary(item) if isinstance(item, dict)
            else (item, self.compile_unsupported, )
            for item in listobj
        ]

