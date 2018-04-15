# -*- coding: utf-8 -*-
from __future__ import print_function

from kivy.lang import Builder
from kivy.base import runTouchApp

import beforetest
from animationbuilder.fakeanimation import Callable
from animationbuilder.animation_classes import Animation


anim1 = (
    Callable(callable=lambda __: print('anim1: start')) +
    Animation(right=800) +
    Callable(callable=lambda __: print('anim1: right is 800')) +
    Animation(top=600) +
    Callable(callable=lambda __: print('anim1: top is 600')) +
    Animation(x=0) +
    Callable(callable=lambda __: print('anim1: x is 0')) +
    Animation(y=0) +
    Callable(callable=lambda __: print('anim1: y is 0')) +
    Callable(callable=lambda __: print('anim1: end'))
)
anim2 = (
    Callable(callable=lambda __: print('anim2: start')) +
    Animation(x=0, d=0.7) +
    Callable(callable=lambda __: print('anim2: right is 800')) +
    Animation(top=600, d=0.7) +
    Callable(callable=lambda __: print('anim2: top is 600')) +
    Animation(right=800, d=0.7) +
    Callable(callable=lambda __: print('anim2: x is 0')) +
    Animation(y=0, d=0.7) +
    Callable(callable=lambda __: print('anim2: y is 0')) +
    Callable(callable=lambda __: print('anim2: end'))
)


root = Builder.load_string(r'''
FloatLayout:
    Image:
        id: image1
        source: 'kivy-logo-black-128.png'
        size_hint: None, None
        size: self.texture_size
    Button:
        id: button
        size_hint: None, None
        center_x: 400
        text: 'start'
    Image:
        id: image2
        source: 'kivy-logo-black-128.png'
        size_hint: None, None
        size: self.texture_size
        right: 800
''')
image1 = root.ids.image1
image2 = root.ids.image2
button = root.ids.button


def on_button_press(button):
    anim1.start(image1)
    anim2.start(image2)


button.bind(on_press=on_button_press)

runTouchApp(root)
