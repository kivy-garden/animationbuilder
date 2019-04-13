# -*- coding: utf-8 -*-

__all__ = ('Compiler', )

from .animation_classes import Animation

EVAL_PREFIX = 'e '
EVAL_PREFIX_LENGTH = len(EVAL_PREFIX)


class Compiler:

    def __init__(self, database, **kwargs):
        init_code = database.pop('__init__', None)
        self.database = {
            key: self._compile_dictionary(data)
            for key, data in database.items()
        }
        self.locals = kwargs.get('locals', None)
        self.globals = kwargs.get('globals', {})
        if init_code is not None:
            exec(init_code, self.globals, self.locals)

    def create_anim_from_id(self, identifier):
        data, func_create_anim = self.database[identifier]
        return func_create_anim(data)

    def _do_eval(self, dictionary):
        dictionary.update({
            key: eval(codeobject, self.globals, self.locals)
            for key, codeobject in dictionary['need_eval'].items()
        })

    def _create_anim(self, dictionary):
        copied = dictionary.copy()
        self._do_eval(copied)
        del copied['need_eval']
        return Animation(**copied)

    def _create_sequential_anim(self, dictionary):
        anims = (func_compile(data) for (data, func_compile, ) in dictionary['sequence'])
        r = sum(anims, next(anims))

        copied = dictionary.copy()
        self._do_eval(copied)

        r.repeat = copied.get('repeat', False)
        return r

    def _create_parallel_anim(self, dictionary):
        anims = (func_compile(data) for (data, func_compile, ) in dictionary['parallel'])
        r = next(anims)
        for anim in anims:
            r &= anim
        return r

    def _raise_exception_unsupported_data(self, data):
        raise Exception(
            "Unsupported data type: " + str(type(data)))

    def _compile_dictionary(self, dictionary):
        # replace short-form with long-form
        temp = dictionary.pop('S', None)
        if temp is not None:
            dictionary['sequence'] = temp
        temp = dictionary.pop('P', None)
        if temp is not None:
            dictionary['parallel'] = temp

        # if value is str and starts with EVAL_PREFIX, compile it as python expression
        need_eval = {}
        for key, value in dictionary.items():
            if isinstance(value, str) and value.startswith(EVAL_PREFIX):
                need_eval[key] = compile(value[EVAL_PREFIX_LENGTH:], '<string>', 'eval')
        dictionary['need_eval'] = need_eval

        # sequence
        sequence = dictionary.get('sequence')
        if sequence is not None:
            dictionary['sequence'] = self.prepare_list(sequence)
            return (dictionary, self._create_sequential_anim, )

        # parallel
        parallel = dictionary.get('parallel')
        if parallel is not None:
            dictionary['parallel'] = self.prepare_list(parallel)
            return (dictionary, self._create_parallel_anim, )

        # simple
        return (dictionary, self._create_anim)

    def prepare_list(self, listobj):
        return [
            (item, self.create_anim_from_id) if isinstance(item, str)
            else self._compile_dictionary(item) if isinstance(item, dict)
            else self._raise_exception_unsupported_data(item)
            for item in listobj
        ]
