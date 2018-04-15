# -*- coding: utf-8 -*-

__all__ = ('Animation', 'Sequence', 'Parallel', 'AnimationTransition', )

from kivy.animation import AnimationTransition
from ._replacement_of_the_animation_class import Animation, Sequence, Parallel
