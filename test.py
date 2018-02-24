# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.base import runTouchApp

from animationbuilder import AnimationBuilder


ANIMATION_DATA = r'''
move_right:
    x: 700
    d: 1.0
move_left:
    x: 0
    d: 1.0
move_up:
    y: 500
    d: 1.0
move_down:
    y: 0
    d: 1.0

keep_moving:
    compound: "move_right + move_up + move_left + move_down + sleep(1)"
    repeat: True

opacity1:
    opacity: 0
    d: .3
    t: 'in_out_cubic'

opacity2:
    opacity: 1
    d: .3
    t: 'in_out_cubic'

blinking:
    compound: "opacity1 + opacity2"
    repeat: True

all_in:
    compound: "keep_moving & blinking"
'''


animations = AnimationBuilder.load_string(ANIMATION_DATA)

root = Builder.load_string(r'''
FloatLayout:
    Button:
        id: button
        size_hint: None, None
        size: 100, 100
        text: 'Start'
''')
button = root.ids.button
# button.bind(on_press=lambda button: animations['move_right'].start(button))
# button.bind(on_press=lambda button: animations['keep_moving'].start(button))
button.bind(on_press=lambda button: animations['all_in'].start(button))

runTouchApp(root)
