# -*- coding: utf-8 -*-


from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.animation import Animation

import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from animationbuilder import AnimationBuilder


ANIMATION_SOURCE = r'''
test:
    P:
        - pos: "globals: external_value"
        - "globals: external_animation"

'''
anims = AnimationBuilder.load_string(ANIMATION_SOURCE)
anims.globals = external_params = {
    'external_value': (700, 500, ),
    'external_animation': Animation(opacity=0, d=1.5),
}
anim1 = anims['test']
external_params['external_value'] = (0, 500, )
# Animation instance can't be shared, so create new one.
external_params['external_animation'] = Animation(opacity=0, d=1.5)
anim2 = anims['test']

root = Builder.load_string(r'''
FloatLayout:
    Button:
        id: button1
        size_hint: None, None
        text: 'anim1'
    Button:
        id: button2
        size_hint: None, None
        text: 'anim2'
        pos: 700, 0
''')
root.ids.button1.bind(on_press=lambda button: anim1.start(button))
root.ids.button2.bind(on_press=lambda button: anim2.start(button))

runTouchApp(root)
