# -*- coding: utf-8 -*-

__all__ = ('Callable', )

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.animation import Parallel, Sequence, AnimationTransition


class Callable(EventDispatcher):
    '''Wrap any callable(takes 1 positional argument) in Animation'''

    __events__ = ('on_start', 'on_progress', 'on_complete')

    callable = ObjectProperty()

    @property
    def duration(self):
        return 0.01

    @property
    def transition(self):
        return AnimationTransition.linear

    @property
    def animated_properties(self):
        return {}

    def start(self, widget):
        self.dispatch('on_start', widget)
        self.callable(widget)
        self._clock_event = Clock.schedule_once(
            lambda dt: self.dispatch('on_complete', widget), -1)

    def stop(self, widget):
        pass

    def cancel(self, widget):
        clock_event = getattr(self, '_clock_event', None)
        if clock_event is not None:
            clock_event.cancel()
            self._clock_event = None

    def stop_property(self, widget, prop):
        pass

    def cancel_property(self, widget, prop):
        pass

    def have_properties_to_animate(self, widget):
        return False

    #
    # Default handlers
    #
    def on_start(self, widget):
        pass

    def on_progress(self, widget, progress):
        pass

    def on_complete(self, widget):
        self._clock_event = None

    def __add__(self, animation):
        return Sequence(self, animation)

    def __and__(self, animation):
        return Parallel(self, animation)
