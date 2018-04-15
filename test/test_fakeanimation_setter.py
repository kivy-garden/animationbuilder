# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.base import runTouchApp

import beforetest
from animationbuilder.fakeanimation import Setter
from animationbuilder.animation_classes import Animation


anim = (
    Setter(pos=(700, 500, ), d=10, t='buz', s=0.1) +
    Animation(pos=(0, 0))
)


root = Builder.load_string(r'''
FloatLayout:
    Button:
        id: button
        size_hint: None, None
        size: 100, 100
        text: 'sequence'
''')
root.ids.button.bind(on_press=anim.start)

runTouchApp(root)
