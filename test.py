# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.base import runTouchApp

from animationbuilder import AnimationBuilder


anims = AnimationBuilder.load_string(r'''
move_to_right:
    right: 800
move_to_top:
    top: 600

sequential_test:
    sequential:
        - move_to_right
        - duration: 1
        - top: 600

freestyle_test:
    freestyle: "move_to_right & move_to_top"

parallel_test:
    parallel:
        - right: 800
          d: 1.5
        - move_to_top
        - opacity: 0
          d: 2
''')

root = Builder.load_string(r'''
FloatLayout:
    Button:
        id: button
        size_hint: None, None
        size: 100, 100
        text: 'Start'
''')
button = root.ids.button
button.bind(on_press=lambda button: anims['freestyle_test'].start(button))

runTouchApp(root)
