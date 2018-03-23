# -*- coding: utf-8 -*-


from kivy.lang import Builder
from kivy.base import runTouchApp

import beforetest
from animationbuilder import AnimationBuilder


anims = AnimationBuilder.load_string(r'''
test_exec:
    S:
        - exec_on_create: |
            from random import random
            destination = (random() * 700, random() * 500, )
        # `widget` is a special identifier that indicates the widget, which
        # associated to the animation. Only available in `exec`.
        - "exec: widget.pos = (random() * 700, random() * 500, )"
        - pos: "eval: destination"
''')
anim = anims['test_exec']

root = Builder.load_string(r'''
FloatLayout:
    Button:
        id: button
        size_hint: None, None
        text: 'Start'
''')
button = root.ids.button
button.bind(on_press=anim.start)

runTouchApp(root)
