# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.base import runTouchApp

from _animationbuilder import AnimationBuilder


ANIMATION_DATABASE = r'''
move1:
    pos: [0, 0]
    d: 1.0
    t: 'linear'

move2:
    pos: [0, 300]
    d: 1.0
    t: 'linear'

opacity1:
    opacity: 0
    d: .5
    t: 'in_out_cubic'

opacity2:
    opacity: 1
    d: .5
    t: 'in_out_cubic'

blinking:
    compound: "opacity1 + opacity2"
    repeat: True

animation:
    compound: "(move1 + sleep(0.5) + move2 + sleep(0.5)) & blinking"
'''


animations = AnimationBuilder.load_string(ANIMATION_DATABASE)
for key in animations.keys():
    print(key)

root = Builder.load_string(r'''
FloatLayout:
    Button:
        id: button
        size_hint: None, None
        size: 100, 100
        text: 'Start Animation'
''')
button = root.ids.button
button.bind(on_press=lambda button: animations['blinking'].start(button))
# button.bind(on_press=lambda button: animations['move2'].start(button))

runTouchApp(root)
