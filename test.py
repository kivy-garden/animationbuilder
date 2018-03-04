# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.base import runTouchApp

from animationbuilder import AnimationBuilder


ANIMATION_DATA = r'''
move_to_center:
    center: [400, 300, ]

keep_moving:
    sequential:
        - right: 800
        - top: 600
        - x: 0
        - y: 0
        - move_to_center
        - d: 1
    repeat: True

blinking:
    sequential:
        - opacity: 0
          t: 'in_out_quad'
          d: 0.3
        - opacity: 1
          t: 'in_out_quad'
          d: 0.3
    repeat: True

all_in:
    freestyle: "keep_moving & blinking"

sleep_test:
    freestyle: "sleep(1) + move_to_center"

parallel_test:
    parallel:
        - right: 800
          d: 1.5
        - top: 600
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
# button.bind(on_press=lambda button: animations['move_to_center'].start(button))
# button.bind(on_press=lambda button: animations['keep_moving'].start(button))
# button.bind(on_press=lambda button: animations['blinking'].start(button))
# button.bind(on_press=lambda button: animations['sleep_test'].start(button))
button.bind(on_press=lambda button: animations['parallel_test'].start(button))
# button.bind(on_press=lambda button: animations['all_in'].start(button))

runTouchApp(root)
