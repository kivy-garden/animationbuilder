# -*- coding: utf-8 -*-


from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.animation import Animation

import beforetest
from animationbuilder import AnimationBuilder


anims = AnimationBuilder.load_string(r'''
test_eval:
    P:
        - "eval: Animation(pos=dst)"
        - opacity: 0
          d: "eval: 1 + 1"
''')
anims.locals = {'Animation': Animation, }
anims.globals = {'dst': (600, 400,), }
anim1 = anims['test_eval']
anims.locals['dst'] = (50, 50,)
anim2 = anims['test_eval']
anim = anim1 + anim2

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
