# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.base import runTouchApp

import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from animationbuilder import AnimationBuilder


anims = AnimationBuilder.load_string(r'''
move_to_right:
    right: 800
move_to_top:
    top: 600

test_sequential:
    sequential:
        - move_to_right
        - duration: 1
        - top: 600

test_sequential_short_form:
    S:
        - move_to_right
        - duration: 1
        - top: 600

test_parallel:
    parallel:
        - right: 800
          d: 1.5
        - move_to_top
        - opacity: 0
          d: 2

test_parallel_short_form:
    P:
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
# button.bind(on_press=lambda button: anims['test_sequential_short_form'].start(button))
button.bind(on_press=lambda button: anims['test_parallel_short_form'].start(button))

runTouchApp(root)
