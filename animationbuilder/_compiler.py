# -*- coding: utf-8 -*-

__all__ = ('Compiler', )


from kivy.animation import Animation


class Compiler:

    def __init__(self, database):
        self.database = {
            key: self.prepare_dictionary(data)
            for key, data in database.items()
        }

    def compile(self, key):
        return self.compile_identifier(key)

    def compile_identifier(self, identifier):
        data, handler = self.database[identifier]
        return handler(data)

    def compile_simple(self, dictionary):
        return Animation(**dictionary)

    def compile_sequential(self, dictionary):
        anims = (handler(data) for (data, handler, ) in dictionary['sequential'])
        r = sum(anims, next(anims))

        for key, value in dictionary.items():
            if key != 'sequential':
                setattr(r, key, value)
        return r

    def compile_parallel(self, dictionary):
        anims = (handler(data) for (data, handler, ) in dictionary['parallel'])
        r = next(anims)
        for anim in anims:
            r &= anim

        for key, value in dictionary.items():
            if key != 'parallel':
                setattr(r, key, value)
        return r

    def raise_exception_unsupported_data(self, data):
        raise Exception(
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
            else self.raise_exception_unsupported_data(item)
            for item in listobj
        ]
