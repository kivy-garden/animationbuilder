# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.properties import StringProperty, BooleanProperty
from kivy.app import runTouchApp
from kivy.graphics.transformation import Matrix

import beforetest
from animationbuilder import AnimationBuilder


animations = AnimationBuilder.load_string(r'''
diagonal:
    right: "eval: parent.width"
    top: "eval: parent.height"

rectangle:
    S:
        - right: "eval: parent.width"
          y: 0
          d: 1.4
        - right: "eval: parent.width"
          top: "eval: parent.height"
        - x: 0
          top: "eval: parent.height"
          d: 1.4
        - pos: [0, 0]

rectangle_repeat:
    S:
        - rectangle
    repeat: True

_ellipse:
    S:
        - exec_on_create: |
            pw = parent.width
            ph = parent.height
            phw = pw / 2
            phh = ph / 2
        - P:
            - center_x: "eval: phw"
              t: in_sine
            - y: 0
              t: out_sine
        - P:
            - right: "eval: pw"
              t: out_sine
            - center_y: "eval: phh"
              t: in_sine
        - P:
            - center_x: "eval: phw"
              t: in_sine
            - top: "eval: ph"
              t: out_sine
        - P:
            - x: 0
              t: out_sine
            - center_y: "eval: phh"
              t: in_sine

ellipse:
    S:
        - "exec: widget.center_y = parent.height / 2"
        - _ellipse

ellipse_repeat:
    S:
        - "exec: widget.center_y = parent.height / 2"
        - S:
            - _ellipse
          repeat: True

blinking:
    S:
        - opacity: 0
          t: in_out_quad
          d: 0.3
        - opacity: 1
          t: in_out_quad
          d: 0.3
    repeat: True

rotate360:
    rotation: 360

rotate_and_rectangle:
    P:
        - rectangle
        - rotation: -2700
          d: 4

in_bounce:
    P:
        - right: "eval: parent.width"
          d: 4
        - top: "eval: parent.height"
          d: 4
          t: in_bounce

''')

Builder.load_string(r'''
<Showcase>:
    target: target
    Scatter:
        id: target
        size_hint: None, None
        Image:
            source: 'kivy-logo-black-128.png'
            size: target.size
    BoxLayout:
        id: menu
        orientation: 'vertical'
        pos_hint: {'right': 1.0}
        size_hint: 0.4, 1
<MenuItem>:
    is_checked: checkbox.active
    CheckBox:
        id: checkbox
        size_hint_x: None
        group: 'menu'
    Label:
        text: root.text
''')


def reset_widget(widget):
    Animation.cancel_all(widget)
    widget.pos = (0, 0, )
    widget.pos_hint = {}
    widget.size = (100, 100, )
    widget.size_hint = (None, None, )
    widget.opacity = 1
    if isinstance(widget, Factory.Scatter):
        widget.transform = Matrix()


class MenuItem(Factory.BoxLayout):
    text = StringProperty()
    is_checked = BooleanProperty()


class Showcase(Factory.FloatLayout):
    def __init__(self, **kwargs):
        super(Showcase, self).__init__(**kwargs)
        add_widget = self.ids.menu.add_widget
        for key in animations.keys():
            if key.startswith('_'):
                continue
            menuitem = MenuItem(text=key)
            menuitem.bind(is_checked=self.on_menuitem_clicked)
            add_widget(menuitem)

    def play_animation(self, key):
        print('playing:', key)
        target = self.target
        reset_widget(target)
        # when the animation completed, replay automatically
        anim = animations[key] + Animation(d=1)
        anim.bind(on_complete=lambda *args: self.play_animation(key))
        anim.start(target)

    def on_menuitem_clicked(self, menuitem, is_checked):
        if is_checked:
            self.play_animation(menuitem.text)


root = Showcase()
animations.locals['parent'] = root
runTouchApp(root)
