# -*- coding: utf-8 -*-

__all__ = ('Exec', )

try:
    from ._callable import Callable
except ImportError:
    from _callable import Callable


class Exec(Callable):

    def __init__(self, **kwargs):
        self.codeobject = kwargs.pop('codeobject')
        self.locals = kwargs.pop('locals', None)
        self.globals = kwargs.pop('globals', {})
        kwargs['callable'] = self.callback
        super(Exec, self).__init__(**kwargs)

    def callback(self, target):
        globals = self.globals
        locals = self.locals
        dictionary = locals if globals is None else globals
        if dictionary is not None:
            dictionary['target'] = target
        exec(self.codeobject, globals, locals)
