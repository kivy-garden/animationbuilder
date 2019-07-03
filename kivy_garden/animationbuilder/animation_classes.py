# -*- coding: utf-8 -*-

'''
Use its own Animation classes, because original ones are buggy.
https://github.com/kivy/kivy/issues/5204
https://github.com/kivy/kivy/issues/5443
https://github.com/kivy/kivy/issues/5929
'''

__all__ = ('Animation', 'Sequence', 'Parallel', 'AnimationTransition', )

from kivy.animation import Animation as OriginalAnimation, AnimationTransition


class Animation(OriginalAnimation):

    def __add__(self, animation):
        return Sequence(self, animation)

    def __and__(self, animation):
        return Parallel(self, animation)


class Sequence(Animation):

    def __init__(self, anim1, anim2):
        super(Sequence, self).__init__()

        #: Repeat the sequence. See 'Repeating animation' in the header
        #: documentation.
        self.repeat = False

        self.anim1 = anim1
        self.anim2 = anim2

        self.anim1.bind(on_complete=self.on_anim1_complete,
                        on_progress=self.on_anim1_progress)
        self.anim2.bind(on_complete=self.on_anim2_complete,
                        on_progress=self.on_anim2_progress)

    @property
    def duration(self):
        return self.anim1.duration + self.anim2.duration

    def start(self, widget):
        self.stop(widget)
        self._widgets[widget.uid] = True
        self._register()
        self.dispatch('on_start', widget)
        self.anim1.start(widget)

    def stop(self, widget):
        props = self._widgets.pop(widget.uid, None)
        self.anim1.stop(widget)
        self.anim2.stop(widget)
        if props:
            self.dispatch('on_complete', widget)
        super(Sequence, self).cancel(widget)

    def stop_property(self, widget, prop):
        self.anim1.stop_property(widget, prop)
        self.anim2.stop_property(widget, prop)
        if (not self.anim1.have_properties_to_animate(widget) and
                not self.anim2.have_properties_to_animate(widget)):
            self.stop(widget)

    def cancel(self, widget):
        self._widgets.pop(widget.uid, None)
        self.anim1.cancel(widget)
        self.anim2.cancel(widget)
        super(Sequence, self).cancel(widget)

    def cancel_property(self, widget, prop):
        '''Even if an animation is running, remove a property. It will not be
        animated further. If it was the only/last property being animated,
        the animation will be canceled (see :attr:`cancel`)

        This method overrides `:class:kivy.animation.Animation`'s
        version, to cancel it on all animations of the Sequence.

        .. versionadded:: 1.10.0
        '''
        self.anim1.cancel_property(widget, prop)
        self.anim2.cancel_property(widget, prop)
        if (not self.anim1.have_properties_to_animate(widget) and
                not self.anim2.have_properties_to_animate(widget)):
            self.cancel(widget)

    def on_anim1_complete(self, instance, widget):
        if widget.uid not in self._widgets:
            return
        self.anim2.start(widget)

    def on_anim1_progress(self, instance, widget, progress):
        self.dispatch('on_progress', widget, progress / 2.)

    def on_anim2_complete(self, instance, widget):
        '''Repeating logic used with boolean variable "repeat".

        .. versionadded:: 1.7.1
        '''
        if widget.uid not in self._widgets:
            return
        if self.repeat:
            self.anim1.start(widget)
        else:
            self.dispatch('on_complete', widget)
            self.cancel(widget)

    def on_anim2_progress(self, instance, widget, progress):
        self.dispatch('on_progress', widget, .5 + progress / 2.)

    def have_properties_to_animate(self, widget):
        return (self.anim1.have_properties_to_animate(widget) or
                self.anim2.have_properties_to_animate(widget))


class Parallel(Animation):

    def __init__(self, anim1, anim2):
        super(Parallel, self).__init__()
        self.anim1 = anim1
        self.anim2 = anim2

        self.anim1.bind(on_complete=self.on_anim_complete)
        self.anim2.bind(on_complete=self.on_anim_complete)

    @property
    def duration(self):
        return max(self.anim1.duration, self.anim2.duration)

    def start(self, widget):
        self.stop(widget)
        self.anim1.start(widget)
        self.anim2.start(widget)
        self._widgets[widget.uid] = {'complete': 0}
        self._register()
        self.dispatch('on_start', widget)

    def stop(self, widget):
        self.anim1.stop(widget)
        self.anim2.stop(widget)
        props = self._widgets.pop(widget.uid, None)
        if props:
            self.dispatch('on_complete', widget)
        super(Parallel, self).cancel(widget)

    def stop_property(self, widget, prop):
        self.anim1.stop_property(widget, prop)
        self.anim2.stop_property(widget, prop)
        if (not self.anim1.have_properties_to_animate(widget) and
                not self.anim2.have_properties_to_animate(widget)):
            self.stop(widget)

    def cancel(self, widget):
        self.anim1.cancel(widget)
        self.anim2.cancel(widget)
        super(Parallel, self).cancel(widget)

    def on_anim_complete(self, instance, widget):
        self._widgets[widget.uid]['complete'] += 1
        if self._widgets[widget.uid]['complete'] == 2:
            self.stop(widget)

    def have_properties_to_animate(self, widget):
        return (self.anim1.have_properties_to_animate(widget) or
                self.anim2.have_properties_to_animate(widget))
