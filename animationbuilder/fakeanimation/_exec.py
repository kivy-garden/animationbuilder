# -*- coding: utf-8 -*-

__all__ = ('Exec', )

try:
    from ._callable import Callable
except ImportError:
    from _callable import Callable


class Exec(Callable):

    def __init__(self, **kwargs):
        self.codeobject = kwargs.pop('codeobject')
        self.locals = kwargs.pop('locals', {})
        self.globals = kwargs.pop('globals', {})
        kwargs['callable'] = self.callback
        super(Exec, self).__init__(**kwargs)

    def callback(self, widget):
        locals = self.locals
        locals['widget'] = widget
        exec(self.codeobject, self.globals, locals)
