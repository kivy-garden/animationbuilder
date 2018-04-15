# -*- coding: utf-8 -*-

__all__ = ('Setter', )

try:
    from ._callable import Callable
except ImportError:
    from _callable import Callable


UNNECESSARY_KEYS = 'd s t duration step transition'.split()


class Setter(Callable):

    def __init__(self, **kwargs):
        for key in UNNECESSARY_KEYS:
            kwargs.pop(key, None)
        self._animated_properties = kwargs
        super(Setter, self).__init__(callable=self.callback)

    def callback(self, target):
        for name, value in self._animated_properties.items():
            setattr(target, name, value)

    @property
    def duration(self):
        return 0

    @property
    def animated_properties(self):
        return self._animated_properties
