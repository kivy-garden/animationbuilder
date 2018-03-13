# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.animation import Animation

import beforetest
from fakeanimations import Exec


anim = (
    Exec(codeobject="widget.pos = [700, 500]") +
    Animation(pos=(0, 0))
)


root = Builder.load_string(r'''
FloatLayout:
    Button:
        id: button
        size_hint: None, None
        size: 100, 100
        text: 'sequential'
''')
root.ids.button.bind(on_press=anim.start)

runTouchApp(root)
