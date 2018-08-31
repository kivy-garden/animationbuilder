# -*- coding: utf-8 -*-

__all__ = ('Compiler', )

from .animation_classes import Animation


class Compiler:

    def __init__(self, database, **kwargs):
        self.database = {
            key: self.prepare_dictionary(data)
            for key, data in database.items()
        }
        self.locals = kwargs.get('locals', None)
        self.globals = kwargs.get('globals', {})

    @property
    def compile(self):
        return self.compile_identifier

    def compile_identifier(self, identifier):
        data, func_compile = self.database[identifier]
        return func_compile(data)

    def _apply_eval(self, dictionary):
        dictionary.update({
            key: eval(codeobject, self.globals, self.locals)
            for key, codeobject in dictionary['need_eval'].items()
        })

    def compile_simple(self, dictionary):
        copied = dictionary.copy()
        self._apply_eval(copied)
        del copied['need_eval']
        return Animation(**copied)

    def compile_sequence(self, dictionary):
        anims = (func_compile(data) for (data, func_compile, ) in dictionary['sequence'])
        r = sum(anims, next(anims))

        copied = dictionary.copy()
        self._apply_eval(copied)

        r.repeat = copied.get('repeat', False)
        return r

    def compile_parallel(self, dictionary):
        anims = (func_compile(data) for (data, func_compile, ) in dictionary['parallel'])
        r = next(anims)
        for anim in anims:
            r &= anim
        return r

    def raise_exception_unsupported_data(self, data):
        raise Exception(
            "Unsupported data type: " + str(type(data)))

    def prepare_dictionary(self, dictionary):
        # replace short-form with long-form
        temp = dictionary.pop('S', None)
        if temp is not None:
            dictionary['sequence'] = temp
        temp = dictionary.pop('P', None)
        if temp is not None:
            dictionary['parallel'] = temp

        # if value is str and starts with 'e: ', compile it as python expression
        need_eval = {}
        for key, value in dictionary.items():
            if isinstance(value, str) and value.startswith('e: '):
                need_eval[key] = compile(value[3:], '<string>', 'eval')
        dictionary['need_eval'] = need_eval

        # sequence
        sequence = dictionary.get('sequence')
        if sequence is not None:
            dictionary['sequence'] = self.prepare_list(sequence)
            return (dictionary, self.compile_sequence, )

        # parallel
        parallel = dictionary.get('parallel')
        if parallel is not None:
            dictionary['parallel'] = self.prepare_list(parallel)
            return (dictionary, self.compile_parallel, )

        # simple
        return (dictionary, self.compile_simple)

    def prepare_list(self, listobj):
        return [
            (item, self.compile_identifier) if isinstance(item, str)
            else self.prepare_dictionary(item) if isinstance(item, dict)
            else self.raise_exception_unsupported_data(item)
            for item in listobj
        ]
