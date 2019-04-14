# -*- coding: utf-8 -*-

__all__ = ('Compiler', )

from functools import partial
from .animation_classes import Animation


class Compiler:

    def __init__(self, database, **kwargs):
        init_code = database.pop('__init__', None)
        self.database = {
            key: self._compile_dictionary(data)
            for key, data in database.items()
        }
        self.locals = kwargs.get('locals', {})
        self.globals = kwargs.get('globals', {})
        if init_code is not None:
            exec(init_code, self.globals, self.locals)

    def create_anim_from_id(self, identifier):
        return self.database[identifier]()

    def _do_eval(self, d):
        d.update({
            key: eval(codeobject, self.globals, self.locals)
            for key, codeobject in d['need_to_eval'].items()
        })

    def _create_anim(self, d):
        copied = d.copy()
        self._do_eval(copied)
        del copied['need_to_eval']
        return Animation(**copied)

    def _create_sequential_anim(self, d):
        anims = (create_anim() for create_anim in d['sequence'])
        r = sum(anims, next(anims))

        copied = d.copy()
        self._do_eval(copied)

        r.repeat = copied.get('repeat', False)
        return r

    def _create_parallel_anim(self, d):
        anims = (create_anim() for create_anim in d['parallel'])
        r = next(anims)
        for anim in anims:
            r &= anim
        return r

    def _raise_exception_unsupported_data(self, data):
        raise Exception(
            "Unsupported data type: " + str(type(data)))

    def _compile_dictionary(self, d):
        # replace short-form with long-form
        temp = d.pop('S', None)
        if temp is not None:
            d['sequence'] = temp
        temp = d.pop('P', None)
        if temp is not None:
            d['parallel'] = temp

        # If 'value' is string-type, compile it as a python expression,
        # unless 'key' is 'transition'
        need_to_eval = {}
        for key, value in d.items():
            if isinstance(value, str) and key not in ('t', 'transition'):
                need_to_eval[key] = compile(value, '<string>', 'eval')
        d['need_to_eval'] = need_to_eval

        # sequence
        listobj = d.get('sequence')
        if listobj is not None:
            d['sequence'] = self._compile_list(listobj)
            return partial(self._create_sequential_anim, d)

        # parallel
        listobj = d.get('parallel')
        if listobj is not None:
            d['parallel'] = self._compile_list(listobj)
            return partial(self._create_parallel_anim, d)

        # simple
        return partial(self._create_anim, d)

    def _compile_list(self, listobj):
        return [
            partial(self.create_anim_from_id, item) if isinstance(item, str)
            else self._compile_dictionary(item) if isinstance(item, dict)
            else self._raise_exception_unsupported_data(item)
            for item in listobj
        ]
