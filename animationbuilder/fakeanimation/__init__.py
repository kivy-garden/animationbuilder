# -*- coding: utf-8 -*-

'''
Fake Animation
==============

When you wanna do some non-Animation stuff between two Animations, you'd write
like this:

anim2 = Animation(...)
def non_animation_stuff(anim, widget):
    ...
    anim2.start(widget)
anim1 = Animation(...)
anim1.bind(on_complete=non_animation_stuff)
anim1.start(some_widget)


By using this module, the code above become like this:

from fakeanimations import Callable

def non_animation_stuff(widget):
    ...

anim = Animation(...) + Callable(callable=non_animation_stuff) + Animation(...)
anim.start(some_widget)
'''

try:
    from ._callable import Callable
    from ._exec import Exec
except ImportError:
    from _callable import Callable
    from _exec import Exec
