# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.animation import Animation

import beforetest
from animationbuilder.fakeanimation import Callable


anim1 = (
    Callable(callable=lambda __: print('start')) +
    Animation(right=800) +
    Callable(callable=lambda __: print('right is 800')) +
    Animation(top=600) +
    Callable(callable=lambda __: print('top is 600')) +
    Callable(callable=lambda __: print('end'))
)
anim2 = (
    (
        Animation(opacity=0) +
        Callable(callable=lambda __: print('opacity is 0')) +
        Animation(opacity=1) +
        Callable(callable=lambda __: print('opacity is 1'))
    ) &
    (
        Animation(x=0, d=0.7) +
        Callable(callable=lambda __: print('x is 0')) +
        Animation(top=600, d=0.7) +
        Callable(callable=lambda __: print('top is 600')) +
        Animation(right=800, d=0.7) +
        Callable(callable=lambda __: print('right is 800'))
    )
)


root = Builder.load_string(r'''
FloatLayout:
    Button:
        id: button1
        size_hint: None, None
        size: 100, 100
        text: 'sequential'
    Button:
        id: button2
        size_hint: None, None
        size: 100, 100
        right: 800
        text: 'sequential\n&\nparallel'
''')
root.ids.button1.bind(on_press=anim1.start)
root.ids.button2.bind(on_press=anim2.start)

runTouchApp(root)
