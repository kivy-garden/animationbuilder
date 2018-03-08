# -*- coding: utf-8 -*-

__all__ = ('Compiler', )


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

    def compile_sequential(self, dictionary):
        anims = [handler(data) for (data, handler, ) in dictionary['sequential']]
        anim = sum(anims[1:], anims[0])

        for key, value in dictionary.items():
            if key != 'sequential':
                setattr(anim, key, value)
        return anim

    def compile_parallel(self, dictionary):
        anims = [handler(data) for (data, handler, ) in dictionary['parallel']]
        r = anims[0]
        for anim in anims[1:]:
            r &= anim

        for key, value in dictionary.items():
            if key != 'parallel':
                setattr(r, key, value)
        return r

    def compile_unsupported(self, data):
        raise AnimationBuilderException(
            "Unsupported data type: " + str(type(data)))

    def prepare_dictionary(self, dictionary):
        # sequential
        sequential = dictionary.pop('S', None)
        if sequential is None:
            sequential = dictionary.get('sequential')
        if sequential is not None:
            dictionary['sequential'] = self.prepare_list(sequential)
            return (dictionary, self.compile_sequential, )
        # parallel
        parallel = dictionary.pop('P', None)
        if parallel is None:
            parallel = dictionary.get('parallel')
        if parallel is not None:
            dictionary['parallel'] = self.prepare_list(parallel)
            return (dictionary, self.compile_parallel, )
        # simple
        return (dictionary, self.compile_simple)

    def prepare_list(self, listobj):
        return [
            (item, self.compile_identifier, ) if isinstance(item, str)
            else self.prepare_dictionary(item) if isinstance(item, dict)
            else (item, self.compile_unsupported, )
            for item in listobj
        ]
